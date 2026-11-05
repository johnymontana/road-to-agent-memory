# Road to Agent Memory — Workshop Outline (v1)

> Delivery outline. Use the [150-minute run of show](docs/run-of-show.md) for live timing and recovery, and the [module guides](docs/modules/) for exercises and answer keys.

## Overview

- **Format:** 2.5-hour live workshop · run-and-explore (complete code, guided exploration) — 150 min = M0 15 + M1 15 + M2 20 + M3 40 + M4 30 + M5 20 + Wrap 5 + 5 min buffer
- **Delivery:** **Codespaces-first** — README badge opens a prebuilt devcontainer (4-core/8 GB via `hostRequirements`, dependencies pre-installed, UI auto-opens); local clone + VS Code Dev Containers is the supported fallback (ADR 003)
- **App:** Full-stack chat application — FastAPI + PydanticAI backend, React + NVL frontend (chat / graph / trace panels)
- **Backend:** `neo4j-agent-memory` Python package, **Bolt backend** on the attendee’s AuraDB for support apps 2–5. Module 1 has five SQLite tools and per-turn scope. Separate Module 5 workflows use the **NAMS** hosted service.
- **Models:** OpenAI — chat model + `text-embedding-3-small` + LLM entity extraction (`extractor_type="llm"`, temperature 0 — no local ML models; ADR 001)
- **Tooling:** **uv** for Python dependencies and virtual environments (committed `uv.lock`; ADR 002) and a **Makefile as the sole attendee command surface** — every setup step, scenario beat, and utility is a `make` target
- **Running scenario:** **"Acme Cloud"** — customer support agent for a fictional SaaS company

## The Arc

Start with a stateless support agent. Add persistent messages, structured entities and execution records in successive modules. In Module 5 derive a portable skill from a separate hosted fixture corpus. At each stage, switch the browser backend, run a named scenario and inspect the evidence it actually produced.

The four controlled probes test named-customer lookup, a conversation phrase, a SQL-grounded date and an exact prior refusal quote. Each checks expected fields and at least one allowed source ID. The example actions, SQL receipts and fresh-agent runs answer different questions from these retrieval probes. [Scorecard details](docs/running-the-app.md#evaluation).

## Modules

---

### Module 0 — Setup *(15 min)*

**Goal:** Everyone has a running app against their own AuraDB — in a prebuilt Codespace.

Codespaces-first flow (ADR 003):

1. Click the **"Open in GitHub Codespaces"** badge in the README → a prebuilt 4-core codespace opens with all dependencies already installed (Python via `uv sync --frozen`, frontend via `npm ci`, SQLite seeded — all captured in the prebuild)
2. Add Aura credentials to `.env` (scaffolded from `.env.example` on creation); `OPENAI_API_KEY` arrives automatically if stored as a personal Codespaces secret in pre-work
3. `make check` — smoke test: env vars present, AuraDB reachable, OpenAI key valid, SQLite seeded (also the pre-work verification command)
4. `make dev` — FastAPI + Vite together; the UI opens in a browser tab automatically (port 5173, labeled); tour the three-panel UI (chat / graph / trace)

*Fallback: local clone + VS Code Dev Containers (same `.devcontainer/` config) for attendees whose accounts disable Codespaces.*

**Guided exploration questions:**

1. What does the graph panel show right now? Why is it empty — what would have to happen for something to appear?
2. Which components are already wired: where does a chat message travel from the UI to the model and back?
3. Open the seeded **Acme Cloud SQLite database** (`acme_cloud.db` — try `sqlite3 data/acme_cloud.db ".tables"`). What business data exists — customers, products, plans, policies, service status?
4. Where does the agent's "company knowledge" come from in module 1 — and what are the limits of that approach?

*Design notes these questions inform: the **SQLite schema and seed dataset** (see Module 1); baseline agent tools; what exists in Aura at t=0 (answer: nothing — all seed data lives app-side until memory is added).*

---

### Module 1 — The stateless control (15 min)

Run `make s1-baseline`: one self-contained SQL lookup, followed by an explicit
per-turn forgetting control. Browser bubbles do not become model history. Run
`make eval MODULE=1`, an isolated retrieval probe with no business tools.

### Module 2 — Persistent messages (20 min)

Run `make s2-return` for same-conversation and cross-conversation contrasts, then
`make s2-restart` for two separate Python processes using the same session. Local
context uses the newest ten prior messages plus scoped semantic user messages.
Inspect evidence paths and source IDs. Bolt observations/reflections are not taught
as available context tiers. Run `make eval MODULE=2` explicitly.

### Module 3 — Structured and grounded facts (40 min)

Compare `make s3-default` with `make s3-ontology`: independent extractor-only snapshots
of one fixed transcript, with hashes and elapsed time. Choose each Saved replay;
no prior chat or hydration participates. LLM output can vary at temperature zero.
Then introduce a Customer in browser chat: extraction → type-safe SQL hydration
of current-message entities → retrieval → answer. Expose grounded email/plan/date
and source IDs. Select a Customer for scoped preferences and inspect actual saved
receipts. Read `module_3/ontology/acme_cloud.yaml` and the local context/hydration code.

Instructor recipes: `uv run scripts/instructor.py strict` shows invalid relation
drop versus raise; `uv run scripts/instructor.py plan` upgrades and rolls back a
private SQL copy. ONTOLOGY=active uses the database ontology; local YAML is the
default override. Optional `make s3-enrich` explicitly caches Wikimedia Organization
facts/status. A 403 is unavailable, not pending; no service-health inference.
Run `make eval MODULE=3`; explain source holdouts, not guaranteed green progression.

### Module 4 — Execution records (30 min)

`make s4-refund`, `make s4-fail`, `make s4-refund-repeat`. Select Saved replay to
inspect CLI output. Browser actions require explicit account/case and per-turn
authorization. SQL enforces identity, finite positive amounts, case amount, current
plan limit and incident uniqueness. Updates read history; no escalation is performed.

Trace before execution and complete on success/exception. ReasoningTrace HAS_STEP
ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Outcome and reply are trace
properties. INITIATED_BY links trace to message. TOUCHED links each step to the same selected-case Customer/Plan references. Inspect captured SQL and tool results for the individual operation. Distinguish execution failure from a declined
business result. Retrieved procedures include bounded steps and observations, never
current policy authority. The ablation uses equal private SQL copies, separate
message scopes, a frozen corpus and no branch recording. Inspect actual safety,
retrieval, calls, tokens and timing; improvement is not guaranteed.

### Module 5 — Skill Distillation on NAMS *(20 min)*

1. **Pre-work.** Create a workshop workspace key and run `make nams-check`. Confirm reachability, distillation capability and that the workspace's active ontology accepts the seed. Save all hosted writes for the workshop.
2. **Minutes 0–5.** Switch to the Module 5 browser and confirm its badge. Explain the separate stores and where the skill comes from. Use a prepared downloaded package, or deliberately run `make nams-seed` and `make nams-distill` once in the designated workspace. The seed creates a new conversation and traces. The generator selects the saved conversation, approves and publishes a version and downloads it.
3. **Minutes 5–13.** With the package ready, inspect SKILL.md, references, provenance and the local skill receipt. Follow Skill → version → step → GROUNDED_IN → evidence. Claim entries live in `provenance.json`. Compare `make s5-fresh-agent WITH_SKILL=off` then `make s5-fresh-agent WITH_SKILL=on`. If hosted capability is unavailable or the package is missing at minute five, use `make s5-fresh-agent WITH_SKILL=fallback` for the second run. This route needs just the checked-in procedure and the local consumer’s prerequisites.
4. **Minutes 13–20.** Record ordered tool names, visible statuses and reply on the authorized $49 case. Identical outcomes are valid. On the hosted route, discuss one prepared provenance example. Fallback participants go from the comparison to the wrap (Google Slides 75 → 82, repo slides 62 → 69). Keep live hosted deletion and re-distillation as a disposable-workspace instructor extension.
5. **Instructor extension.** Use a returned SQL before/after value for the policy edit, a hosted report for dependency drift, and the version and procedure diff for re-distillation. The script checks the seed, downloaded package and current published version before it can delete cited, exact-name policy records in that run’s user scope. Conditionally restore SQL from $150 to $250 according to its actual state. Ravi’s $49 case is below both thresholds. [Detailed commands and answer key](docs/modules/module-5.md).

### Wrap *(5 min)*

Ask for four concrete sources: the SQLite policy row for today’s limit, the message ID for the earlier customer statement, the tool result and SQL for an observed action, and SKILL.md for the portable instructions. Show where the Monday example writes and reads a single phrase. Mapping records to PydanticAI history and running the next agent call is the follow-up integration. Decide whether to keep the environment for this or [clean it up](docs/teardown.md).

## Repository and command surface

### Tooling (ADR 002)

- **uv** for Python dependencies and virtual environments: `pyproject.toml` + committed **`uv.lock`** pinning `neo4j-agent-memory`, PydanticAI, and OpenAI package versions (protection against upstream releases); scripts execute via `uv run` under Make targets; attendees never activate a venv
- Frontend keeps npm for its own dependencies; **Make orchestrates both ecosystems** — `make` is the only command surface exposed to attendees

### Makefile target surface (the spec for the Makefile)

| Group | Targets | Purpose |
|---|---|---|
| Setup & env | `make setup` · `make check` · `make seed` · `make dev` | `uv sync` install; smoke test (env vars, AuraDB reachable, OpenAI key valid, SQLite seeded — doubles as the pre-work verification command); re-seed SQLite; run FastAPI + Vite together |
| Module beats | `make module-0` … `make module-5` | Run selected module beats. Module 5 performs a full hosted replay with fresh seed records and generation/publication. |
| Scenarios | `make s1-baseline` · `make s2-return` · `make s2-restart` · `make s3-default` · `make s3-ontology` · `make s3-enrich` · `make s4-refund` · `make s4-refund-repeat` · `make s4-fail` · `make s5-fresh-agent` | One target per scripted scenario beat; paced/serialized OpenAI calls (ADR 001) |
| NAMS | `make nams-check` · `make nams-seed` · `make nams-distill` · `make nams-drift` · `make policy-change` · `make nams-redistill` | Module 5: verify key/workspace, seed, distill, drift beat (entity delete + the SQLite boundary demo), re-distill |
| Utilities | `make eval` · `make reset-memory` · `make clean` | Run the continuity eval-question set and print the per-module scorecard; wipe the Neo4j memory graph for clean re-runs; clean build artifacts |

### Content & assets

- **Folder per module** (ADR 004): `module_1/` … `module_5/`, each a self-contained copy of the full app at that stage — attendees diff folders to see what a memory layer adds and never `git checkout` mid-session; shared root `.env`, root venv (uv), and `data/acme_cloud.db` so state carries across folders; `make module-N` runs selected module beats
- Per-module README: concepts, **the `make` targets to run**, the guided exploration questions above, expected NVL screenshots
- `data/acme_cloud.db` and `scripts/seed_sqlite.py` hold the Acme Cloud system of record. Setup or Dev Container creation initializes an absent database. Re-running setup preserves the current business rows. An explicit `make seed` rebuilds SQLite and keeps the separately stored replays and request receipts.
- `module_N/app/tools.py` — SQLite-backed agent tools (`lookup_account`, `search_product_catalog`, `fetch_policy`, `check_service_status`, `issue_refund`) using parameterized SQL via stdlib `sqlite3`
- `module_3/ontology/acme_cloud.yaml` — the custom Acme Cloud ontology (entity types, typed relationships, aliases, constraints); a `default-poleo` variant for the module 3 before/after beat
- `module_3/app/hydrate.py` — post-extraction property hydration checks type and identity, reads through SQLite and refreshes flat fields via PropertyWriter
- Optional Wikimedia lab in `module_3/lab/enrichment.py` writes a cache and saved replay.
- `scripts/run_scenario.py` — deterministic canned conversations per scenario (short, turn-bounded messages), invoked by the scenario make targets via `uv run`
- `scripts/seed_nams.py` — wrapper for the hosted fixture writer in `module_5/workflows/seed.py`
- `scripts/change_policy.py` — module 5 drift beat (updates a policy row in SQLite)
- `scripts/eval.py` — the continuity eval-question runner behind `make eval`
- `.devcontainer/` (ADR 003, Codespaces-first): `Dockerfile` (Python 3.12 + sqlite3 + uv), `devcontainer.json` (Node LTS Feature, `hostRequirements` 4 CPU/8 GB, labeled forwarded ports — 5173 auto-opens the UI, 8000 silent; non-secret env defaults), `on-create.sh` (`uv sync --frozen` + `npm ci` + SQLite seed — **captured in prebuilds**), `post-create.sh` (`.env` scaffolding + welcome banner — user-scoped, sees personal Codespaces secrets)
- `.env.example` — AuraDB credentials, OpenAI (personal Codespaces secret preferred), NAMS key (module 5); `post-create.sh` copies it to `.env` on first creation
- **Codespaces prebuilds** — configured in repo Settings → Codespaces (not a repo file): prebuild the default branch's devcontainer, trigger *on configuration change*, restrict to the audience's regions, retain 2 versions, notify on failure; verify the configuration before delivery
- `README.md` — "Open in GitHub Codespaces" badge as the primary entry point; local clone + VS Code Dev Containers documented as fallback
- Seed data: Acme Cloud products, plans, policies, canned ticket scripts (shared source of truth between `seed_sqlite.py` and the scenario scripts)

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Aura provisioning time during live session | Provision in pre-work. If service startup runs long, use the instructor’s labeled example while a helper checks the connection. |
| Codespaces prebuild stale or failing | Trigger on configuration change; rehearsal verifies the prebuild is green before the session; fallback: local VS Code Dev Containers (same config) |
| Codespaces unavailable for an attendee (org-managed account disables it, or quota exhausted) | Local clone with the same `.devcontainer/` config. Open a named saved replay or use the explicit module 5 consumer fallback. |
| Whole-room OpenAI bursts (chat + embeddings + one extraction call per turn) hitting tier-1 rate limits — 429s look like "broken setup" to attendees | Scenario scripts pace/serialize OpenAI calls; pre-work states the key/billing requirement and expected cost (<$1); instructor watches for 429s; extraction at temperature 0 on a small model (ADR 001) keeps call volume and cost minimal |
| Extraction variability live | Compare the returned graphs and input transcript hashes. Use a labeled instructor example when live extraction differs. |
| Wikimedia enrichment is async + network-dependent in live delivery | Enrichment cached (1-week TTL) and explicitly requested and cached by s3-enrich; fallback: stored provider-status replay; hydration (SQLite) is synchronous and carries the demo if enrichment lags |
| NAMS is early-access | Use off and checked-in fallback, record output, then join wrap. Label any prepared hosted example. |
| Content load vs. the 150-minute slot | Budget (M0 15 / M1 15 / M2 20 / M3 40 / M4 30 / M5 20 / Wrap 5) + 5-minute buffer after module 3; module 4 exploration is the droppable section; run-of-show marks trim points |

## Instructor readiness

Before delivery, open the participant checkout, verify the browser badge at each switch, inspect one saved replay and check the intended NAMS capability. Locate the checked-in procedure and a prior ablation run. Rehearse the minute-five fallback decision and the closing take-home or cleanup choice. [Detailed checklist and timing](docs/run-of-show.md).
