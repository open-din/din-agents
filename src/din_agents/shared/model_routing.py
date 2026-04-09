"""LiteLLM-compatible model routing via environment variables.

CrewAI resolves completions through LiteLLM when installed. Model strings must
follow LiteLLM's ``provider/model`` convention (e.g. ``ollama/qwen2.5-coder:14b``,
``anthropic/claude-sonnet-4-5-20250929``, ``openai/gpt-4o``). Override any role via env.
For Anthropic, use **versioned** model ids (e.g. ``anthropic/claude-haiku-4-5-20251001``); aliases
like ``*-latest`` often return ``not_found_error`` from the API.

See https://docs.litellm.ai/docs/providers

Default stack is **Ollama** (ensure models are pulled and ``OLLAMA_API_BASE`` is set if not localhost):

  - Planning / impact / doc / testing / fallback → ``ollama/qwen2.5-coder:14b``
  - Binding / coding / fixing → ``ollama/deepseek-coder:16b``

Role env vars: ``MODEL_PLANNING``, ``MODEL_IMPACT``, ``MODEL_BINDING``, ``MODEL_CODING``,
``MODEL_TESTING``, ``MODEL_FIXING``, ``MODEL_DOC``, ``MODEL_DEFAULT``.
"""

from __future__ import annotations

import os
from typing import Any

from crewai import LLM

# Defaults: Ollama via LiteLLM; override via env for cloud providers or other local models.
_DEFAULTS: dict[str, str] = {
    "planning": "ollama/qwen2.5-coder:14b",
    "impact": "ollama/qwen2.5-coder:14b",
    "binding": "ollama/deepseek-coder:16b",
    "coding": "ollama/deepseek-coder:16b",
    "testing": "ollama/qwen2.5-coder:14b",
    "fixing": "ollama/deepseek-coder:16b",
    "doc": "ollama/qwen2.5-coder:14b",
    "default": "ollama/qwen2.5-coder:14b",
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


def _anthropic_native_tools_enabled() -> bool:
    """Anthropic native tool calling is opt-in until CrewAI/LiteLLM final-answer calls are stable."""
    raw = os.environ.get("DIN_AGENTS_ENABLE_ANTHROPIC_NATIVE_TOOLS", "").strip().lower()
    return raw in ("1", "true", "yes")


def _configure_llm(llm: LLM) -> LLM:
    """Apply repo-specific safety toggles to a freshly created CrewAI LLM."""
    if getattr(llm, "is_anthropic", False) and not _anthropic_native_tools_enabled():
        llm.supports_function_calling = lambda: False  # type: ignore[method-assign]
    return llm


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
    return _configure_llm(LLM(model=get_model(task_type), is_litellm=True))


def get_function_calling_llm() -> LLM | None:
    """Optional cheaper model for tool-calling; unset keeps CrewAI default per agent."""
    raw = os.environ.get("MODEL_FUNCTION_CALLING", "").strip()
    if not raw:
        return None
    return _configure_llm(LLM(model=raw, is_litellm=True))


def agent_llm_kwargs(task_type: str) -> dict[str, Any]:
    """Kwargs for Agent(...): primary LLM plus optional function_calling_llm."""
    kwargs: dict[str, Any] = {"llm": get_llm(task_type)}
    fc = get_function_calling_llm()
    if fc is not None:
        kwargs["function_calling_llm"] = fc
    return kwargs
