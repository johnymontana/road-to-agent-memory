# Road to Agent Memory

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory)

A 2.5-hour live workshop: build up an AI customer-support agent ("SupportBot", for the
fictional SaaS company **Acme Cloud**) from stateless to fully memory-enabled —
short-term, long-term, and reasoning memory backed by Neo4j, ending with skill
distillation on the Neo4j Agent Memory Service (NAMS).

> **Format:** run-and-explore. You'll run a complete app, watch its memory graph grow
> in the NVL panel, and answer guided exploration questions — not write code from
> scratch. Every action is a `make` target.

## Quick start (Codespaces — recommended)

1. **Before the workshop** (see [docs/prework-email.md](docs/prework-email.md)):
   a free AuraDB instance, an `OPENAI_API_KEY` (store it as a personal Codespaces
   secret scoped to this repo), and a NAMS key from
   [memory.neo4jlabs.com](https://memory.neo4jlabs.com) (module 5).
2. Click the badge above → a prebuilt codespace opens with everything installed.
3. Add your AuraDB credentials to `.env` (created from `.env.example` on first boot).
4. `make check` → all green? `make dev` → the UI opens automatically.

**Local fallback:** VS Code Dev Containers (`Reopen in Container`) or manual setup
(`uv sync && npm --prefix web ci && make seed && make dev`).

## The workshop

| Module | Story | Commands |
|---|---|---|
| 0 — Setup | Boot the app, meet the two stores | `make check` · `make dev` |
| 1 — The Stateless Agent | The agent forgets everything | `make s1-baseline` · `make eval` |
| 2 — Short-Term Memory | It survives restarts now | `make s2-return` · `make s2-restart` |
| 3 — Long-Term Memory | It knows *who the customer is* | `make s3-default` → `make s3-ontology` |
| 4 — Reasoning Memory | It remembers *how it solved this before* | `make s4-refund` · `make s4-refund-repeat` |
| 5 — Skill Distillation | One agent's experience becomes everyone's skill | `make nams-seed` · `make nams-distill` · `make nams-drift` |

Per-module guides with tiered exploration questions and answer keys:
[docs/modules/](docs/modules/). New to graphs/agents? Start with
[docs/glossary.md](docs/glossary.md).

## Repo layout

```
module_1/ … module_5/   # complete agent snapshots + a code-reading README per stage
lib/                    # shared SQL, settings, HTTP transport, graph serialization, dispatch
web/                    # React + NVL frontend (chat / graph / trace panels)
scripts/              # scenario runner, seeders, eval, NAMS scripts (driven by make targets)
module_3/ontology/    # local ontology variants (also copied into modules 4 and 5)
tests/                # module agents, runners, HTTP, NAMS choreography, live rehearsal
slides/               # instructor deck (Marp) + Excalidraw diagram sources
docs/                 # glossary, module guides, pre-work, run-of-show, teardown, ADRs
artifacts/            # pre-distilled skill fallback (module 5)
```

## Read and compare the agents

Each lesson owns its complete implementation: start at [module 1](module_1/README.md),
then [module 2](module_2/README.md), [module 3](module_3/README.md),
[module 4](module_4/README.md), and [module 5](module_5/README.md).
Prompts, tools, memory wiring and orchestration are local; duplication is deliberate.

```bash
diff -ru module_2/app module_3/app
```

Run commands from the repo root. At a stage transition, Ctrl+C the server, run
`make dev MODULE=N`, and reload the browser. Run `make eval MODULE=N` explicitly.
`make module-N` replays selected scenarios; it neither switches the server nor
restores a full checkpoint. Scenario output is in the terminal; browser chat/trace
only show browser requests. Reload or change the graph filter after a terminal run.

Module 5's hosted workflows live under `module_5/workflows/`; the root scripts retain
stable Make targets. The fresh agent is `module_5/app/fresh_agent.py`. Use
`make s5-fresh-agent WITH_SKILL=fallback` when live NAMS distillation is unavailable.

## Verify

```bash
uv run pytest tests/ -m "not behavioral" -q
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

The second command uses configured Neo4j and OpenAI services, writes uniquely named
workshop conversations, and uses temporary SQLite data. It never resets the graph.
NAMS lifecycle parity needs a separate configured-workspace rehearsal; offline HTTP
contract tests do not verify the hosted deployment.

See the [module evaluation report](docs/module-evaluation.md) for the verified
behavior of each stage and the remaining live-service checks.

## Status

Workshop materials for a Neo4j Labs project — experimental, community-supported, no
SLAs. See [docs/teardown.md](docs/teardown.md) for post-workshop cleanup.
