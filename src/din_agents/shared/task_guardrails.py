"""Programmatic CrewAI task guardrails for thin or tool-skipping agent outputs.

Note: avoid ``from __future__ import annotations`` here — CrewAI validates guardrail
callables by inspecting real return types (not string forward refs).
"""

import contextvars
import re
from typing import Any, Tuple, Union

from crewai.lite_agent_output import LiteAgentOutput
from crewai.tasks.task_output import TaskOutput
from crewai.utilities.string_utils import sanitize_tool_name

_PREAMBLE_START = re.compile(
    r"^\s*(I will|I'll|I am going to|Let me)\b",
    re.IGNORECASE,
)
_PATH_ROUTE_FP = (
    re.compile(r"^\s*(?:[>*-]\s*)?(?:\*\*)?path(?:\*\*)?\s*:", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*(?:[>*-]\s*)?(?:\*\*)?route(?:\*\*)?\s*:", re.IGNORECASE | re.MULTILINE),
)
_REQUIRED_TOOLS = ("repo_contract_lookup", "change_brief_builder")
# Labels copied from crew inputs; allow flexible line formatting.
_LOOSE_PATH_LABEL = re.compile(
    r"(?m)(^|[\n\r])[ \t>]*(?:[-*+] |\d+\. )?[`>]*Path[`>]*\s*:",
    re.IGNORECASE,
)
_LOOSE_ROUTE_LABEL = re.compile(
    r"(?m)(^|[\n\r])[ \t>]*(?:[-*+] |\d+\. )?[`>]*Route[`>]*\s*:",
    re.IGNORECASE,
)

_guardrail_echo: contextvars.ContextVar[tuple[str, str] | None] = contextvars.ContextVar(
    "din_agents_din_core_guardrail_echo",
    default=None,
)


def set_din_core_guardrail_echo(*, repo_path: str, route: str) -> None:
    """Set Path/Route lines for the next din-core crew run (flow kickoff)."""
    _guardrail_echo.set((f"Path: {repo_path}", f"Route: {route}"))


def clear_din_core_guardrail_echo() -> None:
    """Remove Path/Route echo context after a crew kickoff."""
    _guardrail_echo.set(None)


def _output_text(output: Union[TaskOutput, LiteAgentOutput]) -> str:
    return str(getattr(output, "raw", "") or "").strip()


def _as_message_dict(msg: Any) -> dict[str, Any] | None:
    if isinstance(msg, dict):
        return msg
    dump = getattr(msg, "model_dump", None)
    if callable(dump):
        try:
            d = dump()
        except Exception:  # pragma: no cover — defensive
            return None
        return d if isinstance(d, dict) else None
    return None


def _tool_names_from_messages(messages: list[Any]) -> set[str]:
    names: set[str] = set()
    for msg in messages:
        msg = _as_message_dict(msg)
        if msg is None:
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


def _tools_evident_in_messages(messages: list[Any]) -> bool:
    """True if both required tools appear in structured tool_calls or tool-result messages.

    Do not scan raw message text: task prompts mention these tool names, which would false-pass.
    """
    names = _tool_names_from_messages(messages)
    normalized = {sanitize_tool_name(n) for n in names if isinstance(n, str) and n}
    required = {sanitize_tool_name(t) for t in _REQUIRED_TOOLS}
    return required.issubset(normalized)


def _has_path_route_fingerprints(text: str) -> bool:
    """Match Path:/Route: as emitted by tools, allowing markdown bullets or bold."""
    strict = bool(_PATH_ROUTE_FP[0].search(text) and _PATH_ROUTE_FP[1].search(text))
    if strict:
        return True
    # Models sometimes indent, wrap in quotes, or omit bold — still require line-anchored labels.
    return bool(_LOOSE_PATH_LABEL.search(text) and _LOOSE_ROUTE_LABEL.search(text))


def din_core_require_tools_and_markdown(
    output: Union[TaskOutput, LiteAgentOutput],
) -> Tuple[bool, Any]:
    """Fail fast when the steward / parity tasks skip tools or return meta-only text."""
    text = _output_text(output)
    echo = _guardrail_echo.get()
    if echo and not _has_path_route_fingerprints(text):
        path_line, route_line = echo
        text = f"{path_line}\n{route_line}\n\n{text}"
    messages = getattr(output, "messages", None) or []
    tools_called = _tools_evident_in_messages(messages) if messages else False
    # If message capture misses tool metadata, require pasted fingerprints from both tools.
    tool_outputs_in_text = _has_path_route_fingerprints(text)
    if not tools_called and not tool_outputs_in_text:
        return (
            False,
            "Guardrail FAILED: your Final Answer must include a literal `Path:` line and a "
            "literal `Route:` line — copy them from the pre-computed repo contract and routing "
            "brief sections in the task description above. Deliver the full markdown brief now.",
        )

    if len(text) < 320:
        return (
            False,
            "Guardrail FAILED: answer is too short (<320 chars). "
            "Produce a full markdown brief with `##` sections and concrete bullets. "
            "Include Path: and Route: lines from the pre-computed data. "
            "Do NOT say 'I will' or 'let me' — write the complete brief now.",
        )
    if "##" not in text:
        return (
            False,
            "Guardrail FAILED: output must include at least one markdown `##` section heading.",
        )
    first_line = text.splitlines()[0] if text else ""
    if _PREAMBLE_START.match(first_line) and len(text) < 900:
        return (
            False,
            "Guardrail FAILED: do not start with 'I will' / 'Let me' — "
            "deliver the complete markdown brief as your Final Answer right now.",
        )
    return (True, text)


def require_markdown_execution_brief(
    output: Union[TaskOutput, LiteAgentOutput],
) -> Tuple[bool, Any]:
    """Require a non-trivial markdown execution brief for final planning tasks."""
    text = _output_text(output)
    echo = _guardrail_echo.get()
    if echo and not _has_path_route_fingerprints(text):
        path_line, route_line = echo
        text = f"{path_line}\n{route_line}\n\n{text}"

    if len(text) < 240:
        return (
            False,
            "Guardrail FAILED: final execution brief is too short. "
            "Return complete markdown with `##` headings, Path:, Route:, acceptance criteria, "
            "and the exact quality gates listed in the task inputs.",
        )
    if "##" not in text:
        return (
            False,
            "Guardrail FAILED: final execution brief must include markdown `##` section headings.",
        )
    if not _has_path_route_fingerprints(text):
        return (
            False,
            "Guardrail FAILED: include literal `Path:` and `Route:` lines copied from the task inputs.",
        )
    first_line = text.splitlines()[0] if text else ""
    if _PREAMBLE_START.match(first_line):
        return (
            False,
            "Guardrail FAILED: do not start with 'I will' / 'Let me' — "
            "deliver the full execution brief immediately.",
        )
    return (True, text)
