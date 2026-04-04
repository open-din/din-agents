---
name: crewai-getting-started
description: CrewAI architecture decisions and project scaffolding. Use when starting a CrewAI project, choosing between LLM.call() vs Agent.kickoff() vs Crew.kickoff() vs Flow, scaffolding with `crewai create flow`, wiring YAML config, or designing Flow-based app structure.
---

# CrewAI Getting Started

How to choose the right abstraction, scaffold correctly, and wire a production-friendly CrewAI app.

## Mandatory Rule

Never hand-create a new CrewAI project from scratch when the CLI can scaffold it.

Use:

```bash
crewai create flow my_project
```

Then edit the generated files. Prefer underscores in project names, not hyphens.

## Default Architecture Choice

Use the simplest abstraction that fits:

- `LLM.call()` for one prompt, no tools, no multi-agent orchestration.
- `Agent.kickoff()` for one agent with tools and reasoning.
- `Crew.kickoff()` for multi-agent collaboration inside one bounded workflow.
- `Flow` for production apps with state, routing, retries, branching, persistence, or multiple crews/agents.

Default recommendation:

- For real applications, start with a `Flow`.
- Inside the `Flow`, call `LLM.call()`, `Agent.kickoff()`, or `Crew.kickoff()` as needed.

## Decision Shortcut

1. No tools and no multi-step reasoning -> `LLM.call()`
2. One reasoning agent -> `Agent.kickoff()`
3. Several agents collaborating on one stage -> `Crew.kickoff()`
4. Any app workflow, routing, or stateful orchestration -> `Flow`

## Scaffold Workflow

1. Run `crewai create flow <name>`
2. Edit the generated YAML and Python files
3. Run `crewai install`
4. Run `crewai run`

## Core Wiring Rules

- Keep agent keys in `agents.yaml` aligned with `@agent` method names.
- Keep task keys in `tasks.yaml` aligned with `@task` method names.
- Use `{variable}` placeholders in YAML and pass matching values through `kickoff(inputs={...})`.
- Treat `expected_output` as a human-readable string, not a model class reference.

## Flow-First Pattern

This is the safest default for production:

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class AppState(BaseModel):
    topic: str = ""
    result: str = ""

class AppFlow(Flow[AppState]):
    @start()
    def begin(self):
        ...

    @listen(begin)
    def run_step(self):
        ...
```

Inside Flow steps:

- use `Agent.kickoff()` when each step has one distinct agent
- use `Crew.kickoff()` when several agents must collaborate in that step
- use `LLM.call()` for cheap classification, extraction, or formatting

## Common Mistakes

- Using hyphens in the project name and then hitting import issues
- Forgetting `inputs=` so YAML placeholders stay literal
- Mismatching YAML keys and Python method names
- Reaching for a Crew when a single agent is enough
- Building a production workflow without a Flow

## References

- [Flow Routing, Persistence, Streaming & Human Feedback](references/flow-routing.md)
- [MCP Servers](references/mcp-servers.md)
- [Tools Catalog](references/tools-catalog.md)

## Related Skills

- `crewai-design-agent`
- `crewai-design-task`
- `crewai-ask-docs`
