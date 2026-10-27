# Module 2 — Short-Term Memory

The first memory layer: the agent now remembers *this* conversation — even across a
full restart of the app.

## What you'll learn

- How conversations and messages become nodes and chains in your AuraDB graph.
- How `get_context` assembles what the agent remembers into the prompt on every turn.
- How message search finds things said earlier — even when you paraphrase.
- The three-tier context model: reflections, observations, and recent messages.

## Run it

| Command | What it does |
|---|---|
| `make s2-return` | The customer "returns" in a brand-new chat — and the agent picks up where things left off instead of asking who they are. |
| `make s2-restart` | The killer beat: the backend is stopped and restarted mid-conversation, and the agent continues without losing a word. |

## Explore

**Core**

1. In the graph panel, find the conversation you just had. How are messages linked? What properties does a `:Message` node carry (role, timestamp, embedding, metadata)?
2. Kill and restart the app mid-scenario. What does the agent still know? Trace exactly which records made that possible.
3. What's the boundary of short-term memory? If the customer returns tomorrow in a *new* conversation, what crosses over — and what doesn't?

**Instructor-led**

4. Use message search with a paraphrase of something said earlier (not exact words). Which search path answered — vector or text? How can you tell?

**Stretch**

5. Look at the context tiers: what distinguishes a reflection from an observation from a raw message? When would each matter for a support agent?

## Answer key

1. Each chat is a `:Conversation` node with its `:Message` nodes linked in sequence — a chain you can literally follow in the graph panel. A `:Message` carries its `role` (user/assistant), a `timestamp`, an `embedding` (the numeric fingerprint that powers meaning-based search), and `metadata`.
2. The agent still knows everything that was written to Neo4j via `add_message` — the whole conversation, every message. The records that made it possible are the `:Conversation` node and its `:Message` chain sitting safely in AuraDB, outside the app's process. Only unsaved in-process state is lost on restart.
3. The boundary is the conversation. In a *new* conversation tomorrow, the raw message context doesn't automatically follow — short-term memory is within-conversation continuity. What crosses over is only what gets distilled into long-term memory (entities, facts, preferences) — which is exactly module 3's job.
4. The vector (embedding) path answered. A paraphrase shares meaning but not words, so an exact-text search would miss it — and the fact that a result came back with little keyword overlap is the giveaway (the app also labels which path answered). This is embeddings doing their one job: matching by meaning.
5. Recent messages are raw chat lines; observations are distilled notes about what's happening; reflections are higher-level syntheses over those observations. For a support agent: raw messages when you need the exact quote, observations to track the current issue's state, reflections to know "this customer has recurring billing pain" without re-reading months of chat.

## If you fell behind

From the repo root, run:

```
make module-2
```

That replays this module's beats in order and reproduces the room's current state. If
your dev server is still running an older stage, stop it first with `Ctrl+C`, then
restart with `make dev MODULE=2`.

## Glossary

- [Short-term memory](../glossary.md#short-term-memory) · [Embedding](../glossary.md#embedding) · [Node](../glossary.md#node) / [Edge](../glossary.md#edge) · [Bolt backend](../glossary.md#bolt-backend) · [AuraDB](../glossary.md#auradb)
