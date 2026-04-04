# Example tasks for DIN Agents

These files are **sample user requests** you can pass to the control plane—not CrewAI `tasks.yaml` definitions (those live under `src/din_agents/crews/**/config/`).

## How to run

From the `din-agents` repository root (with `.env` and sibling repo paths configured):

```bash
uv run run_request "Your request text here"
```

Or:

```bash
DIN_AGENTS_REQUEST="Your request text here" uv run kickoff
```

## Contents

| File | Intent |
|------|--------|
| [examples/din-core.md](examples/din-core.md) | Rust patch, registry, FFI, migrations |
| [examples/react-din.md](examples/react-din.md) | Public API, patch schema, docs/coverage |
| [examples/din-studio.md](examples/din-studio.md) | Editor, surfaces, MCP, AI catalog |
| [examples/cross-repo.md](examples/cross-repo.md) | Requests that should stress routing / coordination |

Copy a quoted line into `run_request` or set `DIN_AGENTS_REQUEST` to the same string.
