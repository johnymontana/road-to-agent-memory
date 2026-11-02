# Module 4 — Execution memory and controlled retrieval

Start commands from the repository root. Keep `make dev MODULE=4` in one
terminal and run the lesson commands in another. Before switching modules, stop
the server with Ctrl+C, launch the next module, and reload the browser.

Browser chat has a visible conversation ID, New conversation and Resume controls.
It preserves turn history locally across reloads; clearing browser storage removes
that local history. Neo4j memory remains persistent. Terminal commands print their
own dialogue, tools and timing. Use **Refresh graph → Saved replay** to inspect their
immutable output projection; choose **Live memory** for the replay's persisted
Neo4j message/entity/trace links. CLI runs do not append turns to browser chat. Choose Current
conversation for browser evidence, or All stored memory deliberately.

Refund actions require a selected Customer and Billing case plus **Authorize selected
refund for this message**. Confirmation resets after each turn. The server checks
case identity, amount, current SQL plan limit and incident uniqueness. Asking for
an update reads refund history. A request ID returns its saved operation receipt on
retry; replaying a billing case cannot create a second refund. No escalation tool
exists. Status values are seeded examples with timestamps, never a live monitoring feed.

Run `make eval MODULE=4` explicitly. The evaluation lab starts only on POST/action;
opening or reopening it reads results. Each run uses private SQL, unique memory
fixtures and disabled business tools. Exact facts and source IDs are checked. This
is a controlled retrieval probe, not an end-to-end support-quality score or a promise
of monotonic improvement. A dependency error preserves completed questions.

```bash
make dev MODULE=4
# Second terminal:
make s4-refund
make s4-fail
make s4-refund-repeat
make eval MODULE=4
```

A trace opens before execution and completes on success or exception. It retains
the exact reply and distinguishes execution status from business status. The
server's reject-only policy guard guarantees an inspectable over-limit fixture;
it cannot issue a refund. Actual model tool order may differ from illustrative chains.

The graph uses ReasoningTrace → HAS_STEP → ReasoningStep → USES_TOOL → ToolCall
→ INSTANCE_OF → Tool. Outcome, reply and success are trace properties. INITIATED_BY
links the trace to its source message; TOUCHED links steps to case Customer and Plan.
Tool receipts contain actual executed SQL: a rejection has no refund INSERT.
These are execution records, not hidden model thoughts.

Retrieval loads bounded full steps, tool inputs/results and exact outcomes with source
IDs. Executions are examples, not instructions or current policy. Current SQL guards
apply with retrieval both off and on.

The ablation seeds one fixed reasoning corpus. Control/treatment use identical
private SQL copies, separate message namespaces, and disabled branch trace recording.
Entity extraction is disabled in both branches, so globally resolved entities
cannot transfer state from the control. The corpus cannot learn from the control. The second question explicitly concerns
Pro, carries no refund authorization, and cannot inherit Dana's Enterprise plan.
The artifact records input hashes, retrieved evidence, tools, tokens and timing.
Identical behavior is a valid result; fewer calls or tokens are not guaranteed.

See the [participant guide](../docs/modules/module-4.md) for the same questions and answer key.

## Explore and verify

### Q1: What did the agent actually execute?

Inspect ordered ReasoningSteps and ToolCalls, exact SQL and trace outcome.

### Q2: Did retrieval help?

Compare evidence, business result, tool calls, measured tokens and timing. Do not infer benefit from different prose.

### Q3: What does failure mean?

A declined business request may have a successful execution. A model/dependency exception has execution_status failed. Inspect both fields and warnings.

### Q4: How do provenance links differ?

MENTIONS is source text about an entity. TOUCHED records case dependencies; INITIATED_BY identifies the initiating user message.

## Read the code

Start with `module_4/app/agent.py`, then local `tools.py`. Read local `memory.py` and `context.py` for configuration and retrieval. Read `hydrate.py` and `memory_tools.py` for SQL grounding and preferences. Read `reasoning.py` and `ablation.py` for execution records and comparison fixtures.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
