"""CLI ergonomics: quiet runs and stricter task prompts for terminal/CI use."""

from __future__ import annotations

import os
from typing import Any

from din_agents.shared.runtime_prefs import compact_prompts_enabled

_CLI_MARK = "Terminal output contract"


_CLI_DESCRIPTION_SUFFIX = f"""

{_CLI_MARK} (mandatory for CLI / CI):
- Your **Final Answer** must be **complete markdown** with at least one `##` heading and concrete bullets or checklists.
- Copy a literal `Path:` line and a literal `Route:` line from the task inputs above into your markdown — do not paraphrase those labels away.
- You may use the file reader tool to inspect actual repo files before answering.
- Do **not** reply with only intentions or preambles ("I will...", "I'll gather...", "Let me...", "I'll analyze...") — deliver the full artifact as your Final Answer.
"""

_CLI_DESCRIPTION_SUFFIX_COMPACT = f"""

{_CLI_MARK} (CLI, compact — save input tokens):
- Final Answer: complete markdown with `##` headings; copy literal `Path:` and `Route:` lines from the task inputs above.
- No preamble-only replies — deliver the full brief as your Final Answer.
"""

_CLI_EXPECTED_OUTPUT_SUFFIX = (
    "\n\nThe deliverable must fully satisfy the terminal output contract in the task description "
    "(no meta-only or single-sentence replies). Include literal Path: and Route: lines from the task inputs."
)

_CLI_EXPECTED_OUTPUT_SUFFIX_COMPACT = (
    "\n\nDeliverable: substantive markdown with Path/Route lines from the task inputs and `##` sections."
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
    desc_suffix = _CLI_DESCRIPTION_SUFFIX_COMPACT if compact_prompts_enabled() else _CLI_DESCRIPTION_SUFFIX
    exp_suffix = _CLI_EXPECTED_OUTPUT_SUFFIX_COMPACT if compact_prompts_enabled() else _CLI_EXPECTED_OUTPUT_SUFFIX
    desc = str(cfg.get("description", "")).rstrip()
    if _CLI_MARK not in desc:
        cfg["description"] = desc + desc_suffix + extra_description_suffix
    elif extra_description_suffix:
        cfg["description"] = desc + extra_description_suffix

    exp = str(cfg.get("expected_output", "")).rstrip()
    if _CLI_MARK not in exp:
        cfg["expected_output"] = exp + exp_suffix
    return cfg


def mcp_task_scope_guard() -> str:
    """Extra description suffix for the MCP review task only."""
    return _MCP_SCOPE_GUARD
