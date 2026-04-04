#!/usr/bin/env bash
# Deprecated name: use bootstrap-pre-commit-hooks.sh (installs Husky + din-core git hook).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/bootstrap-pre-commit-hooks.sh" "$@"
