# Module 0 — Setup

Get everyone running: a full-stack chat app, in a prebuilt Codespace, talking to your
own AuraDB. Nothing to memorize yet — this module is about seeing the machine work.

## What you'll learn

- What the three panels of the workshop app do (chat / graph / trace).
- Which credentials live where — and why `make check` exists.
- Where Acme Cloud's business data lives (SQLite) versus where its memory will live (Neo4j — currently empty).
- How a chat message travels from your browser to the model and back.

## Run it

| Command | What it does |
|---|---|
| `make setup` | Installs the exact pinned Python dependencies via `uv sync` (already done for you in a prebuilt Codespace). |
| `make check` | Smoke test: env vars present, AuraDB reachable, OpenAI key valid, SQLite seeded — everything green means you're ready. |
| `make dev` | Starts the FastAPI backend and the Vite frontend together; the UI opens in a browser tab automatically (port 5173). |

If you're continuing from pre-work, your only real jobs are: add your AuraDB
credentials to `.env`, run `make check`, then `make dev`.

## Explore

**Core**

1. What does the graph panel show right now? Why is it empty — what would have to happen for something to appear?
2. Open the seeded **Acme Cloud SQLite database** (`acme_cloud.db` — try `sqlite3 data/acme_cloud.db ".tables"`). What business data exists — customers, products, plans, policies, service status?

**Instructor-led**

3. Which components are already wired: where does a chat message travel from the UI to the model and back?

**Stretch**

4. Where does the agent's "company knowledge" come from in module 1 — and what are the limits of that approach?

## Answer key

1. **Empty, by design.** Nothing has been written to your AuraDB yet — all the seed data lives app-side in SQLite, and Neo4j only starts filling in once the agent stores memories (from module 2 onward). Something appears the moment the app saves a conversation, message, or entity to the graph.
2. Nine tables: `customers`, `organizations`, `products`, `features`, `plans`, `subscriptions`, `policies`, `service_status`, and `refunds`. This is Acme Cloud's *system of record* — the business data the agent acts on. Every agent tool in module 1 reads from (or, for refunds, writes to) these tables.
3. Browser → Vite dev server (port 5173) → `/api` proxy → FastAPI backend (port 8000) → the PydanticAI agent → OpenAI → any tool calls against SQLite → the reply streams back, with the tool calls shown in the trace panel. The graph panel refetches from AuraDB after each reply.
4. From the model's system prompt plus live tool lookups — nothing else. The limits: it only knows what it looks up *right now*, nothing persists between conversations, and it can never learn from experience. That gap is exactly what the rest of the workshop fills.

## If you fell behind

From the repo root, run:

```
make module-0
```

That runs this module's beats in order (install, seed, smoke test). Then run
`make check` — if every line is green, you're caught up. If anything is red, raise a
hand: a helper will triage while the room moves on.

## Glossary

- [Codespaces](../glossary.md#codespaces) · [uv](../glossary.md#uv) · [SQLite](../glossary.md#sqlite) · [AuraDB](../glossary.md#auradb) · [Graph](../glossary.md#graph)
