# Road to Agent Memory — workshop devcontainer
#
# Base: official devcontainers Python image (Debian bookworm, includes common
# build tools and pipx). Node.js is added via a devcontainer Feature in
# devcontainer.json rather than here, so the Feature registry handles versions.

FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# sqlite3 CLI: attendees inspect the Acme Cloud system of record directly in
# module 0 (`make seed` / `sqlite3 data/acme_cloud.db ".tables"`).
RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# uv: Python dependency + venv management (ADR 002). Installed via pip so the
# binary lands on PATH without a shell profile dance.
RUN pip install --no-cache-dir uv
