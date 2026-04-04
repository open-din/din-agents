from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from crewai.crews.crew_output import CrewOutput
from crewai.flow.flow import Flow, listen, or_, router, start

from din_agents.crews.din_core import DinCoreCrew
from din_agents.crews.din_studio import DinStudioCrew
from din_agents.crews.react_din import ReactDinCrew
from din_agents.shared.repo_profiles import get_repo_profile
from din_agents.shared.rules import RoutingDecision, render_routing_decision, route_request, select_quality_gates


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
    """Routes requests across DIN repos and composes a final execution brief."""

    @start()
    def collect_request(self):
        if not self.state.request:
            self.state.request = (
                "Assess a DIN change request and decide whether it belongs in "
                "din-core, react-din, din-studio, or across multiple repos."
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

    @listen("cross_repo")
    def run_cross_repo(self):
        for repo_id in self.state.affected_repos:
            self._run_repo_crew(repo_id)
        self.state.final_output = self._render_final_report()
        return self.state.final_output

    @listen(or_(run_din_core, run_react_din, run_din_studio, run_cross_repo))
    def save_report(self, _result: str):
        report_path = Path(self.state.report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(self.state.final_output, encoding="utf-8")
        return str(report_path)

    def _run_repo_crew(self, repo_id: str) -> None:
        crew_map = {
            "din_core": DinCoreCrew,
            "react_din": ReactDinCrew,
            "din_studio": DinStudioCrew,
        }
        crew_cls = crew_map[repo_id]
        result = crew_cls().crew().kickoff(inputs=self._crew_inputs(repo_id))
        if not isinstance(result, CrewOutput):
            self.state.repo_outputs[repo_id] = str(result)
        else:
            self.state.repo_outputs[repo_id] = _crew_tasks_markdown(result)

    def _crew_inputs(self, repo_id: str) -> dict[str, str]:
        profile = get_repo_profile(repo_id)
        return {
            "request": self.state.request,
            "repo_hint": self.state.repo_hint,
            "repo_path": profile.path,
            "canonical_docs": "\n".join(f"- {path}" for path in profile.canonical_docs),
            "boundaries": "\n".join(f"- {item}" for item in profile.boundaries),
            "quality_gates": "\n".join(
                f"- `{command}`" for command in self.state.quality_commands.get(repo_id, [])
            ),
        }

    def _render_final_report(self) -> str:
        affected_ids = list(self.state.affected_repos)
        if not affected_ids and self.state.route in ("din_core", "react_din", "din_studio"):
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
