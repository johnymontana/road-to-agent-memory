# Workshop review fixes — modules 0–4

Implementation follow-up to [the review](workshop-review-2026-11-01.md), baseline
`3f4837f`. NAMS slides, hosted lifecycle and module-5 lesson content remain outside
this review. Module 5 receives compatible duplicated support-agent/SQL safety fixes.

The fixes retain complete agent implementations in each module. SQLite remains
business authority; Neo4j stores evidence. Saved output projections and live persisted replay graphs are explicitly separate
viewer choices, so provenance walks use actual Neo4j links. Native Google Slides were edited in place,
including presenter notes, without rasterizing narrative or diagrams. The existing
brand colors, typography, icons and native layouts are preserved.

## Resolution map

| ID | Implementation | Verification |
| --- | --- | --- |
| R01 | `lib/graph.py` uses explicit Cypher maps, temporal normalization, endpoint IDs and recursive vector removal. | Populated live FastAPI route checks for every layer in `tests/test_behavioral.py`; map regression in `test_graph_transport.py`. |
| R02 | Vite excludes the NVL layout-worker package, while explicitly optimizing its CommonJS layout dependencies. Graph captions and initial zoom are readable. | Cold Vite Playwright test discovers actual SharedWorker targets and checks their script HTTP 200; live graph screenshots show separated nodes. |
| R03 | Bounded readiness polling, visible Starting/Retry state; launcher announces Ready after both HTTP services respond. | Browser starts with a 503 and recovers without reload; launcher cleanup/failure tests pass. |
| R04 | JSON rubric requires every exact fact and a known source ID; denial/wrong fact/fabricated-source controls fail. | `test_evaluation_contract.py`; partial-run scorer tests. |
| R05 | Per-layer seeded holdouts, unique fixture identity and source IDs; action/lookup tools disabled. Guides distinguish retrieval probes from end-to-end quality. | Live module scorecards and fixture/tool-allowance tests; no promised green progression. |
| R06 | Explicit POST evaluation start, separate GET status; temporary SQLite copy, unique memory and no business tools. | Private SQL hash and factory-option tests; browser opening the lab issues no POST. |
| R07 | Positive finite amounts, confirmed billing-case identity/amount, SQL unique incident constraint, saved request receipts. | Numeric/idempotency tests; live repeated request leaves exactly one refund. |
| R08 | Identical private SQL branch copies, separate message namespaces, fixed reasoning corpus, branch recording and new entity extraction disabled in both branches. | Live artifact records equal input hashes, frozen trace ID and both branches; runner tests. |
| R09 | Trace opens before execution and completes on exceptions; execution and business outcomes are distinct. Reject-only server guard guarantees a declined-case fixture. | Live model-error/hydration-error injection and rejected-case replay; offline both-module trace checks. |
| R10 | Preserve exact reply and structured outcome; retrieve full bounded steps, arguments, results and SQL. | Live retrieval asserts actual reply and executed_sql in retrieved examples. |
| R11 | Explicit `link_trace_to_message`, touched case Customer/Plan references; correct ReasoningStep and trace-property terminology. | Live graph requires INITIATED_BY, TOUCHED, USES_TOOL and INSTANCE_OF. Native trace diagram corrected. |
| R12 | Fixed transcript, independent extractor calls and immutable Saved replay snapshots; no prior chat or hydration. | Transcript hashes and immutable-ID tests; live pair measured separately. |
| R13 | Guides, run sheet, source deck and native slides use explicit MODULE, actual observation surfaces and two-process restart. | Verbatim CLI replay; slide readback and visual inspection. |
| R14 | One self-contained baseline lookup then deliberate per-turn forgetting. | Live module-1 replay; module-1 has no memory client or history injection. |
| R15 | New/Resume controls, canonical session IDs, per-module local history, all-turn execution details. | Browser plain reply retains earlier SQL; reload restores conversation; live screenshots. |
| R16 | Preferences included; bounded newest induced graph, session scope, Saved replay and truncation notice. | Live scoped graph and preference checks; vector/endpoint regression tests. |
| R17 | Preference category/user identity includes namespace and selected Customer; actual stored object/context/dedup receipt. | Live opposing Customer preferences stay separate; actual persisted values asserted. |
| R18 | SQLite trace callback collects executed statements rather than fabricated INSERT constants. | Declined refund has no INSERT; accepted receipt includes validation and write evidence. |
| R19 | Hydrate current-message entities before context/model; distinguish retrieved evidence, hydrated entities and written layers. | Live current-turn Customer grounding; source/type-specific hydration tests. |
| R20 | Typed settings consistently load shell or .env values; explicit local/default/active selection and startup source logging. | Local configuration/lifetime tests; activation instructions state ONTOLOGY=active. |
| R21 | Capture script requires the actual running module, checks health and badge; verified fallback assets are committed. | `artifacts/screenshots/module-[1-4]-live.png` plus source metadata. No module URL spoofing. |
| R22 | Explicit optional Wikimedia workflow caches success/error and exposes provider status; no fictional background enrichment. | Live 403 retained as error; failure-cache test. Core workshop continues. |
| R23 | Executable live graph/action/provenance assertions plus a cold browser CI check; opted-in live credentials fail fast. Historical golden files are labeled schema-only references. | Offline suite, UI check and live regressions; CI runs Playwright and live invariants separately. |
| R24 | Readiness validates SQLite schema/data, configured chat inference, embedding access, memory startup and graph serialization; NAMS checked separately for module 5. | Live `scripts/check_env.py` exits zero after capability checks. |
| R25 | Explicit descending latest-ten query, reverse for chronological context; exclude current message. | Twelve-message live window and per-module context tests. |
| R26 | Explicit validator drop/raise recipe; actual hydrator exercises a private SQL plan upgrade and restoration through one deterministic local writer fixture; catch-up targets documented as replays. | Both instructor recipes executed; participant stores unchanged. |
| R27 | Safe bold formatting, visible composer label, truthful stateless empty state, labeled graph controls and keyboard node details. | Browser formatting/details/reload checks; screenshots. |
| R28 | Hydration requires compatible domain/POLE type and exact nonambiguous identity/aliases. | Wrong Organization/Product type test; alias and rehydration tests. |
| R29 | Context exposes allowlisted structured SQL email/plan/date and IDs; no synthesized account identifiers are authorized. | Live current-turn grounding and account-bound refund guard. |
| R30 | Extractor-only comparison; current-message hydration, one pooled writer, phase progress and timings. | Live pair measured in seconds; full command durations recorded separately. |
| R31 | External status is unknown; Acme statuses are explicitly dated SQL snapshots, not live monitoring. Wikipedia cannot establish health. | Legacy Stripe-row exclusion test; receipt-derived status responses. |
| R32 | Current-message exclusion, deduplicated prior user statements, isolated eval namespaces, grounded employer expansion. | Context regression tests; live cross-conversation recall and scoped Customer evidence. |
| R33 | Model cannot change trusted case identity/amount/plan; explicit Pro policy scope on second ablation turn. Response derives from action receipt/current SQL. | Live wrong-Dana call rejected; ablation policy question performs no refund; SQL hashes equal. |
| R34 | Working `MemoryClient(MemorySettings(...))` recipe with pinned extras, unique message and explicitly scoped retrieval. Native closing slide corrected. | Fresh `uv sync --frozen --no-dev` environment connects, writes and retrieves the unique phrase. |
| R35 | Pooled bounded hydration writes; per-question atomic eval saves, warnings, request receipts and SQL idempotency. Partial replay failures persist and exit nonzero. | Model/hydration fault injection, partial-result tests, explicit eval recovery and live retry checks. |

## Validation evidence

The [fix replay folder](reviews/2026-11-01-workshop-fixes/) records measured command
results, evaluator reports, SQL ledger, slide audit and test summaries. Historic
review evidence remains in its original folder; it describes the pre-fix failures.
The replay completed all 15 commands with zero exits in 17m 03s cumulative runtime.
The fixed extraction pair took 4.31s + 5.07s. Controlled retrieval scores were
**0/4 → 2/4 → 3/4 → 4/4**, with expected source holdouts: messages, then grounded
Customer facts, then exact prior trace reply. These are measured fixture results,
not a guarantee of general task quality.

Both ablation branches issued only Dana's confirmed $129 refund in private copies;
the separate Pro policy question returned the current $250 limit and performed no
action. Tool counts were the same in control and treatment. The final measurement
also disables entity extraction/hydration to prevent global canonical-entity
sharing. Both initial SQL hashes match. A direct persisted-graph audit confirms zero new entity
mentions and zero branch traces, with exactly one trace in the frozen corpus. The
original rehearsal ledger contains only Maya's approved $49 refund; sandboxed
evaluations and ablation branches did not add participant-ledger writes.

Final checks: **122 offline tests passed**, **4 live non-NAMS regression tests passed**,
and the separately opted-in browser test passed; lint, dependency-lock validation and the frontend production build passed.
The build retains its bundle-size advisory; the pinned dependency emits a Pydantic
deprecation warning. Neither was treated as proof of runtime failure. The fresh
locked environment successfully ran the scoped Monday-memory recipe.

The [two-axis final review](reviews/2026-11-01-workshop-fixes/final-review.md)
reports no outstanding findings after the remedies. The native deck retains
59 slides; 30 visual slides and 49 non-NAMS presenter-note entries were corrected.
Readback confirmed NAMS slide content and notes unchanged. Thumbnails were used
for visual QA because the connector's PDF export was not materialized locally.

The optional Wikimedia request returned HTTP 403 during rehearsal. This is a handled
external limitation, not a successful enrichment result. No NAMS endpoint was run.
Fresh Codespaces provisioning and classroom concurrency are not claimed by these checks.
