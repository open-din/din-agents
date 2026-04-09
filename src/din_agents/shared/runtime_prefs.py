"""Environment-driven toggles for prompt size, pacing, and CLI ergonomics."""

from __future__ import annotations

import os


def env_truthy(name: str) -> bool:
    """Return True if ``name`` is set to 1/true/yes (case-insensitive)."""
    return os.environ.get(name, "").lower() in ("1", "true", "yes")


def compact_prompts_enabled() -> bool:
    """Shrink task prompts and injected repo lists to save LLM input tokens."""
    return env_truthy("DIN_AGENTS_COMPACT_PROMPTS")


def pre_crew_sleep_seconds() -> float:
    """Optional delay before a crew kickoff (e.g. let Anthropic TPM window recover)."""
    raw = os.environ.get("DIN_AGENTS_PRE_CREW_SLEEP_S", "").strip()
    if not raw:
        return 0.0
    try:
        return max(0.0, float(raw))
    except ValueError:
        return 0.0


def max_repo_read_tool_chars() -> int:
    """Max UTF-8 characters returned by ``read_*_repo_file`` per tool call.

    Large Rust sources (e.g. ``patch.rs``) can push one LLM request over Anthropic
    input TPM when tool results accumulate in the conversation.

    - Unset: default cap (20_000 chars).
    - Raise for local / generous quotas; lower (e.g. 12000) for tight cloud TPM.
    """
    raw = os.environ.get("DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS", "").strip()
    if not raw:
        return 20_000
    try:
        n = int(raw)
    except ValueError:
        return 20_000
    # Allow low values for tests / aggressive TPM budgets; guard against useless 0/negative.
    return max(1, n)


def max_sequential_task_context_chars() -> int:
    """Max characters of prior-task output injected into later sequential tasks.

    CrewAI concatenates earlier task outputs into each subsequent prompt; large first
    tasks can blow past per-call input limits (e.g. Anthropic TPM on a single request).

    - Unset: default cap (18000 chars, roughly a few thousand tokens).
    - ``0``: disable truncation (full prior output; higher TPM risk).
    """
    raw = os.environ.get("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "").strip()
    if not raw:
        return 18_000
    try:
        return int(raw)
    except ValueError:
        return 18_000
