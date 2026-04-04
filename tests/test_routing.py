from din_agents.shared.rules import route_request


def test_routes_rust_runtime_request_to_din_core():
    decision = route_request("Investigate a Rust FFI and patch migration issue in din-core.")
    assert decision.route == "din_core"
    assert decision.affected_repos == ["din_core"]


def test_routes_public_component_request_to_react_din():
    decision = route_request("Update a public React component and docs/components coverage in react-din.")
    assert decision.route == "react_din"
    assert decision.affected_repos == ["react_din"]


def test_routes_editor_surface_request_to_din_studio():
    decision = route_request("Adjust the launcher panel workflow and SURFACE_MANIFEST entry in din-studio.")
    assert decision.route == "din_studio"
    assert decision.affected_repos == ["din_studio"]


def test_escalates_patch_schema_request_across_repos():
    decision = route_request("Plan a patch schema compatibility update across din-core and react-din.")
    assert decision.route == "cross_repo"
    assert decision.cross_repo is True
    assert "din_core" in decision.affected_repos
    assert "react_din" in decision.affected_repos
