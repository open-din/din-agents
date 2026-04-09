from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from din_agents.shared.repo_profiles import render_quality_gates


class QualityGateToolInput(BaseModel):
    """Input schema for QualityGateTool."""

    repo_id: str = Field(..., description="One of: din_core, react_din, din_studio.")


class QualityGateTool(BaseTool):
    """Looks up shell quality gate commands from repo profiles."""
    name: str = "quality_gate_lookup"
    description: str = (
        "Return the quality gate commands for a DIN repository. "
        "Use when you need the exact validation commands to mention in a plan."
    )
    args_schema: Type[BaseModel] = QualityGateToolInput

    def _run(self, repo_id: str) -> str:
        return render_quality_gates(repo_id)
