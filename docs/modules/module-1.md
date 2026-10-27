# Module 1 — The Stateless Agent

Meet the baseline: a capable support agent with a rich tool set — and the memory of a
goldfish. This module shows the failure everything else fixes.

## What you'll learn

- What an agent actually is: an LLM plus tools it can call, wired together with PydanticAI.
- How the five SQLite-backed tools make the agent *competent* from the first message.
- Why competence isn't continuity: a new chat starts from zero, and a restart loses everything.
- The workshop's core framing: **SQLite is the system of record; Neo4j is the memory.**

## Run it

| Command | What it does |
|---|---|
| `make s1-baseline` | Runs scenario 1 (a billing issue) against the stateless agent — watch it handle the ticket, then watch it forget everything. |
| `make eval` | Runs the fixed continuity eval-question set and prints the scorecard — this is the baseline every later module improves on. |

## Explore

**Core**

1. Ask the agent the eval questions. Which can it answer? Which fail, and why?
2. Watch a tool call in the trace panel: what SQL ran against SQLite? What did the agent "learn" during the call — and where does that learning go when the process exits?

**Instructor-led**

3. Inspect the SQLite schema directly. Which tables back which tools? If the agent looks up the same account five times in one conversation, how many SQL queries run — and what would it take to avoid that?

**Stretch**

4. Run the same ticket twice. Does the agent's procedure differ? What does that cost (tokens, latency, consistency)?
5. If two customers describe the same outage, does the agent connect them? What would it need in order to?

## Answer key

1. It can answer anything that needs a *live* lookup — account details, catalog questions, policy quotes — because the tools work fine. It fails every continuity question ("Do you know who I am?", "What did we discuss last time?") because nothing is stored between chats: each conversation starts with an empty slate.
2. The trace panel shows the actual parameterized SQL each tool ran (e.g. `lookup_account`'s `SELECT` joining customers, organizations, subscriptions, plans). Everything the agent "learned" — the tool results, its reasoning — lives only in the process's in-memory chat state, and vanishes completely when the process exits.
3. `customers`/`organizations`/`subscriptions`/`plans` back `lookup_account`; `products`/`features` back `search_product_catalog`; `policies` backs `fetch_policy`; `service_status` backs `check_service_status`; `refunds` is the write path for `issue_refund`. Five lookups of the same account = five identical SQL queries — SQLite happily re-answers, but the agent re-asks because it can't remember; module 3's hydration fixes exactly this for entities.
4. It re-derives the procedure from scratch — roughly the same tool chain, re-run. The cost is repeated tokens, repeated latency, and (worse) inconsistency: two identical tickets can get two slightly different answers. Module 4's reasoning memory is the fix.
5. No — each conversation is an island. To connect them, the agent would need a shared store where both conversations and the outage itself live as linked data. That's the memory graph you'll build starting in module 2.

## If you fell behind

From the repo root, run:

```
make module-1
```

That replays this module's beats in order and reproduces the room's current state. If
your dev server is still running an older stage, stop it first with `Ctrl+C`, then
restart with `make dev MODULE=1`.

## Glossary

- [Agent](../glossary.md#agent) · [Tool](../glossary.md#tool) · [PydanticAI](../glossary.md#pydanticai) · [SQLite](../glossary.md#sqlite) · [LLM](../glossary.md#llm)
