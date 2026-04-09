"""Runtime environment toggles."""

from din_agents.shared.runtime_prefs import (
    any_anthropic_route_enabled,
    compact_prompts_enabled,
    env_truthy,
    max_repo_read_tool_chars,
    max_sequential_task_context_chars,
    pre_crew_sleep_seconds,
)


def test_env_truthy(monkeypatch) -> None:
    monkeypatch.delenv("TEST_TRUTHY", raising=False)
    assert env_truthy("TEST_TRUTHY") is False
    monkeypatch.setenv("TEST_TRUTHY", "yes")
    assert env_truthy("TEST_TRUTHY") is True


def test_compact_prompts(monkeypatch) -> None:
    monkeypatch.delenv("DIN_AGENTS_COMPACT_PROMPTS", raising=False)
    assert compact_prompts_enabled() is True
    monkeypatch.setenv("DIN_AGENTS_COMPACT_PROMPTS", "1")
    assert compact_prompts_enabled() is True
    monkeypatch.setenv("DIN_AGENTS_COMPACT_PROMPTS", "0")
    assert compact_prompts_enabled() is False


def test_pre_crew_sleep(monkeypatch) -> None:
    monkeypatch.delenv("DIN_AGENTS_PRE_CREW_SLEEP_S", raising=False)
    assert pre_crew_sleep_seconds() == 0.0
    monkeypatch.setenv("DIN_AGENTS_PRE_CREW_SLEEP_S", "12.5")
    assert pre_crew_sleep_seconds() == 12.5


def test_max_repo_read_tool_chars(monkeypatch) -> None:
    for key in ("MODEL_PLANNING", "MODEL_IMPACT", "MODEL_DOC", "MODEL_DEFAULT"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.delenv("DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS", raising=False)
    assert max_repo_read_tool_chars() == 8_000
    monkeypatch.setenv("DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS", "12000")
    assert max_repo_read_tool_chars() == 8_000


def test_max_task_context_chars_default(monkeypatch) -> None:
    for key in ("MODEL_PLANNING", "MODEL_IMPACT", "MODEL_DOC", "MODEL_DEFAULT"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.delenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", raising=False)
    assert max_sequential_task_context_chars() == 12_000


def test_max_task_context_chars_zero_disables(monkeypatch) -> None:
    monkeypatch.setenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "0")
    assert max_sequential_task_context_chars() == 0


def test_anthropic_routes_clamp_prompt_budgets(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_PLANNING", "anthropic/claude-haiku-4-5-20251001")
    monkeypatch.setenv("DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS", "12000")
    monkeypatch.setenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "12000")
    assert any_anthropic_route_enabled() is True
    assert max_repo_read_tool_chars() == 3_000
    assert max_sequential_task_context_chars() == 4_000
