# ADR 003: Codespaces-first delivery with a prebuilt devcontainer

- **Status:** Accepted
- **Date:** 2026-10-27
- **Context:** Workshop delivery environment (all modules, especially Module 0)

## Context

The workshop is a 2-hour live, run-and-explore session where the single highest-failure
point is attendee environment setup (REVIEW_FEEDBACK.md A3: Module 0's 10 minutes are
"fantasy"; D1: unstated prerequisites; G1–G10: operational failure modes). Attendees
arrive with heterogeneous machines (macOS/Linux/Windows — including Windows users
without `make`), unknown Python/Node installs, and varying network conditions.

The workshop requires: Python 3.12 + uv + a pinned `uv.lock` environment, Node LTS +
npm, sqlite3, make, two forwarded dev-server ports, and attendee-supplied credentials
(OpenAI, per-attendee AuraDB, later NAMS).

GitHub Codespaces supports this via the devcontainer spec, with two mechanisms that
make it viable for a live session:

- **Prebuilds** (configured in repo Settings → Codespaces): a GitHub Actions-driven
  template snapshot. Only `onCreateCommand` and `updateContentCommand` output is
  captured by prebuilds — `postCreateCommand` runs after the codespace is assigned to
  the attendee and *can* see user-scoped secrets. Heavy installs therefore belong in
  `onCreateCommand`/`updateContentCommand`; attendee-facing scaffolding belongs in
  `postCreateCommand`.
- **`hostRequirements`** in `devcontainer.json`: Codespaces auto-defaults to a machine
  meeting the declared minimums — we declare 4 CPUs / 8 GB so attendees never land on
  the cramped 2-core default.
- **Personal Codespaces secrets** (repo-scoped) are exported as environment variables
  after creation — ideal for `OPENAI_API_KEY`; per-attendee Aura credentials stay in
  `.env` (scaffolded from `.env.example` by `post-create.sh`).

## Decision

**GitHub Codespaces is the primary, recommended path; local clone is a supported but
secondary fallback.** The repo ships:

- `.devcontainer/Dockerfile` — `devcontainers/python:3.12-bookworm` + `sqlite3` + uv
  (installed via pip)
- `.devcontainer/devcontainer.json` — Node LTS via Feature, `hostRequirements`
  (4 CPU / 8 GB), forwarded ports with labeled `portsAttributes` (5173 UI opens the
  browser once; 8000 backend silent), non-secret `containerEnv` defaults, VS Code
  extensions, lifecycle split per the prebuild semantics above
- `.devcontainer/on-create.sh` — `uv sync --frozen`, `npm ci`, SQLite seed (all
  captured in prebuilds)
- `.devcontainer/post-create.sh` — `.env` scaffolding + welcome banner (fast,
  user-scoped)
- `.env.example` — documents AuraDB, OpenAI (secret-preferred), and NAMS (module 5)
  variables
- **Prebuild configuration** (repo Settings → Codespaces — not a repo file): prebuild
  the default branch's devcontainer, trigger **on configuration change**, limit to
  1–2 regions where the audience lives, retain 2 template versions, notify on failure.
  Documented in the repo plan/README since it can't live in a file.

Attendee-facing entry point: a **"Open in GitHub Codespaces" badge** in the README.

## Alternatives considered

| | Verdict |
|---|---|
| **Local-first, Codespaces as backup** | Rejected — setup variance (OS, Python/Node versions, Windows `make`) directly attacks the 10-minute Module 0 budget; every variance class becomes a live-debug event |
| **Gitpod / other cloud IDEs** | Rejected — another account for attendees to create; the repo lives on GitHub and Codespaces needs no extra account |
| **Browser-only sandboxes (StackBlitz/Replit)** | Rejected — Python + Neo4j Bolt + dual dev servers are not first-class; portability back to real repos is poor |
| **Devcontainer for VS Code only (no Codespaces)** | Accepted as the local fallback — the same `.devcontainer/` config works locally in VS Code Dev Containers, so "Codespaces-first" also improves the local path for attendees with Docker |

## Consequences

**Positive:**
- Module 0 shrinks to: open badge → wait for prebuilt codespace → edit `.env` →
  `make check` → `make dev` (review A3 mitigated; the 10-minute budget becomes
  plausible).
- Identical environment for every attendee — the room sees the same app, the same
  dependency versions, the same ports (supports A2/D1 indirectly).
- Windows attendees are fully supported with no special casing (ADR 002's `make`
  caveat disappears for the primary path).
- `hostRequirements` removes the 2-core machine lottery.
- Personal Codespaces secrets mean the pre-work email can tell attendees to store
  `OPENAI_API_KEY` once, days ahead — it appears automatically at workshop time.

**Negative / accepted risks:**
- **GitHub account required** (free) — stated in pre-work.
- **Core-hours cost to attendees** — 4-core machine ≈ 8 core-hours for the session,
  well within the 120 core-hours/month free tier for personal accounts; stated in
  pre-work (attendees on org-managed accounts where Codespaces is disabled use the
  local fallback).
- **Prebuild storage/Actions minutes are borne by the repo owner** — mitigated by
  region restriction, 2-version retention, and on-configuration-change triggers.
- **Prebuild staleness** — if a push lands without a completed prebuild run, the first
  attendees hit a full build (10–20 min); mitigated by the on-configuration-change
  trigger, a pre-workshop rehearsal that verifies the prebuild is green, and the
  documented fallback.
- **The local fallback still exists** and must be tested — but it is no longer the
  thing Module 0's timing depends on.

## Related

- WORKSHOP_OUTLINE.md — Overview, Module 0, Repo Plan (devcontainer + prebuilds)
- ADR 002 — uv + Makefile tooling (the lifecycle scripts invoke `uv sync` / `make seed`)
- ADR 001 — LLM-based extraction (no local ML models keeps the image small and
  prebuilds fast)
- REVIEW_FEEDBACK.md — items A3, D1, G1, G2, G10
