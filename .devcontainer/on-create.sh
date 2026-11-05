#!/usr/bin/env bash
# on-create.sh — heavy, user-independent setup. Runs inside the container at
# creation time and is captured by Codespaces prebuilds, so keep slow work here.
set -euo pipefail

echo "==> [1/3] Python environment (uv sync — locked versions, ADR 002)"
uv sync --frozen

echo "==> [2/3] Frontend dependencies (npm ci)"
npm --prefix web ci

echo "==> [3/3] Seeding the Acme Cloud system of record (SQLite)"
uv run scripts/seed_sqlite.py --if-missing

echo "==> on-create complete"
