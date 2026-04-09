from din_agents.shared.repo_profiles import get_repo_profile, get_repo_profiles, render_repo_profile


def test_repo_profiles_cover_all_workspace_repos():
    profiles = get_repo_profiles()
    assert set(profiles) == {"din_core", "react_din", "din_studio", "din_agents"}


def test_din_core_profile_exposes_rust_quality_gates():
    profile = get_repo_profile("din_core")
    commands = [gate.command for gate in profile.quality_gates]

    assert profile.role == "runtime"
    assert "cargo fmt --all --check" in commands
    assert "cargo clippy --workspace --all-targets -- -D warnings" in commands
    assert "cargo test --workspace" in commands


def test_react_din_route_card_points_to_schema_and_manifest():
    rendered = render_repo_profile("react_din")
    profile = get_repo_profile("react_din")

    assert "Role: api" in rendered
    assert "schemas/patch.schema.json" in rendered
    assert profile.repo_manifest_path.endswith("react-din/project/REPO_MANIFEST.json")


def test_din_studio_route_card_mentions_surface_and_mcp_entry_points():
    rendered = render_repo_profile("din_studio")
    assert "project/SURFACE_MANIFEST.json" in rendered
    assert "targets/mcp" in rendered


def test_din_agents_profile_mentions_routing_ownership():
    rendered = render_repo_profile("din_agents")
    assert "routing" in rendered.lower()
    assert "src/din_agents/shared/rules.py" in rendered
