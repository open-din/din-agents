from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from din_agents.shared.repo_profiles import render_repo_profile


class RepoContractToolInput(BaseModel):
    """Input schema for RepoContractTool."""

    repo_id: str = Field(..., description="One of: din_core, react_din, din_studio.")


class RepoContractTool(BaseTool):
    """Returns markdown repo profile data (docs paths, boundaries, gates)."""
    name: str = "repo_contract_lookup"
    description: str = (
        "Return the canonical repo profile, ownership boundaries, docs, and quality gates "
        "for a DIN repository. Use when you need repo-specific constraints before drafting a plan."
    )
    args_schema: Type[BaseModel] = RepoContractToolInput

    def _run(self, repo_id: str) -> str:
        return render_repo_profile(repo_id)
