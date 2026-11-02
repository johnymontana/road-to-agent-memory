# Road to Agent Memory — Workshop Outline (v1)

> Status: planning document. No code or assets have been built yet.

## Overview

- **Format:** 2.5-hour live workshop · run-and-explore (complete code, guided exploration) — 150 min = M0 15 + M1 15 + M2 25 + M3 40 + M4 25 + M5 20 + Wrap 5 + 5 min buffer
- **Delivery:** **Codespaces-first** — README badge opens a prebuilt devcontainer (4-core/8 GB via `hostRequirements`, dependencies pre-installed, UI auto-opens); local clone + VS Code Dev Containers is the supported fallback (ADR 003)
- **App:** Full-stack chat application — FastAPI + PydanticAI backend, React + NVL frontend (chat / graph / trace panels)
- **Backend:** `neo4j-agent-memory` Python package, **Bolt backend** on attendee's own AuraDB instance (modules 1–4); **NAMS** hosted service at memory.neo4jlabs.com (module 5)
- **Models:** OpenAI — chat model + `text-embedding-3-small` + LLM entity extraction (`extractor_type="llm"`, temperature 0 — no local ML models; ADR 001)
- **Tooling:** **uv** for Python dependencies and virtual environments (committed `uv.lock`; ADR 002) and a **Makefile as the sole attendee command surface** — every setup step, scenario beat, and utility is a `make` target
- **Running scenario:** **"Acme Cloud"** — customer support agent for a fictional SaaS company

## The Arc

Each module opens by **demonstrating a failure** of the current agent, adds one memory
layer, then **re-runs the same scripted scenario** to show the fix. The NVL graph panel
makes each memory layer visually appear in the graph as it is added. Scripted scenario
beats are **make targets** (`make s1-baseline`, `make s3-ontology`, …), so demos are
deterministic, don't depend on live typing, and attendees always have a one-command
answer to "what do I run now?" — including `make module-N` to catch up if they fall
behind.

**Continuity thread (eval questions, to be refined):** a fixed set of questions asked of
the agent at every module — e.g., *"Do you know who I am? / What did we discuss last
time? / What do you know about my account? / Have you handled a ticket like this
before?"* — showing progressive capability as each memory layer lands.

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
context uses the newest ten prior messages plus scoped semantic user statements.
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
properties. INITIATED_BY links trace to message; TOUCHED links steps to case Customer
and Plan. Record actual executed SQL. Distinguish execution failure from a declined
business result. Retrieved procedures include bounded steps and observations, never
current policy authority. The ablation uses equal private SQL copies, separate
message scopes, a frozen corpus and no branch recording. Inspect actual safety,
retrieval, calls, tokens and timing; improvement is not guaranteed.

### Module 5 — Skill Distillation on NAMS *(20 min)*

**Concepts:** From memory to portable skills; grounded skill distillation; the governance
loop (drift detection, re-distillation); Bolt vs. NAMS backends.

**Flow:**
1. NAMS signup + `nams_` API key were done in **pre-work** (moved out of session — review B4); `make nams-check` verifies the key + workspace
2. Run the provided seed script (`make nams-seed`) — populates the attendee's NAMS workspace with the canonical reasoning memory (~1 min). **Narrated seam:** the slides make the boundary explicit — the attendee's Bolt memory lives in their AuraDB; NAMS is a fresh, managed workspace, and the seed loads the canonical history into it (attendees understand the seam rather than discovering it)
3. Trigger skill distillation over the accumulated refund-procedure memory (`make nams-distill`)
4. Inspect the distilled skill: SKILL.md artifact + skill subgraph with `GROUNDED_IN` edges, grounding and coverage scores
5. **The payoff:** a *fresh* agent — no session history, no prior traces — loads the distilled skill and resolves the refund ticket cold (`make s5-fresh-agent`)

**NVL moment:** The skill subgraph, with `GROUNDED_IN` edges pointing back to the exact
traces, tool calls, and entities that justify each step.

**Guided exploration questions:**

1. Open the distilled SKILL.md. Which steps correspond to which observed tool calls? Follow a `GROUNDED_IN` edge from a claim back to its evidence.
2. What do the grounding and coverage scores tell you? What would a low-grounding step mean, and would you trust it?
3. How is a distilled skill different from a hand-written runbook? From a raw trace? What does each optimize for?
4. **The drift beat, made concrete:** first `make policy-change` (flips the refund limit in SQLite — the system of record) — what does governance flag? *(Nothing: it watches the memory graph, not your database — the honest boundary.)* Then `make nams-drift` (ops retires the refund policy — the policy **entity is deleted** from the workspace memory): the skill's `GROUNDED_IN` claims lose their source nodes. What does the governance loop flag now? What happens on re-distillation (`make nams-redistill`)? *Stretch variant: instead of deleting the entity, mark a grounding `issue_refund` tool call as failed — same governance view, different provenance story.*
5. Who else could load this skill? What does it mean that procedural knowledge is now a portable, versioned artifact rather than trapped in one workspace?
6. Full-circle: which of the three memory types did distillation draw on for this skill? And which store changed in the drift beat — SQLite or Neo4j? Why?

*Design notes these questions inform: the seed script must write traces/steps/tool-calls in realistic agent-loop order, with tool-call inputs/outputs carrying the actual SQL and policy text observed in modules 1–4; the refund procedure must be consistent across seeded traces so distillation converges; the drift beat is a two-step demo — `make policy-change` (SQLite) establishes the boundary (governance watches the memory graph, not the system of record), then `make nams-drift` deletes the refund-policy entity so `GROUNDED_IN` claims lose their source nodes and the documented drift signal fires (verified live in spike 0.6 before content is written); SKILL.md format and `GROUNDED_IN` subgraph shape drive the NVL rendering work.*

---

### Wrap *(5 min)*

- Three memory types recap (short-term / long-term / reasoning — one knowledge graph)
- Bolt vs. NAMS trade-offs; when to choose which
- Pointers: docs (neo4j.com/labs/agent-memory), GraphAcademy "Context Graphs" course, examples repo

## Repo Plan (build phase)

### Tooling (ADR 002)

- **uv** for Python dependencies and virtual environments: `pyproject.toml` + committed **`uv.lock`** pinning `neo4j-agent-memory`, PydanticAI, and OpenAI package versions (protection against upstream releases); scripts execute via `uv run` under Make targets; attendees never activate a venv
- Frontend keeps npm for its own dependencies; **Make orchestrates both ecosystems** — `make` is the only command surface exposed to attendees

### Makefile target surface (the spec for the Makefile)

| Group | Targets | Purpose |
|---|---|---|
| Setup & env | `make setup` · `make check` · `make seed` · `make dev` | `uv sync` install; smoke test (env vars, AuraDB reachable, OpenAI key valid, SQLite seeded — doubles as the pre-work verification command); re-seed SQLite; run FastAPI + Vite together |
| Module beats | `make module-0` … `make module-5` | Run a module's beats in order — also the **catch-up lane** for attendees who fall behind |
| Scenarios | `make s1-baseline` · `make s2-return` · `make s2-restart` · `make s3-default` · `make s3-ontology` · `make s3-enrich` · `make s4-refund` · `make s4-refund-repeat` · `make s4-fail` · `make s5-fresh-agent` | One target per scripted scenario beat; paced/serialized OpenAI calls (ADR 001) |
| NAMS | `make nams-check` · `make nams-seed` · `make nams-distill` · `make nams-drift` · `make policy-change` · `make nams-redistill` | Module 5: verify key/workspace, seed, distill, drift beat (entity delete + the SQLite boundary demo), re-distill |
| Utilities | `make eval` · `make reset-memory` · `make clean` | Run the continuity eval-question set and print the per-module scorecard; wipe the Neo4j memory graph for clean re-runs; clean build artifacts |

### Content & assets

- **Folder per module** (ADR 004): `module_1/` … `module_5/`, each a self-contained copy of the full app at that stage — attendees diff folders to see what a memory layer adds and never `git checkout` mid-session; shared root `.env`, root venv (uv), and `data/acme_cloud.db` so state carries across folders; `make module-N` runs that module's beats from its folder (catch-up lane)
- Per-module README: concepts, **the `make` targets to run**, the guided exploration questions above, expected NVL screenshots
- `data/acme_cloud.db` + `scripts/seed_sqlite.py` — embedded SQLite system of record (customers, organizations, products, features, plans, subscriptions, policies, service_status, refunds) with deterministic seed data; auto-seeded on app boot if missing (`make seed` re-seeds)
- `app/tools/` — SQLite-backed agent tools (`lookup_account`, `search_product_catalog`, `fetch_policy`, `check_service_status`, `issue_refund`) using parameterized SQL via stdlib `sqlite3`
- `module_3/ontology/acme_cloud.yaml` — the custom Acme Cloud ontology (entity types, typed relationships, aliases, constraints); a `default-poleo` variant for the module 3 before/after beat
- `app/memory/hydrate.py` — post-extraction property hydration hook: maps extracted entities to SQLite rows and upserts grounded properties (`email`, `plan`, `plan_tier`, `description`, … — all facts, including categoricals) via `add_entity` MERGE semantics
- Enrichment config (Wikimedia, background, ORGANIZATION-only allowlist) baked into the module 3 settings
- `scripts/run_scenario.py` — deterministic canned conversations per scenario (short, turn-bounded messages), invoked by the scenario make targets via `uv run`
- `scripts/seed_nams.py` — module 5 NAMS workspace seeding (activates a matching Acme Cloud ontology server-side first)
- `scripts/change_policy.py` — module 5 drift beat (updates a policy row in SQLite)
- `scripts/eval.py` — the continuity eval-question runner behind `make eval`
- `.devcontainer/` (ADR 003, Codespaces-first): `Dockerfile` (Python 3.12 + sqlite3 + uv), `devcontainer.json` (Node LTS Feature, `hostRequirements` 4 CPU/8 GB, labeled forwarded ports — 5173 auto-opens the UI, 8000 silent; non-secret env defaults), `on-create.sh` (`uv sync --frozen` + `npm ci` + SQLite seed — **captured in prebuilds**), `post-create.sh` (`.env` scaffolding + welcome banner — user-scoped, sees personal Codespaces secrets)
- `.env.example` — AuraDB credentials, OpenAI (personal Codespaces secret preferred), NAMS key (module 5); `post-create.sh` copies it to `.env` on first creation
- **Codespaces prebuilds** — configured in repo Settings → Codespaces (not a repo file): prebuild the default branch's devcontainer, trigger *on configuration change*, restrict to the audience's regions, retain 2 versions, notify on failure; verified green during the pre-workshop rehearsal
- `README.md` — "Open in GitHub Codespaces" badge as the primary entry point; local clone + VS Code Dev Containers documented as fallback
- Seed data: Acme Cloud products, plans, policies, canned ticket scripts (shared source of truth between `seed_sqlite.py` and the scenario scripts)

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Aura provisioning time during live session | Pre-work email (create free AuraDB before the workshop); shared fallback instance |
| Codespaces prebuild stale or failing | Trigger on configuration change; rehearsal verifies the prebuild is green before the session; fallback: local VS Code Dev Containers (same config) |
| Codespaces unavailable for an attendee (org-managed account disables it, or quota exhausted) | Local clone fallback with the same `.devcontainer/` config; `make module-N` catch-up targets |
| Whole-room OpenAI bursts (chat + embeddings + one extraction call per turn) hitting tier-1 rate limits — 429s look like "broken setup" to attendees | Scenario scripts pace/serialize OpenAI calls; pre-work states the key/billing requirement and expected cost (<$1); instructor watches for 429s; extraction at temperature 0 on a small model (ADR 001) keeps call volume and cost minimal |
| Extraction variability live | temperature 0 + structured outputs = near-deterministic; identical on every attendee machine (no local ML); "expected graph" screenshots per module; ontology descriptions written as tight annotation guidelines |
| Wikimedia enrichment is async + network-dependent in live delivery | Enrichment cached (1-week TTL) and explicitly requested and cached by s3-enrich; fallback: stored provider-status replay; hydration (SQLite) is synchronous and carries the demo if enrichment lags |
| NAMS is early-access | Rehearsed fallback: pre-recorded distillation demo if signups hiccup |
| Content load vs. the 150-minute slot | Times reallocated per review consensus (M0 15 / M1 15 / M2 25 / M3 40 / M4 25 / M5 20 / Wrap 5) + 5-minute buffer after module 3; module 4 exploration is the droppable section; run-of-show marks trim points |

## Open Items

- [ ] Refine the eval-question continuity set (deferred — draft proposed above)
- [ ] Design the SQLite schema + seed dataset (tables per the module 1 design notes; tool vocabulary mirrors ontology labels; every tool returns meaningful results immediately)
- [ ] Draft the full `acme_cloud.yaml` ontology document (entity types, descriptions with negative cases, typed relationships + constraints, aliases) — the module 3 design notes are the spec
- [ ] Design the hydration mapping (entity type → SQLite columns → entity properties, including categoricals) and the post-extraction hook contract
- [ ] Lock the package version in `uv.lock` (ADR 002) and verify `extractor_type="llm"` on the locked release: ontology prompt rendering, relation ingest-validation, per-message latency and cost of one scripted scenario (ADR 001 follow-up)
- [ ] Verify the Wikimedia enrichment flow against a live Aura instance (async timing, `enriched_description`/`wikipedia_url` node properties, ORGANIZATION allowlist behavior)
- [ ] Verify NAMS ontology import for the module 5 seed script (server-side equivalent of the Acme Cloud ontology)
- [ ] Finalize scenario scripts (must satisfy the design notes in each module; paced/serialized OpenAI calls)
- [ ] Confirm NAMS distillation API surface against the live service at build time
- [ ] Rehearse the Codespaces flow end-to-end: devcontainer builds, prebuild configuration green, badge opens a ready codespace, `make check`/`make dev` work from a fresh account
- [ ] Draft the pre-work email: create + verify AuraDB, store `OPENAI_API_KEY` as a personal Codespaces secret scoped to the repo, note the 4-core/8 GB machine default and free-tier core-hours math
