# Module 2 — Conversation memory

Start with [`app/agent.py`](app/agent.py). This folder owns the complete agent for
this stage: its prompt, registered tools, model call and chat orchestration.
Code is intentionally duplicated so changes from the previous lesson are visible.
No lesson imports another lesson's agent.

## Run and explore

Run every command from the **repository root**, not from this folder:

```bash
make dev MODULE=2
```

Keep the server terminal open. Run scenarios in a second terminal. Stop the previous
server with Ctrl+C before switching stages, then reload the browser. The same root
`.env`, SQLite database, virtual environment and AuraDB are reused.

Scenario playback constructs this folder's agent directly and prints dialogue and
tool calls in the terminal. It does not replay the conversation into the browser.
Reload the graph or change its layer filter to see externally written memory.
The browser's tool trace displays only the latest browser chat request.

```bash
make s2-return
make s2-restart
make eval MODULE=2
```

## Read the code

1. [`app/main.py`](app/main.py) connects the local agent factory to the shared HTTP transport.
2. [`app/agent.py`](app/agent.py) constructs the agent and runs one complete chat turn.
3. [`app/tools.py`](app/tools.py) defines all five business tools and their trace collection.
4. [`app/memory.py`](app/memory.py) configures and opens this lesson’s memory client.

## What changes in this stage

The chat loop creates a conversation, writes each user message, retrieves message
context, calls the model, and writes the reply. Extraction, long-term retrieval and
reasoning retrieval are disabled explicitly. Bolt may find relevant messages across
sessions; this does not create structured entity memory. `s2-return` continues the
same conversation. `s2-restart` recreates the agent/client in-process, not the dev server.

## Compare and verify

```bash
diff -ru module_1/app module_2/app
```

Use the [participant guide](../docs/modules/module-2.md) for questions and answers.
The offline tests exercise real PydanticAI runs using local adapters. Live rehearsal
is opt-in and writes unique test conversations without wiping existing graph data.

```bash
uv run pytest tests/test_module_agents.py tests/test_workshop_runners.py -q
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

Shared `lib/` contains credentials, SQL helpers, graph serialization, HTTP transport,
and module dispatch only. Agent behavior is implemented here.
