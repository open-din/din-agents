from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from din_agents.shared.rules import render_routing_decision, route_request


class ChangeBriefToolInput(BaseModel):
    """Input schema for ChangeBriefTool."""

    request: str = Field(..., description="The user request or change description.")
    repo_hint: str = Field(
        default="",
        description="Optional explicit repo hint such as din_core, react_din, or din_studio.",
    )


class ChangeBriefTool(BaseTool):
    name: str = "change_brief_builder"
    description: str = (
        "Summarize routing and cross-repo impact for a DIN change request. "
        "Use when a task needs a deterministic ownership and escalation brief."
    )
    args_schema: Type[BaseModel] = ChangeBriefToolInput

    def _run(self, request: str, repo_hint: str = "") -> str:
        decision = route_request(request=request, repo_hint=repo_hint or None)
        return render_routing_decision(decision)
