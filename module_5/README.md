# Module 5 — Skill distillation with NAMS

**The idea:** turn one agent's experience into a skill any agent can use.
Reasoning traces are seeded into the hosted Neo4j Agent Memory Service (NAMS),
which distills them into a `SKILL.md`. A brand-new agent with no memory loads
that file and handles the ticket correctly on its first try. When the memory a
skill is grounded in changes, NAMS flags the skill as stale.

The support agent itself (`app/agent.py`) is **unchanged from module 4** and
still uses Bolt and your AuraDB. NAMS is a separate hosted workspace; this
module never migrates your AuraDB graph.

## Read the code

```bash
diff -ru module_4/app module_5/app
```

1. [`workflows/seed.py`](workflows/seed.py): writes canonical refund history
   (entities → conversation → messages → traces with steps and tool calls →
   completed outcomes) to NAMS, and records the conversation ID in
   `data/nams-workspace.json`.
2. [`workflows/distill.py`](workflows/distill.py): distills a skill from exactly
   that conversation, polls the run (about a minute), approves and publishes it,
   and unpacks the skill package into `artifacts/distilled/`: `SKILL.md`,
   `references/` and `provenance.json`. Rerunning publishes a new *version* of the
   same skill.
3. [`app/fresh_agent.py`](app/fresh_agent.py): base instructions + `SKILL.md`
   + business tools. No memory client, history or retrieval. It runs on a private
   SQLite copy, so `WITH_SKILL=off` and `on` start from the same state.
4. [`workflows/drift.py`](workflows/drift.py): reads `provenance.json`, deletes
   the refund-policy entities the skill is grounded in, then prints the claims and
   steps NAMS reports as stale.

`workflows/check.py` verifies your NAMS key. `workflows/nams.py` holds the shared
client. The workflows are plain HTTP calls (see
[the API spec](https://memory.neo4jlabs.com/openapi.json)) because
`neo4j-agent-memory` has no client for the NAMS skills API yet.

In the browser, tick **NAMS** above the graph to see the skill graph: Skill →
versions → steps → the entities, agent steps and tool calls each step is
`GROUNDED_IN`.

The root `scripts/nams_*.py` files are thin wrappers behind the make targets.

## Run it

```bash
make dev MODULE=5
# Second terminal:
make nams-check
make nams-seed
make nams-distill
make s5-fresh-agent WITH_SKILL=off   # control: no skill
make s5-fresh-agent WITH_SKILL=on    # with the distilled skill
```

If live distillation is unavailable, use the checked-in skill. This shows how an
agent consumes a skill, not live NAMS distillation:

```bash
make s5-fresh-agent WITH_SKILL=fallback
```

Governance demonstration:

```bash
make policy-change    # changes SQLite; NAMS still reports the skill "current"
make nams-drift       # deletes grounding memory in NAMS; governance flags it
make nams-redistill   # re-distill a new version and diff the SKILL.md
make policy-change    # run again to restore the $250 Pro limit
```

Each `nams-seed` run creates a new conversation and traces, and distillation then
uses the newest one. Offline tests check the requests against the published API
contract; the make targets above were rehearsed live against memory.neo4jlabs.com.

General app notes: [docs/running-the-app.md](../docs/running-the-app.md).
Questions and answers: [participant guide](../docs/modules/module-5.md).
