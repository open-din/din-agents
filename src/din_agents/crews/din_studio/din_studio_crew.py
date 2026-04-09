from crewai import Agent, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from din_agents.shared.cli_prefs import cli_verbose, mcp_task_scope_guard, with_cli_task_config
from din_agents.shared.crew_context import TruncatingCrew
from din_agents.shared.crew_tools import analysis_tools, execution_tools
from din_agents.shared.model_routing import agent_llm_kwargs
from din_agents.shared.task_guardrails import require_markdown_execution_brief


@CrewBase
class DinStudioCrew:
    """Crew specialized in din-studio ownership and validation."""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def editor_node_owner(self) -> Agent:
        return Agent(
            config=self.agents_config["editor_node_owner"],  # type: ignore[index]
            tools=analysis_tools("din_studio"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("planning"),
        )

    @agent
    def surface_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config["surface_guardian"],  # type: ignore[index]
            tools=analysis_tools("din_studio"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("impact"),
        )

    @agent
    def mcp_target_maintainer(self) -> Agent:
        return Agent(
            config=self.agents_config["mcp_target_maintainer"],  # type: ignore[index]
            tools=analysis_tools("din_studio"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("binding"),
        )

    @agent
    def studio_ai_integrator(self) -> Agent:
        return Agent(
            config=self.agents_config["studio_ai_integrator"],  # type: ignore[index]
            tools=execution_tools("din_studio"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("doc"),
        )

    @agent
    def studio_brief_runner(self) -> Agent:
        return Agent(
            config=self.agents_config["studio_ai_integrator"],  # type: ignore[index]
            tools=[],
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("doc"),
        )

    @task
    def assess_editor_ownership(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["assess_editor_ownership"]),  # type: ignore[index]
        )

    @task
    def review_surface_requirements(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["review_surface_requirements"]),  # type: ignore[index]
            context=[],
        )

    @task
    def review_mcp_impact(self) -> Task:
        return Task(
            config=with_cli_task_config(
                self.tasks_config["review_mcp_impact"],  # type: ignore[index]
                extra_description_suffix=mcp_task_scope_guard(),
            ),
            context=[],
        )

    @task
    def plan_studio_execution(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["plan_studio_execution"]),  # type: ignore[index]
            agent=self.studio_brief_runner(),
            context=[],
            guardrail=require_markdown_execution_brief,
            guardrail_max_retries=4,
        )

    @crew
    def crew(self) -> TruncatingCrew:
        return TruncatingCrew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=cli_verbose(),
        )
