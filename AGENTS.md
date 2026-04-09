# AGENTS

Canonical contract for Codex, Claude, Cursor, and other agents operating in `din-agents`.

## Scope

Python CrewAI control plane that routes work across `din-core`, `react-din`, and `din-studio`. For product intent in those repos, use each sibling’s `project/SUMMARY.md`, `project/USERFLOW.md`, and `project/TEST_MATRIX.md`—cite them; do not duplicate them here.

## Quality gates (pre-merge)

From this repository root:

1. `uv run pytest`
2. (Optional docstrings) `uv run ruff check src`

Sibling repos enforce their own gates via `din_agents.shared.repo_profiles` (exposed to crews and tools).

## Documentation Strategy

- Prefer this `AGENTS.md`, `README.md`, and generated HTML under `docs/generated/` (after `./scripts/generate-docs.sh`) when you need module or public API structure.
- Do not load generated docs by default; open them on demand to save tokens.

## Documentation Rules

- Public Python entrypoints (`main.py`, `flow.py`, `shared/*.py`, `tools/*.py`) should use Google-style docstrings for modules, classes, and public functions.
- After changing public behavior, run `./scripts/generate-docs.sh` locally to confirm `pdoc` succeeds.

## Operational notes

- Configure `DIN_CORE_PATH`, `REACT_DIN_PATH`, and `DIN_STUDIO_PATH` to local checkouts.
- Repo profiles and quality gate commands live in `src/din_agents/shared/repo_profiles.py`.
