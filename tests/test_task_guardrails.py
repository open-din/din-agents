from crewai.tasks.task_output import TaskOutput

from din_agents.shared.task_guardrails import (
    clear_din_core_guardrail_echo,
    din_core_require_tools_and_markdown,
    set_din_core_guardrail_echo,
)


def _out(raw: str, messages: list | None = None) -> TaskOutput:
    return TaskOutput(description="t", raw=raw, agent="agent", messages=messages or [])


def test_guard_fails_on_intent_only_answer() -> None:
    ok, err = din_core_require_tools_and_markdown(
        _out("I'll analyze this documentation request for din-core by first gathering tools.")
    )
    assert ok is False
    assert err is not None
    assert "Path:" in err or "repo_contract_lookup" in err


def test_guard_passes_when_path_route_markdown_bold() -> None:
    body = """## Scope
- **Path**: /tmp/din-core
- **Route**: din_core
""" + ("Detail line.\n" * 40)
    ok, _ = din_core_require_tools_and_markdown(_out(body))
    assert ok is True


def test_guard_passes_when_tool_names_only_in_plain_text_messages_fail_until_structured() -> None:
    """Mentioning tools in assistant prose must not satisfy the guard (prompts repeat those names)."""
    messages = [
        {
            "role": "assistant",
            "content": "Turn log: repo_contract_lookup change_brief_builder",
        }
    ]
    body = """## Brief
""" + ("Section.\n" * 40)
    ok, err = din_core_require_tools_and_markdown(_out(body, messages=messages))
    assert ok is False
    assert err is not None
    assert "Path:" in err or "Route:" in err


def test_guard_passes_when_tools_in_structured_calls() -> None:
    messages = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"function": {"name": "repo_contract_lookup"}},
                {"function": {"name": "change_brief_builder"}},
            ],
        }
    ]
    body = """## Brief
""" + ("Section.\n" * 40)
    ok, _ = din_core_require_tools_and_markdown(_out(body, messages=messages))
    assert ok is True


def test_guard_prepends_echo_lines_when_flow_context_set() -> None:
    set_din_core_guardrail_echo(repo_path="/tmp/din-core", route="cross_repo")
    try:
        body = """## Brief
""" + ("Concrete detail line.\n" * 40)
        ok, data = din_core_require_tools_and_markdown(_out(body))
        assert ok is True
        assert "Path: /tmp/din-core" in str(data)
        assert "Route: cross_repo" in str(data)
    finally:
        clear_din_core_guardrail_echo()


def test_guard_passes_when_tool_fingerprints_embedded() -> None:
    body = """## Scope
- Doc + example

## Tool context
Path: /tmp/din-core
Route: din_core
Affected repos: din-core

## Notes
Extra detail so this is long enough for the minimum length check and stays substantive for reviewers.
""" + ("More.\n" * 40)
    ok, data = din_core_require_tools_and_markdown(_out(body))
    assert ok is True
    assert "##" in str(data)
