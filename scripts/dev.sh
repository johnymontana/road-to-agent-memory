#!/usr/bin/env bash
# make dev — run the module backend (:8000) + frontend (:5173) together.
set -euo pipefail
MODULE="${MODULE:-1}"

cleanup() { kill 0 2>/dev/null || true; }
trap cleanup EXIT INT TERM

echo "▶ Backend :8000 (module ${MODULE})  ·  Frontend :5173"
uv run python -m "module_${MODULE}.app.main" &
npm --prefix web dev &
wait
