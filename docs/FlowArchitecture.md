# Control-plane flow architecture

## Purpose

Explain how `din-agents` routes a natural-language request without loading sibling repo sources.

## Flow

1. **`DinControlPlaneFlow` (`src/din_agents/flow.py`)** stores request text + routing results in `ControlPlaneState`.
2. **`route_request` / `select_quality_gates` (`shared/rules.py`)** use keyword scoring and `repo_profiles` metadata.
3. **Crews** (`crews/din_core`, `crews/react_din`, `crews/din_studio`) run templated agents/tasks with tools (file read/write, contract briefs, quality lookup).
4. **Outputs** merge into `output/control-plane-report.md` (configurable) as markdown.

## Quality gates exposed to crews

Defined in `shared/repo_profiles.py`, now including optional doc-generation commands for TypeScript and Rust repos.

## API HTML

Run `./scripts/generate-docs.sh` to refresh `docs/generated/` for this package only.
