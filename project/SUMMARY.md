# SUMMARY

## PURPOSE

Control plane for routing DIN requests to the correct repo, selecting quality gates, and assembling repo-specific briefs.

## OWNS

- Workspace routing heuristics and repo ownership metadata consumption
- Quality-gate selection and compact repo route cards
- CrewAI prompt inputs for sibling repos
- Repo-scoped file and contract tools

## DOES NOT OWN

- Public patch schema, package exports, or docs/components
- Runtime semantics, registry, or migration logic
- Editor workflows, shell UX, or MCP behavior

## USE WHEN

- The task changes routing, repo selection, control-plane prompts, repo metadata, or workspace automation.

## DO NOT USE WHEN

- The task is public API or schema work -> `react-din`
- The task is runtime or registry work -> `din-core`
- The task is editor or MCP work -> `din-studio`

## RELATED REPOS

- `react-din`, `din-core`, and `din-studio` provide the owned product surfaces
- `../project/WORKSPACE_MANIFEST.json` is the routing source of truth
