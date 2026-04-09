# AGENTS

Canonical contract for Codex, Claude, Cursor, and other agents operating in `din-agents`.

## Scope

Python CrewAI control plane that routes work across `din-core`, `react-din`, and `din-studio`. For product intent in those repos, use each sibling’s `project/SUMMARY.md`, `project/USERFLOW.md`, and `project/TEST_MATRIX.md`—cite them; do not duplicate them here.

## Quality gates (pre-merge)

From this repository root:

1. `uv run pytest`
2. `uv run ruff check src`
3. `./scripts/generate-docs.sh` — must succeed before merge when public Python modules or documented entrypoints change

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

## Documentation Access Order (CRITICAL)

Always follow this sequence when gathering context. Do not skip steps.

1. This `AGENTS.md` — ownership, rules, quality gates
2. `README.md` and `docs/FlowArchitecture.md` — hand-written index; use workspace `docs/README.md` when routing the whole stack
3. Workspace summary `../docs/summaries/din-agents-api.md` (when using the `open-din` container) — compressed API overview
4. `docs/generated/` from `./scripts/generate-docs.sh` — reference only, at most two pages at a time
5. Source under `src/din_agents/` — last resort

## Context Budget Rules

- Load at most two documentation files per step; close or stop using them before opening more
- Load at most one repository’s context unless the task is explicitly cross-repo
- Prefer summaries over generated HTML; prefer generated HTML over bulk source reads
- Never bulk-load `docs/generated/` — open only the specific module pages needed
- Minimize total loaded context at all times

## Code Reading Policy

- Do **not** read source files when documentation answers the question
- Exhaust summaries and targeted generated docs before opening `src/`
- When source reading is required, scope to the exact module — do not scan entire directories

## Documentation Ownership

- This repository owns `docs/`, this `AGENTS.md`, and `docs/generated/` from pdoc
- Workspace summaries (`open-din/docs/summaries/`) must stay consistent when flow, tools, or public modules change
- A public control-plane or tool change is incomplete until docstrings, `FlowArchitecture.md`, and the matching summary are updated when the surface changes

## Documentation Freshness

- Regenerate docs after public behavior changes (`./scripts/generate-docs.sh`)
- Treat `docs/generated/` as ephemeral — do not treat stale output as authoritative
- After regeneration, decide whether `../docs/summaries/din-agents-api.md` needs an update
- Do not cite outdated documentation as authoritative
