"""Programmatic CrewAI task guardrails for thin or tool-skipping agent outputs.

Note: avoid ``from __future__ import annotations`` here — CrewAI validates guardrail
callables by inspecting real return types (not string forward refs).
"""

import re
from typing import Any, Tuple, Union

from crewai.lite_agent_output import LiteAgentOutput
from crewai.tasks.task_output import TaskOutput

_PREAMBLE_START = re.compile(
    r"^\s*(I will|I'll|I am going to|Let me)\b",
    re.IGNORECASE,
)


def _output_text(output: Union[TaskOutput, LiteAgentOutput]) -> str:
    return str(getattr(output, "raw", "") or "").strip()


def _tool_names_from_messages(messages: list[Any]) -> set[str]:
    names: set[str] = set()
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        for tc in msg.get("tool_calls") or []:
            if not isinstance(tc, dict):
                continue
            fn = tc.get("function")
            if isinstance(fn, dict):
                n = fn.get("name")
                if isinstance(n, str) and n:
                    names.add(n)
            n = tc.get("name")
            if isinstance(n, str) and n:
                names.add(n)
        n = msg.get("name")
        if isinstance(n, str) and n and msg.get("role") == "tool":
            names.add(n)
    return names


def din_core_require_tools_and_markdown(
    output: Union[TaskOutput, LiteAgentOutput],
) -> Tuple[bool, Any]:
    """Fail fast when the steward / parity tasks skip tools or return meta-only text."""
    text = _output_text(output)
    messages = getattr(output, "messages", None) or []
    names = _tool_names_from_messages(messages) if messages else set()
    tools_called = "repo_contract_lookup" in names and "change_brief_builder" in names
    # If message capture misses tool metadata, require pasted fingerprints from both tools.
    tool_outputs_in_text = "Path:" in text and "Route:" in text
    if not tools_called and not tool_outputs_in_text:
        return (
            False,
            "Guardrail: call repo_contract_lookup and change_brief_builder before answering, "
            "then weave their concrete fields (at minimum Path: and Route:) into the brief.",
        )

    if len(text) < 320:
        return (
            False,
            "Guardrail: answer is too short. Produce a full markdown brief with multiple `##` sections "
            "and concrete bullets, after calling repo_contract_lookup and change_brief_builder.",
        )
    if "##" not in text:
        return (
            False,
            "Guardrail: output must include at least one markdown `##` section heading.",
        )
    first_line = text.splitlines()[0] if text else ""
    if _PREAMBLE_START.match(first_line) and len(text) < 900:
        return (
            False,
            "Guardrail: do not stop at an intent-only line. Deliver the complete brief in this answer.",
        )
    return (True, text)
