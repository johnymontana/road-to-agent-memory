# Phase 0 Verification Log

> Spike results against the live stack: `neo4j-agent-memory==0.8.0` (uv.lock),
> AuraDB (Bolt), OpenAI (gpt-4o-mini + text-embedding-3-small). NAMS spikes
> (0.6/0.7) remain blocked pending a `nams_` key; Codespaces spike (0.9) pending
> repo push. Format per IMPLEMENTATION_PLAN.md Phase 0.

| Spike | Status | Result |
|---|---|---|
| 0.1 Lock + smoke | ✅ PASS | `uv.lock` resolves 61 packages; `neo4j-agent-memory==0.8.0` + pydantic-ai 2.62.0; all imports and API surfaces verified by introspection |
| 0.2 Bolt `get_context` shape | ⚠️ CONFIRMED ASYMMETRY (F1) | **Three-tier context (reflections/observations) is NAMS-only.** Bolt `get_context` returns a plain string: "Conversation History / Recent Conversation" + cross-session "Relevant Past Messages". `get_reflections`/`get_observations` raise `NotSupportedError` on Bolt. Module 2 outline updated accordingly |
| 0.3 `add_message` return | ✅ PASS | Returns `Message` (id, role, content, conversation_id, …) — no extracted-entity list, so the hydration contract is **query `:MENTIONS` via `(Conversation {session_id})-[:HAS_MESSAGE]->(m)`** (session_id lives on the Conversation node, NOT the Message — fixed in `lib/hydrate.py`) |
| 0.4 Bolt reasoning | ✅ PASS (F7) | `record_agent_trace` is async, consumes `AgentRunResult`, creates `ReasoningTrace`/`ReasoningStep`/`ToolCall`/`Tool` nodes; `get_similar_traces` works on Bolt. **Naming: steps are `ReasoningStep`, not `AgentStep`** — outline + frontend palette updated. Trace→step rel is `HAS_STEP`; tool rels are `USES_TOOL`/`INSTANCE_OF` |
| 0.5 LLM extraction | ✅ PASS (quality) / ⚠️ LATENCY | Extraction with `acme_cloud.yaml`: all 5 entity types with correct ontology labels, 4-7 typed relations, 0 undeclared (dropped at ingest as documented), `USES` reaches support=2. **Latency: ~6.5-13s per message** (first call worst) vs the <2s target — scenario scripts pace through it and the run-of-show narrates the wait; a faster extraction model is a tuning option. Cost: gpt-4o-mini, fractions of a cent/message |
| 0.6 NAMS drift | ⛔ BLOCKED | Requires `nams_` key (commented out in .env). D4 delete-entity design remains unverified — **module 5 content stays gated** |
| 0.7 NAMS seed | ⛔ BLOCKED | Same. `scripts/seed_nams.py` written against the documented v1 surface |
| 0.8 Wikimedia enrichment | ✅ PASS | With the config actually applied (see bug below), explicit `add_entity` enriches in **~5s** (`enriched_description` + `wikipedia_url` verified on a real third party). Extraction-created entities did NOT enrich in 60s pre-fix; re-verify post-fix during rehearsal |
| 0.9 Codespaces prebuild | ⛔ BLOCKED | Requires repo push to GitHub |

## Bugs found and fixed during verification

1. **`MemorySettings(enrichment=None)` raises** — enrichment must be omitted, not
   None (`lib/memory.py` now builds kwargs conditionally).
2. **OpenAI adapters read the raw env var** — pydantic-settings loading of `.env`
   isn't seen by the package's OpenAI client or PydanticAI; `get_settings()` now
   exports `OPENAI_API_KEY` into the process env.
3. **Hydration query used a non-existent `Message.session_id`** — session identity
   lives on `Conversation`; traversal fixed.
4. **`add_entity` does not write `attributes`/`metadata` on the ON MATCH path**
   (F6 resolved empirically) — description upserts, attributes don't. Hydration now
   writes flat node properties via the app's own driver session (`SET e += $map`),
   which also makes hydrated facts directly visible in the NVL details panel.
5. **`query.cypher` is read-only on Bolt** (write keywords rejected) — the flat-property
   write path above uses our own driver, not the memory client.
6. **Run-time `agent.run(instructions=…)` REPLACES constructor instructions** — the
   memory-tool usage rule never reached the model until `base_instructions` was
   unified. This was the root cause of "agent claims it checked memory without
   calling the tool".
7. **`search_memory` (shipped tool) searches messages only** — wrapped to also run
   `long_term.search` so hydrated entity facts are recallable; wrapper records into
   the tool-call collector (memory-tool calls were invisible to the trace panel).
8. **Missing `**kwargs` in `build_settings`** — the enrichment dict was built but
   never passed to `MemorySettings` (spike 0.8's original failure).
9. **`s2-restart` scenario alias missing** in the runner's file mapping.
10. **Failed refunds were recorded as successful traces** — the chat pipeline now
    marks `success=false` with the rejection outcome when `issue_refund` returns
    `rejected_over_limit` (the module 4 failed-trace beat).

## Eval-instrument findings (H3/C3 — the continuity scorecard)

The eval is a **narrative instrument, not a formal proof**. Verified boundaries on
clean-room runs (wipe → module sequence → eval per boundary):

- Module 2: same-session recall (q2) and Northwind-handle identity (q1) pass.
- Module 3: signup-date (hydration-only fact) answered from the hydrated entity.
- Module 4: full board green; the ablation usage line (`◆ memory used:` in the
  scenario runner) is the provable mechanism delta (control: `short_term, long_term`
  vs treatment: `short_term, reasoning, long_term`).

**Known attribution limits (teachable, documented for the run-of-show):**

- Bolt message search retrieves **cross-session** ("Relevant Past Messages" — the
  F9 behavior), so any fact stated in any conversation is potentially recallable
  from module 2 onward.
- The agent legitimately **combines memory recall with tools** (retrieves the email
  from memory → `lookup_account` → signup date), so tool competence can answer
  "memory" questions early.
- Signals must never appear in the question text (the model's restatement of the
  question matches them — found with "400").

Instructor framing: early-module passes via tool cleverness are teachable moments
("notice the agent had to find the email first — at module 3 the knowledge is
structured, grounded, and deduplicated"). Phase 6 buddy rehearsal owns final
question phrasing.

## Clean-room end-to-end run (final state)

Sequence: `reset-memory` → `s2-return` → `s3-default` → `s3-ontology` → `s4-refund`
→ `s4-fail` → `s4-refund-repeat` (ablation) → `eval` per boundary. All beats
demonstrated their designed behavior:

- M1 (verified earlier): stateless failure — asks for email twice; second session
  zero continuity.
- M2: restart beat — same conversation continues with full context after simulated
  process restart.
- M3: all 5 ontology entity types; `USES` support=2; hydration properties on
  Customer nodes (`email`, `plan_tier`, `hydrated_from`); preference saved via the
  agent's own `save_preference` call; before/after (default-poleo vs acme_cloud)
  contrast confirmed.
- M4: refund issued (in-limit) / rejected+escalated (over-limit, recorded as the
  failed trace) / ablation pair with visible retrieval delta.

Golden snapshots: `tests/golden/m2-state.json`, `m3-state.json`, `m4-state.json`
(m4 captured live: 29 entities, 9 traces incl. 1 failed).

## Remaining open (gated)

- 0.6/0.7 NAMS verification (needs `nams_` key) → module 5 content finalization
- 0.9 Codespaces prebuild rehearsal (needs GitHub push)
- Extraction-created entities + enrichment timing re-verification post-fix
- Scenario tuning notes: "Billing API" extracted as its own node vs canonical
  "Acme Cloud Billing API" (ontology alias exists; surface form kept); "AcmeCloud"
  typed as Organization with alias — rehearse the alias beat narrative
