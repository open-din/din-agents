from din_agents.shared.rules import select_quality_gates


def test_select_quality_gates_returns_expected_commands_for_each_repo():
    commands = select_quality_gates(["din_core", "react_din", "din_studio"])

    assert commands["din_core"] == [
        "cargo fmt --all --check",
        "cargo clippy --workspace --all-targets -- -D warnings",
        "cargo test --workspace",
    ]
    assert "npm run ci:check" in commands["react_din"]
    assert "npm run test:e2e" in commands["din_studio"]
