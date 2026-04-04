---
name: crewai-skills-router
description: Route CrewAI questions to the right local skill. Use when a request is about CrewAI architecture, agent design, task design, or when deciding whether to consult official CrewAI docs.
---

# CrewAI Skills Router

Use this skill first when a request mentions CrewAI but the right specialized skill is not obvious.

## Routing

Choose exactly one default skill when possible:

- `crewai-getting-started` for project scaffolding, choosing between `LLM.call()`, `Agent.kickoff()`, `Crew.kickoff()`, or `Flow`, and for overall app structure.
- `crewai-design-agent` for agent role/goal/backstory, tools, LLM selection, memory, knowledge, delegation, planning, and execution controls.
- `crewai-design-task` for task descriptions, `expected_output`, dependencies, guardrails, structured output, task-level tools, and task configuration.
- `crewai-ask-docs` when the question is API-specific, newer than the curated skills, error-driven, or needs confirmation from the official docs.

## Selection Rules

1. If the user is starting a project or asking "which abstraction should I use?", pick `crewai-getting-started`.
2. If the user is shaping agent behavior, capabilities, or configuration, pick `crewai-design-agent`.
3. If the user is defining what work gets done and what the output must look like, pick `crewai-design-task`.
4. If the curated skill might be outdated or incomplete for the question, pick `crewai-ask-docs`.

## Mixed Requests

For mixed requests, choose the primary skill first, then load one secondary skill only if needed:

- Architecture + agent setup: start with `crewai-getting-started`, then `crewai-design-agent`.
- Agent + task quality: start with `crewai-design-task`, then `crewai-design-agent`.
- Design question + API verification: start with the relevant design skill, then `crewai-ask-docs`.

## Quick Examples

- "Should I use a Flow or a Crew?" -> `crewai-getting-started`
- "How should I configure this researcher agent?" -> `crewai-design-agent`
- "How do I write `expected_output` for this task?" -> `crewai-design-task`
- "What parameters does `Crew()` support?" -> `crewai-ask-docs`
