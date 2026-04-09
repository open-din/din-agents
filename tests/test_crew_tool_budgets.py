"""Prompt-budget regressions for repo-scoped toolsets."""

from crewai.utilities.agent_utils import parse_tools, render_text_description_and_args

from din_agents.shared.crew_tools import analysis_tools, execution_tools


def _tool_desc_chars(tools: list) -> int:
    return len(render_text_description_and_args(parse_tools(tools)))


def test_analysis_tools_are_smaller_than_execution_tools() -> None:
    analysis = _tool_desc_chars(analysis_tools("din_core"))
    execution = _tool_desc_chars(execution_tools("din_core"))
    assert analysis < execution
    assert analysis < 1_500


def test_execution_tools_exclude_quality_gate_lookup() -> None:
    tools = execution_tools("din_core")
    names = [tool.name for tool in tools]
    assert "quality_gate_lookup" not in names
