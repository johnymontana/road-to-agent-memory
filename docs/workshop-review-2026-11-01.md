# Workshop review and live replay — modules 0–4

Implementation follow-up: [fix status and evidence](workshop-fixes-2026-11-01.md).

Review date: 2026-11-01. Repository baseline: `3f4837f` (`refactor module implementations`).
NAMS, module 5, distillation, drift, and the fresh skill agent are excluded.

## Assessment

**The agent checkpoints are useful teaching material, but the workshop is not ready
for the advertised graph-led delivery.** The live browser cannot render memory from
the actual graph endpoint. The evaluator can pass incorrect answers, changes business
state, and does not isolate the capabilities attributed to each memory layer.
The completed ablation treatment also issued a $400 refund to the wrong fictional
account and described it as a successful Pro-account refund. That is a correctness
failure, not a demonstrated benefit of memory.

Preserve the module-local agent architecture, the fictional support domain, and the
separation between SQLite business facts and Neo4j memory. Fix the observable demo
contract before adding more content. Successful CLI exit codes and passing agent
tests are insufficient evidence that the participant exercises work.

This is a feedback deliverable: runtime code, scenarios, slides, and existing guides
were not changed during this review. Suggested fixes below remain proposed work.

## What was exercised

- Reviewed the outline, run sheet, slides, prework/teardown, module 0–4 guides and
  reading maps, ADRs, agents, tools, hydration, memory setup, HTTP transport, frontend,
  evaluation/scenario runners, container setup, CI, and existing test coverage.
- Read the linked native Google Slides outline through the connected Drive plugin,
  revision `QDmoL4ElpcYHAA`, covering slides 1–45 and general closing items on
  slides 54–56 and 59. This was a content consistency audit, not a new rendered-layout
  or branding review. NAMS-specific sections and claims were excluded.
- Replayed actual Make targets against configured OpenAI and Neo4j. A review-only
  Python startup hook prefixed conversation IDs and recorded responses, tool calls,
  timing and trace retrieval. It did not replace the model or business tools.
- Used a separately seeded temporary SQLite database. Existing participant SQLite
  data was not reseeded. Existing Neo4j data was not cleared; prefixed conversations
  separate writes, **but do not isolate retrieval from the populated graph**.
- Booted actual module 1, 2 and 3 servers with `make dev MODULE=N`, and used local
  Chromium for desktop/mobile, chat, eval, graph errors and cold-start checks.
- A separate, clearly synthetic two-node graph probe isolated frontend rendering
  from the broken live endpoint. It is not evidence of a working live memory graph.
- Ran offline tests, repository lint and the frontend production build. Fresh
  Codespaces provisioning, container creation, classroom concurrency and billing
  totals were not measured. No NAMS endpoint was invoked.

Evidence is in
[the replay folder](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay).
The earlier [module evaluation](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/module-evaluation.md)
tested agent behavior; this broader review additionally tested participant-facing
claims and the real frontend/backend seam.

## Replay results

| Command | Time | Exit | Observed result |
| --- | ---: | ---: | --- |
| `make check` | 0:04.4 | 0 | Basic readiness passed; populated graph capability was not checked. |
| `make s1-baseline` | 0:18.3 | 0 | Per-turn forgetting reproduced; ticket details did not accumulate. |
| `make eval MODULE=1` | 0:09.9 | 0 | 0/4; prime also issued a $49 refund. |
| `make s2-return` | 1:35.2 | 0 | Same-conversation recall worked; refund issued. |
| `make s2-restart` | 2:11.0 | 0 | In-process client recreation; update caused another refund. |
| `make eval MODULE=2` | 1:40.9 | 0 | 4/4, including later-stage questions; q3 used account SQL. |
| `make s3-default` | 4:53.4 | 0 | Hydration still ran; mixed/previous graph labels and type mismatch. |
| `make s3-ontology` | 6:14.6 | 0 | Custom extraction ran; invented Ravi email used for lookup. |
| `make s3-enrich` | 1:14.3 | 0 | Wikimedia 403; no business tools; unsupported Stripe status claim. |
| `make eval MODULE=3` | 4:53.4 | 0 | 1/4; repeated questions crowded out useful identity evidence. |
| `make s4-refund` | 1:44.0 | 0 | Refund issued with one tool call; no explicit policy-fetch observation. |
| `make s4-fail` | 1:31.9 | 0 | $400 rejected by tool against Pro $250 limit. |
| `make s4-refund-repeat` | 5:32.8 | 0 | Shared-state comparison; duplicate $129 and wrong-account $400 refund. |
| `make eval MODULE=4` | 5:53.2 | 2 | q4 hydration routing failure; no final scorecard. |

**Totals:** 13/14 commands exited zero; 37:57.2 cumulative command runtime; 48 chat turns returned and 1 aborted. These counts exclude the additional browser and offline diagnostic probes.

The three completed CLI scorecards were **0/4 → 4/4 → 1/4** for modules 1–3. Module 4 failed before printing its scorecard. The all-denial negative control separately scored **4/4**. These are observations of the current scorer, not validated capability grades.

**Verification:** 68 existing offline tests passed. The production frontend build passed with a bundle-size advisory. Repository-wide Ruff still reports four pre-existing E501 violations in `slides/diagrams/generate_svgs.py` at lines 169, 236, 256 and 257; wrap those lines to restore the static CI check.

All scenario/check/eval commands used real services and temporary SQL data. A zero exit status means the script finished; it does not establish the learning outcome, safe action selection or a functioning graph UI. The final error is preserved in the evidence. A subsequent bounded read succeeded, and the q4 assistant reply was already stored in Neo4j; the application failed after that partial completion. The underlying routing cause was not isolated.

## Priority findings and proposed fixes

Severity: **P0** blocks the central workshop activity; **P1** should be fixed before
delivery; **P2** improves correctness, clarity or reliability; **P3** is polish.
“Live” means observed during this review; “source” means confirmed from the code or
materials, with an explicit acceptance check proposed rather than a claimed replay.

### R01 — P0 — The real memory graph endpoint crashes

**Evidence: live and source.** Module 2 `/api/health` returned 200 while every graph
filter (`all`, `short_term`, `long_term`, `reasoning`) returned 500. The server failed
with `AttributeError: 'dict' object has no attribute 'element_id'` at
[graph.py:44](/Users/lyonwj/github/johnymontana/road-to-agent-memory/lib/graph.py:44).
The installed query API uses `result.data()`, which returns dictionaries rather than
driver node/relationship objects. This shared mapper serves modules 2–4.

**Impact:** participants cannot follow message chains, inspect hydration, compare
ontologies or reconstruct a trace. “Health OK” is misleading for this workshop.

**Fix:** return explicit node/relationship maps from Cypher using `elementId`,
`labels`, `properties`, `startNode` and `endNode`; handle null relationships and
normalize temporal values. Strip every vector property, including task embeddings.
Avoid depending on driver-object methods after serialization.

**Acceptance:** seed one conversation, one hydrated entity and one trace, then assert
HTTP 200, valid endpoint IDs, JSON-safe properties and visible connected nodes for
all filters through the actual FastAPI route. Add a browser graph smoke test.

### R02 — P1 — Development graph layout workers are missing

**Evidence: live.** Vite logged missing `HierarchicalLayout.worker.js` and
`CoseBilkentLayout.worker.js` under its optimized dependency directory; direct
requests returned 404. The same 404s persisted after forcing Vite dependency
optimization. In the synthetic probe, canvases existed but the graph did
not produce a useful separated layout. The production build still succeeded.
See [worker HTTP evidence](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/worker-http.json).

**Fix:** adjust NVL worker/dependency handling in
[vite.config.js](/Users/lyonwj/github/johnymontana/road-to-agent-memory/web/vite.config.js)
against the installed package, starting with optimizer exclusions for packages that
construct worker URLs. Do not assume the production build validates `make dev`.

**Acceptance:** from a cold Vite cache, render a connected three-node graph; verify
worker requests succeed, node positions separate, and pan/zoom/drag/node details work.

### R03 — P1 — Cold-start errors do not recover

**Evidence: live.** Opened the UI during module 3 startup. After the backend returned
healthy module 3 metadata, the page still had no module badge and retained its
“Could not reach backend” error. The health effect in
[App.jsx:17](/Users/lyonwj/github/johnymontana/road-to-agent-memory/web/src/App.jsx:17)
runs once. This is particularly relevant when Codespaces auto-opens port 5173.

**Fix:** show an explicit starting state, poll readiness with bounded backoff, offer
Retry, and avoid reporting an expected startup delay as a configuration failure.
Have the launcher print a ready URL only when both services are usable.

**Acceptance:** open the frontend before backend readiness and verify automatic
recovery, badges and graph refresh without a manual reload.

### R04 — P1 — The scorecard accepts denials as correct answers

**Evidence: executable negative control.** Using the actual `run_eval` scorer, four
denials scored **4/4**: “I do not know Maya or her email,” “I cannot remember whether
we discussed Compute,” “I do not know your signup date,” and “I cannot issue an answer
because I do not remember that conversation.”
[The scorer](/Users/lyonwj/github/johnymontana/road-to-agent-memory/scripts/eval.py:68)
checks whether any substring appears, without checking correctness or negation.

**Fix:** assert concrete facts and provenance, separate refusal/unknown from correct,
and require all requested fields. For example, q1 needs the correct name **and**
email; q3 needs the seeded date; q4 needs a real recorded decision with its source.
Use an explicit rubric if model judging is needed, with negative controls.

**Acceptance:** all four denial controls fail; deliberately wrong names/dates fail;
correct answers pass; the displayed evidence explains each result.

### R05 — P1 — Eval does not prove the layer progression

**Evidence: live and source.** Module 2 already scored **4/4**, including the questions
advertised as requiring modules 3 and 4. Its q3 answer used `lookup_account`, whose
SQL already returns `signup_date` in module 1. q4 can be answered from message
retrieval, policy knowledge or unsupported generalization. Existing graph data adds
another confound. Module 3 is not the first possible cross-session recall layer.
In this replay module 3 then scored **1/4**, failing identity/account questions.
This is an observed demo-stability problem, not evidence that the third layer is
inherently worse: the models, retrieval contents and prior state are uncontrolled.
Also make the customer question unambiguous: both Maya and Ravi work at Northwind.

**Fix:** distinguish demonstration questions from capability tests. Use uniquely
seeded facts and holdouts, controlled memory sources, expected provenance, and
explicit tool allowances. Replace “the score proves each layer landed” with an
observable explanation of what each layer added.

**Acceptance:** demonstrate why each control cannot answer a question and why the
treatment can, using the retrieved evidence rather than a green keyword badge.

### R06 — P1 — “Run Eval” performs business writes

**Evidence: live.** The prime message in
[eval.py:16](/Users/lyonwj/github/johnymontana/road-to-agent-memory/scripts/eval.py:16)
triggered `issue_refund` in both modules 1 and 2. Clicking the UI’s Run Eval executes
the same workflow through a GET endpoint. Reopening it can issue another refund and
add more memory; it is not a read-only score display.

**Fix:** make evaluation a named sandboxed operation, isolate its SQL/memory fixtures,
or remove write tools from the evaluation agent. Expose a POST run action and a
separate GET results endpoint. Tell participants what will run before execution.

**Acceptance:** repeated evals leave participant business data unchanged and produce
separately identifiable results. Canceling/reopening the modal does not launch an
untracked duplicate run.

### R07 — P1 — Refund replay is not idempotent; numeric validation is incomplete

**Evidence: live and direct tool probe.** During `s2-restart`, a follow-up asking for
an update caused another $49 refund. A temporary-DB probe also accepted a **-$49**
refund, and issued two refunds for the same repeated incident. The helper only
checks whether `amount > limit` in
[db.py](/Users/lyonwj/github/johnymontana/road-to-agent-memory/lib/db.py:93).

**Fix:** validate finite positive amounts and attach an incident/payment identifier
with a uniqueness constraint. Add a read-only refund-status tool, or return refund history from the account tool,
so “any update?”
has a safe action. Preserve tool-side policy enforcement in every module.

**Acceptance:** repeated scenario execution for one charge yields one refund; status
questions never issue another; zero, negative and non-finite amounts are rejected
with structured errors. Tests must exercise the real SQL helper.

### R33 — P1 — Treatment issues the refund to the wrong account

**Evidence: live, temporary SQLite only.** The second ablation question concerns an
ops lead's separate **Pro** account and a $400 request. Treatment called
`issue_refund(customer_email="dana.w@contoso.example", amount=400)` and received
`customer="Dana Whitfield", plan="Enterprise", status="issued"`. Its reply then
claimed the ops lead's Pro refund had been issued. The plan guard accepted Dana's
$500 limit; it did not validate that Dana was the intended customer. See
[the full ablation case](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/ablation-case.json).

**Fix:** bind each action to an explicitly resolved, confirmed account and incident.
A new third-party subject cannot inherit the previous speaker's account. Missing
ops-lead identity must produce a clarification or an explanation of the Pro approval
path, not a write against Dana. Distinguish a request to explain a process from
authorization to execute it. Keep the policy/account checks at the tool boundary.

**Acceptance:** the mixed-account conversation never inserts a refund for Dana on
behalf of the ops lead; the Pro $250 approval threshold is applied to the stated
subject; an unidentified account cannot be refunded. The recorded outcome must not
label a wrong-subject action as a successful learning example.

### R08 — P1 — The retrieval ablation changes more than retrieval

**Evidence: source and live retrieval instrumentation.**
[run_scenario.py:81](/Users/lyonwj/github/johnymontana/road-to-agent-memory/scripts/run_scenario.py:81)
runs control then treatment with the same conversation IDs, shared SQLite and shared
memory. Control writes messages, refunds and traces that treatment can then see.
Turning off reasoning retrieval does not turn off cross-session message recall.
In this replay, treatment's first reasoning retrieval returned the just-created
control trace at similarity **1.0**, from the same `s4-c` conversation.

The control also answered the ops lead's **Pro** account question using Dana's
**Enterprise** limit: “Since you're on the Enterprise plan ... $500 ... allows me
to issue the $400 refund ... without needing additional approval.” No $400 write
occurred in that turn, but the policy advice addressed the wrong account.

**Fix:** use independent but equivalent session/SQL fixtures and the same fixed
pre-existing reasoning corpus; freeze recording during measurement or keep both
branches' new traces out of retrieval. Capture selected trace IDs, tools, token use,
latency, business outcome and policy validity. Do not promise fewer steps/tokens.

**Acceptance:** treatment cannot retrieve its control's writes; the only intended
input difference is reasoning context. Reversing run order does not reverse the
apparent benefit. Both branches still validate current policy.
The mixed-account regression must apply the Pro $250 limit regardless of the
previous speaker's Enterprise plan; memory retrieval cannot be the only protection
against applying policy to the wrong subject.
The completed treatment did worse than the control's incorrect advice: it actually
issued the wrong-account refund described in R33. Both branches also issued the
same $129 refund, producing two records for the repeated billing issue.

### R09 — P1 — “Failure is memory” needs a reliable failure definition

**Evidence: source.** The natural-language `s4-fail` request may be refused before
`issue_refund` runs. The agent marks failure only when a collected tool output starts
with `rejected`; an unfulfilled refund declined in prose is marked successful.
The earlier live test explicitly forced this branch with `FunctionModel`, which
validates the mechanism but does not guarantee the canned live scenario.
This replay did produce a real `rejected_over_limit` response for the $400 request;
that successful demonstration should be preserved without assuming it is guaranteed.
The reply also promised escalation, although no approval/escalation action exists.
An additional offline fault injection made `agent.run` raise; the real ChatService
recorded **zero traces**. Recording only happens after the run and hydration return.

**Fix:** distinguish execution success, policy-compliant handling and the requested
business outcome. Keep a deterministic rejected-tool fixture for teaching the guard;
show a real-model refusal as another valid handling path. Do not depend on inducing
an unsafe attempt to make the red trace appear.
Open the trace before execution and complete it on success or exception. Explain
the approval path without claiming an escalation was performed unless a tool did it.

**Acceptance:** both a tool rejection and a pre-tool refusal are recorded with clear,
different statuses. The room can always inspect a known failed business outcome.
An actual execution exception also leaves a completed error trace with its cause.

### R10 — P1 — The recorded trace is richer than the retrieved procedure

**Evidence: source.** Module 4 records tool calls, but the prompt receives only task,
success and a generic outcome. The code then overwrites the recorder's answer with
“Replied to customer (N tool calls)” or a rejection summary at
[agent.py:129](/Users/lyonwj/github/johnymontana/road-to-agent-memory/module_4/app/agent.py:129).
This does not retrieve the actual tool sequence, policy observation or exact prior
reply promised by the procedure-recall story and q4.
In the live `s4-refund` replay the model called only `issue_refund`, not the advertised
three-tool chain. Its SQL guard still checked the plan limit, but there is no
separate `fetch_policy` observation to inspect in that trace.

**Fix:** preserve the final reply and business outcome; retrieve bounded relevant
steps/tool observations using the installed `get_trace_with_steps` API. Include IDs
and provenance, and treat retrieved executions as examples rather than authority.

**Acceptance:** the retrieved example contains the earlier procedure and policy
evidence, and an exact-quote question can be checked against a stored assistant reply.

### R11 — P1 — The advertised provenance walk is not implemented

**Evidence: source.** The adapter does not pass entity references to materialize
`:TOUCHED` edges, and the module does not call `link_trace_to_message`. Success and
outcome are trace properties, not a separate outcome node. The slides still say
`AgentStep`, and the module 4 answer key promises an edge-by-edge walk to the user's
message. The committed m4 golden lists no `TOUCHED` relationship. A live audit of
all six replay scenario traces confirmed zero `TOUCHED` destinations and zero
`INITIATED_BY` message links.

**Fix:** retain the returned user message ID and call
`reasoning.link_trace_to_message`; pass explicit entity references when recording
tool calls if dependence edges are taught. Align node names/outcomes in the guide,
slides and graph. Describe this as an execution trace, not exposed model thoughts.

**Acceptance:** a query follows trace → initiating message and step → relevant entity
for the lesson fixture, or remove those exercises and teach the graph that exists.

### R12 — P1 — The ontology comparison reuses accumulating state

**Evidence: source.** Default/custom runs load the same JSON scenario name and reuse
the same conversation IDs. Both write into one graph; the default run still uses the
module 3 memory tools, hydration, and previously stored entities. The “before” can
already contain custom labels/relationships, and the custom run gets previous text
as context. A change in ontology is not the only input difference.

**Fix:** compare immutable run-scoped subgraphs from equivalent clean fixtures,
preferably one fixed transcript through extraction before the open-ended chat demo.
Show expected invariants rather than claiming identical graphs at temperature zero.

**Acceptance:** repeat custom then default and default then custom; the comparison
remains interpretable and shows only each run's extraction results and provenance.

### R13 — P1 — The run sheet contradicts the actual participant workflow

**Evidence: docs and live UI.** It asks attendees to watch terminal scenarios in the
browser trace panel, claims `s2-return` creates a new chat, calls the in-process
restart a killed backend, and uses bare `make eval` at later checkpoints. Bare eval
defaults to module 1 regardless of the running server. The root README is clearer
than the instructor’s detailed minute-by-minute instructions.

**Fix:** choose one demo surface and rewrite every corresponding run-sheet row and
slide note. Use `make eval MODULE=N` everywhere. Say “same conversation” and “client
recreation” unless adding a true process restart. Include the necessary graph refresh.
Remove the module 0 “streaming reply” claim and module 2 claim that the app labels
the search path: the current app exposes synchronous responses and layer summaries.

**Acceptance:** a new facilitator can follow the run sheet verbatim, and the named
screen, module, session and restart event match what the room sees.

## Native Google Slides content corrections

The current [native deck](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8/edit)
still carries several claims already corrected in the module reading maps. Apply
these changes alongside R13, then read back the deck and guides together. The saved
outline identifies stable slide object IDs as well as slide numbers.

| Slides | Correction |
| --- | --- |
| 16, 23–24 | Terminal playback does not populate the browser trace; `s2-return` continues the same conversation; `s2-restart` recreates clients in-process. Use the real observation surface and restart description. |
| 21 | Reflections and observations are presented as Bolt context tiers. They are not part of this verified Bolt lesson; teach recent conversation and semantic message retrieval instead. The module 2 guide already states the backend distinction. |
| 23 and later eval prompts | Replace bare `make eval` with the correct `MODULE=N`; do not imply the server selects the CLI stage. |
| 27 | Replace deleted `ontology/acme_cloud.yaml` with `module_3/ontology/acme_cloud.yaml`. |
| 29–30 | Remove “only the ontology changes” until state and transcript inputs are isolated. Default runs also receive hydration; “bare properties” is inaccurate. |
| 32, 35–36 | Customer nodes are SQL-hydrated; the configured enrichment allowlist is Organization-only. The provider returned 403, and no prewarming/caching workflow was found. No SQLite Incident/severity hydration exists despite the severity example on slide 36. |
| 37 | Exploration numbering does not match the current guide: Customer properties is Q3, change since module 2 is Q4, negative cases is Q5, strict mode is Q6, and plan-upgrade hydration is Q7. Link stable question anchors and the actual participant guide. |
| 38–40, 44–45 | Correct `AgentStep` to `ReasoningStep`, outcome-node claims to trace properties, and `TOUCHED`/message-edge exercises to what is actually recorded. Real execution exceptions currently leave no trace. |
| 41–43 | Do not promise a particular three-tool chain or a visible behavioral benefit from retrieval. Show the recorded run and controlled retrieval evidence, with current-policy validation in both branches. |
| 54–56 | Apply the corrected eval command and layer explanations to the wrap. General connected-graph claims also depend on implementing the missing provenance links. |
| 59 | `MemoryClient(backend="bolt")` raises `TypeError` with the pinned release. Use a configured `MemorySettings` object, matching dependency extras and a tested copy/paste recipe (R34). |

## Additional improvements

| ID / priority | Finding and suggested change | Concrete verification |
| --- | --- | --- |
| R14 / P2 | Module 1 forgets on every `agent.run`, even within the same visible chat. Its six-turn billing scenario cannot accumulate the supplied details. Either keep an in-process history to isolate persistence as the new lesson, or explicitly teach a per-turn stateless baseline and use self-contained prompts. | The email/account/billing sequence produces the intentionally documented behavior; no accidental guessed email is passed to the account tool. |
| R15 / P2 | The UI has no New Chat, session identifier or resume control; browser reload loses React state. It replaces the trace with the latest turn, so a no-tool answer erases the previous SQL evidence. Add explicit session controls and a turn-indexed trace history. | Start/return/resume are distinct visible actions; an earlier tool call remains inspectable after a plain-text response. |
| R16 / P2 | The graph mapper omits `Preference` from both long-term and all-layer label sets; its unordered 500-row limit can hide recent lesson data. Add preference support, session/run filtering, latest-run focus and an explicit truncation indicator. | A newly saved preference and current conversation appear predictably even after many replay runs. |
| R17 / P2 | Preference storage/search is workspace-wide and not bound to a Customer. `save_preference` ignores the returned object and can claim it saved details even when deduplication reused an older preference. Preserve actual stored results, show deduplication and context, and teach explicit customer scope. | Two fictional customers with opposite contact preferences retrieve their own choice; repeated writes report what actually persisted. |
| R18 / P2 | The refund trace always displays the INSERT SQL constant, even when the guard only executed a SELECT and rejected the write. Record actual executed statements/results, including policy/account reads. | A rejected refund shows no executed INSERT; an accepted refund shows both validation and write evidence. |
| R19 / P2 | Hydration runs after the answer, so newly extracted user entities cannot supply their new SQL facts to that answer. Memory `summary` then counts those writes as “used” and labels mixed retrieved context short-term. Hydrate before context assembly where current-turn facts are needed; report retrieved, written and hydrated layers separately. | A newly introduced customer can use grounded facts in the intended turn, and memory indicators do not claim post-answer writes caused an answer. |
| R20 / P2 | The activation script says restarting module 3 picks up the active ontology, but the module defaults to loading a local YAML override. `ONTOLOGY` and the reasoning toggle are read with `os.environ`, unlike `.env` settings. Print the resolved source and document `ONTOLOGY=active`; make environment-file behavior consistent. | Active/local/default selection is visible and changes exactly as documented after restart. |
| R21 / P1 | Screenshot capture visits `?module=N`, but the frontend ignores that query. In the live probe, `?module=4` still displayed Module 3. No promised screenshots or pre-warmed Stripe assets were found under `artifacts/`. Boot each backend and assert health before capture; ship verified fallbacks. | Each screenshot’s badge, data and filename agree; fallback assets exist and contain actual lesson evidence. |
| R22 / P2 | Wikimedia returned 403, not merely a short async wait. Prewarming/caching is not implemented by the container setup. Keep enrichment optional and show provider status or a clearly labeled stored example. | The exercise remains useful without Wikipedia, and no waiting narration promises imminent properties after a hard provider error. |
| R23 / P1 | Green tests miss the delivery seam: golden tests validate JSON shape, not graph invariants; agent tests omit populated real graph mapping. Add live HTTP/browser checks and executable assertions for the exact scenario learning outcomes. | CI catches R01/R02 and a naturally refused `s4-fail`; changing a fixture label or removing a required edge fails the relevant check. An opted-in live CI job must run its expected checks rather than pass through missing-credential skips. |
| R24 / P2 | `make check` verifies database existence, connectivity and OpenAI model-list auth, but not SQLite schema/content, selected-model inference, embedding access, memory startup or graph serialization. Add fast capability checks and separate required/optional service status. | A present-but-empty SQLite file, inaccessible model or broken graph mapper cannot produce an all-ready workshop verdict. |
| R25 / P2 | Installed short-term context fetches conversation messages ascending with a limit, then slices that already-limited list. This can preserve the first ten messages rather than the latest ten. Validate the dependency behavior and explicitly request/assemble the intended window. | A 12-message fixture includes the newest turn and excludes the oldest as specified; restart does not change the window. |
| R26 / P2 | Instructor exercises lack repeatable recipes for strict mode, plan upgrades and rollback. Catch-up targets replay selected beats; they do not restore a checkpoint. Add short instructor scripts, expected output and recovery steps instead of “never type live” promises. | A helper can perform and undo each demo using only the guide, without clearing participant data. |
| R27 / P3 | Chat renders Markdown literally (visible `**Pro**`), graph empty-state text promises memory creation even in module 1, and the composer relies on placeholder text. Improve message rendering, stage-aware empty states and visible labels; audit keyboard graph interaction. Mobile width itself passed at 390 px. | Test formatted replies, keyboard navigation, labeled graph controls and a truthful module 1 empty state. |
| R28 / P2 | The replay snapshot contains `Acme Cloud Compute` as both an Object and an Organization; both received `sqlite:products` facts because hydration matches names without checking type compatibility. Validate the entity's domain/POLE type before hydrating, and surface incompatible extraction separately. | A misclassified Organization does not receive Product facts; the correctly typed Product still hydrates. |
| R29 / P1 | Grounded fields are stored but not all exposed to the agent. Customer email is a flat property, while local memory search and the installed context formatter emit only name/description. The Ravi turn retrieved his grounded description without email, then business tools were called with the invented `ravi.shah@northwindrobotics.com`. Return allowlisted structured facts and provenance; do not synthesize account identifiers from names. | With email absent from the conversation but hydrated from SQLite, returning-customer lookup uses the exact grounded email. No invented email reaches an action tool. |
| R30 / P1 | The default/custom ontology pair took 293 + 375 seconds (11m 8s), before inspection. Both runs cannot fit the run sheet's eight-minute comparison slot with inspection. Reduce the core transcript, profile extraction/context/hydration separately, and add phase progress. Hydration currently revisits the entire session and creates a new driver per entity write. | Measure a full pair including startup/shutdown against the allocated slot, leave time for interpretation, and verify any optimization preserves the same grounded facts. |
| R31 / P1 | The enrichment reply claimed Stripe and Billing API were operational despite making no tool calls. The repository has no live Stripe-status source; Wikipedia company enrichment cannot establish service health. Change the stretch prompt to public organization facts, and require verified source data or an explicit unknown for operational status. | The Stripe-status question never receives an unsupported current-status assertion; known Acme statuses remain backed by the status tool. |
| R32 / P1 | Module 3's failed identity lookup retrieved five copies of the question itself and two Organization descriptions, rather than customer evidence. Search does not traverse the organization-to-customer relationship, and repeated evals pollute its top results. Exclude the current message, deduplicate/diversify candidates, isolate eval memory, and add a narrow grounded relationship lookup when the question requires it. | Repeating eval does not crowd out useful facts; an organization lookup returns the relevant Customer evidence or asks which person when multiple customers match. |
| R34 / P1 | The closing native slide’s `MemoryClient(backend="bolt")` fails immediately with an unexpected-keyword `TypeError` in the installed release. Replace it with the actual `MemoryClient(settings)` pattern, include the verified extras/credential setup, and test the complete Monday-morning recipe in a fresh environment. | The published example imports, constructs, connects, writes and retrieves using the same pinned API as the workshop. |
| R35 / P1 | The final module 4 eval aborted on q4 with Neo4j `Unable to retrieve routing information` during post-answer hydration. The entire scorecard was lost after earlier questions and business writes had completed. Reuse pooled connections, retry idempotent hydration with bounds, preserve per-question results/operation status and expose a clear degraded/failure state. Do not blindly rerun write-capable evals. | An injected hydration/routing failure preserves completed results, records the failure and cannot duplicate a refund on retry. A transient dependency error does not erase the whole evaluation's evidence. |

## Suggested delivery changes

Use one deliberate question → observation → explanation loop per stage:

1. **Module 0:** verify capabilities, identify the two stores, boot the app, and wait
   for readiness. Do not promise a fresh Codespace in a fixed number of minutes.
2. **Module 1:** one self-contained ticket, one actual SQL lookup and one explicit
   forgetting control. Explain whether history is absent per turn or per session.
3. **Module 2:** plant a unique phrase, recreate the process/client, and recover it
   in the same named conversation. Then deliberately contrast a new conversation.
4. **Module 3:** inspect one fixed transcript under two ontologies in scoped views;
   trace a Customer back to its source message and verify its signup date against
   SQLite. Add a correctly scoped preference. Keep strict mode and enrichment optional.
5. **Module 4:** inspect a known recorded procedure, compare retrieval inputs under
   controlled conditions, validate policy in both cases, and distinguish a declined
   business request from a failed tool execution. End with a real provenance walk.

If delivering a non-NAMS session, a plausible **130-minute** allocation is setup 15,
baseline 15, conversation memory 20, long-term memory 40, break/buffer 5, execution
memory 30, wrap 5. If retaining the original 150-minute slot, use the remaining
20 minutes for guided inspection and troubleshooting rather than another feature.
Revise this allocation using the measured command times above; automation time is
a lower bound, not a classroom completion estimate.

Replace guaranteed “full board green” and “fewer tokens” endings with a factual
recap: what persisted, what was retrieved, which system supplied each fact, what
action occurred, and what evidence supports the answer.

## Proposed implementation order

1. **Restore the graph experience:** R01–R03, a populated API/browser test, and truthful
   startup/empty states. Verify both development and production delivery.
2. **Make actions and evaluation trustworthy:** R04–R07 and R33, sandboxed eval, read-only
   refund status and idempotent writes, with negative controls and hydration-failure
   handling (R35).
3. **Make the comparisons honest:** R08–R12, isolated replay fixtures, complete
   procedure retrieval, explicit outcomes, actual provenance edges and complete
   grounded-field retrieval (R29) and query-resistant, relationship-aware retrieval
   (R32).
4. **Synchronize the teaching assets:** R13–R22 and R26–R27, real screenshots and
   exact instructor recipes, including type-safe hydration (R28) and measured
   pacing (R30). Correct the closing API recipe (R34) and unsupported status claims
   (R31). Preserve the complete local agent copies.
5. **Rehearse the participant contract:** R23–R25, including cold startup, stage
   transitions, graph exploration, replay reruns, failures and helper recovery.

## Readiness gate for the next rehearsal

- The live graph renders all taught node/edge types, can be navigated, and shows the
  current run without leaking vector arrays into the details drawer.
- The UI recovers from normal startup, supports new/resumed sessions, and retains
  the evidence the facilitator asks attendees to inspect.
- Evaluation cannot mutate participant business data or award passes to denials.
- Default/custom and control/treatment comparisons have equivalent isolated state.
- A refund status question cannot create another refund; rejected business requests
  have an explicit, inspectable outcome.
- A Pro-account request cannot be fulfilled against a different Enterprise account;
  unresolved customer identity prevents the business write.
- Every promised trace/provenance edge and fallback screenshot actually exists.
- A facilitator follows the updated non-NAMS run sheet verbatim without translating
  between terminal output, browser state and a different module’s eval.

This gate covers workshop correctness and delivery. Use observed evidence and
explicit invariants rather than promising identical LLM output across the room.


## Evidence index

The structured replay evidence contains fictional support data and review-prefixed
conversation IDs. Credentials were not exported. Browser eval and CLI replay used
the same temporary SQL store; its ledger includes both. Review servers were stopped.

| Evidence | Use |
| --- | --- |
| [Command results](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/command-results.json) | Exit codes and measured durations for all 14 invocations. |
| [Replay turns](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/replay-turns.json) | Prompts, replies, actual tool inputs/outputs, timing and retrieval mode. |
| [Ablation case](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/ablation-case.json) | Control/treatment action sequence, wrong-account refund and retrieved trace IDs. |
| [Trace audit](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/trace-audit.json) | Six completed scenario traces, one rejected business request, no taught provenance edges. |
| [Temporary refund ledger](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/temporary-refund-ledger.json) | Actual temporary SQLite rows and customer/plan attribution. |
| [Eval negative control](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/eval-negative-control.json) | Four denials all marked correct. |
| [Final eval failure](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/final-eval-failure.json) | Error phase, successful follow-up read, and already-persisted assistant reply. |
| [Graph failure screenshot](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/module-2-live-graph-error.png) | Actual participant-facing populated graph error. |
| [Cold-start screenshot](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/module-3-cold-start.png) | Stale connection error after backend readiness. |
| [Stateless two-turn screenshot](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/module-1-two-turns.png) | Forgetting inside one visible conversation; previous trace disappears. |
| [Native slide content snapshot](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/google-slides-content-outline.json) | Stable slide IDs, text and revision for introduction/modules 0–4. |
| [General closing content](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/google-slides-closing-outline.json) | Closing copy reviewed without assessing NAMS-specific claims. |
| [Environment and versions](/Users/lyonwj/github/johnymontana/road-to-agent-memory/docs/reviews/2026-11-01-workshop-replay/environment.json) | Installed versions and review scope, without service credentials. |

The folder also includes browser observations, both ontology snapshots, the forced
Vite worker probe, refund-boundary and exception probes, scorecard text, and the
review-only instrumentation as `.py.txt` files. Those scripts are an audit record,
not new attendee-facing commands.
