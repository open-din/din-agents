"""CrewAI Flow wiring that routes user requests across per-repo crews."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path

from pydantic import BaseModel, Field

from crewai.crews.crew_output import CrewOutput
from crewai.flow.flow import Flow, listen, or_, router, start

from din_agents.crews.din_core import DinCoreCrew
from din_agents.crews.din_studio import DinStudioCrew
from din_agents.crews.react_din import ReactDinCrew
from din_agents.shared.repo_profiles import get_repo_profile, render_repo_profile
from din_agents.shared.rules import RoutingDecision, render_routing_decision, route_request, select_quality_gates
from din_agents.shared.runtime_prefs import compact_prompts_enabled, pre_crew_sleep_seconds
from din_agents.shared.task_guardrails import clear_din_core_guardrail_echo, set_din_core_guardrail_echo

logger = logging.getLogger(__name__)

_MAX_RETRIES = int(os.environ.get("DIN_AGENTS_RATE_LIMIT_MAX_RETRIES", "6"))
_INITIAL_BACKOFF_S = int(os.environ.get("DIN_AGENTS_RATE_LIMIT_BACKOFF_INITIAL_S", "30"))
# Anthropic-style input TPM uses a ~1 min rolling window; sub-minute retries often fail again.
_TPM_BACKOFF_BASE_S = int(os.environ.get("DIN_AGENTS_TPM_BACKOFF_BASE_S", "120"))

_COMPACT_MAX_ENTRY_POINTS = 8
_COMPACT_MAX_HARD_BOUNDARIES = 6


def _is_input_tpm_rate_limit(exc_text: str) -> bool:
    t = exc_text.lower()
    return (
        "tokens per minute" in t
        or "input tpm" in t
        or ("per minute" in t and "exceed" in t and "rate limit" in t)
    )


def _rate_limit_wait_seconds(attempt: int, exc: Exception) -> float:
    """Sleep duration before retrying after a provider rate-limit error."""
    text = str(exc)
    if _is_input_tpm_rate_limit(text):
        return float(_TPM_BACKOFF_BASE_S * (2**attempt))
    return float(_INITIAL_BACKOFF_S * (2**attempt))


def _truncate_repo_prompt_list(items: list[str], max_show: int, label: str) -> str:
    if len(items) <= max_show:
        return "\n".join(f"- {item}" for item in items)
    head = "\n".join(f"- {item}" for item in items[:max_show])
    rest = len(items) - max_show
    return f"{head}\n- … (+{rest} more {label}; see `project/ROUTE_CARD.json` in repo)"


def _crew_tasks_markdown(result: CrewOutput) -> str:
    """Use every sequential task output; ``result.raw`` is often only the final task."""
    if result.tasks_output:
        chunks: list[str] = []
        for task_out in result.tasks_output:
            label = (task_out.name or "task").strip() or "task"
            body = (task_out.raw or "").strip()
            if body:
                chunks.append(f"#### Task: `{label}`\n\n{body}")
        if chunks:
            return "\n\n---\n\n".join(chunks)
    return (result.raw or "").strip()


class ControlPlaneState(BaseModel):
    """Mutable flow state shared between routing, crews, and report assembly."""
    request: str = ""
    repo_hint: str = ""
    route: str = ""
    affected_repos: list[str] = Field(default_factory=list)
    cross_repo: bool = False
    reasons: list[str] = Field(default_factory=list)
    quality_commands: dict[str, list[str]] = Field(default_factory=dict)
    repo_outputs: dict[str, str] = Field(default_factory=dict)
    final_output: str = ""
    report_path: str = "output/control-plane-report.md"


class DinControlPlaneFlow(Flow[ControlPlaneState]):
    """Top-level CrewAI Flow that routes work across DIN repos and composes the final brief."""

    @start()
    def collect_request(self):
        if not self.state.request:
            self.state.request = (
                "Assess a DIN change request and decide whether it belongs in "
                "din-core, react-din, din-studio, din-agents, or across multiple repos."
            )
        return self.state.request

    @listen(collect_request)
    def plan_routing(self):
        decision = route_request(
            request=self.state.request,
            repo_hint=self.state.repo_hint or None,
        )
        self.state.route = decision.route
        self.state.affected_repos = decision.affected_repos
        self.state.cross_repo = decision.cross_repo
        self.state.reasons = decision.reasons
        self.state.quality_commands = select_quality_gates(decision.affected_repos)
        return decision.route

    @router(plan_routing)
    def route_repo(self):
        return self.state.route

    @listen("din_core")
    def run_din_core(self):
        self._run_repo_crew("din_core")
        self.state.final_output = self._render_final_report()
        return self.state.final_output

    @listen("react_din")
    def run_react_din(self):
        self._run_repo_crew("react_din")
        self.state.final_output = self._render_final_report()
        return self.state.final_output

    @listen("din_studio")
    def run_din_studio(self):
        self._run_repo_crew("din_studio")
        self.state.final_output = self._render_final_report()
        return self.state.final_output

    @listen("din_agents")
    def run_din_agents(self):
        self._run_repo_brief("din_agents")
        self.state.final_output = self._render_final_report()
        return self.state.final_output

    @listen("cross_repo")
    def run_cross_repo(self):
        for repo_id in self.state.affected_repos:
            self._run_repo_brief(repo_id)
        self.state.final_output = self._render_final_report()
        return self.state.final_output

    @listen(or_(run_din_core, run_react_din, run_din_studio, run_din_agents, run_cross_repo))
    def save_report(self, _result: str):
        report_path = Path(self.state.report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(self.state.final_output, encoding="utf-8")
        return str(report_path)

    def _run_repo_brief(self, repo_id: str) -> None:
        if repo_id == "din_agents":
            profile = get_repo_profile(repo_id)
            lines = [
                "Ownership verdict: `din-agents`",
                "",
                "Use the manifest-driven route card below before opening source files.",
                "",
                "```text",
                "\n".join(
                    [
                        f"Repo: {profile.display_name}",
                        f"Role: {profile.role}",
                        "Entry points:",
                        *[f"- {item}" for item in profile.entry_points],
                        "Hard boundaries:",
                        *[f"- {item}" for item in profile.hard_boundaries],
                    ]
                ),
                "```",
            ]
            self.state.repo_outputs[repo_id] = "\n".join(lines)
            return
        self._run_repo_crew(repo_id)

    def _run_repo_crew(self, repo_id: str) -> None:
        crew_map = {
            "din_core": DinCoreCrew,
            "react_din": ReactDinCrew,
            "din_studio": DinStudioCrew,
        }
        crew_cls = crew_map[repo_id]
        inputs = self._crew_inputs(repo_id)
        set_din_core_guardrail_echo(
            repo_path=inputs["repo_path"],
            route=inputs["routing_route"],
        )

        last_exc: Exception | None = None
        try:
            for attempt in range(_MAX_RETRIES + 1):
                if attempt == 0:
                    pre_wait = pre_crew_sleep_seconds()
                    if pre_wait > 0:
                        logger.info(
                            "Pre-crew sleep %.0fs (%s) before kickoff — DIN_AGENTS_PRE_CREW_SLEEP_S",
                            pre_wait,
                            repo_id,
                        )
                        time.sleep(pre_wait)
                try:
                    result = crew_cls().crew().kickoff(inputs=inputs)
                    break
                except Exception as exc:
                    if "Task failed guardrail validation" in str(exc):
                        self.state.repo_outputs[repo_id] = self._render_guardrail_fallback(
                            repo_id=repo_id,
                            inputs=inputs,
                            error=exc,
                        )
                        return
                    if _is_input_tpm_rate_limit(str(exc)):
                        self.state.repo_outputs[repo_id] = self._render_guardrail_fallback(
                            repo_id=repo_id,
                            inputs=inputs,
                            error=exc,
                        )
                        return
                    exc_name = type(exc).__name__.lower()
                    exc_text = str(exc).lower()
                    looks_rate_limited = (
                        "rate_limit" in exc_name
                        or "ratelimit" in exc_name
                        or "rate_limit" in exc_text
                        or "rate limit" in exc_text
                        or "tokens per minute" in exc_text
                    )
                    if not looks_rate_limited:
                        raise
                    last_exc = exc
                    if attempt >= _MAX_RETRIES:
                        raise
                    wait = _rate_limit_wait_seconds(attempt, exc)
                    kind = "TPM/window" if _is_input_tpm_rate_limit(str(exc)) else "rate limit"
                    logger.warning(
                        "Rate-limited on %s (%s, attempt %d/%d), retrying in %.0fs…",
                        repo_id,
                        kind,
                        attempt + 1,
                        _MAX_RETRIES + 1,
                        wait,
                    )
                    time.sleep(wait)
            else:
                raise last_exc  # type: ignore[misc]
        finally:
            clear_din_core_guardrail_echo()

        if not isinstance(result, CrewOutput):
            self.state.repo_outputs[repo_id] = str(result)
        else:
            self.state.repo_outputs[repo_id] = _crew_tasks_markdown(result)

    def _render_guardrail_fallback(self, *, repo_id: str, inputs: dict[str, str], error: Exception) -> str:
        """Return a deterministic markdown brief when a repo crew fails guardrail validation."""
        profile = get_repo_profile(repo_id)
        quality_gates = self.state.quality_commands.get(repo_id, [])
        quality_lines = "\n".join(f"- `{command}`" for command in quality_gates) or "- _No quality gates configured._"
        return (
            "## Ownership Verdict\n"
            f"- Repo: `{profile.display_name}`\n"
            f"- Path: {inputs['repo_path']}\n"
            f"- Route: {inputs['routing_route']}\n"
            "\n"
            "## Request\n"
            f"{self.state.request}\n"
            "\n"
            "## Fallback Summary\n"
            "- The automated crew did not produce a valid markdown brief after guardrail retries.\n"
            "- This fallback preserves the routed repo, current request text, and validation commands so the control-plane run still completes.\n"
            f"- Crew failure: `{type(error).__name__}: {str(error).strip()}`\n"
            "\n"
            "## Repo Inputs\n"
            f"- Summary: `{inputs['summary_path']}`\n"
            f"- API summary: `{inputs['api_summary_path']}`\n"
            f"- Repo manifest: `{inputs['repo_manifest_path']}`\n"
            "\n"
            "## Quality Gates\n"
            f"{quality_lines}\n"
        )

    def _crew_inputs(self, repo_id: str) -> dict[str, str]:
        profile = get_repo_profile(repo_id)
        if compact_prompts_enabled():
            entry_points = _truncate_repo_prompt_list(
                list(profile.entry_points),
                _COMPACT_MAX_ENTRY_POINTS,
                "entry points",
            )
            hard_boundaries = _truncate_repo_prompt_list(
                list(profile.hard_boundaries),
                _COMPACT_MAX_HARD_BOUNDARIES,
                "boundaries",
            )
        else:
            entry_points = "\n".join(f"- {path}" for path in profile.entry_points)
            hard_boundaries = "\n".join(f"- {item}" for item in profile.hard_boundaries)
        repo_contract_text = render_repo_profile(repo_id)
        decision = route_request(
            request=self.state.request,
            repo_hint=repo_id,
        )
        change_brief_text = render_routing_decision(decision)

        return {
            "request": self.state.request,
            "repo_hint": self.state.repo_hint,
            "repo_path": profile.path,
            "routing_route": decision.route,
            "summary_path": profile.summary_path,
            "api_summary_path": profile.api_summary_path,
            "repo_manifest_path": profile.repo_manifest_path,
            "entry_points": entry_points,
            "hard_boundaries": hard_boundaries,
            "quality_gates": "\n".join(
                f"- `{command}`" for command in self.state.quality_commands.get(repo_id, [])
            ),
            "repo_contract_output": repo_contract_text,
            "change_brief_output": change_brief_text,
        }

    def _render_final_report(self) -> str:
        affected_ids = list(self.state.affected_repos)
        if not affected_ids and self.state.route in ("din_core", "react_din", "din_studio", "din_agents"):
            affected_ids = [self.state.route]
        reasons = list(self.state.reasons)
        if not reasons:
            reasons = [f"Route `{self.state.route}` (no reasons captured in flow state)."]

        decision = RoutingDecision(
            route=self.state.route,
            affected_repos=affected_ids,
            cross_repo=self.state.cross_repo,
            reasons=reasons,
        )

        quality_commands = dict(self.state.quality_commands)
        for repo_id, commands in select_quality_gates(affected_ids).items():
            quality_commands.setdefault(repo_id, commands)

        sections: list[str] = [
            "# DIN Control Plane Report",
            "",
            "## Request",
            self.state.request,
            "",
            "## Routing",
            "```text",
            render_routing_decision(decision).rstrip(),
            "```",
            "",
            "## Repo Briefs",
        ]

        for repo_id in affected_ids:
            profile = get_repo_profile(repo_id)
            sections.extend(
                [
                    f"### {profile.display_name}",
                    self.state.repo_outputs.get(repo_id, "_No crew output available._"),
                    "",
                ]
            )

        sections.extend(["## Quality Gates"])
        for repo_id in affected_ids:
            profile = get_repo_profile(repo_id)
            sections.append(f"### {profile.display_name}")
            for command in quality_commands.get(repo_id, []):
                sections.append(f"- `{command}`")
            sections.append("")

        return "\n".join(sections).rstrip() + "\n"
