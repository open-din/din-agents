# AGENTS — din-agents

## LOAD ORDER

1. `AGENTS.md`
2. `project/ROUTE_CARD.json`
3. `../project/WORKSPACE_MANIFEST.json`
4. One matching file in `project/skills/`
5. The exact source file and exact test file

## ROUTE HERE WHEN

- The request changes routing, quality-gate selection, CrewAI prompts, repo ownership metadata, or workspace automation.
- The request changes `src/din_agents/shared/repo_profiles.py`, `rules.py`, `flow.py`, or repo-scoped tools.

## ROUTE AWAY WHEN

- Public patch schema, exports, or docs/components -> `react-din`
- Runtime, compiler, registry, migration, FFI, WASM -> `din-core`
- Editor, MCP, launcher, or shell workflows -> `din-studio`

## ENTRY POINTS

- `project/ROUTE_CARD.json`
- `src/din_agents/flow.py`
- `src/din_agents/shared/repo_profiles.py`
- `src/din_agents/shared/rules.py`

## SKILL MAP

- Repo routing -> `project/skills/skills-router/SKILL.md`
- CrewAI bootstrap -> `project/skills/getting-started/SKILL.md`
- Agent shaping -> `project/skills/design-agent/SKILL.md`
- Task/output shaping -> `project/skills/design-task/SKILL.md`
- Docs lookup -> `project/skills/ask-docs/SKILL.md`

## HARD RULES

- Routing metadata comes from `../project/WORKSPACE_MANIFEST.json`.
- Use `project/ROUTE_CARD.json` before loading repo summaries or API summaries.
- Keep repo file tools scoped to one repo root.
- Do not redefine sibling ownership in code without updating manifests and docs.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
