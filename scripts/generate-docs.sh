#!/usr/bin/env bash
# Generate HTML API docs for `din_agents` into docs/generated/ (gitignored).
set -euo pipefail
cd "$(dirname "$0")/.."
uv run pdoc din_agents -o docs/generated --docformat google
