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
