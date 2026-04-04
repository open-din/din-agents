# DIN Agents

`din-agents` is the CrewAI control plane for the sibling repositories:

- `din-core`
- `react-din`
- `din-studio`

It provides:

- one CrewAI crew per repository
- a global Flow that routes requests to the right repo crew
- cross-repo escalation when a request touches shared contracts or ownership boundaries
- deterministic repo profiles and quality gate selection

## Requirements

- Python `>=3.10,<3.14`
- [`uv`](https://docs.astral.sh/uv/)
- CrewAI CLI

## Install

From the repository root:

```bash
uv sync
```

Or use the CrewAI workflow:

```bash
crewai install
```

## Environment

Set the variables from `.env.example`.

At minimum, provide:

```bash
OPENAI_API_KEY=...
OPENAI_MODEL_NAME=gpt-4o-mini
```

The control plane also expects local checkout paths for:

- `DIN_CORE_PATH`
- `REACT_DIN_PATH`
- `DIN_STUDIO_PATH`

### Models (LiteLLM)

CrewAI resolves chat completions through [LiteLLM](https://docs.litellm.ai/). This project forces the LiteLLM code path (`is_litellm=True`) so `provider/model` strings behave consistently (for example `anthropic/claude-3-5-sonnet-20241022`, `openai/gpt-4o`). Configure provider API keys as required by LiteLLM.

| Role | Env var | Typical use in this repo |
|------|---------|---------------------------|
| Planner (Claude) | `MODEL_PLANNING` | First assessor in each crew |
| Impact (Claude) | `MODEL_IMPACT` | Registry / coverage / surface impact |
| Binding (Codex/OpenAI) | `MODEL_BINDING` | Patch schema steward, MCP maintainer |
| Coder (Codex/OpenAI) | `MODEL_CODING` | Reserved for future coding agents |
| Tester (cheap) | `MODEL_TESTING` | Quality-gate / validation brief agents |
| Fixer (Codex/OpenAI) | `MODEL_FIXING` | Reserved for fix loops |
| Doc (Claude) | `MODEL_DOC` | Final studio execution brief |
| Fallback | `MODEL_DEFAULT` | Unknown task types |

Optional: `MODEL_FUNCTION_CALLING` sets a smaller model for tool calls on agents that use tools.

Provider keys: set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc., per [LiteLLM providers](https://docs.litellm.ai/docs/providers).

## Run

Use the default request from the environment:

```bash
crewai run
```

Or run a specific request:

```bash
uv run run_request "Plan a node catalog change that affects din-studio and react-din"
```

Or set request inputs explicitly:

```bash
DIN_AGENTS_REQUEST="Assess a Rust patch migration change" uv run kickoff
```

## Output

The global Flow writes the latest report to:

```text
output/control-plane-report.md
```

## Repo Coverage

### `din-core`

- Rust patch/runtime authority
- patch compatibility and registry parity
- Rust quality gates:
  - `cargo fmt --all --check`
  - `cargo clippy --workspace --all-targets -- -D warnings`
  - `cargo test --workspace`

### `react-din`

- public React library and patch schema export
- docs/components and coverage manifest governance
- library quality gates:
  - `npm run lint`
  - `npm run typecheck`
  - `npm run ci:check`
  - `npm run validate:changes`

### `din-studio`

- editor workflows, app shell, AI UI, MCP target
- surface manifest and scenario alignment
- app quality gates:
  - `npm run lint`
  - `npm run typecheck`
  - `npm run validate:manifests`
  - `npm run validate:docs`
  - `npm run test`
  - `npm run test:e2e`

## Tests

Run:

```bash
uv run pytest
```

## Project Layout

```text
src/din_agents/
  crews/
    din_core/
    react_din/
    din_studio/
  shared/
  tools/
  flow.py
  main.py
tests/
```
