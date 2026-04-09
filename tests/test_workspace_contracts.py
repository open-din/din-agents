import json
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def _word_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def test_workspace_manifest_and_repo_manifests_stay_aligned():
    manifest = json.loads((WORKSPACE_ROOT / "project/WORKSPACE_MANIFEST.json").read_text(encoding="utf-8"))
    for entry in manifest["repos"]:
        repo_manifest_path = WORKSPACE_ROOT / entry["path"] / "project/REPO_MANIFEST.json"
        repo_manifest = json.loads(repo_manifest_path.read_text(encoding="utf-8"))["repo"]
        assert repo_manifest["id"] == entry["id"]
        assert repo_manifest["role"] == entry["role"]
        assert repo_manifest["entry_points"] == entry["entry_points"]


def test_workspace_router_and_invariants_have_required_sections():
    agents = (WORKSPACE_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    invariants = (WORKSPACE_ROOT / "docs/KNOWN_INVARIANTS.md").read_text(encoding="utf-8")

    assert "# WORKSPACE ROUTER" in agents
    assert "## REPO MAP" in agents
    assert "## ROUTING RULES" in agents
    assert "## HARD BOUNDARIES" in agents
    assert "## SHARED CONTRACTS" in invariants


def test_summary_and_api_summary_budgets_stay_compact():
    repo_summaries = [
        WORKSPACE_ROOT / "react-din/project/SUMMARY.md",
        WORKSPACE_ROOT / "din-core/project/SUMMARY.md",
        WORKSPACE_ROOT / "din-studio/project/SUMMARY.md",
        WORKSPACE_ROOT / "din-agents/project/SUMMARY.md",
    ]
    api_summaries = [
        WORKSPACE_ROOT / "docs/summaries/react-din-api.md",
        WORKSPACE_ROOT / "docs/summaries/din-core-api.md",
        WORKSPACE_ROOT / "docs/summaries/din-studio-api.md",
        WORKSPACE_ROOT / "docs/summaries/din-agents-api.md",
    ]

    assert _word_count(WORKSPACE_ROOT / "AGENTS.md") <= 220
    for path in repo_summaries:
        assert _line_count(path) <= 80
        assert _word_count(path) <= 220
    for path in api_summaries:
        assert _line_count(path) <= 180
        assert _word_count(path) <= 220


def test_readme_intro_exposes_agent_navigation_headings():
    for repo in ("react-din", "din-core", "din-studio", "din-agents"):
        first_lines = "\n".join((WORKSPACE_ROOT / repo / "README.md").read_text(encoding="utf-8").splitlines()[:25])
        assert "## PURPOSE" in first_lines
        assert "## ENTRY FILES" in first_lines
        assert "## DO NOT TOUCH" in first_lines
        assert "## RELATED REPOS" in first_lines
