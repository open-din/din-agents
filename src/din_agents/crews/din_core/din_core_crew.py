from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from din_agents.shared.cli_prefs import cli_verbose, with_cli_task_config
from din_agents.shared.model_routing import agent_llm_kwargs
from din_agents.tools import ChangeBriefTool, QualityGateTool, RepoContractTool


@CrewBase
class DinCoreCrew:
    """Crew specialized in din-core ownership and validation."""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def patch_contract_steward(self) -> Agent:
        return Agent(
            config=self.agents_config["patch_contract_steward"],  # type: ignore[index]
            tools=[RepoContractTool(), ChangeBriefTool(), QualityGateTool()],
            verbose=cli_verbose(),
            **agent_llm_kwargs("planning"),
        )

    @agent
    def registry_parity_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["registry_parity_engineer"],  # type: ignore[index]
            tools=[RepoContractTool(), ChangeBriefTool(), QualityGateTool()],
            verbose=cli_verbose(),
            **agent_llm_kwargs("impact"),
        )

    @agent
    def rust_quality_runner(self) -> Agent:
        return Agent(
            config=self.agents_config["rust_quality_runner"],  # type: ignore[index]
            tools=[RepoContractTool(), QualityGateTool()],
            verbose=cli_verbose(),
            **agent_llm_kwargs("testing"),
        )

    @task
    def assess_patch_contract(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["assess_patch_contract"]),  # type: ignore[index]
        )

    @task
    def review_registry_and_runtime(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["review_registry_and_runtime"]),  # type: ignore[index]
        )

    @task
    def plan_rust_validation(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["plan_rust_validation"]),  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=cli_verbose(),
        )
