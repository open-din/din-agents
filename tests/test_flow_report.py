"""Flow report assembly (no LLM)."""

from din_agents.flow import DinControlPlaneFlow


def test_render_final_report_falls_back_when_affected_repos_empty() -> None:
    flow = DinControlPlaneFlow()
    flow.state.route = "din_studio"
    flow.state.affected_repos = []
    flow.state.reasons = []
    flow.state.request = "add husky pre-commit"
    flow.state.cross_repo = False
    flow.state.repo_outputs = {"din_studio": "_stub crew output_"}
    flow.state.quality_commands = {}
    md = flow._render_final_report()
    assert "din-studio" in md
    assert "_stub crew output_" in md
    assert "npm run lint" in md
    assert "Affected repos:" in md and "Reasons:" in md


def test_render_guardrail_fallback_contains_route_request_and_quality_gate() -> None:
    flow = DinControlPlaneFlow()
    flow.state.request = "Implement gain"
    flow.state.quality_commands = {"din_core": ["cargo test"]}
    md = flow._render_guardrail_fallback(
        repo_id="din_core",
        inputs={
            "repo_path": "/tmp/din-core",
            "routing_route": "din_core",
            "summary_path": "project/SUMMARY.md",
            "api_summary_path": "docs/api.md",
            "repo_manifest_path": "project/REPO_MANIFEST.json",
        },
        error=RuntimeError("Task failed guardrail validation after 4 retries"),
    )
    assert "Path: /tmp/din-core" in md
    assert "Route: din_core" in md
    assert "Implement gain" in md
    assert "`cargo test`" in md
    assert "fallback" in md.lower()
