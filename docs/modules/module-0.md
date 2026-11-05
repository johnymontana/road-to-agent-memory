# Module 0 — Setup

[Open the workshop Codespace](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) or [get the workshop repository](https://github.com/johnymontana/road-to-agent-memory) for a local Dev Container. Run commands from the repository root. Find [Module 1’s complete agent](../../module_1/app/agent.py) before the first scenario.

## What you'll learn

- What the three panels of the workshop app do (chat / graph / trace).
- Which credentials live where — and why `make check` exists.
- Where Acme Cloud's business data lives (SQLite) versus where its memory will live (Neo4j for modules 2–5).
- How a chat message travels from your browser to the model and back.

## Run it

| Command | What it does |
|---|---|
| `make setup` | Installs the locked Python and frontend dependencies and creates SQLite if absent. Re-running setup preserves existing rows. The Dev Container handles these steps during setup. |
| `make check` | Smoke test: env vars present, AuraDB reachable, configured chat/embedding inference, SQLite schema/data, memory startup and graph serialization. Optional services are reported separately. |
| `make dev MODULE=1` | Starts the FastAPI backend and the Vite frontend together; waits for readiness; open port 5173. The browser retries while the backend starts. |

If you're continuing from pre-work, your only real jobs are: add your AuraDB
credentials to your private `.env`, run `make check`, then start `make dev MODULE=1` in terminal 1. Reload port 5173 and confirm the **Module 1** badge. Reserve terminal 2 for scenario commands.

## Explore

**Core**

1. What does the graph panel show right now? Why is it empty — what would have to happen for something to appear?
2. Open the seeded **Acme Cloud SQLite database** (`acme_cloud.db` — try `sqlite3 data/acme_cloud.db ".tables"`). What business data exists — customers, products, plans, policies, service status?

**Instructor-led**

3. Which components are already wired: where does a chat message travel from the UI to the model and back?

**Stretch**

4. Where does the agent's "company knowledge" come from in module 1 — and what are the limits of that approach?

## Answer key

1. The Module 1 backend is stateless, so this view has no persisted conversation memory from this agent. Existing records can still be present in a previously used AuraDB. From Module 2 onwards the app persists conversation messages.
2. Ten tables, including `billing_cases`: `customers`, `organizations`, `products`, `features`, `plans`, `subscriptions`, `policies`, `service_status`, and `refunds`. This is Acme Cloud's *system of record* — the business data the agent acts on. Every agent tool in module 1 reads from (or, for refunds, writes to) these tables.
3. Browser → Vite dev server (port 5173) → `/api` proxy → FastAPI backend (port 8000) → the PydanticAI agent → OpenAI → any tool calls against SQLite → a complete JSON reply returns, with the tool calls shown in the trace panel. The graph panel refreshes through `/api/graph`. Module 1 returns an empty graph locally. Module 2 connects that endpoint to AuraDB.
4. From the model's system prompt plus live tool lookups — nothing else. The limits: it only knows what it looks up *right now*, nothing persists between conversations, and it can never learn from experience. That gap is exactly what the rest of the workshop fills.

## If you fell behind

From the repo root, run:

```
make module-0
```

That runs the readiness check; run `make setup` separately if dependencies or seed data are missing. Read the required checks, including the median time across five Bolt queries. Check optional NAMS capabilities separately for the hosted capstone. A helper can investigate a failing capability while the room continues.

## Glossary

- [Codespaces](../glossary.md#codespaces) · [uv](../glossary.md#uv) · [SQLite](../glossary.md#sqlite) · [AuraDB](../glossary.md#auradb) · [Graph](../glossary.md#graph)
