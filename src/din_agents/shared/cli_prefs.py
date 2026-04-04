"""CLI ergonomics: quiet runs and stricter task prompts for terminal/CI use."""

from __future__ import annotations

import os
from typing import Any

_CLI_MARK = "Terminal output contract"


_CLI_DESCRIPTION_SUFFIX = f"""

{_CLI_MARK} (mandatory for CLI / CI):
- Your **final answer** must be **complete markdown** with at least one `##` heading and concrete bullets or checklists.
- Do **not** reply with only intentions or preambles ("I will...", "I'll gather...", "Let me...", "I'll analyze...") without delivering the full artifact in this turn.
- When this task says to use tools first, call `repo_contract_lookup` and `change_brief_builder` at least once **before** the final answer.
- When calling `change_brief_builder`, set `request` to the **verbatim** change description from the user (the same topic as in this task), not a generic placeholder like "analyze this request".
"""

_CLI_EXPECTED_OUTPUT_SUFFIX = (
    "\n\nThe deliverable must fully satisfy the terminal output contract in the task description "
    "(no meta-only or single-sentence replies)."
)

_MCP_SCOPE_GUARD = """

Scope guard (this task only):
- If the request concerns **only** generic developer tooling (Git hooks, Husky, lint-staged, simple pre-commit scripts, npm lifecycle scripts, local CI) and does **not** mention MCP, `targets/mcp`, bridge code, Desktop integrations, or WS protocol surfaces, answer with a short markdown whose first heading is `## MCP impact` and state clearly: **No `targets/mcp` impact** — local git/npm automation only. Do **not** invent MCP bridge work, protocol risks, or `targets/mcp/tests` updates for that case.
"""


def cli_verbose() -> bool:
    """False when DIN_AGENTS_QUIET is set (1/true/yes); reduces Crew/agent terminal noise."""
    return os.environ.get("DIN_AGENTS_QUIET", "").lower() not in ("1", "true", "yes")


def with_cli_task_config(
    task_cfg: dict[str, Any],
    *,
    extra_description_suffix: str = "",
) -> dict[str, Any]:
    """Merge shared CLI discipline into a CrewAI task config loaded from YAML."""
    cfg = dict(task_cfg)
    desc = str(cfg.get("description", "")).rstrip()
    if _CLI_MARK not in desc:
        cfg["description"] = desc + _CLI_DESCRIPTION_SUFFIX + extra_description_suffix
    elif extra_description_suffix:
        cfg["description"] = desc + extra_description_suffix

    exp = str(cfg.get("expected_output", "")).rstrip()
    if _CLI_MARK not in exp:
        cfg["expected_output"] = exp + _CLI_EXPECTED_OUTPUT_SUFFIX
    return cfg


def mcp_task_scope_guard() -> str:
    """Extra description suffix for the MCP review task only."""
    return _MCP_SCOPE_GUARD
