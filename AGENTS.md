# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

Material for a hands-on workshop, **Road to Agent Memory**. Participants clone the
repo (or open it in Codespaces) and run `make` targets. They do not write code.
They watch a PydanticAI customer-support agent ("SupportBot" for the fictional SaaS
company **Acme Cloud**) gain memory one stage at a time. The memory is backed by
Neo4j through the `neo4j-agent-memory` package.

| Stage | Folder | Adds |
|---|---|---|
| 1 | `module_1/` | Stateless baseline agent with five business tools |
| 2 | `module_2/` | Short-term memory: conversation and message persistence, recent and semantic message context |
| 3 | `module_3/` | Long-term memory: LLM entity extraction (POLE+O / Acme Cloud ontology), memory tools, SQL-grounded hydration |
| 4 | `module_4/` | Reasoning memory: recorded task traces, similar-task retrieval, ablation |
| 5 | `module_5/` | Skill distillation on the hosted Neo4j Agent Memory Service (NAMS), plus a fresh agent that loads the distilled skill |

Module 0 is environment setup only (`make check`). It has no folder.

## The most important rule: modules are isolated on purpose

Each `module_N/` is a **complete, standalone snapshot** of the agent at that stage
(ADR 004, `docs/adr/004-folder-per-module-progression.md`). Code is **copied, not
shared**. Participants learn by reading one folder or by running
`diff -ru module_2/app module_3/app`. That diff is the lesson.

- **Never** make one module import from another (`module_3` must not import
  `module_2.*`). `tests/test_module_agents.py` enforces this.
- **Never** move agent behavior into `lib/`. Prompts, tools, memory wiring,
  context assembly, hydration and orchestration stay local to each module. The
  test also forbids `lib.chat`, `lib.memory`, `lib.hydrate` and `lib.tools`.
- **Never** branch on the module number inside shared code to switch features on
  or off.
- **Do not "DRY up" duplication between modules.** It is intentional.
- When you fix a bug in a file that is copied forward (for example `tools.py`,
  `context.py`, `memory.py`, `hydrate.py` or the `ontology/*.yaml` files), apply
  the fix to **every module that has a copy**. Keep each later module equal to
  the earlier one plus that stage's additions, so the diffs between stages stay
  clean and show only the new concept.
- After any change, update that module's `README.md` and the matching
  `docs/modules/module-N.md` guide (exploration questions and answer keys) if
  the behavior they describe changed.

### Module layout

`app/agent.py` is the entry point for reading every module. Expected files:

```
module_N/
  README.md            # concept first: what this stage adds, reading order, commands
  app/main.py          # FastAPI entry: create_app(open_agent, ...) on :8000
  app/agent.py         # agent construction + ChatService._turn (numbered memory steps)
  app/tools.py         # business tools (lookup_account, search_product_catalog,
                       #   fetch_policy, check_service_status, issue_refund) + ToolDeps
  app/guardrails.py    # refund/reply safety checks; identical in every module
  app/memory.py        # (2+) MemoryClient configuration (Bolt backend)
  app/context.py       # (2+) pre-turn retrieval → message_history + evidence
  app/hydrate.py       # (3+) SQL-grounded entity hydration (PropertyWriter)
  app/memory_tools.py  # (3+) search_memory / save_preference / recall_preferences
  app/reasoning.py     # (4+) similar_executions + record_execution
  app/fresh_agent.py   # (5) agent that consumes a distilled SKILL.md
  ontology/*.yaml      # (3+) default-poleo and acme_cloud ontologies
  lab/                 # experiments behind make targets, not used by the agent:
                       #   module_3/lab/{compare,enrichment}.py, module_4/lab/ablation.py
  workflows/           # (5) NAMS check / seed / distill / drift
```

Copied files stay byte-identical until the stage that changes them, so
`diff -ru module_N/app module_N+1/app` shows only the new concept. For example,
`guardrails.py` never differs, and `tools.py` changes only in module 3, which
adds memory fields to `ToolDeps`.

Where a module uses hand-written Cypher instead of a `neo4j-agent-memory` API,
the docstring says why (usually namespace-scoped retrieval). Prefer library APIs
for new code, and document any exception the same way.

## Shared infrastructure (what *is* allowed to be shared)

Only infrastructure is shared. Agent prompts and memory policy are not.

- `lib/app_factory.py`: shared FastAPI HTTP transport. Each module passes in its
  own agent factory.
- `lib/settings.py`: env config (env vars override `.env`). The default chat model
  is `gpt-4o-mini` and embeddings use `text-embedding-3-small`.
- `lib/db.py`: SQLite system of record (Acme Cloud). Queries are always
  parameterized.
- `lib/graph.py`: maps Neo4j (Bolt) and NAMS graph state to the NVL shape.
- `lib/operations.py`: atomic operation receipts and `ReceiptGuard` (run a
  request ID at most once).
- `lib/response.py`: the `/api/chat` response envelope (`build_response`), so
  modules don't carry fields for memory layers they lack.
- `lib/workshop.py`: loads a module's agent by stage number. It must not hold
  any agent behavior.
- `web/`: the **single React + Vite + NVL frontend** used by every module, with
  chat, graph and trace panels. It talks to whichever module backend is running
  on :8000. The API contract is in `docs/frontend-contract.md`. A backend
  change that affects the API must keep every module compatible with this one
  frontend.
- `scripts/`: the scenario runner, seeders, eval and NAMS scripts that the
  Makefile drives. The scenario definitions are in `scripts/scenarios/*.json`.

## Commands

The **Makefile is the only command surface participants use** (ADR 002). Run
everything from the repo root.

```bash
make setup                 # uv sync --frozen + npm ci in web/ + seed SQLite
make check                 # env / AuraDB / OpenAI / SQLite / NAMS smoke test
make dev MODULE=N          # backend :8000 (module N) + frontend :5173
make s1-baseline ...       # scenario beats per module (see `make help`)
make eval MODULE=N         # continuity eval scorecard
make reset-memory          # DESTRUCTIVE: wipes the Neo4j memory graph
```

There are exactly **29 canonical targets**. `tests/command_surface_spec.py` is the
machine-readable list, and `tests/test_command_surface.py` checks the Makefile
against it. If you add, remove or rename a target, update the Makefile, the
`help` text, `command_surface_spec.py` and `WORKSHOP_OUTLINE.md` together.

Python tooling uses **uv** only. Do not use pip or poetry. `uv.lock` is committed,
and CI runs `uv lock --check`.

## Testing and linting

```bash
uv run ruff check .                                   # lint (line length 100, py311)
uv run pytest tests/ -m "not behavioral" -q           # offline suite, no credentials
npm --prefix web run build                            # frontend build
RUN_UI=1 uv run pytest tests/test_ui.py -q            # Playwright UI tests
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v   # live: Neo4j + OpenAI, spends tokens
```

- The offline suite runs every module's agent through real PydanticAI runs with
  `FunctionModel` and local memory adapters, and needs no network. Run it before
  you call a change done.
- Behavioral tests use the configured Neo4j and OpenAI services. They write
  uniquely named conversations and never reset the graph. Do not run them unless
  the user asks, because they cost money.
- CI (`.github/workflows/ci.yml`) runs ruff, the offline tests, the lock check,
  the frontend build and the UI tests on every push and PR.

## Environment and secrets

- Copy `.env.example` to `.env`. It needs `NEO4J_URI/USERNAME/PASSWORD` (AuraDB,
  modules 1–4), `OPENAI_API_KEY`, and `NAMS_API_KEY` (`nams_...`, module 5 only).
- Optional lesson knobs: `ONTOLOGY`, `VALIDATION_MODE`, `MEMORY_NAMESPACE`,
  `AGENT_REASONING_RETRIEVAL`, `DATA_DIR`.
- **Never** read out, print, commit or log the contents of `.env`.
- Do not run `make reset-memory`, `policy-change`, `nams-drift` or anything else
  that changes a participant's or instructor's live graph or NAMS workspace
  unless the user explicitly asks.

## Domain invariants worth preserving

These are part of the workshop's safety story. Tests cover them, so do not
weaken them:

- A refund (`issue_refund`) needs an explicitly selected customer, an explicitly
  selected billing case, and authorization for that one message. The server
  re-checks the case identity, the amount, the current SQL plan limit and that
  the incident has not already been refunded. Retrying the same request ID
  returns the saved receipt instead of a second refund.
- The agent has no escalation tool. Service status values are seeded examples,
  not live monitoring.
- Eval runs use private SQLite data, namespaced memory and disabled business
  tools.
- The graph API never returns embeddings.
- Module 4 ablation turns off both routes to reasoning retrieval but still
  records traces.

## Docs map

- `README.md`: participant quick start and repo layout
- `WORKSHOP_OUTLINE.md`: the canonical workshop spec (timing, arc, target table)
- `docs/modules/module-N.md`: participant guides with tiered questions and answer keys
- `docs/frontend-contract.md`: HTTP API contract between backend and `web/`
- `docs/adr/`: decisions (LLM extraction, uv + Makefile, Codespaces-first,
  folder-per-module)
- `docs/run-of-show.md`, `docs/teardown.md`, `docs/prework-email.md`: instructor
  and logistics docs
- `slides/`: Marp instructor deck and Excalidraw/SVG diagrams
- `artifacts/pre-distilled-skill/SKILL.md`: module 5 fallback when live NAMS
  distillation is unavailable (`make s5-fresh-agent WITH_SKILL=fallback`)

## Style

- Python 3.11+, ruff rules `E,F,I,UP,B`, line length 100.
- Code is teaching material. Keep it readable and explicit, with short module
  docstrings that say what the file is for. Readability beats cleverness.
- Keep participant-facing text (READMEs, `make` output, UI copy) short and
  accurate. Every `make` target should run with no extra flags beyond
  `MODULE=N` or `WITH_SKILL=`.
