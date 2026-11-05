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

```bash
make dev MODULE=4
# Second terminal:
make s4-refund
make s4-fail
make s4-refund-repeat
make eval MODULE=4
```

- **The trace graph:** ReasoningTrace → HAS_STEP → ReasoningStep → USES_TOOL →
  ToolCall → INSTANCE_OF → Tool. INITIATED_BY links the trace to its user
  message; TOUCHED links tool calls to the case's Customer and Plan. A trace
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

### Q3: What does failure mean?

A declined business request may have a successful execution. A model/dependency exception has execution_status failed. Inspect both fields and warnings.

### Q4: How do provenance links differ?

MENTIONS is source text about an entity. TOUCHED records case dependencies; INITIATED_BY identifies the initiating user message.
