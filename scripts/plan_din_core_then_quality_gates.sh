#!/usr/bin/env bash
# Plan via CrewAI control plane, then run din-core Rust quality gates (mutates nothing by itself except generating the report).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 'Your change request in quotes'" >&2
  exit 1
fi

uv run run_request --repo-hint din_core "$@"

DIN_CORE_PATH="${DIN_CORE_PATH:-$HOME/Sites/din-core}"
if [[ ! -d "$DIN_CORE_PATH" ]]; then
  echo "DIN_CORE_PATH not found: $DIN_CORE_PATH" >&2
  exit 1
fi

cd "$DIN_CORE_PATH"
cargo fmt --all --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
