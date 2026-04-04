"""LiteLLM-compatible model routing via environment variables.

CrewAI resolves completions through LiteLLM when installed. Model strings must
follow LiteLLM's ``provider/model`` convention (e.g. ``anthropic/claude-sonnet-4-5-20250929``,
``openai/gpt-4o``). Older Anthropic snapshot IDs may return ``not_found``; override via env.
See https://docs.litellm.ai/docs/providers

Role mapping (requested):
  - Planner  → Claude   (MODEL_PLANNING)
  - Impact   → Claude   (MODEL_IMPACT)
  - Binding  → Codex    (MODEL_BINDING)   # typically OpenAI route in LiteLLM
  - Coder    → Codex    (MODEL_CODING)
  - Tester   → cheap    (MODEL_TESTING)
  - Fixer    → Codex    (MODEL_FIXING)
  - Doc      → Claude   (MODEL_DOC)
"""

from __future__ import annotations

import os
from typing import Any

from crewai import LLM

# Defaults are LiteLLM route strings; override via env for your keys and providers.
_DEFAULTS: dict[str, str] = {
    "planning": "anthropic/claude-sonnet-4-5-20250929",
    "impact": "anthropic/claude-sonnet-4-5-20250929",
    "binding": "openai/gpt-4o",
    "coding": "openai/gpt-4o",
    "testing": "openai/gpt-4o-mini",
    "fixing": "openai/gpt-4o",
    "doc": "anthropic/claude-sonnet-4-5-20250929",
    "default": "openai/gpt-4o-mini",
}

_ENV_KEYS: dict[str, str] = {
    "planning": "MODEL_PLANNING",
    "impact": "MODEL_IMPACT",
    "binding": "MODEL_BINDING",
    "coding": "MODEL_CODING",
    "testing": "MODEL_TESTING",
    "fixing": "MODEL_FIXING",
    "doc": "MODEL_DOC",
    "default": "MODEL_DEFAULT",
}


def get_model(task_type: str) -> str:
    """Return the LiteLLM model route for a logical task type."""
    key = task_type.lower().strip()
    if key == "planning":
        return os.environ.get("MODEL_PLANNING", _DEFAULTS["planning"])
    if key == "impact":
        return os.environ.get("MODEL_IMPACT", _DEFAULTS["impact"])
    if key == "binding":
        return os.environ.get("MODEL_BINDING", _DEFAULTS["binding"])
    if key == "coding":
        return os.environ.get("MODEL_CODING", _DEFAULTS["coding"])
    if key == "testing":
        return os.environ.get("MODEL_TESTING", _DEFAULTS["testing"])
    if key == "fixing":
        return os.environ.get("MODEL_FIXING", _DEFAULTS["fixing"])
    if key == "doc":
        return os.environ.get("MODEL_DOC", _DEFAULTS["doc"])
    return os.environ.get("MODEL_DEFAULT", _DEFAULTS["default"])


def get_llm(task_type: str) -> LLM:
    """Build a CrewAI LLM that always routes through LiteLLM (not native SDK shortcuts)."""
    return LLM(model=get_model(task_type), is_litellm=True)


def get_function_calling_llm() -> LLM | None:
    """Optional cheaper model for tool-calling; unset keeps CrewAI default per agent."""
    raw = os.environ.get("MODEL_FUNCTION_CALLING", "").strip()
    if not raw:
        return None
    return LLM(model=raw, is_litellm=True)


def agent_llm_kwargs(task_type: str) -> dict[str, Any]:
    """Kwargs for Agent(...): primary LLM plus optional function_calling_llm."""
    kwargs: dict[str, Any] = {"llm": get_llm(task_type)}
    fc = get_function_calling_llm()
    if fc is not None:
        kwargs["function_calling_llm"] = fc
    return kwargs
