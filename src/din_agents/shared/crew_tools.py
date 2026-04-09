"""Shared CrewAI tool lists tuned for prompt size and repo-scoped execution."""

from __future__ import annotations

from din_agents.tools.repo_file_read_tool import make_repo_file_read_tool
from din_agents.tools.repo_file_write_tool import make_repo_file_write_tool


def analysis_tools(repo_id: str) -> list:
    """Minimal analysis toolkit: targeted repo reads only."""
    return [
        make_repo_file_read_tool(repo_id),
    ]


def execution_tools(repo_id: str) -> list:
    """Execution toolkit: targeted reads and optional writes.

    Quality gates are injected into task inputs directly; keeping them out of the
    native tool list avoids low-value lookup loops on Anthropic-backed runs.
    """
    return [
        make_repo_file_read_tool(repo_id),
        make_repo_file_write_tool(repo_id),
    ]
