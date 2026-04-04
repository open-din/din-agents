from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from din_agents.shared.cli_prefs import cli_verbose, mcp_task_scope_guard, with_cli_task_config
from din_agents.shared.model_routing import agent_llm_kwargs
from din_agents.tools import ChangeBriefTool, QualityGateTool, RepoContractTool


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
            tools=[RepoContractTool(), ChangeBriefTool(), QualityGateTool()],
            verbose=cli_verbose(),
            **agent_llm_kwargs("planning"),
        )

    @agent
    def surface_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config["surface_guardian"],  # type: ignore[index]
            tools=[RepoContractTool(), ChangeBriefTool(), QualityGateTool()],
            verbose=cli_verbose(),
            **agent_llm_kwargs("impact"),
        )

    @agent
    def mcp_target_maintainer(self) -> Agent:
        return Agent(
            config=self.agents_config["mcp_target_maintainer"],  # type: ignore[index]
            tools=[RepoContractTool(), ChangeBriefTool(), QualityGateTool()],
            verbose=cli_verbose(),
            **agent_llm_kwargs("binding"),
        )

    @agent
    def studio_ai_integrator(self) -> Agent:
        return Agent(
            config=self.agents_config["studio_ai_integrator"],  # type: ignore[index]
            tools=[RepoContractTool(), QualityGateTool()],
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
        )

    @task
    def review_mcp_impact(self) -> Task:
        return Task(
            config=with_cli_task_config(
                self.tasks_config["review_mcp_impact"],  # type: ignore[index]
                extra_description_suffix=mcp_task_scope_guard(),
            ),
        )

    @task
    def plan_studio_execution(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["plan_studio_execution"]),  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=cli_verbose(),
        )
