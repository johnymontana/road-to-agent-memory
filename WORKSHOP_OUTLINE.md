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

### Module 1 — The Stateless Agent *(15 min)*

**Failure mode:** Customer reports an issue, then "returns" in a new chat — the agent
asks who they are again. Restart mid-conversation: context gone.

**What happens:**
- Baseline PydanticAI support agent with a rich tool set, each backed by SQL queries against the embedded, pre-seeded SQLite database (`data/acme_cloud.db`, stdlib `sqlite3` — no extra services to run):
  - `lookup_account(customer_email)` — customer, organization, subscription, plan
  - `search_product_catalog(query)` — products and features
  - `fetch_policy(topic)` — refund policy, SLA, API key rotation, data export, etc.
  - `check_service_status(service)` — current status of Acme Cloud services
  - `issue_refund(account_id, amount)` — validates against policy, writes to the refunds table
- Run scenario 1 (billing issue) — `make s1-baseline` — and observe zero continuity across chats
- Establish the eval-question baseline (`make eval` prints the scorecard from here on)

**Key framing introduced here:** two stores with two jobs. **SQLite is the system of
record** — the business data the agent *acts on* (accounts, catalog, policies). **Neo4j
is the memory** — what the agent *learned while acting* (conversations, entities,
traces). Memory doesn't replace the systems of record; it captures experience over them.
This distinction runs through the whole workshop.

**Guided exploration questions:**

1. Ask the agent the eval questions. Which can it answer? Which fail, and why?
2. Run the same ticket twice. Does the agent's procedure differ? What does that cost (tokens, latency, consistency)?
3. If two customers describe the same outage, does the agent connect them? What would it need in order to?
4. Watch a tool call in the trace panel: what SQL ran against SQLite? What did the agent "learn" during the call — and where does that learning go when the process exits?
5. Inspect the SQLite schema directly. Which tables back which tools? If the agent looks up the same account five times in one conversation, how many SQL queries run — and what would it take to avoid that?

*Design notes these questions inform: the **SQLite schema** — tables for customers,
organizations, products, features, plans, subscriptions, policies (keyed by topic),
service_status, refunds (write-path); the seed dataset must be rich enough that every
tool returns meaningful results immediately (attendees see agent competence from the
first message, so module 1's failure is *memory*, not capability); tools use
parameterized SQL and return typed, tool-call-visible results (their inputs/outputs
become the reasoning-memory and distillation material in modules 4–5); scenario 1 must
contain entity-rich dialogue so its loss is felt in module 3; the tool vocabulary
(`products`, `plans`, `policies`) deliberately mirrors the Acme Cloud ontology labels
so extracted entities line up with catalog rows.*

---

### Module 2 — Short-Term Memory *(25 min)*

**Concepts:** Conversations and messages; session continuity; `get_context`; context
assembly into PydanticAI dynamic instructions; message search (including **cross-session
"relevant past messages"** — a real capability with attribution nuance, see the
verification log); the three-tier context model (reflections / observations / recent
messages) **as a NAMS capability** — on Bolt, `get_context` returns recent + relevant
messages and reflections/observations raise `NotSupportedError` (a live
backend-asymmetry teaching moment; verified in spike 0.2).

**What changes:** `MemoryClient` (Bolt backend), conversation creation, `add_message` on
each turn, retrieved context injected per request.

**Run:** `make s2-return` (customer returns in a new chat) · `make s2-restart` (the
kill-and-restart-mid-conversation beat).

**Failure mode fixed:** The agent survives restarts and continues mid-conversation.

**NVL moment:** Sequential message chains appear — `:Message` nodes linked per conversation.

**Guided exploration questions:**

1. In the graph panel, find the conversation you just had. How are messages linked? What properties does a `:Message` node carry (role, timestamp, embedding, metadata)?
2. Kill and restart the app mid-scenario. What does the agent still know? Trace exactly which records made that possible.
3. Use message search with a paraphrase of something said earlier (not exact words). Which search path answered — vector or text? How can you tell?
4. Try `get_reflections` / `get_observations` on Bolt — what happens, and why? (They raise `NotSupportedError`: the three-tier model is a hosted/NAMS feature; Bolt gives you recent + semantically-relevant messages. Which would you pick for a self-hosted deployment, and what would you give up?)
5. What's the boundary of short-term memory? If the customer returns tomorrow in a *new* conversation, what crosses over — and what doesn't?

*Design notes these questions inform: conversation/message schema and metadata fields; embedding config; scenario must include a restart point and a paraphrasable statement; question 5 sets up module 3's motivation and implies conversations must link to a stable customer identity.*

---

### Module 3 — Long-Term Memory *(40 min)*

**Concepts:** Entity extraction with a **custom domain ontology** (not the default POLE+O
template) using **LLM-based extraction** (ADR 001: `extractor_type="llm"`, OpenAI,
structured outputs, temperature 0 — no local ML models); ontology-driven extraction —
one YAML document driving the LLM extraction prompt (entity types, annotation-guideline
descriptions, relationship patterns), relation validation on ingest, and entity
resolution; aliases; **structured, multi-property entities** (the hybrid pipeline
below); preferences and facts; memory tools (`save_preference`, `recall_preferences`,
`search_memory`); permissive vs. strict validation modes.

**What changes:**

1. Write the **Acme Cloud ontology** (`acme_cloud.yaml`) — domain-specific entity types and typed relationships, each anchored to a POLE+O `pole_type` for storage labels
2. Validate it with the CLI (`neo4j-agent-memory ontology validate`)
3. Configure **LLM extraction** (`extractor_type="llm"`, `llm="openai/gpt-4o-mini"`, temperature 0 — near-deterministic, identical on every attendee machine); store and **activate the ontology in the database** so every app restart picks it up automatically
4. Register the memory tools on the agent
5. Wire the **property-hydration and enrichment hooks** (below)

**The hybrid pipeline for rich, structured entities.** The LLM's structured payload
(`EntityPayload`) deliberately excludes `attributes` and `description` — facts never
come from the extractor. Rich entities come from a deliberate three-source split —
each source doing only what it's actually good at:

1. **LLM → structure.** Entity spans, types, and typed relations, extracted via
   structured outputs at temperature 0. The ontology is rendered into the extraction
   prompt (entity types with their annotation-guideline descriptions, legal
   relationship patterns), and relations the ontology doesn't permit are dropped at
   ingest.
2. **SQLite → grounded facts (hydration).** When extraction creates "Maya Chen" as a
   `Customer`, a post-extraction hook calls the system of record (`lookup_account`,
   catalog queries) and re-writes the entity via `add_entity(..., description=…,
   attributes={email, plan, signup_date, …})`. `add_entity` MERGEs on `(name, type)`
   with `ON MATCH SET e.description = COALESCE($description, e.description)` — so this
   **updates the extracted node in place** rather than duplicating it. *All* properties
   come from SQLite, including categoricals (`plan_tier`, `severity`) — grounded in
   real business data, never LLM-invented: no hallucinated emails, no hallucinated
   plan tiers.
3. **Wikipedia → external knowledge (enrichment).** Acme Cloud is fictional, but its
   *integrations* aren't — scenario dialogue mentions real third parties ("we pipe
   Acme Cloud webhooks into Stripe"). For those `Organization` entities, background
   enrichment (`EnrichmentConfig`, Wikimedia provider — free, no API key, rate-limited)
   writes `enriched_description`, `wikipedia_url`, `wikidata_id`, `image_url` onto the
   node asynchronously after extraction.

   **Enrichment steps (stretch — demoted off the critical path; the instructor shows
   one pre-warmed Stripe node in passing and moves on):**
   1. Enable enrichment in settings: `enrichment={"enabled": True,
      "providers": ["wikimedia"], "entity_types": ["ORGANIZATION"]}` — background,
      non-blocking, cached
   2. Run the scenario that mentions the Stripe integration (`make s3-enrich`); extraction creates the
      `Stripe` `Organization` entity
   3. Wait for the background worker (seconds at Wikimedia's ~2 req/s rate limit) —
      it's async, so the node appears first and enrichment fields follow
   4. Inspect the node in the graph panel: `enriched_description`, `wikipedia_url`,
      `wikidata_id` now present alongside the extraction-created properties

4. **The design-principle beat.** Show (briefly) *why* facts don't come from the LLM:
   it could infer an email or a plan tier, but the stock `EntityPayload` schema drops
   `attributes` and `description` by design — and that's the point. We use the LLM for
   *structure* precisely because we don't let it invent *facts*. Extending the payload
   for LLM property extraction is possible in custom builds; point at the extension,
   don't build it live.

**Teaching beat:** start with the default POLE+O entity types and show what generic
extraction produces on a support conversation (`make s3-default` — loosely labeled
nodes, no typed relations, bare properties) — then swap in the custom ontology (which
re-renders the extraction prompt) and re-run the same scenario (`make s3-ontology`) to
show the difference. This makes the value of ontology-driven extraction concrete.

**Failure mode fixed:** New session — the agent knows *who the customer is*: their plan,
their products, their preferences — not just what was said.

**NVL moment:** The knowledge graph blooms — `Customer`, `Organization`, `Product`,
`Plan`, `Incident` entities connected by typed edges (`REPORTED`, `USES`, `AFFECTS`,
`SUBSCRIBES_TO`, …), with `:MENTIONS` edges back to the source messages. Click a
`Customer` node: the details panel shows hydrated properties (email, plan) and a
`Stripe` node shows its Wikipedia enrichment (stretch beat — shown pre-warmed).

**Guided exploration questions** — tiered: **core** (everyone): 1, 2, 9, 13 ·
**instructor-demonstrated live** (config edits / re-runs): 3, 7, 12 · **stretch**
(answer key in the module README): the rest:

1. Find an entity extracted from your conversation. Follow its `:MENTIONS` edge back to the exact message that created it. Why is provenance valuable for a support org?
2. Compare the graph from the default POLE+O run vs. the custom-ontology run on the same scenario. What changed — labels, relationships, precision? Which would you rather build a support workflow on?
3. Read the ontology's entity-type descriptions. They're rendered verbatim into the LLM's extraction prompt — why do they include negative cases ("Not the support engineer who answers")? Rewrite one description without its negative cases and re-run — what gets extracted differently?
4. Trigger the alias beat: the customer says "AcmeCloud" after earlier saying "Acme Cloud". The ontology declares the alias — where's the evidence in the graph that they resolved to one node? What would have happened without the alias declaration?
5. Find a typed edge (e.g., `REPORTED`). What do its `support`, `confidence`, and `source_message_ids` properties tell you? Find an edge with `support >= 2` — what does that mean?
6. Query the Neo4j labels: why does a `Customer` land as `(:Entity:Person:Customer {subtype: "CUSTOMER"})`? What is the ontology label vs. the POLE+O anchor, and why keep both?
7. Switch validation to strict and feed the agent an entity type the ontology doesn't declare. What happens — dropped, warned, or stored? When would you choose strict vs. permissive?
8. Save a preference via chat ("I prefer email over phone"). Where does it land in the graph, and how does the agent surface it in a later session? How is a preference different from an entity?
9. Click into a `Customer` node's properties. Which came from the LLM (type, subtype, typed relations), which from SQLite hydration (email, plan, signup date), and which from Wikipedia enrichment (`enriched_description`, `wikipedia_url`)? How could you tell the *source* of each property if the panel didn't label them?
10. The LLM could infer properties like an email address — so why do we hydrate every fact from SQLite instead? What failure mode does LLM-invented data invite, and what does the stock `EntityPayload` schema's decision to drop `attributes` tell you about how the library's authors think about this?
11. Find the `Stripe` entity. Which properties are enrichment-written, and why did enrichment work for Stripe but would miss for "Acme Cloud"? When is external enrichment the right tool vs. internal hydration?
12. Watch a hydration upsert: re-run a scenario where the customer's plan was upgraded in SQLite between runs. What changed on the entity node — and what *didn't* (name, type, `:MENTIONS` edges)? Why is MERGE-on-`(name, type)` upsert semantics the right behavior here?
13. Compare what the agent knows about the customer now vs. module 2. Which eval questions changed answers?

*Design notes these questions inform: the **Acme Cloud ontology document** — entity
types (Customer, Organization, Product, Plan, Feature/Component, Incident) with
annotation-guideline descriptions and negative cases (rendered into the LLM extraction
prompt); typed relationships (WORKS_AT, SUBSCRIBES_TO, USES, REPORTED, AFFECTS,
PART_OF, INCLUDES) with at least one constraint (e.g. `unique_source` on WORKS_AT) to
teach constraint behavior; declared aliases covering the near-duplicate beat; the
**extraction config** — `extractor_type="llm"` with a pinned small OpenAI model at
temperature 0 (ADR 001); the **hydration mapping** — which SQLite columns populate
which entity properties per entity type (customers → email/plan/plan_tier/signup_date
on Customer; catalog rows → description on Product; policy topics → description on
Policy objects), with *all* properties including categoricals (`plan_tier`, `severity`)
hydrated from the system of record, implemented as a post-extraction hook calling the
existing SQLite tools and re-writing via `add_entity` upserts; the **enrichment
scenario beat** — dialogue must mention a real, Wikipedia-notable third party (Stripe)
whose entity type is in the enrichment allowlist, with the async gap (node first,
enrichment fields seconds later) rehearsed for live delivery; seed dialogue must
reliably exercise every entity type and at least two relationship patterns twice (for
`support >= 2`); a preference statement must be scripted; the ontology must be stored +
activated in the DB (resolved at connect time) so FastAPI restarts follow it;
**scenario pacing** — scripted conversations serialize OpenAI calls (chat + embedding +
extraction per turn) to avoid whole-room rate-limit bursts.*

---

### Module 4 — Reasoning Memory *(25 min)*

**Concepts:** Reasoning traces; agent steps, tool calls, outcomes; `record_agent_trace`
consuming a PydanticAI `AgentRunResult`; similar-task retrieval; provenance.

**What changes:** Every agent run recorded as a trace; similar past traces retrieved to
prime the agent on familiar tasks.

**Run:** `make s4-refund` (first refund ticket, recorded as a trace) ·
`make s4-refund-repeat` (the "same shape" ticket days later) · `make s4-fail` (the
deliberately over-limit refund that `issue_refund` rejects — the failed trace).

**Failure mode fixed:** A refund ticket identical in shape to one solved "yesterday" —
the agent recalls *how it solved it* instead of re-deriving the procedure.

**NVL moment:** Trace subgraphs — `ReasoningStep → ToolCall` chains (`HAS_STEP` /
`USES_TOOL` edges — naming verified in spike 0.4), `:TOUCHED` edges to
entities, outcome nodes (success/failure).

**Guided exploration questions:**

1. Pick a completed trace in the graph. Reconstruct the story: what was the task, which tools were called in what order, what was the outcome?
2. Find the `:TOUCHED` edges from a reasoning step. Which entities did the agent's decision depend on? How is this different from `:MENTIONS`?
3. Run the "same shape" refund ticket. What does similar-task retrieval return, and how does it change the agent's behavior (tool order, steps skipped, confidence)?
4. Find a *failed* trace (scenario includes one — e.g., a refund over the policy limit that `issue_refund` rejected). What went wrong, and how would the next agent avoid it? What does it mean that failures are first-class memory?
5. Answer the provenance question: "Why did you issue that refund?" — trace the answer from final outcome back through steps and tool calls (including the `fetch_policy` result the decision relied on) to the customer's original message.
6. Which eval question does reasoning memory unlock that modules 2–3 couldn't answer?

*Design notes these questions inform: scenario must include (a) a successful refund procedure executed at least twice with a consistent tool order (`lookup_account` → `fetch_policy("refund")` → `issue_refund`), (b) one deliberately failed trace (refund over the SQLite policy limit, rejected by `issue_refund`), (c) tool-call inputs/outputs — especially the SQL queries and `fetch_policy` results — rich enough to distill a procedure from in module 5; trace schema (task, steps, actionTaken, result, success) must be visible in NVL.*

---

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
- `ontology/acme_cloud.yaml` — the custom Acme Cloud ontology (entity types, typed relationships, aliases, constraints); a `default-poleo` variant for the module 3 before/after beat
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
| Wikimedia enrichment is async + network-dependent in live delivery | Enrichment cached (1-week TTL) and pre-warmed in the devcontainer; fallback: screenshot of the enriched Stripe node; hydration (SQLite) is synchronous and carries the demo if enrichment lags |
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
