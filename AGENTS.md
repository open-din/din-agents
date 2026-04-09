# AGENTS — din-agents

## LOAD ORDER

1. `AGENTS.md`
2. `project/SUMMARY.md`
3. `../docs/summaries/din-agents-api.md`
4. `project/REPO_MANIFEST.json`
5. One matching file in `project/skills/`

## ROUTE HERE WHEN

- The request changes routing, quality-gate selection, CrewAI prompts, repo ownership metadata, or workspace automation.
- The request changes `src/din_agents/shared/repo_profiles.py`, `rules.py`, `flow.py`, or repo-scoped tools.

## ROUTE AWAY WHEN

- Public patch schema, exports, or docs/components -> `react-din`
- Runtime, compiler, registry, migration, FFI, WASM -> `din-core`
- Editor, MCP, launcher, or shell workflows -> `din-studio`

## ENTRY POINTS

- `src/din_agents/flow.py`
- `src/din_agents/shared/repo_profiles.py`
- `src/din_agents/shared/rules.py`
- `project/REPO_MANIFEST.json`

## SKILL MAP

- Repo routing -> `project/skills/skills-router/SKILL.md`
- CrewAI bootstrap -> `project/skills/getting-started/SKILL.md`
- Agent shaping -> `project/skills/design-agent/SKILL.md`
- Task/output shaping -> `project/skills/design-task/SKILL.md`
- Docs lookup -> `project/skills/ask-docs/SKILL.md`

## HARD RULES

- Routing metadata comes from `../project/WORKSPACE_MANIFEST.json`.
- Keep repo file tools scoped to one repo root.
- Do not redefine sibling ownership in code without updating manifests and docs.

## VALIDATION

- `uv run pytest`
- `uv run ruff check src`
