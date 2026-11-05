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
4. `make check` → all green? `make dev` → the UI opens automatically. If a pop-up
   blocker stops it, open the **Ports** tab and click the globe icon next to port 5173.

**Local fallback:** VS Code Dev Containers (`Reopen in Container`) or manual setup
(`uv sync && npm --prefix web ci && make seed && make dev`).

## The workshop

| Module | Story | Eval score |
|---|---|---|
| 0 — Setup | Boot the app, meet the two stores (SQLite = system of record, Neo4j = memory) | — |
| 1 — The Stateless Agent | The agent forgets everything | 0/4 |
| 2 — Short-Term Memory | It remembers the conversation, even after a restart | 2/4 |
| 3 — Long-Term Memory | It knows *who the customer is* | 3/4 |
| 4 — Reasoning Memory | It remembers *how it solved this before* | 4/4 |
| 5 — Skill Distillation | One agent's experience becomes everyone's skill | — |

Per-module guides with exploration questions and answer keys are in
[docs/modules/](docs/modules/); the instructor timing is in
[docs/run-of-show.md](docs/run-of-show.md). New to graphs or agents? Start with
[docs/glossary.md](docs/glossary.md).

### How to work: two terminals and the website

Run every command from the repository root.

- **Terminal 1 runs the app:** `make dev MODULE=N` starts module N's agent (:8000)
  and the website (:5173). Leave it running.
- **Terminal 2 runs the module's commands** (scenarios, eval, NAMS workflows).
- **Switching modules:** Ctrl+C in terminal 1 → `make dev MODULE=<next>` → reload
  the browser. The website is the same for every module; it shows whichever agent
  is running.

Terminal scenarios and browser chat are two separate ways to drive the agent:

- **Terminal scenarios** (`make s2-return`, …) replay a fixed script and print the
  dialogue, tools called, memory used and timing. They do not appear in the browser
  chat. To inspect one, click **Refresh graph** and pick it in the graph-view
  dropdown:
  - **Saved replay · <name> · <time>**: the recorded output, with tool calls and
    the SQL they executed.
  - **Live memory · <name> · <session>**: the nodes that run actually wrote to Neo4j.
- **Browser chat** is where you try things yourself. The toolbar controls:
  - **New conversation / Resume**: start or return to a conversation.
  - **Customer**: who is speaking (needed to save preferences).
  - **Billing case** + **Authorize selected refund for this message**: both are
    required before any refund. The checkbox resets after every message.
  - **Policy question**: ask about a plan's rules without acting on an account.
- **Memory graph** (right): Current conversation / All stored memory / Saved replay /
  Live memory, a layer filter (short term · long term · reasoning) and
  **Refresh graph** / **Fit graph**. Module 5 adds a **NAMS** checkbox.
- **Execution evidence** (bottom): each browser turn's tool calls, executed SQL,
  retrieved memory and business result.
- **Evaluation lab** (top right): the latest `make eval` result for this module, or
  start a new isolated run.

### Module 0 — Setup

| Command | What it does |
|---|---|
| `make check` | Checks `.env`/secrets, SQLite, AuraDB (with time per query), OpenAI and memory startup |
| `make dev MODULE=1` | Starts module 1; the website opens in your browser |

### Module 1 — The stateless agent

| Command | What it does |
|---|---|
| `make s1-baseline` | Turn 1 gives Maya's email and looks up her account; turn 2 asks "what email did I give you?" and the agent cannot say |
| `make eval MODULE=1` | Controlled retrieval scorecard: 0/4 |

**In the website:** open the `s1-baseline` Saved replay, then try the same two
messages in chat. The graph reads "Module 1 is stateless."

### Module 2 — Short-term memory

| Command | What it does |
|---|---|
| `make dev MODULE=2` | (Terminal 1) restart on module 2, reload the browser |
| `make s2-return` | Recalls a phrase in the same conversation, then from a *new* conversation via semantic search |
| `make s2-restart` | The same conversation across two separate Python processes: memory survives a restart |
| `make eval MODULE=2` | 2/4 |

**In the website:** chat, then click **New conversation** and ask again. The graph
shows Conversation → Message chains; the evidence panel separates
`recent_conversation` (sent to the model as message history) from `semantic_message`.

### Module 3 — Long-term memory

| Command | What it does |
|---|---|
| `make dev MODULE=3` | (Terminal 1) restart on module 3, reload the browser |
| `make s3-default` | Extracts entities from a fixed transcript with the generic POLE+O ontology and prints them (no graph writes) |
| `make s3-ontology` | The same transcript with the Acme Cloud ontology: Customer / Plan / Incident types and domain relations |
| `uv run scripts/instructor.py strict` | Guided: permissive vs strict ontology validation |
| `uv run scripts/instructor.py plan` | Guided: a plan change in SQLite re-hydrates the same entity |
| `make s3-enrich` | *(optional)* Looks up Stripe on Wikipedia |
| `make eval MODULE=3` | 3/4 |

**In the website:**
1. Compare the two **Saved replay · Extractor only** snapshots.
2. In chat, introduce yourself as Maya Chen from Northwind Robotics. The graph shows
   Message -MENTIONS-> entities, with facts (email, plan, signup date) copied from SQLite.
3. Select **Customer = Maya Chen**, ask SupportBot to save a contact preference, then
   ask what preferences it has on file.

### Module 4 — Reasoning memory

| Command | What it does |
|---|---|
| `make dev MODULE=4` | (Terminal 1) restart on module 4, reload the browser |
| `make s4-refund` | An authorized $49 refund, recorded as a ReasoningTrace |
| `make s4-fail` | A $400 over-limit refund, rejected by the server guard (a valid outcome, not an error) |
| `make s4-refund-repeat` | Ablation: the same tickets with past-execution retrieval off vs on, on identical SQLite copies |
| `make eval MODULE=4` | 4/4 |

**In the website:**
1. **Saved replay** shows receipts and SQL; **Live memory** with the **reasoning**
   layer shows Trace → Step → ToolCall → Tool.
2. Try a refund in chat: choose Customer and Billing case, tick **Authorize**, send.
3. Ask for the same refund again: it is refused with the existing receipt.

### Module 5 — Skill distillation (NAMS)

| Command | What it does |
|---|---|
| `make dev MODULE=5` | (Terminal 1) restart on module 5, reload the browser |
| `make nams-check` | Verifies your NAMS key and that distillation is enabled |
| `make nams-seed` | Writes canonical refund history and traces to your hosted NAMS workspace (separate from AuraDB) |
| `make nams-distill` | ~1 min: distills, approves and publishes a skill; downloads `artifacts/distilled/SKILL.md` |
| `make s5-fresh-agent WITH_SKILL=off` | Control: a brand-new agent with no memory and no skill |
| `make s5-fresh-agent WITH_SKILL=on` | The same agent with the skill follows the procedure: account → policy → refund |

`make s5-fresh-agent WITH_SKILL=fallback` uses the checked-in skill if NAMS is unavailable.

**Governance (instructor-led, follow along):**

| Command | What it does |
|---|---|
| `make policy-change` | Changes the Pro refund limit in SQLite; NAMS still reports the skill "current" (the blind spot) |
| `make nams-drift` | Deletes the policy entities the skill is grounded in; NAMS flags it "drifted" and lists stale claims |
| `make nams-redistill` | Distills a new skill version and diffs `SKILL.md` |
| `make policy-change` | Run again to restore the $250 limit |

**In the website:** tick **NAMS** to see Skill → versions → steps → the memory each
step is grounded in. Open `artifacts/distilled/SKILL.md` in the editor.

### Wrap-up

`uv run scripts/monday_memory.py` is the take-home recipe: write a message to
memory and read it back with your own credentials.

### Other commands

- `make module-N` replays that module's scenarios to catch up. It does not switch
  the server or restore a checkpoint.
- `make help` lists every target. `make clean` removes build caches.
- `make reset-memory` wipes the Neo4j memory graph (asks to confirm); you should not
  need it.

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

## Verify

```bash
uv run pytest tests/ -m "not behavioral" -q
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

The second command uses configured Neo4j and OpenAI services, writes uniquely named
workshop conversations, and uses temporary SQLite data. It never resets the graph.
The NAMS workflow tests follow the published API contract; run the module 5 make
targets with your key to rehearse against the hosted service.

See the [module evaluation report](docs/module-evaluation.md) for the verified
behavior of each stage and the remaining live-service checks.

## Status

Workshop materials for a Neo4j Labs project — experimental, community-supported, no
SLAs. See [docs/teardown.md](docs/teardown.md) for post-workshop cleanup.

