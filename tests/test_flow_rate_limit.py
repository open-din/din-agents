"""Rate-limit backoff helpers on the control-plane flow."""

from din_agents.flow import _is_input_tpm_rate_limit, _rate_limit_wait_seconds


def test_tpm_detection_from_anthropic_message():
    msg = (
        'litellm.RateLimitError: {"message":"would exceed '
        "your organization's rate limit of 30,000 input tokens per minute"
    )
    assert _is_input_tpm_rate_limit(msg)


def test_tpm_backoff_longer_than_generic():
    tpm_exc = Exception("rate_limit_error input tokens per minute")
    generic_exc = Exception("rate_limit_error: too many requests")
    assert _rate_limit_wait_seconds(0, tpm_exc) > _rate_limit_wait_seconds(0, generic_exc)
    assert _rate_limit_wait_seconds(0, tpm_exc) >= 120
    assert _rate_limit_wait_seconds(1, tpm_exc) >= 240


def test_generic_backoff_doubles():
    exc = Exception("generic rate limit")
    assert _rate_limit_wait_seconds(1, exc) == 2 * _rate_limit_wait_seconds(0, exc)
