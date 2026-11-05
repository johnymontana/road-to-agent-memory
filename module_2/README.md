# Module 2 — Short-term memory

**The idea:** store the conversation in Neo4j and give it back to the model.
Every message becomes a `(:Message)` in a `(:Conversation)`, embedded for
similarity search. Before each turn the agent recalls:

- **recent_conversation**: the last 10 turns of this conversation, passed to
  PydanticAI as `message_history` (the model sees real prior turns).
- **semantic_message**: similar statements the customer made in *other*
  conversations in this namespace, added to the instructions as cited evidence.

## Read the code

```bash
diff -ru module_1/app module_2/app
```

1. [`app/memory.py`](app/memory.py): opens the `neo4j-agent-memory`
   `MemoryClient` (Bolt backend, your AuraDB). Entity extraction stays off until
   module 3.
2. [`app/agent.py`](app/agent.py): `_turn` now runs *remember → recall →
   answer → remember the reply*.
3. [`app/context.py`](app/context.py): the two retrieval paths. Its docstring
   explains why semantic search uses scoped Cypher instead of
   `short_term.search_messages()`.

## Run it

```bash
make dev MODULE=2
# Second terminal:
make s2-return
make s2-restart
make eval MODULE=2
```

`s2-return` continues one conversation, then asks from a new one. `s2-restart`
runs two separate Python processes with the same session and namespace. The
saved artifact lists both process IDs, and your browser backend keeps running.

General app notes: [docs/running-the-app.md](../docs/running-the-app.md).
Questions and answers: [participant guide](../docs/modules/module-2.md).

## Explore and verify

### Q1: Which records persist?

Conversation HAS_MESSAGE Message, plus message ordering links. Inspect IDs and timestamps.

### Q2: What survives restart?

The same named conversation is retrieved by a new process; inspect the saved process IDs.

### Q3: How does a new conversation differ?

Recent history is per conversation. Semantic retrieval can still find earlier user messages from any conversation in the namespace.

### Q4: Which search path answered?

Inspect recent_conversation versus semantic_message evidence IDs. Paraphrases need semantic similarity; empty evidence is visible.
