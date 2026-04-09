# SKILL: design-task

## REPO

`din-agents`

## WHEN TO USE

- A request changes task descriptions, expected outputs, or guardrails
- Crew tasks need tighter routing, repo scoping, or validation language

## STEPS

1. Read the din-agents summary, API summary, and repo manifest.
2. Keep task prompts centered on route card, boundaries, and validation commands.
3. Remove redundant repo prose if the manifest already covers it.
4. Ensure output contracts stay decision-oriented and repo-scoped.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
