# ADR 004: Complete agent snapshots in each workshop module

- **Status:** Accepted; implementation clarified 2026-11-01
- **Original decision:** 2026-10-27
- **Context:** Participants need to read and compare each stage's complete agent.

## Decision

Every `module_N/` owns its agent construction, instructions, business-tool
definitions, chat orchestration, and the memory behavior introduced by that stage.
This duplication is intentional. No lesson imports or inherits another lesson's
agent, and no shared implementation enables features by comparing module numbers.

| Stage | Local implementation |
| --- | --- |
| 1 | Stateless agent and five business tools |
| 2 | Conversation/message persistence and short-term context |
| 3 | Local ontology variants, LLM extraction, memory tools and SQL-grounded hydration |
| 4 | Similar-task retrieval and recorded executions, including tool rejections |
| 5 | Complete reasoning-enabled support agent plus a separate fresh skill-consuming agent and NAMS workflows |

`app/agent.py` is the reading entry point in every folder. `app/tools.py` is also
local: registering and implementing tools is part of understanding an agent.
`app/guardrails.py` (refund and reply safety) is local too but identical in every
module, so it never appears in a stage diff. Experiments run by make targets but
not used by the agent live in `module_N/lab/`. The HTTP response envelope and
request receipts are shared transport in `lib/response.py` and `lib/operations.py`.
`app/memory.py` appears in module 2; `memory_tools.py`, `hydrate.py`, and local
`ontology/` files appear in module 3. Module 5 owns `app/fresh_agent.py` and
`workflows/{check,seed,distill,drift}.py`.

Each folder has a README with a reading order, commands, verification steps, and a
summary of the change from the previous lesson. For example:

```bash
diff -ru module_2/app module_3/app
```

## Shared infrastructure and state

The React frontend, root Makefile, dependency locks, configuration/credentials,
SQLite schema and query helpers, graph serialization, and HTTP transport remain
shared. They implement infrastructure, not agent prompts or memory policy.

One root `.env`, virtual environment, `data/acme_cloud.db`, and participant AuraDB
carry across stages. Run all Make commands from the repository root. To switch:
Ctrl+C the old server, `make dev MODULE=N`, then reload the browser. No branch
checkout or directory change is required.

`make module-N` replays the selected beats for that stage. It does not switch the
server, reconstruct every previous stage, clear memory, or restore a checkpoint.
Scenario playback runs an independent agent in-process; it prints chat/tool output
in the terminal and writes to the shared memory database. The browser graph needs
reloading or a filter change to observe those writes.

## Interface used by workshop tooling

Each lesson exposes `open_agent(settings, ...)`, an async context manager owning its
agent and connection lifetime. The agent supplies `chat(message, session_id)`,
`module`, `memory_layers`, and its memory handle for graph inspection. Chat keeps
the existing frontend response shape.

`lib/workshop.py` validates and dispatches the module requested by CLI tools.
The HTTP entry point imports its local factory directly. HTTP, scenarios and eval
therefore exercise the same lesson implementation. Shared dispatch contains no
agent behavior. Root NAMS scripts are compatibility CLI wrappers around module 5.

Ontology selection belongs to modules 3–5. `acme_cloud` and `default-poleo` load local
files; `active` opts into the version stored in AuraDB. A file explicitly overrides
the active database version. Module 4's retrieval toggle is an experimental control,
not a progression switch; turning it off disables both automatic and tool-based
reasoning retrieval while recording continues.

## Alternatives and trade-offs

A single shared agent with stage flags minimized code duplication but hid the
workshop's subject behind conditionals. Inheritance from previous stages would also
force participants to leave their lesson to reconstruct the complete implementation.
Runtime generation and symlinked agent files have the same teaching problem.

The accepted cost is maintaining explicit copies of prompts, tools and memory code.
Preserve consistent organization and formatting across copies so diffs show the
concept being added. Test each stage's behavior; do not require all copies to remain
identical, since their differences are the teaching material.

## Verification

Offline tests run real PydanticAI agent loops with deterministic model and memory
adapters, verify tool-backed SQL behavior and hydration, exercise the HTTP routes,
and check scenario/eval dispatch. Tests also guard against cross-lesson imports and
calls into removed shared agent implementations.

Live rehearsal is opt-in, uses temporary SQLite data and unique conversation IDs,
and never resets existing graph data. The NAMS seed/lifecycle needs its own
configured-workspace verification; mocked HTTP choreography is not evidence of
hosted-service parity.


## 2026-11-01 workflow clarification

Browser chat, conversational replay and controlled eval select the local lesson
factory. Two deliberate teaching exceptions apply: `s2-restart` launches two
separate Python processes around the same persisted conversation, and the module-3
default/custom pair calls independent extractors on a fixed transcript, without
running the agent or hydration. The module-4 ablation disables new extraction and
hydration in both branches as well as branch trace recording, preventing shared
canonical entities from transferring control writes into treatment context. The
SQL-selected case facts remain identical inputs to both business agents.
