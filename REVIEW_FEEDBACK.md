# WORKSHOP_OUTLINE.md — Adversarial Multi-Persona Review (v1)

> Review date: 2026-10-27. The outline was NOT modified. This document tracks feedback,
> gaps, and issues for triage. Five personas reviewed independently:
>
> 1. **Producer** — veteran live-workshop producer (logistics, clock, failure modes)
> 2. **Engineer** — neo4j-agent-memory/NAMS insider (technical accuracy vs. real APIs)
> 3. **Designer** — learning experience designer (curriculum, cognitive load)
> 4. **Attendee** — first-time attendee, mid-level dev, no Neo4j/PydanticAI/graph background
> 5. **DevRel** — conference-track reviewer (narrative, positioning, demo choreography)

---

## 1. Consolidated Issue Register

Severity: C = Critical, H = High, M = Medium, L = Low.
"Status" notes where our earlier direct source-code research (clone of the repo `main`
branch) already resolves or partially resolves an issue raised against published docs.

### Theme A — The clock is broken before anyone arrives

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| A1 | C | Module times sum to 125 min in a 120-min slot — zero buffer for transitions, questions, stragglers, or async waits | Producer, Designer, DevRel | |
| A2 | C | Module 3 is 2–3 modules in one: ontology authoring, two CLI steps, GLiNER attribute pass, three property sources, aliases, strict/permissive, before/after beat, 13 questions — realistically 45–55 min | Producer, Designer, DevRel, Attendee | All four personas independently flagged this |
| A3 | C | Module 0's 10 min is fantasy: Codespaces creation (1–20 min), .env editing with two credential systems, dual dev-server boot, 3-panel tour, 4 questions incl. sqlite3 CLI — plan 20 min | Producer, Designer, Attendee | |
| A4 | H | Module 5 must fit signup + key + seed + distill + inspect + payoff + drift + re-distill into 20 min; two async external systems chained behind an email-verification signup | Producer, DevRel, Engineer | |
| A5 | M | The designated flex point (Module 4 explore) is the wrong module to trim — it's the setup for distillation; the actual overflow modules (0, 3) have no trim plan | Producer, Designer | |
| A6 | M | Module 2's restart beat (kill app mid-scenario, whole room) costs ~5 min of its 25 | Producer | |
| A7 | L | Eval-question thread = ~20 extra agent runs per attendee, unbudgeted | Producer | |

### Theme B — Module 5: risk concentration + narrative seam at the climax

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| B1 | C | **Drift beat may not work as written**: NAMS drift semantics (per live API docs) flag claims whose source nodes were *deleted or merged* — updating a SQLite policy row touches zero NAMS graph nodes, so governance may flag nothing. Beat needs redesign or live verification | Engineer | Top verification priority per Engineer |
| B2 | C | Emotional climax is single-threaded on the least-confirmed component: live NAMS signup (early-access, unknown friction), unconfirmed distillation API, unknown run latency, unknown output quality. Only fallback is a pre-recorded video, which converts run-and-explore into watch-a-video | DevRel, Producer | |
| B3 | C | Payoff runs on seed-script memory, not the attendee's accumulated modules 1–4 memory — the "watch YOUR agent learn" arc silently resets at the climax; the seam is never narrated to attendees | DevRel, Designer, Attendee | User decision was "pre-seeded NAMS workspace" — reviewers flag the narrative cost; worth revisiting vs. replay approach |
| B4 | C | NAMS signup placed at minute ~100 of a Tuesday-evening workshop — worst possible logistics moment; 6 min of friction = attendee misses the payoff on their own screen | Attendee, Producer | Fix candidate: move signup to pre-work |
| B5 | H | Skill lifecycle simplified: review/publish gating (409 unless approved), publish thresholds (groundingThreshold/coverageThreshold), possible `feature_disabled (skill_distillation)` on the public deployment, workspace-key scopes — none accounted for | Engineer | |
| B6 | H | Distillation run latency unknown (202 + poll); drift beat needs TWO distillation cycles inside the module | Engineer, Producer, DevRel | |
| B7 | H | NVL graph panel can't render the NAMS skill subgraph without new REST-backed plumbing (attendees never connect to the NAMS workspace DB over Bolt) — an unplanned workstream | Engineer | |
| B8 | M | Seed script dependency chain unexamined: entities → traces → steps → tool-calls ordering, `touchedEntityIds` ID capture, resolve-before-create merges returning different IDs, rate limits on burst writes. "1 minute" is asserted, not measured | Engineer | |
| B9 | M | "Fresh agent resolves ticket cold" doesn't prove the skill did anything — the tools validate against SQLite policy regardless; without a paired control (fresh agent, no skill) it demonstrates tool design, not skill portability | DevRel, Engineer | Ablation gap — see Theme C |

### Theme C — Missing ablation beats (unprovable "fix" demos)

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| C1 | C | Module 4's fix is asserted, not demonstrated: a competent LLM with `lookup_account`/`fetch_policy`/`issue_refund` will likely execute the refund procedure with zero memory. No control run (retrieval off vs. on) is specified — if behavior is identical with/without memory, the arc collapses live | DevRel | |
| C2 | C | Same disease at module 5's payoff (see B9): no paired control run | DevRel | |
| C3 | H | Module 1's failure is undercut by its own toolset: `lookup_account(email)` lets the agent "know" the customer within a session; scripts must be engineered so tools demonstrably can't fix the failure (customer never states email; new session = no identity) | Designer | Design-note gap in Module 1 |

### Theme D — Prerequisites, audience, and jargon

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| D1 | C | No prerequisites/audience section anywhere. Implied prereqs: Python/uv, SQL CLI, reading FastAPI+React, YAML, env config, graph/NVL literacy, and (Q6 module 3) Cypher | Designer | |
| D2 | C | Jargon lands before definition, no glossary: POLE+O (never expanded anywhere in the doc), ontology, GLiNER, hydration, JointIE, EntityPayload, reflections/observations, distillation, SKILL.md, governance, drift, grounding/coverage scores, `support`, provenance | Designer, Attendee | Attendee's #1 requested fix: one-page plain-English glossary |
| D3 | C | PydanticAI never explained ("agent framework that gives an LLM callable functions") — attendees spend Module 1 reverse-engineering the architecture instead of thinking about memory | Attendee | |
| D4 | H | Several questions presuppose untaught graph/Cypher literacy (M3 Q6 "query the Neo4j labels" — with what tool? No Cypher console or query snippets exist in the repo plan) | Designer, Attendee | |
| D5 | H | The hybrid-pipeline paragraphs (JointIE carries no node properties / EntityPayload drops attributes) are written for library maintainers; first-timers read it twice, understand nothing, check out | Attendee | Keep the conclusion (grounded facts, no invented emails); move the justification to instructor notes |
| D6 | M | "Eval questions" reads as benchmark jargon; "skill distillation" debuts as a module title before existing as a concept | Attendee, DevRel | |

### Theme E — Exploration question design

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| E1 | H | 39 questions total, no core-vs-stretch tiering; at ~2 min/question there is no room; fast attendees idle, slow attendees dragged forward mid-thought | Designer, Attendee | |
| E2 | H | Several "questions" are actually mini-labs requiring config edits, restarts, re-extraction (M3 Q3 rewrite description + re-run; Q7 strict-mode experiment; Q12 hydration upsert) — 5–10 min each; they become instructor demos whether planned or not | Designer, Attendee | |
| E3 | H | Several questions assume instrumentation never specified: which search path answered (no UI indicator on Bolt), token/latency costs (no display), property-source labeling ("if the panel didn't label them" admits it may not exist) | Designer | |
| E4 | M | Discussion/show-off questions interleaved with comprehension checks undifferentiated — attendees can't tell which have a right answer to verify | Designer | |
| E5 | M | "Deterministic demos" over-claims: scripted inputs ≠ deterministic stochastic pipelines (LLM responses, GLiNER, resolution, distillation); no fallback for "the fix demo produced a worse graph than the failure demo" | DevRel, Engineer | |

### Theme F — Unverified technical claims

| # | Sev | Issue | Raised by | Status per our source-code research |
|---|---|---|---|---|
| F1 | C | Three-tier context (reflections/observations/recentMessages) is documented as a NAMS REST feature; whether Bolt's `get_context` returns tiers is unverified — Module 2's concept list and Q4 depend on it | Engineer | OPEN — must test on Bolt |
| F2 | C | Enum properties + `gliner_extract_attributes` not in the 0.7.0-documented ontology YAML format | Engineer | PARTIALLY RESOLVED — verified present in `main` source (`PropertyDef.enum`, `gliner_extract_attributes` setting, `compile_attribute_schema`); remaining risk: confirm the pinned PyPI release (0.8.0) ships them |
| F3 | C | `EnrichmentConfig` / Wikimedia provider existence unconfirmed against docs | Engineer | PARTIALLY RESOLVED — verified in `main` source (`EnrichmentConfig`, WIKIMEDIA provider, background, caching, ORGANIZATION filter); remaining risk: same pin-to-release check + live behavior timing |
| F4 | H | No version pin anywhere; outline mixes 0.7.0-documented and presumed-0.8.0 features; a pre-1.0 release could break the workshop on release day | Engineer | OPEN — pin + per-module smoke-test matrix needed |
| F5 | H | Hydration hook: no documented post-extraction hook; the contract depends on `add_message`'s return shape (does it expose extraction results?) — determines whether `app/memory/hydrate.py` is trivial or awkward | Engineer | OPEN — we verified ingest internals but not the return shape |
| F6 | H | Quoted `add_entity` MERGE semantics; how `attributes` merges (per-key vs wholesale) unverified; ingest-time resolution could route hydration writes onto a different node | Engineer | PARTIALLY RESOLVED — MERGE on (name,type) + `ON MATCH SET e.description = COALESCE(...)` verified in source; attributes land in `metadata.attributes` — merge behavior of that blob + resolution interaction still open |
| F7 | M | Similar-task retrieval + `:TOUCHED` verified for NAMS, assumed for Bolt (interface similarity ≠ behavioral portability per docs) | Engineer | OPEN — must test `client.reasoning` on Bolt |
| F8 | M | GLiNER CPU inference latency per message inside `add_message` (synchronous on Bolt) — 1–5 s/turn × 10-turn scenarios = minutes of spinner; devcontainer SKU must be benchmarked | Engineer | OPEN |
| F9 | M | Documented Bolt bug: semantic message search ignores `session_id` — undermines Module 2 Q3's in-conversation search interpretation; Bolt has no `searchType` indicator | Engineer | OPEN |
| F10 | M | GLiNER checkpoint revision not pinned; `feasible=False` quiet failure mode; threshold sensitivity | Engineer | OPEN |
| F11 | M | NAMS ontology import of `acme_cloud.yaml` (incl. enum properties) unverified; server-side extraction semantics differ from Bolt (422 vs flag-not-drop, RELATED_TO fallback) | Engineer | OPEN |
| F12 | L | Stored-ontology activation trap: a client with `ontology_path` set overrides the stored active version, and activation doesn't rewire a connected client — Module 3's flow must unset the file config after activation or the restart demo silently reads the file | Engineer | VERIFIED pitfall; not handled in outline narrative |
| F13 | L | Preferences/facts are Bolt-only — fine for 1–4, but Module 5's NAMS agent can't demo `save_preference` (NAMS-only tool set differs) | Engineer | Note for module 5 agent wiring |

### Theme G — Operational gaps (live delivery)

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| G1 | C | Branch-per-module transition mechanics unspecified: does `git checkout module-3` restart servers, preserve .env/GLiNER cache, keep deps compatible? 4 switches × 3–8 min sync events, unbudgeted | Producer | |
| G2 | H | Local-clone attendees get the 407 MB GLiNER download at minute ~60 over venue wifi (prebuild mitigation only covers Codespaces) | Producer | |
| G3 | H | Aura free-tier auto-pause hits the most compliant attendees (created early, untouched); pre-work has no verification loop | Producer | |
| G4 | H | Shared fallback instance breaks Module 3's core mechanics: ontology activation is singleton-per-DB, hydration MERGEs are singleton-per-name, strict/permissive experiments collide across tenants | Producer | Fallback and module design conflict |
| G5 | H | Screenshot/video fallbacks contradict run-and-explore: a screenshot can't be clicked in NVL or traced along edges; ~1/3 of guided questions become unanswerable when a fallback fires, and which-to-skip is undefined | Producer | |
| G6 | H | No helper staffing / TA ratio / triage policy specified; run-and-explore with per-attendee DBs = environment-debug sessions | Producer | |
| G7 | H | No fallen-behind recovery path for modules 2–4 (module 5 has seed_nams.py; earlier modules have nothing) — branch-hopping restores code, not database state, and questions are state-dependent | Producer | Candidate: per-module `seed_state.py` |
| G8 | M | OpenAI billing/rate-limit prerequisites invisible (paid account, 429s during scenario bursts look like breakage) | Producer, Attendee | |
| G9 | M | Codespaces shared egress IPs vs Wikimedia per-IP rate limiting — the whole room's enrichment can throttle as one | Producer | |
| G10 | M | Pre-work is one bullet in a risk table; needs a multi-step email with deadline + verification ("reply with a screenshot" / smoke-test script) | Producer, Attendee | |
| G11 | M | GLiNER cold-start dead air (first model load + CPU inference, ×3 extraction-bearing runs in Module 3) unchoreographed | Producer | |

### Theme H — Narrative & positioning

| # | Sev | Issue | Raised by | Notes |
|---|---|---|---|---|
| H1 | H | "Run-and-explore" ≠ "build an agent": attendees never write agent code or author the ontology from scratch; if the abstract promises building, it's bait-and-switch. Attendee-facing promise must match format | DevRel | |
| H2 | H | Module 2's memory partially pre-solves Module 3's failure (persistent searchable history + stable identity); the boundary needs a choreographed question that module 2 provably fails and module 3 nails | Designer, DevRel | Same seam issue as C3 |
| H3 | H | Eval-question thread is load-bearing but deferred and ambiguous — "have you handled a ticket like this before?" is answerable by layers 2, 3, OR 4; attribution per layer unsettled | DevRel, Designer | |
| H4 | M | Two-stores framing silently becomes three stores at module 5 (NAMS workspace); "why not SQLite for everything?" and "why a graph at all?" only half-preempted; the graph-vs-SQLite sentence is never said | DevRel | |
| H5 | M | Wikipedia enrichment is demo candy — fixes no failure mode, consumes the most overloaded module's minutes, adds a live network dependency; obvious cut/demote candidate | DevRel | Conflicts with user's request to include enrichment — resolve by demoting to stretch/README, not deleting |
| H6 | M | Wrap overloaded (recap + Bolt/NAMS trade-offs + pointers in 5 min); eval board never re-run at the end; no "one graph" recap visual; no "here's your Monday-morning path to add memory to your own agent" transfer step; realistic takeaway is module-2-level wiring only | DevRel, Designer, Attendee | |
| H7 | M | Labs/early-access disclaimers are author-facing only; no attendee-facing caveat at NAMS signup; no post-workshop teardown story (orphaned Aura instances, NAMS keys, costs) | DevRel | |
| H8 | M | Distilling from ~2 refund traces is a toy evidence base — grounding/coverage scores over 2 observations invite the "how many traces before trust?" question | DevRel | Seed script partially masks; be ready with the honest answer |
| H9 | L | Branch delivery makes "progressive" actually discrete config-switched jumps; discerning attendees may notice; presentation of branches matters | DevRel | |
| H10 | L | Design notes (instructor-facing) interleaved with attendee-facing curriculum — risk of leaking into READMEs | Designer | |

---

## 2. Persona verdicts, condensed

- **Producer:** "This fails first at Module 3, minute 70–80: already 10–15 min behind from Module 0 overrun, half the room hits the GLiNER cold-start stall simultaneously, one instructor debugs divergent graphs while the custom-ontology re-run hasn't started. Everything after is triage."
- **Engineer:** 20 issues; 4 Critical — drift-beat semantics (likely wrong as written), Bolt three-tier context, enum-attribute/enrichment existence (partially resolved by our source research, release-pin remains), version drift. Top-3 must-verify list: (1) drift/governance behavior, (2) enum pass + enrichment on the pinned release, (3) Bolt `get_context` shape + `add_message` return shape.
- **Designer:** No prerequisites, no learning objectives, Module 3 is three modules in a trench coat, 39 untiered questions, eval thread not operationalized. Three fixes: split/tier Module 3; prereqs + graph-literacy floor + glossary; finalize the eval scorecard as the actual assessment instrument.
- **Attendee:** "Module 3's hybrid-pipeline paragraphs are the deepest water with no ladder; NAMS signup at minute 100 is the worst-placed logistics in the outline; module 3's 13 questions are where I flip into spectator mode." #1 request: a one-page plain-English glossary up front. #2: move NAMS signup to pre-work.
- **DevRel:** Verdict **accept-with-changes**, conditional on: (1) ablation beats in modules 4 & 5, (2) structural de-risking of module 5 (pre-distilled skill artifact in repo, attendee-facing disclaimers, teardown story), (3) clock rebalance (module 3 is a 50-min module in a 25-min slot; demote enrichment), (4) land the ending (re-run eval board, one-graph recap, narrate the Aura→NAMS seam). "The story in the planning doc is more beautiful than the story the room will experience."

---

## 3. Cross-Persona Consensus (issues flagged by 3+ personas independently)

1. **Module 3 is over capacity** (all 5 personas) — the single strongest signal in the review
2. **The clock doesn't add up** (4 personas: 125 > 120, no buffer)
3. **Module 5's risk concentration + signup timing** (4 personas)
4. **Jargon before definition / no glossary / no prereqs** (3 personas)
5. **Untiered, partly-unanswerable exploration questions** (3 personas)
6. **Module 2→3 failure-mode seam leaks** (2 personas + adjacent C3)

---

## 4. Proposed Triage Order (for discussion — outline unchanged)

**P0 — factual correctness (before any content build):**
- B1 drift-beat verification/redesign · F1 Bolt `get_context` shape · F2/F3 release-pin check on 0.8.0 · F5 `add_message` return shape · F7 Bolt similar-task retrieval · B5/B6 distillation surface + latency rehearsal

**P1 — structural (outline revision):**
- Re-scope Module 3 (split 3a structure / 3b property provenance; demote enrichment to stretch) · Fix the clock (Module 0 → 15–20 min with pre-work verification; NAMS signup → pre-work) · Add ablation beats (C1/C2/C3) · Tier all questions core/stretch, halve the count · Prereqs + glossary + graph-literacy floor + Cypher snippets · Resolve the module 5 memory-continuity seam narratively (or revisit pre-seeded vs. replay decision) · Operationalize the eval scorecard

**P2 — operational (repo/build phase):**
- G1 branch mechanics · G2 local GLiNER download script · G4 fallback redesign (per-attendee seeded DB snapshot vs shared instance) · G5 fallback-compatible question marking · G7 per-module `seed_state.py` catch-up lanes · G6 staffing plan · F4 version pin + smoke-test matrix · H7 teardown script + disclaimers

**P3 — polish:**
- H6 wrap redesign (eval board re-run, one-graph visual, Monday-morning path) · D5 move insider-justification prose to instructor notes · H10 separate design notes from attendee content · H4 say the "why a graph, not SQLite" sentence explicitly · F12 unset-ontology_path-after-activation step in module 3 flow
