# SKILL: getting-started

## REPO

`din-agents`

## WHEN TO USE

- A request changes the control-plane bootstrap or workspace entry flow
- You need the default path for routing a new DIN workspace request

## STEPS

1. Start from `../project/WORKSPACE_MANIFEST.json`.
2. Resolve one repo first, then load that repo summary and API summary.
3. Escalate only for shared contracts or explicit workspace-wide requests.
4. Keep prompts, docs, and manifests aligned with the same ownership map.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
