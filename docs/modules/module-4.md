# Module 4 — Execution memory and controlled retrieval

Start at the [full Module 4 agent](../../module_4/app/agent.py). Compare its behavior with the adjacent module using the [code map](../../module_4/README.md). The [app guide](../running-the-app.md) explains replay views, refund authorization and the isolated evaluation.

Terminal 1 at the repository root. Stop the old server with Ctrl+C first.

```bash
make dev MODULE=4
```

Reload the browser on port 5173 and confirm the **Module 4** badge. In terminal 2 run the lesson commands.

```bash
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

## Explore and verify

### Q1: What did the agent actually execute?

Inspect ordered ReasoningSteps and ToolCalls, exact SQL and trace outcome.

### Q2: Did retrieval help?

Compare evidence, business result, tool calls, measured tokens and timing. Do not infer benefit from different prose.

One archived November 1 run offers a comparison when the live measurement is unavailable. On the first ticket, control and treatment each called `issue_refund` once and returned `issued`. They started with equal input SQL hashes. Control used 2,712 input tokens and 31.470 seconds. Treatment used 3,456 input tokens and 33.589 seconds. For that ticket the business action matched and treatment consumed more context. Compare your own rows separately. [Archived output](../reviews/2026-11-01-workshop-fixes/command-09.log).

### Q3: What does failure mean?

A declined business request may have a successful execution. A model/dependency exception has execution_status failed. Inspect both fields and warnings.

### Q4: How do provenance links differ?

`MENTIONS` links message to entity. `INITIATED_BY` links trace to initiating message. `TOUCHED` links a step to selected-case entities. The recorder computes Customer/Plan references for the case and attaches that same set to the captured calls. To establish what an operation read or changed, inspect its tool output, captured SQL and receipt in **Saved replay**. Trace relationships are visible under **Live memory**.

## Read the code

Start with `module_4/app/agent.py`, then local `tools.py`. Read local `memory.py` and `context.py` for configuration and retrieval. Read `hydrate.py` and `memory_tools.py` for SQL grounding and preferences. Read `reasoning.py` for execution records and `lab/ablation.py` for the comparison corpus.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
