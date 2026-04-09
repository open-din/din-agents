from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_din_core_prompt_contract_contains_expected_agents_and_tasks():
    agents = _read("src/din_agents/crews/din_core/config/agents.yaml")
    tasks = _read("src/din_agents/crews/din_core/config/tasks.yaml")

    assert "patch_contract_steward:" in agents
    assert "registry_parity_engineer:" in agents
    assert "rust_quality_runner:" in agents
    assert "assess_patch_contract:" in tasks
    assert "plan_rust_validation:" in tasks
    assert "Do not look up quality gates with tools." in tasks


def test_react_din_prompt_contract_contains_expected_agents_and_tasks():
    agents = _read("src/din_agents/crews/react_din/config/agents.yaml")
    tasks = _read("src/din_agents/crews/react_din/config/tasks.yaml")

    assert "patch_schema_steward:" in agents
    assert "component_coverage_maintainer:" in agents
    assert "library_quality_runner:" in agents
    assert "assess_public_surface:" in tasks
    assert "plan_library_validation:" in tasks
    assert "Do not look up quality gates with tools." in tasks


def test_din_studio_prompt_contract_contains_expected_agents_and_tasks():
    agents = _read("src/din_agents/crews/din_studio/config/agents.yaml")
    tasks = _read("src/din_agents/crews/din_studio/config/tasks.yaml")

    assert "editor_node_owner:" in agents
    assert "surface_guardian:" in agents
    assert "mcp_target_maintainer:" in agents
    assert "studio_ai_integrator:" in agents
    assert "review_mcp_impact:" in tasks
    assert "plan_studio_execution:" in tasks
    assert "Do not look up quality gates with tools." in tasks
