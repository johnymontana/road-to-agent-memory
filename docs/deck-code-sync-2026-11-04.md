# Deck synchronization with current workshop code — 2026-11-04

Reviewed all 75 slides in the existing native [Google Slides deck](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8), including modules 0–5 and the wrap. Forty slides received visible content changes; all 75 presenter notes were refreshed. All 14 code walkthroughs were checked against current module implementations and installed package signatures. Native slide IDs/order, Neo4j template layouts and 45 circular graph nodes are preserved.

This review uses the current working tree, including the module rearchitecture and uncommitted application updates. No application code was modified. Source hashes in `slides/technical-walkthroughs-verification.json` identify the reviewed Python files. Final native revision: `DDts8zxWoZw1ng`.

## Corrections by module

| Area | Current implementation reflected in the slides | Main evidence |
| --- | --- | --- |
| Architecture / baseline | Every module owns a complete agent. Local `guardrails.py` validates scope/replies; `ReceiptGuard` and response envelopes are infrastructure. Module 1 has no memory client. | `AGENTS.md`, `module_1/app/agent.py`, `lib/operations.py`, `lib/response.py` |
| Client lifecycle | Explicit `MemorySettings` passed to a module-local client, whose async lifetime spans turns. The package permits omitted settings; `backend` belongs in settings, not constructor keywords. | `module_2/app/memory.py`, installed SDK signature |
| Short-term memory | `add_message` creates the conversation on first use. `Context.history` carries ten prior messages as typed PydanticAI messages; `Context.prompt` carries semantic evidence; `Context.evidence` carries UI provenance. A two-path diagram shows the integration. | `module_2/app/agent.py`, `context.py` |
| Semantic retrieval | Namespace-scoped Cypher, cosine ≥0.5, up to five deduplicated user statements; same or other conversations may match. Prefix heuristics filter some recall questions. | `module_2/app/context.py` and copies |
| Long-term memory | Current prompt constants, LLM extraction, `grounded_facts` / `lookup_facts` and `PropertyWriter.set_properties`. Check `hydrated_from` for SQL provenance; generated descriptions alone are not authoritative. | `module_3/app/agent.py`, `memory.py`, `hydrate.py` |
| Preferences | Customer-scoped category and user identity; `add_preference` writes `User → HAS_PREFERENCE → Preference`; `get_preferences_for` retrieves it. Local `recall_preferences()` takes no topic. | `module_3/app/memory_tools.py`, `context.py` |
| Labs / graph semantics | Comparison and Wikimedia enrichment are in `module_3/lab/`; Saved replay snapshots do not write the live graph. Live semantic edges use `RELATED_TO` with a `type` property; diagram/UI captions can show logical domain relations. | `module_3/lab/compare.py`, `enrichment.py`, `app/context.py` |
| Reasoning memory | `similar_executions`, `record_execution`, `checked_reply`; only completed traces match, excluding the current open trace. Cosine ≥0.45, at most three; completed declines remain eligible. | `module_4/app/agent.py`, `reasoning.py`, `memory_tools.py` |
| Outcomes / ablation | Trace success derives from `error_kind`; exact reply, execution and business status stay separate. Manual retrieval-off still records. Controlled ablation also disables recording, extraction and hydration in both branches. Step → TOUCHED → Entity remains accurate. | `module_4/app/reasoning.py`, `module_4/lab/ablation.py`, `scripts/run_scenario.py` |
| Hosted skills | Separate authored fixtures; REST generate, poll, publish and download. Publication 409 triggers automatic review approval, not a human checkpoint. No fabricated SDK skills API. | `module_5/workflows/distill.py`, `seed.py` |
| Fresh agent | Explicit off/on commands run separately on private SQL copies. Base instructions plus Markdown, without memory history/search. The demo skips app turn/reply guards; refund-tool SQL checks remain. Fallback is `WITH_SKILL=fallback`. | `module_5/app/fresh_agent.py`, `scripts/fresh_agent.py` |
| Drift | Select exact name `Pro`, delete its ID, list skills and query `/v1/skills/{id}/drift`. Inspect actual returned claims; no guaranteed stale result or correctness claim. | `module_5/workflows/drift.py` |
| Flow / wrap | 150-minute budget includes wrap and buffer. Catch-up commands replay selected beats. Apps 2–5 use Bolt; hosted fixtures stay separate. The Monday recipe teaches typed history and does not itself invoke an agent. | `Makefile`, `docs/run-of-show.md`, `scripts/monday_memory.py` |

## Validation and visual review

- Offline workshop suite: **139 passed, 1 skipped, 4 deselected**; one existing SDK Pydantic deprecation warning. Command: `UV_CACHE_DIR=<temporary-cache> uv run --offline pytest tests/ -m 'not behavioral' -q`.
- All 14 code fragments parse as contextual async fragments. Displayed arguments match installed `neo4j-agent-memory==0.8.0`, `pydantic-ai-slim==2.62.0`, local helper and HTTP client signatures. Scopes and notes explain omitted setup/error handling and presentation aliases.
- Final native readback matches expected text, code, asides, source captions and notes. Slide IDs/order and layouts are unchanged. All 45 graph circles remain native ELLIPSE objects with equal physical width and height.
- Inspected all 75 delivered LARGE previews and each code slide separately at full size. One consolidated repair pass fixed two crowded openers, one long title, a broken inline identifier, the context diagram's persistence label, shell continuations and a constructor note. All seven repaired slides were re-inspected.
- Final issue checker: **zero errors**, with 29 preserved template caption/eyebrow/micro-label warnings reviewed visually. Connector previews were used because the prior PDF helper could not materialize an export; unchanged source previews from the same initial revision were reused.
- Synchronized `slides/deck.md`, both walkthrough mirrors and all 17 diagram sources. Regenerated SVGs and local Marp HTML. Normalized legacy literal newline escapes in the scene source so SVG labels break correctly. Both diagram generators pass lint; `git diff --check` passes.
- No OpenAI, Neo4j, Wikimedia or hosted NAMS live rehearsal was run. Hosted behavior still requires a configured-workspace rehearsal; mocked HTTP contracts do not establish service parity.

## Slide-by-slide coverage

| Slide | Native ID | Title / role | Review result |
| --- | --- | --- | --- |
| 1 | `ram_slide_001` | Road to Nodes Agent Memory | Content verified; notes refreshed |
| 2 | `ram_design_002` | What you’ll leave with | Content verified; notes refreshed |
| 3 | `ram_slide_003` | Three memory types, one knowledge graph | Content verified; notes refreshed |
| 4 | `ram_slide_004` | Agenda · 150 min | Visible content + notes synchronized |
| 5 | `ram_design_005` | The workshop arc | Content verified; notes refreshed |
| 6 | `ram_slide_006` | Failure → memory layer → fix | Visible content + notes synchronized |
| 7 | `ram_design_007` | Your environment | Content verified; notes refreshed |
| 8 | `ram_slide_008` | Workshop environment | Content verified; notes refreshed |
| 9 | `ram_design_009` | Credential checklist | Content verified; notes refreshed |
| 10 | `ram_design_010` | Smoke test, live | Content verified; notes refreshed |
| 11 | `ram_design_011` | System of record | Content verified; notes refreshed |
| 12 | `ram_slide_012` | Two stores, two jobs | Visible content + notes synchronized |
| 13 | `ram_design_013` | Meet the agent | Visible content + notes synchronized |
| 14 | `ram_code_m1` | The baseline: PydanticAI + business tools | Visible content + notes synchronized |
| 15 | `ram_design_014` | The failure: statelessness | Content verified; notes refreshed |
| 16 | `ram_slide_015` | Stateless turns have no bridge | Content verified; notes refreshed |
| 17 | `ram_design_016` | The stateless baseline | Content verified; notes refreshed |
| 18 | `ram_design_017` | The eval baseline | Content verified; notes refreshed |
| 19 | `ram_mem_intro` | Meet neo4j-agent-memory | Visible content + notes synchronized |
| 20 | `ram_mem_seam` | Where memory meets PydanticAI | Visible content + notes synchronized |
| 21 | `ram_code_client` | Configure and open one memory client | Visible content + notes synchronized |
| 22 | `ram_design_018` | Short-term memory | Visible content + notes synchronized |
| 23 | `ram_design_019` | Message chains in the graph | Content verified; notes refreshed |
| 24 | `ram_slide_020` | Conversation memory survives restarts | Content verified; notes refreshed |
| 25 | `ram_code_m2_write` | Persist both sides of a conversation | Visible content + notes synchronized |
| 26 | `ram_design_021` | Context assembly | Visible content + notes synchronized |
| 27 | `ram_slide_022` | Per-turn context assembly | Visible content + notes synchronized |
| 28 | `ram_code_m2_inject` | Retrieve evidence, then call the agent | Visible content + notes synchronized |
| 29 | `ram_design_023` | The returning customer | Content verified; notes refreshed |
| 30 | `ram_design_024` | The restart beat | Content verified; notes refreshed |
| 31 | `ram_design_025` | Exploration brief | Content verified; notes refreshed |
| 32 | `ram_design_026` | Long-term memory | Visible content + notes synchronized |
| 33 | `ram_design_027` | Ontology-driven extraction | Content verified; notes refreshed |
| 34 | `ram_slide_028` | Ontology-driven extraction | Content verified; notes refreshed |
| 35 | `ram_code_m3_extract` | Turn on ontology-driven extraction | Visible content + notes synchronized |
| 36 | `ram_design_029` | Default POLE+O | Content verified; notes refreshed |
| 37 | `ram_slide_030` | Default vs. custom ontology | Visible content + notes synchronized |
| 38 | `ram_design_031` | The hybrid pipeline | Visible content + notes synchronized |
| 39 | `ram_slide_032` | The hybrid pipeline | Visible content + notes synchronized |
| 40 | `ram_code_m3_ground` | Ground extracted entities in SQL facts | Visible content + notes synchronized |
| 41 | `ram_design_033` | Entity resolution and aliases | Content verified; notes refreshed |
| 42 | `ram_slide_034` | One real-world entity, many surface forms | Content verified; notes refreshed |
| 43 | `ram_design_035` | Watch the graph bloom | Visible content + notes synchronized |
| 44 | `ram_design_036` | Under the hood | Visible content + notes synchronized |
| 45 | `ram_code_m3_tools` | Expose memory tools to PydanticAI | Visible content + notes synchronized |
| 46 | `ram_code_m3_preferences` | Save and recall one customer’s preferences | Visible content + notes synchronized |
| 47 | `ram_design_037` | Exploration brief | Content verified; notes refreshed |
| 48 | `ram_design_038` | Reasoning memory | Visible content + notes synchronized |
| 49 | `ram_design_039` | Anatomy of a trace | Content verified; notes refreshed |
| 50 | `ram_slide_040` | Anatomy of a trace | Content verified; notes refreshed |
| 51 | `ram_code_m4_lifecycle` | Open the trace before execution | Visible content + notes synchronized |
| 52 | `ram_code_m4_tools` | Attach observations and provenance | Visible content + notes synchronized |
| 53 | `ram_code_m4_outcome` | Complete the trace with an outcome | Visible content + notes synchronized |
| 54 | `ram_design_041` | Similar-task retrieval | Visible content + notes synchronized |
| 55 | `ram_slide_042` | Similar-task retrieval | Visible content + notes synchronized |
| 56 | `ram_code_m4_recall` | Recall completed executions | Visible content + notes synchronized |
| 57 | `ram_design_043` | Record, decline, compare | Content verified; notes refreshed |
| 58 | `ram_design_044` | “Why did you issue that refund?” | Content verified; notes refreshed |
| 59 | `ram_design_045` | Exploration brief | Content verified; notes refreshed |
| 60 | `ram_design_046` | Skill distillation | Content verified; notes refreshed |
| 61 | `ram_slide_047` | From seeded evidence to a skill | Content verified; notes refreshed |
| 62 | `ram_design_048` | Your AuraDB | Visible content + notes synchronized |
| 63 | `ram_code_m5_distill` | Turn hosted experience into a skill file | Visible content + notes synchronized |
| 64 | `ram_design_049` | Seed → distill → fresh agent | Visible content + notes synchronized |
| 65 | `ram_code_m5_agent` | Give the skill to a fresh PydanticAI agent | Visible content + notes synchronized |
| 66 | `ram_design_050` | The governance loop | Visible content + notes synchronized |
| 67 | `ram_slide_051` | The governance loop | Visible content + notes synchronized |
| 68 | `ram_design_052` | Labs / early-access disclosure | Visible content + notes synchronized |
| 69 | `ram_design_053` | Exploration brief | Content verified; notes refreshed |
| 70 | `ram_design_054` | The controlled retrieval scorecard | Content verified; notes refreshed |
| 71 | `ram_design_055` | One knowledge graph | Content verified; notes refreshed |
| 72 | `ram_slide_056` | A connected memory model | Content verified; notes refreshed |
| 73 | `ram_design_057` | Bolt | Visible content + notes synchronized |
| 74 | `ram_slide_058` | Bolt and NAMS consumption models | Visible content + notes synchronized |
| 75 | `ram_design_059` | Your Monday morning path | Visible content + notes synchronized |
