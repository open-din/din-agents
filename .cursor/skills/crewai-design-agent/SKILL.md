---
name: crewai-design-agent
description: CrewAI agent design and configuration. Use when creating, configuring, or debugging CrewAI agents, including role/goal/backstory, model selection, tools, delegation, planning, code execution, memory, and knowledge sources.
---

# CrewAI Agent Design

How to design focused agents that have the right expertise, configuration, and capabilities.

## Priority Rule

Spend more effort on task quality than agent polish. If a request is mostly about what should be done and what success looks like, switch to `crewai-design-task`.

## Role-Goal-Backstory Framework

Every agent needs:

- `role`: who the agent is; make it specific
- `goal`: what outcome it is trying to produce
- `backstory`: why it is qualified and how it tends to work

Prefer:

- `Senior Data Researcher specializing in {topic}`

Over:

- `Researcher`

## Good Agent Defaults

- Prefer specialist agents over generalists
- Keep tools focused: usually 3-5 max
- Disable delegation unless the workflow truly benefits from it
- Lower `max_iter` when tasks are well-defined
- Add timeouts for production agents

## Core Configuration

```python
from crewai import Agent

agent = Agent(
    role="Senior Research Analyst",
    goal="Find factual, source-backed answers",
    backstory="Expert researcher known for careful sourcing and explicit uncertainty.",
    llm="openai/gpt-4o",
    tools=[...],
    max_iter=15,
    max_execution_time=300,
    verbose=True,
)
```

## Tool Rules

- If an agent must search, fetch, browse, or read external data, give it tools.
- An agent with no relevant tools will invent data instead of retrieving it.
- Prefer official MCP servers over native tools when available.
- Use task-level tools only when that single task needs narrower or different access.

## Model Rules

- Use the main `llm` for reasoning quality.
- Use `function_calling_llm` to save cost on tool-calling mechanics.
- Choose stronger models for vague or high-stakes outputs, not for every task by default.

## Advanced Capabilities

Enable only when justified:

- `planning=True` for complex tasks that benefit from explicit pre-planning
- `allow_delegation=True` for crews with clear handoff boundaries
- `allow_code_execution=True` only in controlled environments
- `inject_date=True` for time-sensitive work

## Memory And Knowledge

Use memory when the system should learn from prior executions.

Use knowledge sources when the agent must consult domain documents or data.

Keep the distinction clear:

- memory = past runs and outcomes
- knowledge = reference material via RAG

## Agent In YAML

Prefer YAML for reusable projects:

```yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover the top developments in {topic} with supporting evidence.
  backstory: >
    You're a careful researcher who always cites sources and flags uncertainty.
```

Keep the Python method name aligned with the YAML key.

## Common Mistakes

- Generic roles like `Assistant`
- Too many tools on one agent
- No tools for external-data tasks
- Turning backstory into task instructions
- Using delegation by default
- Raising `max_iter` instead of fixing a vague task

## References

- [Custom Tools](references/custom-tools.md)
- [Memory & Knowledge](references/memory-and-knowledge.md)

## Related Skills

- `crewai-getting-started`
- `crewai-design-task`
- `crewai-ask-docs`
