"""Shared CrewAI tool lists (contract lookup + optional brief + quality gates + repo-scoped writer)."""

from __future__ import annotations

from din_agents.tools.change_brief_tool import ChangeBriefTool
from din_agents.tools.quality_gate_tool import QualityGateTool
from din_agents.tools.repo_contract_tool import RepoContractTool
from din_agents.tools.repo_file_write_tool import make_repo_file_write_tool


def tools_with_change_brief(repo_id: str) -> list:
    """Contract, routing brief, quality gates, and file writes for ``repo_id``."""
    return [
        RepoContractTool(),
        ChangeBriefTool(),
        QualityGateTool(),
        make_repo_file_write_tool(repo_id),
    ]


def tools_without_change_brief(repo_id: str) -> list:
    """Contract, quality gates, and file writes (no change-brief builder)."""
    return [
        RepoContractTool(),
        QualityGateTool(),
        make_repo_file_write_tool(repo_id),
    ]
