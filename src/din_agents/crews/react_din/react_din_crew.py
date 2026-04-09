from crewai import Agent, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from din_agents.shared.cli_prefs import cli_verbose, with_cli_task_config
from din_agents.shared.crew_context import TruncatingCrew
from din_agents.shared.crew_tools import analysis_tools, execution_tools
from din_agents.shared.model_routing import agent_llm_kwargs
from din_agents.shared.task_guardrails import require_markdown_execution_brief


@CrewBase
class ReactDinCrew:
    """Crew specialized in react-din ownership and validation."""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def patch_schema_steward(self) -> Agent:
        return Agent(
            config=self.agents_config["patch_schema_steward"],  # type: ignore[index]
            tools=analysis_tools("react_din"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("binding"),
        )

    @agent
    def component_coverage_maintainer(self) -> Agent:
        return Agent(
            config=self.agents_config["component_coverage_maintainer"],  # type: ignore[index]
            tools=analysis_tools("react_din"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("impact"),
        )

    @agent
    def library_quality_runner(self) -> Agent:
        return Agent(
            config=self.agents_config["library_quality_runner"],  # type: ignore[index]
            tools=execution_tools("react_din"),
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("testing"),
        )

    @agent
    def library_brief_runner(self) -> Agent:
        return Agent(
            config=self.agents_config["library_quality_runner"],  # type: ignore[index]
            tools=[],
            max_iter=10,
            verbose=cli_verbose(),
            **agent_llm_kwargs("testing"),
        )

    @task
    def assess_public_surface(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["assess_public_surface"]),  # type: ignore[index]
        )

    @task
    def review_docs_and_coverage(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["review_docs_and_coverage"]),  # type: ignore[index]
            context=[],
        )

    @task
    def plan_library_validation(self) -> Task:
        return Task(
            config=with_cli_task_config(self.tasks_config["plan_library_validation"]),  # type: ignore[index]
            agent=self.library_brief_runner(),
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
