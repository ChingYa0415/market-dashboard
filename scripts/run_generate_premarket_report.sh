#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
PYTHON_BIN="$ROOT/.venv/bin/python3"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing virtualenv python: $PYTHON_BIN" >&2
  exit 1
fi

exec "$PYTHON_BIN" "$ROOT/scripts/generate_premarket_report.py"
