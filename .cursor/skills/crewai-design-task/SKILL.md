---
name: crewai-design-task
description: CrewAI task design and configuration. Use when creating, configuring, or debugging CrewAI tasks, including descriptions, expected_output, dependencies, structured output, guardrails, task-level tools, and output files.
---

# CrewAI Task Design

How to write tasks that reliably produce good outputs.

## Priority Rule

Task quality matters more than agent polish. If the work is failing, first tighten the task before changing the agent.

## Anatomy Of A Good Task

Every task needs:

- `description`: what to do, how to do it, context, constraints, and inputs
- `expected_output`: what done looks like

Good `expected_output` should specify:

- format
- structure
- scope or length
- quality markers

## Single-Purpose Rule

One task should have one objective.

Split this:

- research
- analysis
- writing
- editing

Do not collapse all of them into one large task.

## Core Example

```yaml
research_task:
  description: >
    Research {topic}. Identify the top 5 developments, cite sources,
    and note uncertainty or competing views.
  expected_output: >
    A structured brief with 5 sections. Each section includes the trend,
    a short summary, sources, and an impact rating.
  agent: researcher
```

## Dependencies

- In sequential crews, later tasks automatically receive earlier outputs.
- Use `context=[...]` when you need explicit non-linear dependencies.
- In hierarchical workflows, be explicit about data flow.

## Structured Output

Use:

- `response_format=Model` for `LLM.call()` and `Agent.kickoff()`
- `output_pydantic=Model` for `Task`
- `output_json=Model` when downstream code wants a dictionary

Critical rule:

- `expected_output` stays a plain-language string
- the model class goes in `response_format`, `output_pydantic`, or `output_json`

## Guardrails

Add guardrails when output quality matters to downstream steps.

Use:

- function guardrails for deterministic checks
- LLM guardrails for subjective quality checks

Guardrails should reject bad output with a concrete retry instruction.

## Task-Level Tools

Use task-level tools when:

- one task needs tools the agent does not normally carry
- you want to narrow the tool set for one task
- the same agent has different tool needs across tasks

## Output Files

Use `output_file` when the task should produce a durable artifact such as a report or JSON file.

## Common Mistakes

- Vague descriptions
- Vague `expected_output`
- Multiple objectives in one task
- Missing context between dependent tasks
- Referring to a Pydantic class inside `expected_output`
- Asking for external facts without tools
- Over-constraining the output until retries loop

## References

- [Structured Output](references/structured-output.md)

## Related Skills

- `crewai-getting-started`
- `crewai-design-agent`
- `crewai-ask-docs`
