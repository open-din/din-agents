from din_agents.shared.repo_profiles import get_repo_profile, get_repo_profiles, render_repo_profile


def test_repo_profiles_cover_all_three_repos():
    profiles = get_repo_profiles()
    assert set(profiles) == {"din_core", "react_din", "din_studio"}


def test_din_core_profile_exposes_rust_quality_gates():
    profile = get_repo_profile("din_core")
    commands = [gate.command for gate in profile.quality_gates]

    assert profile.primary_language == "Rust"
    assert "cargo fmt --all --check" in commands
    assert "cargo clippy --workspace --all-targets -- -D warnings" in commands
    assert "cargo test --workspace" in commands


def test_react_din_profile_mentions_public_patch_schema():
    rendered = render_repo_profile("react_din")
    assert "@open-din/react/patch/schema.json" in get_repo_profile("react_din").prompt_notes[-1]
    assert "PatchDocument" in rendered or "patch" in rendered.lower()


def test_din_studio_profile_mentions_surface_and_mcp_ownership():
    rendered = render_repo_profile("din_studio")
    assert "SURFACE_MANIFEST" in rendered
    assert "targets/mcp" in rendered
