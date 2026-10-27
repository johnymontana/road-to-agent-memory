# Road to Agent Memory — Implementation Plan

> Derived from: `WORKSHOP_OUTLINE.md` (v1) · `docs/adr/001`–`003` · `REVIEW_FEEDBACK.md`
> Status: execution plan. Phases are dependency-ordered; Phase 0 gates later phases.

## How to read this plan

- **Phases 0→6** run mostly in order; Phase 4 (slides) and parts of Phase 2 can run in
  parallel once their inputs are stable.
- **Phase 0 is a hard gate with three outcomes per spike**, not two: pass, fallback, or
  **stop-and-replan**. A spike result can reopen a resolved decision (e.g. spike 0.6
  reopens D4; spike 0.2 reopens Module 2's concept list) — reopenings are recorded in
  the verification log and the decisions table, and dependent downstream work halts
  until the owner re-approves. A fallback is only chosen when its cost is written into
  the affected phase's budget at that moment.
- **Review traceability:** tasks cite REVIEW_FEEDBACK item IDs (e.g. *fixes B1*) and
  plan-review items (P1–P3, from the adversarial review of this plan).
- **Decisions** (resolved and reopenable) are collected at the end.

---

## Phase 0 — Verification spikes (gate)

*Purpose: retire every P0 item from the review before writing content. One throwaway
Codespace + one throwaway NAMS workspace. Each spike is a small `uv run` script or curl
sequence; record results in `docs/verification-log.md`.*

**0.0 Spike infrastructure (prerequisite task — resolves the Phase 0/1 circularity,
P2):** spikes need a minimal scaffold that Phase 1 later hardens, so Phase 0 owns it
explicitly: a throwaway `pyproject.toml` + `uv.lock` (pinning `neo4j-agent-memory`),
a scratch `scripts/spikes/` directory, and a draft `.devcontainer/` pushed to a
**throwaway test repo** for spike 0.9. These artifacts are disposable; Phase 1.1–1.2
create the real ones in the workshop repo. No Phase 1 deliverable is required for any
spike to run.

| # | Spike | Method | Pass criteria | Gates |
|---|---|---|---|---|
| 0.1 | **Lock + smoke matrix** | Use the spike-infra scaffold (0.0): `uv lock` pins `neo4j-agent-memory`; run a smoke script per backend operation used by the workshop | All green on locked version; log notes exact version | Everything (F4) |
| 0.2 | **Bolt `get_context` shape** | Store messages on Bolt; inspect `get_context` return | Confirms whether reflections/observations tiers exist on Bolt or are NAMS-only (F1). *If absent: rework Module 2 concept list + Q4* | Module 2 content |
| 0.3 | **`add_message` return shape** | Inspect return value on the locked release | Determines hydration-hook contract (F5): does the app learn which entities a message created directly, or must it query `:MENTIONS`? | Module 3 hydration hook |
| 0.4 | **Bolt reasoning retrieval** | Record traces via `record_agent_trace`; query similar tasks; inspect `:TOUCHED` edges | Similar-task retrieval works on Bolt with documented call shape (F7) | Module 4 content |
| 0.5 | **LLM extraction on locked release** | `extractor_type="llm"` + custom ontology; verify ontology renders into prompt, forbidden relations dropped at ingest; measure per-message latency + cost on a scripted scenario | Behavior matches source expectations; latency < ~2 s/turn; cost logged (ADR 001 follow-up) | Module 3 content |
| 0.6 | **NAMS skill lifecycle + drift semantics** | `GET /v1/skills/capabilities` on the live deployment; seed → `POST /v1/skills/generate` → poll → review → publish → download; then **run the D4 drift design live**: `DELETE` the refund-policy entity and check `/v1/skills/{id}/drift` + `/v1/skills/governance` flag the orphaned `GROUNDED_IN` claims; also verify the SQLite-side policy change produces NO signal (the boundary the beat teaches) | Delete-entity drift fires as designed (documented semantics confirmed); SQLite change confirmed invisible to governance; publish gating + run latency measured (B5/B6) | Module 5 content |
| 0.7 | **NAMS ontology import + seed choreography** | Import `acme_cloud.yaml` server-side; run the entity→trace→step→tool-call seed ordering with ID capture; time it | Ontology imports cleanly (F11); seed completes in a measured time; resolve-merge ID surprises catalogued (B8) | Module 5 seed script |
| 0.8 | **Wikimedia enrichment** | Enable `EnrichmentConfig`; extract "Stripe"; measure time-to-enrichment on a 4-core Codespace | Fields (`enriched_description`, `wikipedia_url`) land within a presentable window (F3/F17) | Module 3 enrichment beat |
| 0.9 | **Codespaces prebuild rehearsal** | Push devcontainer to a test repo; configure prebuild; open a fresh codespace as a clean account would; time badge → `make check` green | Badge-to-green < 3 min with warm prebuild; 4-core machine auto-selected; OPENAI_API_KEY personal secret visible | ADR 003 validation |

**Phase 0 exit criteria:** verification log complete; each spike's outcome is one of
**pass** (content proceeds), **fallback** (chosen, costed, written into the gated
phase's budget, outline section updated), or **stop-and-replan** (owner decision before
any gated work proceeds). A spike outcome that contradicts a resolved decision formally
reopens it in the decisions table.

---

## Phase 1 — Repo scaffolding & infrastructure

*Deliverable: a repo that boots in Codespaces with stub app + full Makefile, CI green.*

1. **Repo init** — `pyproject.toml` (deps pinned via `uv.lock` per ADR 002),
   `.gitignore`, license, README skeleton. **Command surface (canonical — fixes P1):**
   the outline's Repo Plan spec table is the single source of truth: **29 targets**
   (4 setup + 6 module beats + 10 scenarios + 6 NAMS + 3 utilities). Architecture:
   **one root Makefile** — module targets resolve paths per folder via a `MODULE`
   variable (`make dev MODULE=3`, `make module-3`); module folders contain **no**
   per-folder Makefiles (ADR 004 amended accordingly; ADR 002's table corrected to
   include `make nams-drift`). All targets initially stubbed with
   `echo "not yet implemented"`; they light up as phases land. `make help` is generated
   from the spec table, and CI (1.5) verifies the Makefile implements exactly the
   29-target spec — the three documents can never disagree again without CI going red.
2. **Devcontainer validation** — the shipped `.devcontainer/` config (ADR 003): build
   it locally with the VS Code Dev Containers CLI, then in a real Codespace; confirm
   port labels, auto-open behavior, extension set, `hostRequirements` machine default.
3. **App skeleton** — FastAPI + Vite/React boots via `make dev`; three-panel layout with
   placeholder panels; health endpoint; `.env` loading (env vars beat `.env`; ADR 003
   secrets strategy).
4. **`make check` implementation** — validates: env vars present, AuraDB reachable
   (driver ping), OpenAI key valid (cheap models list call), SQLite seeded, NAMS key
   valid *only when module 5 env present*. Prints a green/red checklist — this is the
   pre-work verification command (G10).
5. **CI (GitHub Actions)** — three lanes:
   - **Static:** lint (ruff + eslint), Python unit tests, `uv lock --check`, frontend
     build, devcontainer build on any PR touching `.devcontainer/` (the prebuild config
     is exercised in CI, not just at rehearsal).
   - **Command surface:** every one of the 29 Makefile targets exists, parses, and is
     idempotent where claimed; `make help` output matches the outline's spec table
     verbatim (the same table the slides quote — P1).
   - **Behavioral (the workshop's real test lane — fixes P3):** integration tests run
     scenarios against an ephemeral Neo4j (testcontainers) using the locked deps:
     run `s3-ontology` → dump the resulting subgraph → compare against the committed
     **golden-graph snapshot** with the declared tolerances (2.7). A dependency bump or
     model drift that changes extraction output, `:MENTIONS` wiring, or trace schema
     goes red here — not in front of the room. A scheduled (weekly) job re-runs this
     lane plus the Phase 0 spike suite against live services so a NAMS deploy or model
     re-point invalidates assumptions in CI, not on stage.
   Prebuild trigger set to *on configuration change* (repo settings).
6. **Folder-per-module scaffolding (ADR 004 — D1 resolved)** — create `module_1/` …
   `module_5/` as self-contained app copies with shared root `.env`, root uv venv, and
   root `data/acme_cloud.db`; Makefile targets resolve paths per folder
   (`make module-N`, `make dev MODULE=N`); CI diff-checks intended deltas between
   adjacent folders to catch copy drift.

**Exit:** a clean account can badge-open the repo, run `make check` (red on missing
creds), and `make dev` shows the three panels.

---

## Phase 2 — Content & data design

*Deliverable: the Acme Cloud domain is fully specified before code depends on it.*

1. **SQLite schema + seed data** (`scripts/seed_sqlite.py`, `data/acme_cloud.db`):
   tables `customers`, `organizations`, `products`, `features`, `plans`,
   `subscriptions`, `policies`, `service_status`, `refunds`. Seed must make every tool
   return meaningful results on first use (module 1 design note) and include the
   refund-limit row that `issue_refund` validates against (module 4's failed trace).
2. **Ontology** (`ontology/acme_cloud.yaml` + `ontology/default-poleo.yaml`):
   entity types (Customer, Organization, Product, Plan, Feature, Incident) with
   annotation-guideline descriptions *including negative cases*; typed relationships
   (WORKS_AT, SUBSCRIBES_TO, USES, REPORTED, AFFECTS, PART_OF, INCLUDES) with one
   constraint demo (`unique_source` on WORKS_AT); aliases covering the
   "Acme Cloud"/"AcmeCloud" beat. Validate via `neo4j-agent-memory ontology validate`
   in CI.
3. **Hydration mapping** — entity type → SQLite columns → entity properties table
   (Customer ← customers/email/plan/plan_tier/signup_date; Product ←
   products/description; …). This table *is* the spec for `app/memory/hydrate.py`.
4. **Scenario scripts** (`scripts/scenarios/`) — canned conversations per make target:
   `s1-baseline`, `s2-return`, `s2-restart`, `s3-default`, `s3-ontology`, `s3-enrich`
   (mentions Stripe + includes the scripted preference statement), `s4-refund`,
   `s4-refund-repeat`, `s4-fail`, `s5-fresh-agent`. Constraints from design notes:
   exercise every entity type; at least two relationship patterns appear twice
   (for `support >= 2`); serialized OpenAI calls (ADR 001); module 1's scripts must be
   engineered so tools *can't* fix the failure (customer never states their email
   until the fix lands — C3).
5. **Eval question set finalization** (`scripts/eval.py` content) — resolve the
   per-layer attribution the review flagged (H3): each eval question must be provably
   answerable starting at exactly one module. Output: fixed question list + expected
   answers per module + scorecard format for `make eval`.
6. **Glossary** (`docs/glossary.md`, one sentence per term — Attendee persona's #1
   ask): agent, tool, PydanticAI, Neo4j/AuraDB, graph/node/edge, ontology, POLE+O,
   extraction, entity resolution, hydration, enrichment, trace, provenance,
   distillation, grounding/coverage, NAMS, Bolt. Linked from every module README and
   the deck's appendix. *Fixes D2.*

7. **Golden-graph snapshot format + tolerances** (`tests/golden/`) — the contract the
   CI behavioral lane (1.5) enforces: per scenario, a committed expected subgraph
   (node/edge labels, counts, key properties — exported as JSON from a known-good run)
   plus a **declared tolerance policy**: which assertions are exact (entity labels
   present, `support >= 2` edges, alias resolution) vs. aspirational (exact counts,
   which vary with near-deterministic LLM extraction). The README's expected-graph
   screenshots and these snapshots share one source of truth.

**Exit (authored — P2):** all Phase 2 artifacts are *authored and self-consistent*:
seed script, ontology (validated by CLI), scenario scripts, eval question set with
draft expected answers, glossary, golden-snapshot format with tolerances. **Boundary
verification is deliberately NOT a Phase 2 exit criterion** — module boundaries don't
exist until Phase 3 builds them; each Phase 3 module exit (below) includes validating
the eval scorecard at that boundary and regenerating the golden snapshots.

---

## Phase 3 — App implementation (module by module)

*Each sub-phase: backend + frontend + Makefile targets + per-module README section.
Graph panel rendering lights up with each memory layer.*

### 3.1 Module 1 — Stateless baseline
- PydanticAI agent, five SQLite tools (`lookup_account`, `search_product_catalog`,
  `fetch_policy`, `check_service_status`, `issue_refund`) — parameterized SQL, typed
  returns; tool calls streamed to the **trace panel** with SQL visible (E3).
- Chat panel end-to-end; `make s1-baseline` replays scenario 1; `make eval` baseline.
- **Controls for ablation (C1):** build the `AGENT_MEMORY=off|on` flag NOW — modules
  4–5's fix/payoff demos need control runs (agent without memory layer) to be
  provable. Cheap to add early, expensive to retrofit.

### 3.2 Module 2 — Short-term memory
- `MemoryClient` wiring (Bolt), conversation per chat, `add_message` per turn,
  `get_context` into PydanticAI dynamic instructions — *final shape decided by spike
  0.2* (F1).
- Graph panel v1: conversation + `:Message` chains (NVL Canvas renderer; node details
  panel showing role/timestamp/metadata).
- Message search UI with the paraphrase demo; *spike 0.1/0.2 decides how the "which
  search path answered" question is made observable* (F9 workaround — e.g. the app
  logs/labels the path itself rather than relying on a Bolt indicator).
- Targets: `s2-return`, `s2-restart` (script kills/restarts the backend mid-scenario).

### 3.3 Module 3 — Long-term memory
- Ontology load → validate → store + activate in DB (ADR: resolved at connect time;
  the activation step must unset the file config afterward — F12 pitfall is a
  *scripted step* in the README, not a trap).
- `extractor_type="llm"` wiring (ADR 001); `s3-default` vs `s3-ontology` before/after
  runs; app labels property provenance in the details panel (answers E3 for module 3:
  the panel *does* label sources).
- `app/memory/hydrate.py` post-extraction hook — *contract decided by spike 0.3* (F5);
  `add_entity` upsert semantics per Phase 2 mapping table.
- Enrichment: `EnrichmentConfig` (Wikimedia, ORGANIZATION allowlist), async; graph
  panel shows `enriched_description`/`wikipedia_url` when they land; `s3-enrich`.
- Graph panel v2: entity nodes with custom ontology labels, typed edges
  (`support`/`confidence` visible), `:MENTIONS` links.

### 3.4 Module 4 — Reasoning memory
- `record_agent_trace` on `AgentRunResult`; trace subgraph rendering (`AgentStep →
  ToolCall` chains, `:TOUCHED` edges, outcome nodes); failed-trace styling (red
  outcome node).
- Similar-task retrieval priming the agent — *final shape decided by spike 0.4* (F7).
- **Ablation demo (C1):** `make s4-refund-repeat` runs the same ticket twice —
  once with retrieval off (control) and once on (treatment) — with the trace panel
  showing the behavioral difference side by side. This is the module's proof moment.
- Targets: `s4-refund`, `s4-refund-repeat`, `s4-fail`.

### 3.5 Module 5 — Skill distillation (NAMS)
- `scripts/seed_nams.py` (choreography from spike 0.7; activates the Acme Cloud
  ontology server-side first); `make nams-check`/`nams-seed`/`nams-distill`.
- **Frontend second data source (B7):** graph panel gains a NAMS mode that renders
  the skill subgraph (`Skill`/`SkillVersion`/`SkillStep` + `GROUNDED_IN` edges) via
  the NAMS REST graph-neighborhood endpoint — the attendee's AuraDB is unreachable for
  this data, so this is REST-backed rendering, not Bolt.
- Fresh-agent payoff: `make s5-fresh-agent` loads the distilled SKILL.md into a
  new PydanticAI agent (control run: without the skill — C2).
- Drift beat (D4 resolved): two-step — `make policy-change` (SQLite limit flip) shows
  governance's blind spot, then `make nams-drift` deletes the refund-policy entity so
  `GROUNDED_IN` claims lose their sources and drift flags; `make nams-redistill`
  completes the loop. Stretch variant: mark a grounding `issue_refund` tool call
  failed. **Final confirmation from spike 0.6 before content is written.**
- **Seam narration (D2):** the M5 slides state explicitly that Bolt memory lives in the
  attendee's AuraDB while NAMS is a fresh managed workspace receiving the canonical
  seed — the boundary is taught, not discovered.
- **Fallback artifact (B2):** check a *pre-distilled* SKILL.md + exported skill
  subgraph JSON into the repo (`artifacts/pre-distilled-skill/`), loadable via
  `make s5-fallback`, so the payoff survives a NAMS outage.

**Exit (Phase 3):** `make module-1` … `make module-5` each reproduce their module's
full beat sequence from a clean AuraDB; **each module's exit includes validating the
eval scorecard at that module boundary and committing its golden-graph snapshot**
(the deferred Phase 2 verification — P2); every NVL screenshot in the outline is
reproducible; the CI behavioral lane (1.5) is green on the full scenario suite.

---

## Phase 4 — Slides & visual assets

*Deliverable: the instructor deck + per-module README diagrams. Deck is concept
transitions and framing — demos carry the workshop.*

**Two-milestone structure (fixes the deck↔rehearsal circularity, P2):**
- **Deck v0.9 (draft)** — all slides present, all spike-invariant diagrams final
  (D-01…D-08, D-16, D-18 can be drawn as soon as Phase 2 content stabilizes), and
  **placeholder boxes** where screenshot-dependent content lands (D-09, D-12, D-13,
  D-14, D-17 — these need Phase 3 exit and spike outcomes). Gates the buddy rehearsal
  (6.2).
- **Deck v1.0 (final)** — screenshots captured during the solo dry run (6.1) via the
  capture script (4.5) drop into the placeholders; gates the load rehearsal (6.3).

### 4.1 Diagram tooling decision (owner-visible, low-stakes)
- **Excalidraw** for all diagrams: source `.excalidraw` files committed under
  `slides/diagrams/`, exported PNG/SVG used in deck + READMEs. Rationale: matches the
  ecosystem's existing diagram conventions (memory-type colors, ellipse-node style),
  diffable-ish sources, fast iteration.
- **Color conventions (fixed, from the memory-type palette):** Short-term
  `#B2F2BB`/`#2F9E44` · Long-term `#FFEC99`/`#F08C00` · Reasoning `#D0BFFF`/`#9C36B5` ·
  Neo4j/store `#A5D8FF`/`#1971C2` · Labs accent `#6366F1`. One legend slide reuses
  these throughout so colors become the workshop's visual grammar.

### 4.2 Diagram inventory (committed sources + exports)

| # | Diagram | Used in |
|---|---|---|
| D-01 | **The two stores** — SQLite (system of record) vs. Neo4j (memory), agent between them; *reused in M1, M3 hydration, M5 drift* | Intro + M1 + M5 |
| D-02 | **Three memory types, one knowledge graph** — the trinity with color legend | Intro + Wrap |
| D-03 | **The workshop arc** — five-module failure→fix ladder with the eval scorecard overlay | Intro |
| D-04 | **Environment map** — Codespace (FastAPI, Vite, uv, scripts) ↔ AuraDB ↔ OpenAI ↔ NAMS; shows where each credential lives | M0 |
| D-05 | **Statelessness** — two identical sessions, no bridge (M1 failure) | M1 |
| D-06 | **Message chains** — `:Conversation` → `:Message` sequence; restart-survival animation frames | M2 |
| D-07 | **Context assembly** — `get_context` → dynamic instructions → model call | M2 |
| D-08 | **Ontology-driven extraction** — ontology YAML → extraction prompt → typed graph; forbidden relation dropped at ingest | M3 |
| D-09 | **POLE+O vs. custom ontology before/after** — two mini-graphs side by side | M3 |
| D-10 | **The hybrid pipeline** — three sources (LLM structure / SQLite facts / Wikipedia externals) converging on one entity node with provenance-colored properties | M3 |
| D-11 | **Entity resolution** — alias beat: "AcmeCloud" → one node; SAME_AS review edge | M3 |
| D-12 | **Reasoning trace anatomy** — task → AgentSteps → ToolCalls → outcome; `:TOUCHED` vs `:MENTIONS` contrast | M4 |
| D-13 | **Similar-task retrieval** — new ticket embeds near yesterday's trace; ablation callout (control vs treatment) | M4 |
| D-14 | **Distillation pipeline** — traces+entities+observations → SKILL.md + skill subgraph with `GROUNDED_IN` edges; grounding/coverage scores | M5 |
| D-15 | **Governance loop** — skill goes stale when grounding changes → re-distill (shape finalized after spike 0.6) | M5 |
| D-16 | **The finale: one agent's experience becomes everyone's skill** — fresh agent loading the skill | M5 |
| D-17 | **One knowledge graph recap** — single canvas showing all three layers + skill subgraph connected | Wrap |
| D-18 | **Bolt vs. NAMS** — consumption models table rendered as a diagram | Wrap |

### 4.3 Deck structure (~42 slides)

| Section | Slides | Key content |
|---|---|---|
| Title & framing | 4 | Title; "what you'll leave with" (honest run-and-explore promise — H1); agenda; D-03 arc |
| M0 Setup | 3 | D-04 environment map; credential checklist; `make check` live |
| M1 | 5 | D-01 two stores; the agent + tools; D-05 statelessness; live demo; eval baseline |
| M2 | 6 | Concept (short-term ≠ temporary); D-06; D-07; live demo + restart beat; exploration brief (core questions only) |
| M3 | 8 | Concept (entities vs. messages); D-08; D-09; D-10 (three sources — the design-principle slide: *structure from LLM, facts from SQLite*); D-11; live before/after; exploration brief (core questions only — 40-min module per D5) |
| M4 | 6 | Concept (the agent's own execution as memory); D-12; D-13; live ablation demo; exploration brief |
| M5 | 6 | D-14 distillation; **seam narration slide (D2)**: Aura vs. NAMS workspace boundary; D-16 payoff; live fresh-agent run; D-15 governance (delete-entity drift beat — D4); Labs/early-access disclosure (H7); exploration brief |
| Wrap | 4 | Eval scoreboard re-run (full board green — H6); D-17 one-graph recap; D-18 Bolt vs. NAMS; "Monday morning" path (add memory to your own agent in 20 min) + teardown + resources |

- Every concept term on a slide links its one-sentence glossary definition in speaker
  notes (D2); slides reference make targets verbatim so slides and terminal agree.
- Screenshots: expected-graph PNGs per module captured during rehearsal (E5 fallback).

### 4.4 Module READMEs (`docs/modules/module-N.md`)
Concepts (plain English), the make targets, **core vs. stretch tiering of the outline's
exploration questions** (E1: ≤3 core + rest marked stretch with answer key included),
expected-graph screenshots, glossary links, "if you fell behind: `make module-N`".

### 4.5 Screenshot capture tooling (feeds v0.9 → v1.0)
A Playwright capture script per module (`scripts/capture_screenshots.py`) run against
the seeded state after `make module-N` — produces the expected-graph PNGs used by both
the deck (4.3 placeholders) and the READMEs (4.4), repeatably instead of by hand at
rehearsal time. Doubles as visual-regression evidence in CI's behavioral lane (1.5)
alongside the golden-graph snapshots (2.7).

---

## Phase 5 — Packaging, pre-work & operational readiness

1. **Pre-work email** (open item): create + verify AuraDB free instance *and test
   connectivity*; store `OPENAI_API_KEY` as a personal Codespaces secret scoped to the
   repo; NAMS signup + `nams_` key (moves B4's minute-100 signup out of session);
   cost note (<$1 OpenAI, core-hours math); verification reply loop (`make check`
   output pasted back). *Fixes G10, B4, G8.*
2. **Instructor run-of-show** — minute-by-minute with transition scripts, the
   waiting-choreography notes (what to say during enrichment/async waits — G11),
   fallback decision points ("if enrichment hasn't landed by X, show screenshot"),
   and helper/TA triage policy (G6).
3. **Fallback kit** — `artifacts/`: pre-distilled skill (3.5), pre-recorded
   distillation video (B2), expected-graph screenshots, a seeded AuraDB snapshot
   script per module (`make module-N` catch-up uses it — G7).
4. **Teardown story** (H7): `docs/teardown.md` — delete codespace, delete/pause AuraDB
   instance, revoke NAMS key; Labs/early-access disclaimers attendee-facing in module 5
   slides and README.
5. **Labs positioning pass** — all materials carry the experimental/community-supported
   framing; no SLA/production claims (H7, skill checklist).

---

## Phase 6 — Rehearsals & launch checklist

1. **Solo dry run** — full run-through in a fresh Codespace as a clean account would
   experience it; time every module against the 150-minute budget (D5) and confirm the
   buffer + module 4 droppable section cover realistic slippage. **Captures the
   screenshots** (via 4.5's capture script) that turn deck v0.9 into v1.0 (P2).
2. **Buddy rehearsal** — one naive attendee (no Neo4j background) running with only
   the READMEs + **deck v0.9** (P2: final screenshots not required to validate
   comprehension); log every confusion point against the glossary/questions.
3. **Load rehearsal** — 3–5 parallel Codespaces hitting the same OpenAI key class
   (validates ADR 001 rate-limit pacing) and Wikimedia shared-egress behavior (G9).
4. **Go/no-go checklist** — prebuild green **after the final content commit** (no
   commits land between go/no-go and the event — content freeze); verification log
   complete; fallback kit present; **CI behavioral lane green, including the weekly
   live-service re-verification job** (1.5 — spike results are re-validated, not
   assumed permanent); `make module-1..5` green on a clean AuraDB; timing sheet signed
   off.

---

## Decisions (resolved 2026-10-27 in interactive review)

| # | Decision | Outcome |
|---|---|---|
| D1 | Module progression mechanics | **Folder-per-module** — `module_1/`…`module_5/` self-contained full code; shared root `.env`/venv/SQLite; `make module-N` per folder. ADR 004. Replaces branch-per-module (G1) and feature flags |
| D2 | Module 5 memory continuity | **Pre-seeded NAMS snapshot stands** (original choice); module 5 slides explicitly narrate the Aura→NAMS seam so attendees understand the boundary (B3 mitigation) |
| D3 | Enrichment prominence | **Keep, demoted to stretch** — instructor shows one pre-warmed Stripe node in passing; exploration steps live in module 3 README as stretch with screenshot fallback (H5 resolved, G9 risk off the critical path) |
| D4 | Drift beat | **Delete-entity beat** — `make policy-change` (SQLite) first shows governance's blind spot (it watches the memory graph, not the system of record), then `make nams-drift` deletes the refund-policy entity so `GROUNDED_IN` claims lose their sources and drift flags. Stretch variant: mark a grounding `issue_refund` tool call failed. Spike 0.6 still verifies live behavior before content is written |
| D5 | Clock | **Workshop extends to 2.5 hours** — M0 15 / M1 15 / M2 25 / M3 40 / M4 25 / M5 20 / Wrap 5 + 5-min buffer = 150. Module 3 re-scoped: enrichment stretch (D3), questions tiered (core 1, 2, 9, 13; instructor-demoed 3, 7, 12; rest stretch) |

## Traceability — top review items → where they're addressed

| Review item | Addressed in |
|---|---|
| B1 drift semantics (Critical) | D4 resolved (delete-entity beat); spike 0.6 confirms live before content |
| B2 climax single-threaded | Phase 3.5 fallback artifact + Phase 5.3 fallback kit |
| B3 memory-continuity seam | D2 resolved — seam explicitly narrated in M5 slides (Phase 3.5/4.3) |
| B4 signup at minute 100 | Phase 5.1 pre-work moves it out |
| B7 NVL can't render NAMS subgraph | Phase 3.5 REST-backed graph mode |
| C1/C2 missing ablations | Phase 3.1 flag + 3.4/3.5 control runs |
| C3 module 1 failure undercut by tools | Phase 2.4 scenario constraint |
| A1/A2 clock + module 3 overload | D5 resolved (2.5 h, M3 re-scope); Phase 6.1 empirical timing; 4.4 question tiering |
| D1/D2/D3 prereqs + jargon | Phase 2.6 glossary + 4.3 speaker notes + pre-work |
| E1/E2 question tiering/mini-labs | Outline M3 tiered (D5); Phase 4.4 tiers all modules; mini-labs → instructor demos in run-of-show |
| F1/F5/F7/F9/F12 Bolt unknowns | Spikes 0.2/0.3/0.4; F12 scripted step in 3.3 |
| F4 version pinning | ADR 002 `uv.lock` + spike 0.1 + CI lock check |
| G1 branch mechanics | D1 resolved — folder-per-module (ADR 004), Phase 1.6 |
| G7 catch-up lanes | `make module-N` (folders) + Phase 5.3 seeded snapshots |
| G9 Wikimedia shared egress | D3 — enrichment demoted off critical path |
| G10 pre-work verification | `make check` (1.4) + Phase 5.1 email |
| H1 run-and-explore promise | Phase 4.3 title-section honesty slide |
| H3/H6 eval thread + wrap | Phase 2.5 + 4.3 wrap slides |
| H5 enrichment demo candy | D3 resolved — stretch |
| H7 disclaimers/teardown | Phase 5.4/5.5 |

### Plan-review items (adversarial review of this plan)

| Item | Addressed in |
|---|---|
| **P1 — documents disagreed on the command surface** (22 vs 29 targets; root vs per-folder Makefile; ADR 002 missing `nams-drift`) | Phase 1.1: canonical spec — outline table is the source of truth (29 targets), **one root Makefile** with `MODULE` path resolution, `make help` generated from the spec, CI verifies target-for-target agreement (1.5 command-surface lane); ADR 002 + ADR 004 amended |
| **P2 — circular gates** (Phase 0 borrowed Phase 1 outputs; Phase 2's exit needed Phase 3; deck needed rehearsal outputs while rehearsal needed the deck) | Phase 0.0 spike infrastructure owns the throwaway scaffold; Phase 2 exit is now *authored*-only with boundary verification deferred into each Phase 3 module exit; Phase 4 two-milestone deck (v0.9 placeholders → gates buddy rehearsal 6.2; v1.0 screenshots from solo dry run 6.1 → gates load rehearsal 6.3); gate discipline amended (pass / costed fallback / stop-and-replan + decision-reopening protocol) |
| **P3 — no behavioral test lane** | Phase 2.7 golden-graph snapshot format + tolerances; Phase 1.5 CI behavioral lane (ephemeral Neo4j, scenario → subgraph → snapshot compare, devcontainer build job, weekly live-service re-verification); Phase 3 exit requires golden snapshots committed per module; Phase 4.5 capture script doubles as visual-regression evidence; go/no-go requires the lane green |

## Critical path

**Spike 0.6 (NAMS drift confirmation of the D4 design) → Phase 3.5 (module 5) → deck
v0.9 → solo dry run (screenshots) → deck v1.0 → buddy rehearsal → load rehearsal →
go/no-go.** Everything else can proceed in parallel once spikes 0.1–0.5 and 0.8 land,
but module 5's content cannot be finalized before the drift behavior is observed live,
and the deck is final only after the dry run feeds it (P2's two-milestone structure).
