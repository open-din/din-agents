from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from din_agents.shared.repo_profiles import render_repo_profile


class RepoContractToolInput(BaseModel):
    """Input schema for RepoContractTool."""

    repo_id: str = Field(..., description="One of: din_core, react_din, din_studio, din_agents.")


class RepoContractTool(BaseTool):
    """Returns a compact manifest-driven repo route card."""
    name: str = "repo_contract_lookup"
    description: str = (
        "Return the compact repo route card with role, tags, entry points, boundaries, "
        "and validation commands for a DIN repository."
    )
    args_schema: Type[BaseModel] = RepoContractToolInput

    def _run(self, repo_id: str) -> str:
        return render_repo_profile(repo_id)
