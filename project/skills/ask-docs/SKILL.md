# SKILL: ask-docs

## REPO

`din-agents`

## WHEN TO USE

- A CrewAI question needs official documentation, not local repo logic
- The local skills are insufficient or potentially stale

## STEPS

1. Confirm the question belongs to CrewAI or control-plane behavior.
2. Query official CrewAI docs for the exact API or behavior.
3. Return the shortest answer that resolves the blocker.
4. Keep workspace routing rules separate from generic CrewAI guidance.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
