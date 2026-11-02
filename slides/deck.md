---
marp: true
theme: default
---

# Road to Agent Memory

- From stateless chatbot to an agent that learns
- A Neo4j Labs workshop · 2.5 hours · live
- Built on `neo4j-agent-memory` + your own AuraDB instance
- Running scenario: **Acme Cloud**, a fictional SaaS support desk

<!-- notes: Welcome everyone. This is a workshop about giving agents memory — not in the abstract, but by running a complete support-agent app and watching its memory graph grow layer by layer. Everything you'll touch today runs against your own [glossary: Neo4j/AuraDB] instance, so what you build is yours to keep poking at after the session. -->

---

# What you'll leave with (an honest promise)

- Format is **run-and-explore**: you'll run a complete app, explore its graph, and answer guided questions — not write code from scratch
- A working full-stack agent app on **your** AuraDB, with three memory layers added one at a time
- A mental model: short-term / long-term / reasoning memory in one knowledge graph
- An eval scoreboard that proves each layer landed
- A ~20-minute path to add the same memory to your own agent on Monday

![diagram](../slides/diagrams/d02-three-memory-types.svg)

<!-- notes: Setting expectations honestly: nobody is typing out an app from scratch today. You'll run scripted scenarios via make targets, explore the graph they produce, and answer guided questions — the learning is in the exploring. If you fell behind at any point, `make module-N` is the one-command catch-up lane. [glossary: agent] -->

---

# Agenda (150 min + buffer)

- **M0** Setup — 15 min · **M1** The stateless agent — 15 min
- **M2** Short-term memory — 25 min
- **M3** Long-term memory — 40 min (the big one)
- **M4** Reasoning memory — 25 min · **M5** Skill distillation on NAMS — 20 min
- Wrap + Monday-morning path — 5 min

<!-- notes: Module 3 gets the most time because long-term memory — entities, ontologies, hydration — is where the most concepts land. Module 4 exploration is the designated trim zone if we run long; there's a 5-minute buffer after module 3. Every module ends with an exploration brief, so keep the app open. [glossary: ontology] -->

---

# The workshop arc

![diagram](../slides/diagrams/d03-workshop-arc.svg)

- Every module: **demonstrate a failure → add one memory layer → re-run the same scenario**
- Scripted scenario beats are `make` targets — deterministic, no live typing
- Continuity thread: the same eval questions asked at every module
- The colors on this ladder recur all day — they're the workshop's visual grammar

<!-- notes: This ladder is the whole day. We start with an agent that forgets everything, and each module adds exactly one memory layer that fixes exactly one failure — and we prove it by re-running the same scenario and the same eval questions. Watch the colors: green is short-term, orange is long-term, purple is reasoning, blue is a store. [glossary: short-term memory] [glossary: long-term memory] [glossary: reasoning memory] -->

---

# Module 0 — Your environment

![diagram](../slides/diagrams/d04-environment-map.svg)

- **Codespaces-first**: the README badge opens a prebuilt 4-core / 8 GB devcontainer
- Your Codespace talks to: your AuraDB (Bolt), OpenAI, and (module 5) NAMS
- Credentials: AuraDB in `.env`, `OPENAI_API_KEY` as a personal Codespaces secret
- Fallback: local clone + VS Code Dev Containers — same `.devcontainer/` config

<!-- notes: Everything is prebuilt — dependencies were installed when the prebuild ran, not just now. The only thing the codespace doesn't have is your credentials, because they're yours. Take a moment to orient: the terminal, the `.env` file, and the forwarded ports. [glossary: Neo4j/AuraDB] [glossary: Bolt] [glossary: NAMS] -->

---

# Module 0 — Credential checklist

- `.env` was scaffolded from `.env.example` on codespace creation
- Add: `NEO4J_URI` / `NEO4J_USERNAME` / `NEO4J_PASSWORD` from your free AuraDB instance
- `OPENAI_API_KEY` arrives automatically if you stored it as a personal Codespaces secret (pre-work)
- `NAMS_API_KEY` (`nams_…`) — needed only in module 5, also from pre-work
- Pre-work email has the step-by-step if anything is missing

<!-- notes: Three credentials, three different homes: AuraDB connection details go in `.env`, the OpenAI key should already be present as a personal secret, and the NAMS key only matters at module 5. If `make check` disagrees in a moment, that's the first thing to look at. [glossary: Neo4j/AuraDB] [glossary: NAMS] -->

---

# Module 0 — Smoke test, live

- Live demo: `make check` — env vars present, AuraDB reachable, OpenAI key valid, SQLite seeded
- Live demo: `make dev` — FastAPI + Vite together; the UI auto-opens (port 5173)
- Tour the three panels: **chat** · **graph** · **trace**
- Lost later? The answer to "what do I run now?" is always a `make` target

<!-- notes: Run `make check` now — everyone should see a green checklist; this exact command was also your pre-work verification. Then `make dev` and tour the UI: chat on the left, the NVL graph panel, and the trace panel where tool calls will show up. Notice the graph is empty — the first exploration question is: why, and what would have to happen for something to appear? [glossary: tool] [glossary: trace] -->

---

# Module 1 — Two stores, two jobs

![diagram](../slides/diagrams/d01-two-stores.svg)

- **SQLite is the system of record** — accounts, catalog, policies: what the agent *acts on*
- **Neo4j is the memory** — conversations, entities, traces: what the agent *learned while acting*
- Memory doesn't replace systems of record; it captures experience over them
- This distinction runs through the whole workshop — remember it in module 5's drift beat

<!-- notes: This is the most important framing of the day. The agent's business data lives in SQLite and stays there — memory is not a database migration. Neo4j holds what the agent learned by operating: what was said, who was mentioned, what it did and how it went. Two stores, two jobs. [glossary: Neo4j/AuraDB] [glossary: trace] -->

---

# Module 1 — Meet the agent

- Acme Cloud support agent: PydanticAI + FastAPI backend, React + NVL frontend
- Five tools, all parameterized SQL against the seeded `acme_cloud.db`:
  - `lookup_account` · `search_product_catalog` · `fetch_policy`
  - `check_service_status` · `issue_refund` (validates against policy, writes to refunds)
- The agent is competent from the first message — today's failure is **memory**, not capability
- Tool vocabulary deliberately mirrors the ontology labels you'll meet in module 3

<!-- notes: Before we break the agent, appreciate that it works: it can look up accounts, search the catalog, quote policy, check service status, and even issue refunds. The seed data is rich enough that every tool returns real results immediately. So when it fails in a moment, notice carefully *how* it fails. [glossary: PydanticAI] [glossary: tool] [glossary: ontology] -->

---

# Module 1 — The failure: statelessness

- Every model run starts without prior messages—even inside the same visible chat.
- Use one self-contained account lookup, then ask for the email without a lookup.
- SQL knowledge is available through tools; previous dialogue is not model memory.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 1 — Live demo: the stateless baseline

- Run `make s1-baseline`.
- Refresh graph and choose Saved replay to inspect CLI results.
- Browser chat has its own conversation and retained turn history.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 1 — The eval baseline

- Run `make eval MODULE=1`.
- Four controlled fixtures: exact identity, unique phrase, grounded date, recorded reply.
- Private SQL, unique memory, no business tools; exact facts and source IDs required.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 2 — Concept: short-term memory

- Conversations and messages become graph data — `:Conversation` → `:Message` chains
- **Short-term ≠ temporary**: it survives restarts; it's scoped to a conversation
- `MemoryClient` on the Bolt backend, against your AuraDB
- `add_message` on every turn; `get_context` retrieved per request
- Context is injected into PydanticAI dynamic instructions

<!-- notes: Short-term memory is the first layer, and the naming trips people up: it's not temporary — it survives killing the app — it's *scoped*. The boundary is the conversation, and question 5 in your exploration brief probes exactly that boundary. Mechanically it's simple: write every message, read context back on every request. [glossary: Bolt] [glossary: PydanticAI] [glossary: graph/node/edge] -->

---

# Module 2 — Message chains in the graph

![diagram](../slides/diagrams/d06-message-chains.svg)

- Each `:Message` node carries role, timestamp, embedding, metadata
- Messages link sequentially within a conversation — the NVL panel shows chains appear live
- The graph panel is your microscope: everything we claim, you can see
- First NVL moment of the day: memory you can point at

<!-- notes: After the demo, find your own conversation in the graph panel. Follow the chain, click a message node, look at its properties — role, timestamp, the embedding that powers search. This is the pattern for the whole workshop: every capability claim comes with a graph you can inspect to verify it. [glossary: graph/node/edge] -->

---

# Module 2 — Context assembly

- Local `build_context`: newest ten prior conversation messages plus scoped semantic user messages.
- Exclude the current turn, repeated questions and duplicate statements.
- Inspect evidence IDs and recent_conversation / semantic_message paths. Bolt does not provide hosted reflections/observations here.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 2 — Live demo: the returning customer

- `make s2-return` first continues the same session, then compares a new one.
- Choose Saved replay; browser chat remains separate.
- Run `make eval MODULE=2`; explain retrieved sources.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 2 — The restart beat

- `make s2-restart` launches two separate Python processes using one session and namespace.
- Inspect the saved process IDs and recovered unique phrase.
- This command does not kill the browser backend.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 2 — Exploration brief

- Core questions (do these first):
  1. Find your conversation in the graph — how are messages linked, what properties does a `:Message` carry?
  2. What survived the restart — trace exactly which records made it possible?
  3. Search with a paraphrase — which search path answered, vector or text?
- Stretch questions + answer key: module 2 README
- Fell behind? `make module-2` reproduces this module's state

<!-- notes: You have about ten minutes. Do the three core questions; the stretch ones — including the context-tiers question and the all-important "what's the boundary of short-term memory" — are in the README with an answer key. Question 5's answer is the motivation for the next module, so if you get there, you're ahead of me. [glossary: graph/node/edge] -->

---

# Module 3 — Concept: long-term memory

- Messages say what was said; **entities** say who and what the conversation is *about*
- New session, new conversation — and the agent knows *who the customer is*: plan, products, preferences
- Entity extraction with a **custom domain ontology**, LLM-based, temperature 0 (ADR 001)
- Memory tools join the tool set: `save_preference`, `recall_preferences`, `search_memory`
- 40 minutes — the deepest module of the day

<!-- notes: Module 2's boundary question set this up: when the customer returns tomorrow in a new conversation, what crosses over? The answer is a second memory layer — long-term entities, preferences, facts — that lives above individual conversations. This module has the most concepts, so we've tiered the exploration questions: four core, three I'll demo live, the rest are stretch. [glossary: extraction] [glossary: ontology] [glossary: entity resolution] -->

---

# Module 3 — Ontology-driven extraction

- Edit `module_3/ontology/acme_cloud.yaml`: types, relations, aliases and annotation descriptions.
- The app drops invalid relations in both modes; strict also drops undeclared entity types.
- Run `uv run scripts/instructor.py strict` for the explicit drop/raise validator recipe.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 3 — Before / after: default vs. custom ontology

- `make s3-default` and `make s3-ontology` use the same fixed transcript.
- Independent extractor calls; no chat history, SQL hydration or shared graph inputs.
- Compare transcript hashes, types and edges in Saved replay snapshots. Temperature zero does not guarantee identical output.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 3 — The hybrid pipeline (the design-principle slide)

- LLM supplies entity spans, types and relations.
- SQLite supplies Customer email, plan and signup_date through type-safe hydration.
- Optional Wikimedia supplies public Organization facts, with visible provider status.
- Company knowledge is not current operational status.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 3 — Entity resolution & aliases

![diagram](../slides/diagrams/d11-entity-resolution.svg)

- The customer says "AcmeCloud" after earlier saying "Acme Cloud" — one node, not two
- Aliases are declared in the ontology; resolution is evidence you can see in the graph
- `add_entity` MERGEs on `(name, type)` — hydration **updates in place**, never duplicates
- Typed edges carry `support`, `confidence`, `source_message_ids` — find one with `support >= 2`

<!-- notes: Near-duplicates are where naive extraction pipelines rot. The alias declaration means "AcmeCloud" and "Acme Cloud" resolve to one node, and the MERGE-on-name-and-type upsert means hydration enriches the same node instead of forking it. While you explore, find an edge with support of 2 or more — that's the same relation observed in two different messages, and it's a signal worth understanding. [glossary: entity resolution] [glossary: hydration] [glossary: provenance] -->

---

# Module 3 — Live demo: watch the graph bloom

- Compare each immutable extraction snapshot through Saved replay.
- In browser chat introduce Maya; inspect MENTIONS and SQL-grounded fields.
- `make s3-enrich` is optional; continue if the provider is unavailable.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 3 — Under the hood: hydration & enrichment

- Current-message extraction → pooled SQL hydration → context → answer.
- Skip incompatible types and ambiguous aliases; expose structured grounded facts and IDs.
- Explicit Wikimedia workflow: one-week success cache, five-minute error cache; no fictional-company background lookup.
- A 403 is unavailable, not a reason to wait for properties.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 3 — Exploration brief (40-min module, tiered)

- Core Q1 source MENTIONS; Q2 fixed snapshots; Q3 Customer sources; Q4 changes since module 2.
- Instructor Q5 negative descriptions; Q6 strict recipe; Q7 private plan-upgrade and rollback.
- Stretch: save and recall a customer-scoped preference; inspect the actual receipt.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 4 — Concept: reasoning memory

- Record actual execution: task, steps, tool calls, exact reply and outcome.
- Open before execution; complete on success or exception.
- A declined business request differs from a failed execution. Prior procedures are examples, not current policy.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 4 — Anatomy of a trace

- ReasoningTrace → HAS_STEP → ReasoningStep → USES_TOOL → ToolCall → INSTANCE_OF → Tool.
- Outcome and exact reply are trace properties, not a separate Outcome node.
- Trace INITIATED_BY Message; Step TOUCHED case Customer and Plan.
- Tool receipts show actual SQL, including validation reads and performed writes.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 4 — Similar-task retrieval

- Retrieve bounded full steps, tool inputs/results and the exact stored outcome with IDs.
- Current SQL policy governs every action in both branches.
- The ablation uses identical private SQL copies, separate message scopes and one frozen corpus; branch recording is disabled.
- Measure evidence, safety, calls, tokens and timing. Better results are not guaranteed.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 4 — Live demo: the refund, twice

- `make s4-refund`; `make s4-fail`; `make s4-refund-repeat`.
- Confirm account, case and action per turn. SQL validates identity, amount, policy and uniqueness.
- The reject-only server guard records an over-limit case without issuing or escalating it.
- Inspect actual tools; a three-call chain is illustrative, not guaranteed.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 4 — The provenance question

- Why did you issue that refund?
- Trace → INITIATED_BY → message; Step → TOUCHED → Customer / Plan.
- Inspect the operation receipt, exact SQL and current policy. This is an execution record.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 4 — Exploration brief

- Reconstruct actual steps, tools and business result.
- Compare retrieved evidence and measured behavior; identical outcomes are possible.
- Distinguish declined policy outcome, model exception and degraded persistence. Inspect warnings and receipts before retrying.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Module 5 — Skill distillation

<!-- SCREENSHOT PLACEHOLDER: m5-skill-subgraph — captured via scripts/capture_screenshots.py -->

- From memory to **portable skills**: distillation reads the accumulated refund-procedure memory
- Output: a **SKILL.md** artifact + a skill subgraph in the graph
- Every claim carries `GROUNDED_IN` edges back to the exact traces, tool calls, and entities that justify it
- **Grounding and coverage scores** tell you how much of the skill is backed by evidence

<!-- notes: Module 5 turns accumulated experience into a portable artifact. Distillation reads the traces and entities and produces a skill — a SKILL.md a fresh agent can load — where every step is grounded in evidence via GROUNDED_IN edges, with scores to prove it. A low-grounding step is a step you shouldn't trust, and you'll see one if you look. [glossary: distillation] [glossary: grounding/coverage] [glossary: trace] -->

---

# Module 5 — The seam, made explicit

- Your Bolt memory from modules 1–4 lives in **your AuraDB** — untouched by this module
- NAMS is a **fresh, managed workspace** at memory.neo4jlabs.com — a separate memory
- Live demo: `make nams-seed` loads the canonical reasoning history into NAMS (~1 min)
- Why the seam? Distillation + governance are NAMS capabilities today — the boundary is **taught, not discovered**

<!-- notes: Let's be explicit about the boundary you're crossing. Everything you built so far is in your own AuraDB over Bolt, and it stays there. NAMS — the hosted Neo4j Agent Memory Service — is a separate managed workspace; the seed script loads the canonical refund-procedure history into it so the whole room distills the same memory. You're not migrating anything; you're seeing the hosted consumption model on a clean, known-good dataset. [glossary: NAMS] [glossary: Bolt] -->

---

# Module 5 — Live: seed → distill → the fresh-agent payoff

- Live demo: `make nams-check` — key + workspace verified (signup was pre-work)
- Live demo: `make nams-seed` → `make nams-distill` — skill generated over the seeded memory
- Inspect: SKILL.md, the skill subgraph, `GROUNDED_IN` edges, grounding/coverage scores
- **The payoff:** Live demo: `make s5-fresh-agent` — a fresh agent, no history, loads the skill and resolves the refund ticket **cold** (control run: without the skill)

<!-- notes: This is the climax of the workshop. A brand-new agent — no session history, no prior traces — loads the distilled skill and handles the refund correctly on day one. One agent's experience has become everyone's skill: procedural knowledge as a portable, versioned artifact instead of something trapped in one workspace. If NAMS hiccups, `make s5-fallback` loads the pre-distilled skill from the repo. [glossary: distillation] [glossary: grounding/coverage] [glossary: NAMS] -->

---

# Module 5 — The governance loop: drift, made concrete

![diagram](../slides/diagrams/d15-governance-loop.svg)

- Live demo: `make policy-change` — flips the refund limit in **SQLite** → governance flags… **nothing**
- The honest boundary: governance watches the **memory graph**, not your system of record
- Live demo: `make nams-drift` — ops retires the policy; the **entity is deleted** → `GROUNDED_IN` claims lose their sources → drift fires
- Live demo: `make nams-redistill` — the loop closes

<!-- notes: The drift beat is two steps, and the first step is deliberately disappointing: change the refund limit in SQLite and governance says nothing — it watches the memory graph, not your database, and knowing that boundary is the lesson. Then delete the refund-policy entity from the workspace memory and watch the skill's grounded claims lose their evidence. Re-distillation completes the loop. [glossary: distillation] [glossary: grounding/coverage] [glossary: provenance] -->

---

# Module 5 — Labs / early-access disclosure

- NAMS is **Neo4j Labs**: experimental, community-supported, **no SLA** — not for production
- APIs and behavior may change; today's workshop pins versions for a reason
- `neo4j-agent-memory` (modules 1–4, Bolt) is the open-source library you can build on now
- Teardown at the end: revoke the `nams_` key, delete the codespace, pause/delete AuraDB — `docs/teardown.md`

<!-- notes: Honest positioning: everything in modules 1 through 4 runs on the open-source library against your own database — that's the part to build on. NAMS is early-access Labs software; treat module 5 as a preview of where managed agent memory is going, not a production commitment. The teardown doc walks through cleaning up every resource you touched today. [glossary: NAMS] [glossary: Bolt] -->

---

# Module 5 — Exploration brief

- Core questions:
  1. Follow a `GROUNDED_IN` edge from a SKILL.md claim back to its evidence
  2. What do grounding and coverage scores tell you — would you trust a low-grounding step?
  3. Drift beat: what did `make policy-change` flag vs. `make nams-drift` — and why the difference?
- Stretch: skill vs. runbook vs. raw trace; who else could load this skill? — module 5 README
- Fell behind? `make module-5`

<!-- notes: The exploration here is short but dense. The grounding-edge walk is the core skill — being able to audit a distilled claim back to evidence is the whole governance story. And the full-circle question is worth a minute of thought: which of the three memory types did distillation draw on, and which store changed in the drift beat — SQLite or Neo4j? [glossary: grounding/coverage] [glossary: distillation] -->

---

# Wrap — The eval scoreboard, re-run

- Run `make eval MODULE=N` explicitly.
- Exact name/email and phrase: seeded messages. Signup date: grounded fixture. Exact reply: trace fixture.
- Private SQL, unique memory, no business tools. Inspect source IDs; this is a retrieval probe, not an end-to-end quality grade.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->

---

# Wrap — One knowledge graph

<!-- SCREENSHOT PLACEHOLDER: wrap-recap — captured via scripts/capture_screenshots.py -->

- Three memory types — **short-term / long-term / reasoning** — one knowledge graph
- Green = short-term · orange = long-term · purple = reasoning · blue = stores
- Messages, entities, traces, and the skill subgraph — connected, queryable, auditable
- Memory isn't a feature bolted on; it's a graph that grows with every interaction

<!-- notes: Step back and look at the whole canvas: everything the agent experienced today lives in one connected graph — conversations linked to the entities they mention, traces touching the entities they depended on, a skill grounded in the traces that justify it. That's the answer to "why a graph for agent memory?" — the layers aren't three databases, they're one structure. [glossary: graph/node/edge] [glossary: distillation] -->

---

# Wrap — Bolt vs. NAMS: when to choose which

![diagram](../slides/diagrams/d18-bolt-vs-nams.svg)

- **Bolt (modules 1–4):** your AuraDB, client-side extraction, you operate it — the open-source path
- **NAMS (module 5):** managed service, server-side extraction, distillation + governance — Labs preview
- Same concepts, same memory types — different consumption model
- Start with Bolt; watch NAMS for managed distillation and governance

<!-- notes: The honest trade-off slide. Bolt gives you control: your database, your extraction config, your data residency — and it's what the open-source library ships today. NAMS trades control for operations: managed extraction, and the distillation and governance capabilities you just saw. The concepts transfer completely either way. [glossary: Bolt] [glossary: NAMS] -->

---

# Wrap — Your Monday morning path (~20 min)

- Use the pinned `neo4j-agent-memory[pydantic-ai,openai]` environment and set Bolt/OpenAI credentials.
- Construct `MemoryClient(MemorySettings(...))`.
- Run `uv run scripts/monday_memory.py` to connect, write and retrieve.
- Inject retrieved context into your agent instructions before the next model call.

<!-- notes: Follow docs/run-of-show.md and the corresponding participant guide. Show measured evidence; do not promise a particular model response. -->
