# SKILL: skills-router

## REPO

`din-agents`

## WHEN TO USE

- The right local CrewAI or control-plane skill is unclear
- A request mixes bootstrap, agent, task, and doc-lookup concerns

## STEPS

1. Choose exactly one default skill from `getting-started`, `design-agent`, `design-task`, or `ask-docs`.
2. Prefer the smallest skill that resolves the current blocker.
3. Load a second skill only when the first one leaves a concrete gap.
4. Keep the routing decision separate from generic CrewAI implementation details.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
