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
module_1/ … module_5/   # the app at each stage — diff folders to see memory land (ADR 004)
lib/                    # shared machinery (tools, memory wiring, hydration, graph API)
web/                    # React + NVL frontend (chat / graph / trace panels)
scripts/              # scenario runner, seeders, eval, NAMS scripts (driven by make targets)
ontology/             # acme_cloud.yaml (custom ontology) + default-poleo.yaml (before/after beat)
tests/                # command-surface, seed, golden-graph snapshots, behavioral lane
slides/               # instructor deck (Marp) + Excalidraw diagram sources
docs/                 # glossary, module guides, pre-work, run-of-show, teardown, ADRs
artifacts/            # pre-distilled skill fallback (module 5)
```

## Status

Workshop materials for a Neo4j Labs project — experimental, community-supported, no
SLAs. See [docs/teardown.md](docs/teardown.md) for post-workshop cleanup.
