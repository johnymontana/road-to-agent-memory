# Module 4 — Reasoning Memory

Code-reading map: [module_4/README.md](../../module_4/README.md). Start with
[`module_4/app/agent.py`](../../module_4/app/agent.py); the full agent is local to this lesson.


Modules 2–3 remembered *what was said* and *what is true*. This module remembers *what
the agent did* — every step, every tool call, every outcome — so it can recall
procedures instead of re-deriving them.

## What you'll learn

- What a reasoning trace is: the agent's own execution recorded as a queryable subgraph.
- How similar-task retrieval primes the agent with "how I solved this yesterday."
- Why failed runs are stored as first-class memory, not thrown away.
- How to answer "why did you do that?" by walking the graph from outcome back to the customer's words.

## Run it

| Command | What it does |
|---|---|
| `make s4-refund` | Runs the first refund ticket — recorded as a trace (`lookup_account` → `fetch_policy("refund")` → `issue_refund`). |
| `make s4-refund-repeat` | Runs a "same shape" ticket days later — twice, once with retrieval off and once on — so you can see the behavioral difference side by side. |
| `make s4-fail` | Runs a deliberately over-limit refund that `issue_refund` rejects — the failed trace that becomes a lesson. |

## Explore

**Core**

1. Pick a completed trace in the graph. Reconstruct the story: what was the task, which tools were called in what order, what was the outcome?
2. Run the "same shape" refund ticket. What does similar-task retrieval return, and how does it change the agent's behavior (tool order, steps skipped, confidence)?
3. Which eval question does reasoning memory unlock that modules 2–3 couldn't answer?

**Instructor-led**

4. Find a *failed* trace (the refund over the policy limit that `issue_refund` rejected). What went wrong, and how would the next agent avoid it? What does it mean that failures are first-class memory?
5. Answer the provenance question: "Why did you issue that refund?" — trace the answer from final outcome back through steps and tool calls (including the `fetch_policy` result the decision relied on) to the customer's original message.

**Stretch**

6. Find the `:TOUCHED` edges from a reasoning step. Which entities did the agent's decision depend on? How is this different from `:MENTIONS`?

## Answer key

1. The trace reads like a story: the task (a refund request) → a chain of `ReasoningStep` nodes, each with its `ToolCall` (`lookup_account`, then `fetch_policy("refund")`, then `issue_refund`) → an outcome node (success). It's the agent's own execution, stored as a graph you can query like any other data.
2. Similar-task retrieval returns yesterday's successful refund trace, and the agent primes on it: it follows the same tool order, skips the re-derivation (and the dead ends), and acts with more confidence — visible in the side-by-side control/treatment run as fewer steps and fewer tokens.
3. "Have you handled a ticket like this before?" Short-term memory knows what was said and long-term memory knows what is true — but only reasoning memory makes past *procedures* retrievable.
4. The failed trace shows an over-limit refund attempt that `issue_refund` rejected after the policy check. The next agent can retrieve this failure and check the limit *before* attempting the write. Failures as first-class memory means the agent learns what not to do — a lesson, not a lost log line.
5. Walk the edges backwards: outcome node → the `issue_refund` tool call → the `fetch_policy` result that authorized it → the reasoning steps → the customer's original message. Every hop is an edge in the graph, so "why did you do that?" has a complete, inspectable audit trail instead of a shrug.
6. `:TOUCHED` edges connect a reasoning step to the entities the decision actually depended on — this customer, this policy. `:MENTIONS` (module 3) says "this message talked about X"; `:TOUCHED` says "the agent *used* X to act." One is reference, the other is cause.

## If you fell behind

From the repo root, run:

```
make module-4
```

That replays this module's beats in order (refund, repeat-with-ablation, failed refund)
and reproduces the room's current state. If your dev server is still running an older
stage, stop it first with `Ctrl+C`, then restart with `make dev MODULE=4`.

## Glossary

- [Reasoning memory](../glossary.md#reasoning-memory) · [Trace](../glossary.md#trace) · [Provenance](../glossary.md#provenance) · [Tool](../glossary.md#tool) · [Edge](../glossary.md#edge)
