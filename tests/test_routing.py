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


def test_routes_control_plane_request_to_din_agents():
    decision = route_request("Tighten repo routing and quality gate selection in din-agents.")
    assert decision.route == "din_agents"
    assert decision.affected_repos == ["din_agents"]


def test_escalates_patch_schema_request_across_repos():
    decision = route_request("Plan a patch schema compatibility update across din-core and react-din.")
    assert decision.route == "cross_repo"
    assert decision.cross_repo is True
    assert decision.affected_repos == ["react_din", "din_core"]


def test_studio_request_escalates_when_public_api_contract_is_touched():
    decision = route_request("Update din-studio codegen after a public API contract change.")
    assert decision.route == "cross_repo"
    assert decision.cross_repo is True
    assert decision.affected_repos == ["din_studio", "react_din"]


def test_husky_for_each_project_routes_product_repos_only():
    decision = route_request(
        "For each project, install Husky pre-commit hook that runs tests before commit.",
    )
    assert decision.route == "cross_repo"
    assert decision.cross_repo is True
    assert decision.affected_repos == ["din_core", "react_din", "din_studio"]
