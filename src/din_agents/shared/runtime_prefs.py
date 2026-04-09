"""Environment-driven toggles for prompt size, pacing, and CLI ergonomics."""

from __future__ import annotations

import os


def env_truthy(name: str) -> bool:
    """Return True if ``name`` is set to 1/true/yes (case-insensitive)."""
    return os.environ.get(name, "").lower() in ("1", "true", "yes")


def any_anthropic_route_enabled() -> bool:
    """True when any configured model route targets Anthropic."""
    for key in (
        "MODEL_PLANNING",
        "MODEL_IMPACT",
        "MODEL_BINDING",
        "MODEL_CODING",
        "MODEL_TESTING",
        "MODEL_FIXING",
        "MODEL_DOC",
        "MODEL_DEFAULT",
        "MODEL_FUNCTION_CALLING",
    ):
        if os.environ.get(key, "").strip().startswith("anthropic/"):
            return True
    return False


def compact_prompts_enabled() -> bool:
    """Shrink task prompts and injected repo lists to save LLM input tokens.

    Compact mode is enabled by default because the common CLI workload is
    Anthropic-backed planning with tight input TPM limits. Set
    ``DIN_AGENTS_COMPACT_PROMPTS=0`` to opt back into the larger prompt form.
    """
    raw = os.environ.get("DIN_AGENTS_COMPACT_PROMPTS", "").strip().lower()
    if raw in ("0", "false", "no"):
        return False
    if raw in ("1", "true", "yes"):
        return True
    return True


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

    - Unset: default cap (8_000 chars).
    - Raise for local / generous quotas; lower (e.g. 12000) for tight cloud TPM.
    """
    anthropic_tight_budget = any_anthropic_route_enabled()
    default_limit = 3_000 if anthropic_tight_budget else 8_000
    hard_cap = 3_000 if anthropic_tight_budget else 8_000
    raw = os.environ.get("DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS", "").strip()
    if not raw:
        return default_limit
    try:
        n = int(raw)
    except ValueError:
        return default_limit
    # Allow low values for tests / aggressive TPM budgets; guard against useless 0/negative.
    return min(max(1, n), hard_cap)


def max_sequential_task_context_chars() -> int:
    """Max characters of prior-task output injected into later sequential tasks.

    CrewAI concatenates earlier task outputs into each subsequent prompt; large first
    tasks can blow past per-call input limits (e.g. Anthropic TPM on a single request).

    - Unset: default cap (12_000 chars, roughly a few thousand tokens).
    - ``0``: disable truncation (full prior output; higher TPM risk).
    """
    anthropic_tight_budget = any_anthropic_route_enabled()
    default_limit = 4_000 if anthropic_tight_budget else 12_000
    hard_cap = 4_000 if anthropic_tight_budget else 12_000
    raw = os.environ.get("DIN_AGENTS_MAX_TASK_CONTEXT_CHARS", "").strip()
    if not raw:
        return default_limit
    try:
        n = int(raw)
    except ValueError:
        return default_limit
    if n <= 0:
        return n
    return min(n, hard_cap)
