# Module 5 — Portable skills and hosted distillation

Start with [`app/agent.py`](app/agent.py). This folder owns the complete agent for
this stage: its prompt, registered tools, model call and chat orchestration.
Code is intentionally duplicated so changes from the previous lesson are visible.
No lesson imports another lesson's agent.

## Run and explore

Run every command from the **repository root**, not from this folder:

```bash
make dev MODULE=5
```

Keep the server terminal open. Run scenarios in a second terminal. Stop the previous
server with Ctrl+C before switching stages, then reload the browser. The same root
`.env`, SQLite database, virtual environment and AuraDB are reused.

Scenario playback constructs this folder's agent directly and prints dialogue and
tool calls in the terminal. It does not replay the conversation into the browser.
Reload the graph or change its layer filter to see externally written memory.
The browser's tool trace displays only the latest browser chat request.

```bash
make nams-check
make nams-seed
make nams-distill
make s5-fresh-agent WITH_SKILL=off
make s5-fresh-agent WITH_SKILL=on
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

[`app/agent.py`](app/agent.py) is a complete local copy of the reasoning-enabled
support agent. It still uses Bolt and your AuraDB.

[`app/fresh_agent.py`](app/fresh_agent.py) is the separate fresh-agent experiment:
it loads SKILL.md into instructions and registers business tools, with no memory
client or prior conversation history.

[`workflows/`](workflows/) owns NAMS checking, canonical seeding, distillation,
review/publish/download, and drift inspection. Root scripts are thin CLI wrappers.
NAMS is a separate workspace; these workflows never migrate your AuraDB graph.
Live NAMS parity still needs a configured-key rehearsal; mock HTTP tests validate
our request choreography, not the external service.

Select an ontology with `ONTOLOGY=acme_cloud` (default), `ONTOLOGY=default-poleo`,
or `ONTOLOGY=active` to use the version activated in AuraDB. An explicit selection
in a scenario overrides the environment for that invocation only. A local YAML
selection overrides an active database ontology; edits resolve on client creation.

`AGENT_REASONING_RETRIEVAL=off make dev MODULE=5` disables similar-task
retrieval for manual experiments; the ablation scenario passes this option explicitly.

When live distillation is unavailable:

```bash
make s5-fresh-agent WITH_SKILL=fallback
```

This loads the checked-in skill. It demonstrates skill consumption, not live NAMS
distillation or a hosted skill graph. `make s5-fallback` is not a target.

For the governance demonstration:

```bash
make policy-change
make nams-drift
make nams-redistill
```

The first command changes SQLite; the second deletes grounding memory in NAMS.
Governance observes the latter. The seed creates new conversations/traces on each
run, so repeated runs are not a pristine checkpoint restore.

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
diff -ru module_4/app module_5/app
```

Use the [participant guide](../docs/modules/module-5.md) for questions and answers.
The offline tests exercise real PydanticAI runs using local adapters. Live rehearsal
is opt-in and writes unique test conversations without wiping existing graph data.

```bash
uv run pytest tests/test_module_agents.py tests/test_workshop_runners.py -q
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

Shared `lib/` contains credentials, SQL helpers, graph serialization, HTTP transport,
and module dispatch only. Agent behavior is implemented here.
