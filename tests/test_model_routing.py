import pytest

from din_agents.shared import model_routing


def test_get_model_switch_uses_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MODEL_PLANNING", "anthropic/claude-opus-4")
    monkeypatch.setenv("MODEL_IMPACT", "anthropic/claude-sonnet-4")
    monkeypatch.setenv("MODEL_BINDING", "openai/gpt-4.1")
    monkeypatch.setenv("MODEL_CODING", "openai/gpt-4.1")
    monkeypatch.setenv("MODEL_TESTING", "openai/gpt-4o-mini")
    monkeypatch.setenv("MODEL_FIXING", "openai/gpt-4.1")
    monkeypatch.setenv("MODEL_DOC", "anthropic/claude-haiku-4-5-20251001")
    monkeypatch.setenv("MODEL_DEFAULT", "openai/gpt-4o-mini")

    assert model_routing.get_model("planning") == "anthropic/claude-opus-4"
    assert model_routing.get_model("impact") == "anthropic/claude-sonnet-4"
    assert model_routing.get_model("binding") == "openai/gpt-4.1"
    assert model_routing.get_model("coding") == "openai/gpt-4.1"
    assert model_routing.get_model("testing") == "openai/gpt-4o-mini"
    assert model_routing.get_model("fixing") == "openai/gpt-4.1"
    assert model_routing.get_model("doc") == "anthropic/claude-haiku-4-5-20251001"
    assert model_routing.get_model("unknown") == "openai/gpt-4o-mini"


def test_get_model_falls_back_when_env_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "MODEL_PLANNING",
        "MODEL_IMPACT",
        "MODEL_BINDING",
        "MODEL_CODING",
        "MODEL_TESTING",
        "MODEL_FIXING",
        "MODEL_DOC",
        "MODEL_DEFAULT",
    ):
        monkeypatch.delenv(key, raising=False)

    assert model_routing.get_model("planning") == model_routing._DEFAULTS["planning"]
    assert model_routing.get_model("other") == model_routing._DEFAULTS["default"]


def test_agent_llm_kwargs_includes_optional_function_calling(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MODEL_FUNCTION_CALLING", raising=False)
    kw = model_routing.agent_llm_kwargs("testing")
    assert "llm" in kw
    assert "function_calling_llm" not in kw

    monkeypatch.setenv("MODEL_FUNCTION_CALLING", "openai/gpt-4o-mini")
    kw2 = model_routing.agent_llm_kwargs("testing")
    assert "function_calling_llm" in kw2
