# Module 3 — Structured long-term memory

Start with [`app/agent.py`](app/agent.py). This folder owns the complete agent for
this stage: its prompt, registered tools, model call and chat orchestration.
Code is intentionally duplicated so changes from the previous lesson are visible.
No lesson imports another lesson's agent.

## Run and explore

Run every command from the **repository root**, not from this folder:

```bash
make dev MODULE=3
```

Keep the server terminal open. Run scenarios in a second terminal. Stop the previous
server with Ctrl+C before switching stages, then reload the browser. The same root
`.env`, SQLite database, virtual environment and AuraDB are reused.

Scenario playback constructs this folder's agent directly and prints dialogue and
tool calls in the terminal. It does not replay the conversation into the browser.
Reload the graph or change its layer filter to see externally written memory.
The browser's tool trace displays only the latest browser chat request.

```bash
make s3-default
make s3-ontology
make eval MODULE=3
```

## Read the code

1. [`app/main.py`](app/main.py) connects the local agent factory to the shared HTTP transport.
2. [`app/agent.py`](app/agent.py) constructs the agent and runs one complete chat turn.
3. [`app/tools.py`](app/tools.py) defines all five business tools and their trace collection.
4. [`app/memory.py`](app/memory.py) configures and opens this lesson’s memory client.
5. [`app/memory_tools.py`](app/memory_tools.py) exposes memory search and preferences.
6. [`app/hydrate.py`](app/hydrate.py) grounds extracted entities in SQLite facts.
7. [`ontology/acme_cloud.yaml`](ontology/acme_cloud.yaml) is this lesson’s editable domain ontology.

## What changes in this stage

LLM extraction is enabled, local memory tools join the business tools, and hydration
updates extracted entities with facts from SQLite. Memory search includes messages,
entities and preferences, but never reasoning traces. Both ontology variants are
owned by this directory. Default/custom runs share one graph; inspect each result
before the next run, rather than expecting isolated canvases.

Select an ontology with `ONTOLOGY=acme_cloud` (default), `ONTOLOGY=default-poleo`,
or `ONTOLOGY=active` to use the version activated in AuraDB. An explicit selection
in a scenario overrides the environment for that invocation only. A local YAML
selection overrides an active database ontology; edits resolve on client creation.

Optional enrichment: `make s3-enrich`. Inspect the grounded `Customer` properties and
follow `MENTIONS` from messages to extracted entities. Wikimedia enrichment is async.

Hydration checks the stored name and recorded aliases against exact SQLite
records. It preserves resolved node names and skips conflicting alias matches.
Explicit preference-save requests call `save_preference` before confirmation.

Wikimedia enrichment is best-effort. Extracted organizations without SQLite
records (for example Stripe) are queued through the public entity upsert;
they are not counted as SQL-hydrated facts. The provider can return an error
when Wikipedia blocks automated requests. The support reply and internally
grounded facts still work; do not expect external properties on those runs.

## Compare and verify

```bash
diff -ru module_2/app module_3/app
```

Use the [participant guide](../docs/modules/module-3.md) for questions and answers.
The offline tests exercise real PydanticAI runs using local adapters. Live rehearsal
is opt-in and writes unique test conversations without wiping existing graph data.

```bash
uv run pytest tests/test_module_agents.py tests/test_workshop_runners.py -q
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

Shared `lib/` contains credentials, SQL helpers, graph serialization, HTTP transport,
and module dispatch only. Agent behavior is implemented here.
