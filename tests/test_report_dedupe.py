from din_agents.main import _dedupe_control_plane_report


def test_dedupe_exact_double_markdown():
    body = "# DIN Control Plane Report\n\n## Request\nhello\n"
    doubled = body + body
    assert _dedupe_control_plane_report(doubled).strip() == body.strip()
