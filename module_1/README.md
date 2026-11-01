# Module 1 — The stateless support agent

Start with [`app/agent.py`](app/agent.py). This folder owns the complete agent for
this stage: its prompt, registered tools, model call and chat orchestration.
Code is intentionally duplicated so changes from the previous lesson are visible.
No lesson imports another lesson's agent.

## Run and explore

Run every command from the **repository root**, not from this folder:

```bash
make dev MODULE=1
```

Keep the server terminal open. Run scenarios in a second terminal. Stop the previous
server with Ctrl+C before switching stages, then reload the browser. The same root
`.env`, SQLite database, virtual environment and AuraDB are reused.

Scenario playback constructs this folder's agent directly and prints dialogue and
tool calls in the terminal. It does not replay the conversation into the browser.
Reload the graph or change its layer filter to see externally written memory.
The browser's tool trace displays only the latest browser chat request.

```bash
make s1-baseline
make eval MODULE=1
```

## Read the code

1. [`app/main.py`](app/main.py) connects the local agent factory to the shared HTTP transport.
2. [`app/agent.py`](app/agent.py) constructs the agent and runs one complete chat turn.
3. [`app/tools.py`](app/tools.py) defines all five business tools and their trace collection.

## What changes in this stage

The agent has business tools but no memory client. Every model call is stateless;
even reusing a session ID does not supply conversation history. The graph is empty.

## Compare and verify

Use the [participant guide](../docs/modules/module-1.md) for questions and answers.
The offline tests exercise real PydanticAI runs using local adapters. Live rehearsal
is opt-in and writes unique test conversations without wiping existing graph data.

```bash
uv run pytest tests/test_module_agents.py tests/test_workshop_runners.py -q
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

Shared `lib/` contains credentials, SQL helpers, graph serialization, HTTP transport,
and module dispatch only. Agent behavior is implemented here.
