# Tasks and sample requests for DIN Agents

Sample markdown lines under `examples/` are **optional prompts** you can paste into `run_request`. CrewAI `tasks.yaml` definitions live under `src/din_agents/crews/**/config/`.

## How to run

From the `din-agents` repository root (with `.env` and sibling repo paths configured):

```bash
uv run run_request "Your request text here"
```

Or:

```bash
DIN_AGENTS_REQUEST="Your request text here" uv run kickoff
```

### Anthropic input TPM (e.g. 30k/min)

If you see **“would exceed … input tokens per minute”** on the first LLM call, the crew prompt may be too large for your quota. In `.env` try:

- `DIN_AGENTS_COMPACT_PROMPTS=1` — shorter task instructions and truncated `entry_points` / `hard_boundaries` in each task.
- `DIN_AGENTS_PRE_CREW_SLEEP_S=60` — pause before kickoff so a rolling window can clear.
- Point `MODEL_PLANNING` / `MODEL_IMPACT` at a smaller Claude tier, e.g. `anthropic/claude-haiku-4-5-20251001` (versioned id required; `*-latest` is not valid on the Anthropic API).

## Executable din-core audio backlog

Run one **typed backlog item** (25 surfaces: nodes, effects, sources, patch, analysis). This composes an English request and invokes the control plane with `--repo-hint din_core` so routing targets din-core.

```bash
# List all task ids
uv run run_din_core_audio_task

# Tab-separated id, category, surface
uv run run_din_core_audio_task --list

# Run the control plane for one surface (e.g. Gain, Reverb, Patch)
uv run run_din_core_audio_task gain

# Strict one-send-at-a-time: backlog step 1, then 2, … (prints the next command after each run)
uv run run_din_core_audio_task --step 1

# Or: run all tasks but wait for Enter between each crew (no burst; best for 30k TPM)
uv run run_din_core_audio_task --all --interactive

# Optional extra delay after you press Enter (TPM recovery)
uv run run_din_core_audio_task --all --interactive --pause-between 60

# Run all 25 tasks with automatic spacing (default 90s between tasks)
uv run run_din_core_audio_task --all

# Stronger spacing or no pause
uv run run_din_core_audio_task --all --pause-between 120
uv run run_din_core_audio_task --all --pause-between 0

# Same, but write reports to a chosen directory
uv run run_din_core_audio_task --all --output-dir /tmp/din-core-audio-reports
```

Definitions live in [`src/din_agents/din_core_audio_tasks.py`](../src/din_agents/din_core_audio_tasks.py).

## Sample request files

| File | Intent |
|------|--------|
| [examples/din-core.md](examples/din-core.md) | Rust patch, registry, FFI, migrations |
| [examples/react-din.md](examples/react-din.md) | Public API, patch schema, docs/coverage |
| [examples/din-studio.md](examples/din-studio.md) | Editor, surfaces, MCP, AI catalog |
| [examples/cross-repo.md](examples/cross-repo.md) | Requests that should stress routing / coordination |

Copy a quoted line into `run_request` or set `DIN_AGENTS_REQUEST` to the same string.
