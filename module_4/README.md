# Module 4 — Reasoning memory

**The idea:** remember *how* a ticket was handled, not just what was said.
Every turn is recorded as a `(:ReasoningTrace)`: each tool call becomes a step
with its input, output and executed SQL, and the trace ends with its outcome.
Before answering a new ticket, the agent retrieves past executions of similar
tasks as examples.

## Read the code

```bash
diff -ru module_3/app module_4/app
```

1. [`app/agent.py`](app/agent.py): `_turn` opens a trace first (step 0), adds
   past executions to the instructions, and records the trace last (step 6).
2. [`app/reasoning.py`](app/reasoning.py): `similar_executions` (recall) and
   `record_execution` (record). Its docstring explains why these are not the
   library's `get_similar_traces()` / `record_agent_trace()`.
3. [`app/memory_tools.py`](app/memory_tools.py): `search_memory` now also
   returns similar procedures.

[`lab/ablation.py`](lab/ablation.py) seeds the fixed corpus for the
retrieval-on/off comparison. The agent does not use it.

## Run it

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

- **The trace graph:** ReasoningTrace → HAS_STEP → ReasoningStep → USES_TOOL →
  ToolCall → INSTANCE_OF → Tool. INITIATED_BY links the trace to its user
  message; TOUCHED links each captured step to its case’s Customer and Plan. A trace
  opens before execution and completes on success *and* on exception.
- **Execution vs business status:** a declined refund can be a successful
  execution. A model or dependency error has `execution_status: failed`.
- **Records, not thoughts:** steps are the tools that actually ran, with real
  SQL. A rejected refund has no INSERT. The model's hidden reasoning is not
  stored.
- **Examples, not policy:** retrieved executions guide the model, but current
  SQL policy is enforced the same way with retrieval on or off.
- **The ablation (`s4-refund-repeat`):** both branches read one fixed corpus,
  with identical private SQL copies, separate message namespaces, no trace
  recording and no entity extraction, so neither branch can leak state into the
  other. The artifact records input hashes, evidence, tools, tokens and timing.
  Identical behavior is a valid result.

`AGENT_REASONING_RETRIEVAL=off make dev MODULE=4` turns retrieval off for manual
experiments.

General app notes: [docs/running-the-app.md](../docs/running-the-app.md).
Questions and answers: [participant guide](../docs/modules/module-4.md).

## Explore and verify

### Q1: What did the agent actually execute?

Inspect ordered ReasoningSteps and ToolCalls, exact SQL and trace outcome.

### Q2: Did retrieval help?

Compare evidence, business result, tool calls, measured tokens and timing. Do not infer benefit from different prose.

One archived November 1 run offers a comparison when the live measurement is unavailable. On the first ticket, control and treatment each called `issue_refund` once and returned `issued`. They started with equal input SQL hashes. Control used 2,712 input tokens and 31.470 seconds. Treatment used 3,456 input tokens and 33.589 seconds. For that ticket the business action matched and treatment consumed more context. Compare your own rows separately. [Archived output](../docs/reviews/2026-11-01-workshop-fixes/command-09.log).

### Q3: What does failure mean?

A declined business request may have a successful execution. A model/dependency exception has execution_status failed. Inspect both fields and warnings.

### Q4: How do provenance links differ?

`MENTIONS` links message to entity. `INITIATED_BY` links trace to initiating message. `TOUCHED` links a step to selected-case entities. The recorder computes Customer/Plan references for the case and attaches that same set to the captured calls. To establish what an operation read or changed, inspect its tool output, captured SQL and receipt in **Saved replay**. Trace relationships are visible under **Live memory**.
