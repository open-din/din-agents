# SKILL: design-agent

## REPO

`din-agents`

## WHEN TO USE

- A request changes agent roles, goals, tools, memory, or model assignment
- Crew behavior needs to be reshaped without changing repo ownership

## STEPS

1. Read the din-agents summary, API summary, and repo manifest.
2. Update the agent contract with explicit ownership and output expectations.
3. Keep prompts short and grounded in manifest-driven repo routing.
4. Avoid embedding sibling repo semantics that belong in their own docs.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
