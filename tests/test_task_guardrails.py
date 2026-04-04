from crewai.tasks.task_output import TaskOutput

from din_agents.shared.task_guardrails import din_core_require_tools_and_markdown


def _out(raw: str, messages: list | None = None) -> TaskOutput:
    return TaskOutput(description="t", raw=raw, agent="agent", messages=messages or [])


def test_guard_fails_on_intent_only_answer() -> None:
    ok, err = din_core_require_tools_and_markdown(
        _out("I'll analyze this documentation request for din-core by first gathering tools.")
    )
    assert ok is False
    assert err is not None
    assert "Path:" in err or "repo_contract_lookup" in err


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
