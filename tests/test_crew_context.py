"""Sequential task context truncation."""

from din_agents.crews.din_core.din_core_crew import DinCoreCrew
from din_agents.shared.crew_context import truncate_sequential_context


def test_truncate_when_over_limit(monkeypatch) -> None:
    monkeypatch.setenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "100")
    body = "x" * 200
    out = truncate_sequential_context(body)
    assert out.startswith("x" * 100)
    assert "truncated" in out.lower()
    assert "DIN_AGENTS_MAX_TASK_CONTEXT_CHARS" in out


def test_truncation_shortens_large_prior_blob(monkeypatch) -> None:
    monkeypatch.setenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "500")
    body = "para\n" * 4000
    out = truncate_sequential_context(body)
    assert len(out) < len(body)
    assert "truncated" in out.lower()


def test_no_truncate_when_under_limit(monkeypatch) -> None:
    monkeypatch.setenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "5000")
    body = "short"
    assert truncate_sequential_context(body) == body


def test_truncate_disabled_at_zero(monkeypatch) -> None:
    monkeypatch.setenv("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "0")
    body = "x" * 50_000
    assert truncate_sequential_context(body) == body


def test_din_core_follow_up_tasks_opt_out_of_sequential_context() -> None:
    crew = DinCoreCrew().crew()
    assert crew.tasks[1].context == []
    assert crew.tasks[2].context == []


def test_din_core_final_validation_task_has_no_tools() -> None:
    crew = DinCoreCrew().crew()
    assert crew.tasks[2].agent is not None
    assert crew.tasks[2].agent.tools == []
