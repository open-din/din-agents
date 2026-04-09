"""Control-plane crew input shaping."""

from din_agents.flow import DinControlPlaneFlow, _truncate_repo_prompt_list


def test_truncate_repo_prompt_list() -> None:
    items = [f"item-{i}" for i in range(10)]
    out = _truncate_repo_prompt_list(items, 4, "widgets")
    assert "item-0" in out
    assert "item-3" in out
    assert "item-4" not in out
    assert "+6 more widgets" in out


def test_crew_inputs_compact_truncates_lists(monkeypatch) -> None:
    class Profile:
        path = "p"
        summary_path = "s"
        api_summary_path = "a"
        repo_manifest_path = "m"
        entry_points = tuple(f"e{i}" for i in range(30))
        hard_boundaries = tuple(f"b{i}" for i in range(20))

    monkeypatch.setenv("DIN_AGENTS_COMPACT_PROMPTS", "1")
    monkeypatch.setattr("din_agents.flow.get_repo_profile", lambda _rid: Profile())

    flow = DinControlPlaneFlow()
    flow.state.request = "test"
    flow.state.repo_hint = ""
    flow.state.quality_commands = {"din_core": []}

    inputs = flow._crew_inputs("din_core")
    assert "+22 more entry points" in inputs["entry_points"]
    assert "+14 more boundaries" in inputs["hard_boundaries"]


def test_crew_inputs_drop_redundant_brief_blobs(monkeypatch) -> None:
    class Profile:
        path = "p"
        summary_path = "s"
        api_summary_path = "a"
        repo_manifest_path = "m"
        entry_points = ["e0"]
        hard_boundaries = ["b0"]

    monkeypatch.setattr("din_agents.flow.get_repo_profile", lambda _rid: Profile())

    flow = DinControlPlaneFlow()
    flow.state.request = "test"
    flow.state.repo_hint = ""
    flow.state.quality_commands = {"din_core": []}

    inputs = flow._crew_inputs("din_core")
    assert "repo_contract_output" not in inputs
    assert "change_brief_output" not in inputs
    assert "routing_reasons" in inputs
