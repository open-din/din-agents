from din_agents.shared.rules import select_quality_gates


def test_select_quality_gates_returns_expected_commands_for_each_repo():
    commands = select_quality_gates(["din_core", "react_din", "din_studio", "din_agents"])

    assert commands["din_core"] == [
        "cargo fmt --all --check",
        "cargo clippy --workspace --all-targets -- -D warnings",
        "cargo test --workspace",
    ]
    assert commands["react_din"] == [
        "npm run lint",
        "npm run typecheck",
        "npm run ci:check",
    ]
    assert commands["din_studio"] == [
        "npm run lint",
        "npm run typecheck",
        "npm run test",
        "npm run test:e2e",
    ]
    assert commands["din_agents"] == [
        "uv run pytest",
        "uv run ruff check src",
    ]
