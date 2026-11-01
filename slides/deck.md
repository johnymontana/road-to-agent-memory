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

![diagram](../slides/diagrams/d05-statelessness.svg)

- Customer reports an issue, "returns" in a new chat → the agent asks who they are again
- Restart the app mid-conversation → context gone
- Every session starts from zero; two identical sessions have no bridge between them
- Nothing in the tool set can fix this — the failure is architectural, not a missing tool

<!-- notes: Here's the failure mode in its natural habitat. The scenario scripts are engineered so the tools *can't* rescue the agent — the customer never states their email until a memory layer exists to remember it. When you watch this, pay attention to how much the agent learned during the conversation and where exactly that learning goes when the chat ends. [glossary: agent] -->

---

# Module 1 — Live demo: the stateless baseline

- Live demo: `make s1-baseline` — the billing-issue scenario, run end to end
- Then "return" in a new chat as the same customer — watch the agent ask who you are
- Watch the trace panel: what SQL ran against SQLite? What did the agent learn?
- Where does that learning go when the process exits?

<!-- notes: Run `make s1-baseline` and let it play out, then start a fresh chat and come back as the same customer. The trace panel shows every tool call with its SQL — the agent clearly *did* things. But ask it what it learned and the answer is nothing: the learning evaporated with the session. [glossary: trace] [glossary: tool] -->

---

# Module 1 — The eval baseline

- Live demo: `make eval` — prints the continuity scorecard (from here on, every module)
- Four fixed questions asked at every module: *"Do you know who I am? / What did we discuss last time? / What do you know about my account? / Have you handled a ticket like this before?"*
- Each question becomes answerable at exactly one module boundary
- Today's arc, in one picture: turning this board green

<!-- notes: This scorecard is the workshop's continuity thread. Right now the board is mostly red — the stateless agent can't answer any of these, and it *shouldn't* be able to. Each question was chosen so it becomes answerable at exactly one module, so the scorecard tells you which memory layer unlocked which capability. Keep this output in mind at wrap time. -->

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

![diagram](../slides/diagrams/d07-context-assembly.svg)

- `get_context` → assembled into dynamic instructions → the model call
- Three tiers: **reflections / observations / recent messages**
- Message search: ask with a paraphrase — which path answered, vector or text?
- The agent now assembles its own relevant past, per request

<!-- notes: Retrieval isn't just "the last N messages." There's a tiered context model — reflections, observations, recent messages — and your exploration questions ask you to figure out what distinguishes them and when each matters for a support agent. The paraphrase search question is the fun one: say something in different words and work out which search path found it. [glossary: PydanticAI] -->

---

# Module 2 — Live demo: the returning customer

- Live demo: `make s2-return` — the customer returns in a **new chat**
- The agent continues where it left off — no "who are you?"
- Find the new conversation in the graph panel; how does it relate to the old one?
- Run the eval questions — which ones flipped?

<!-- notes: Same customer, brand-new chat session — and this time the agent picks up the thread. Notice what crossed over from the previous conversation and what didn't; that boundary is the whole point of module 3 coming up. Re-run `make eval` if you want the scorecard delta right now. [glossary: agent] -->

---

# Module 2 — The restart beat

- Live demo: `make s2-restart` — the app is **killed mid-conversation**, then restarted
- What does the agent still know? Be precise: which records made that possible?
- Trace the answer in the graph panel, node by node
- This is the beat that makes "short-term ≠ temporary" concrete

<!-- notes: This is the theatrical beat of module 2: we kill the process in the middle of a conversation and bring it back. The agent survives because the memory never lived in the process — it lived in your AuraDB. When you answer the exploration question, name the actual records: which conversation, which messages. [glossary: Neo4j/AuraDB] [glossary: trace] -->

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

![diagram](../slides/diagrams/d08-ontology-extraction.svg)

- `ontology/acme_cloud.yaml`: entity types, typed relationships, aliases, constraints
- The ontology is rendered **into the LLM extraction prompt** — descriptions are annotation guidelines, negative cases included
- Relations the ontology doesn't permit are **dropped at ingest**
- Validate it yourself: `neo4j-agent-memory ontology validate`

<!-- notes: One YAML document does two jobs: it drives what the LLM looks for, and it validates what comes back. Read the entity-type descriptions during exploration — they're written like annotation guidelines, including negative cases like "not the support engineer who answers," and they're rendered verbatim into the prompt. Extraction runs at temperature 0 with structured outputs, so the whole room sees the same graph. [glossary: ontology] [glossary: extraction] [glossary: POLE+O] -->

---

# Module 3 — Before / after: default vs. custom ontology

<!-- SCREENSHOT PLACEHOLDER: m3-before-after — captured via scripts/capture_screenshots.py -->

- `make s3-default`: the default POLE+O template — loosely labeled nodes, no typed relations, bare properties
- `make s3-ontology`: the same scenario with the Acme Cloud ontology — typed edges, precise labels
- Same input, same model, same temperature — the *ontology* is the only difference
- Which graph would you rather build a support workflow on?

<!-- notes: This before/after is the concrete proof that ontology-driven extraction matters. Generic extraction gives you *a* graph; the custom ontology gives you *your* graph — Customer, Product, Plan, Incident, with typed edges like REPORTED and SUBSCRIBES_TO. Hold the two side by side and the value sells itself. [glossary: ontology] [glossary: POLE+O] -->

---

# Module 3 — The hybrid pipeline (the design-principle slide)

![diagram](../slides/diagrams/d10-hybrid-pipeline.svg)

- **LLM → structure**: entity spans, types, typed relations — nothing else
- **SQLite → grounded facts (hydration)**: email, plan, signup date — every fact from the system of record
- **Wikipedia → external knowledge (enrichment)**: real third parties like Stripe, async
- **Structure from the LLM — facts never from the LLM**

<!-- notes: This is the module's centerpiece. The LLM could *infer* an email or plan tier — and it would sometimes be wrong, which is how you get hallucinated facts in a support workflow. So the stock EntityPayload drops attributes and description by design; a hydration hook re-writes the entity with real SQLite data via add_entity upserts, and enrichment adds public knowledge about real organizations. Each source does only what it's actually good at. [glossary: hydration] [glossary: enrichment] [glossary: extraction] -->

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

- Live demo: `make s3-default` — baseline extraction with default POLE+O types
- Live demo: `make s3-ontology` — the same scenario, custom ontology active
- Click a `Customer` node: hydrated properties (email, plan) labeled by **source** in the details panel
- Stretch beat (shown pre-warmed): the `Stripe` node with its Wikipedia enrichment — `make s3-enrich`

<!-- notes: Run both scenarios back to back and watch the NVL panel: the second run blooms with typed entities and edges, plus :MENTIONS edges back to the exact messages that created them. I'll show the enriched Stripe node in passing — enrichment is async and rate-limited, so it's a stretch beat with a screenshot fallback, not a critical-path demo. [glossary: enrichment] [glossary: hydration] [glossary: provenance] -->

---

# Module 3 — Under the hood: hydration & enrichment

- Post-extraction hook: extracted `Customer` → `lookup_account` → `add_entity(description=…, attributes={email, plan, signup_date, …})`
- *All* properties come from SQLite — including categoricals like `plan_tier` and `severity`
- Enrichment: `EnrichmentConfig`, Wikimedia provider, ORGANIZATION-only allowlist, background + cached
- Why this discipline? LLM-invented facts are the failure mode; the schema's dropped `attributes` field tells you how the library's authors think about it

<!-- notes: For those who want the machinery: hydration is a post-extraction hook that calls the same SQLite tools the agent uses and upserts grounded properties — so a plan upgrade in SQLite shows up on the entity on the next run, while name, type, and provenance edges stay put. Enrichment is the opposite direction: public knowledge about real third parties, written asynchronously. [glossary: hydration] [glossary: enrichment] [glossary: provenance] -->

---

# Module 3 — Exploration brief (40-min module, tiered)

- **Core (everyone):** Q1 provenance via `:MENTIONS` · Q2 default vs. custom graph compare · Q9 property sources on a `Customer` node · Q13 what changed vs. module 2
- **Instructor-demoed live:** Q3 negative-case descriptions · Q7 strict vs. permissive validation · Q12 hydration upsert on a plan change
- **Stretch:** the rest — answer key in the module 3 README
- Fell behind? `make module-3`

<!-- notes: Fifteen-plus minutes of exploration. The four core questions take you from provenance to property sources to the eval-question delta; I'll demo the config-edit questions live so nobody has to break their working setup. The strict-vs-permissive question is worth watching — it decides what happens when the LLM emits an entity type the ontology doesn't declare. [glossary: provenance] [glossary: ontology] -->

---

# Module 4 — Concept: reasoning memory

- The agent's **own execution** becomes memory: tasks, steps, tool calls, outcomes
- `record_agent_trace` consumes a PydanticAI `AgentRunResult` — every run recorded
- Similar past traces retrieved to prime the agent on familiar tasks
- **Failures are first-class memory** — a rejected refund teaches as much as an approved one

<!-- notes: Modules 2 and 3 remembered what was said and who was involved. Module 4 remembers what the agent *did* — the procedure, not just the facts. The payoff: a ticket identical in shape to one solved yesterday shouldn't require re-deriving the procedure from scratch. And note the philosophy: failed runs are recorded too, deliberately. [glossary: trace] [glossary: PydanticAI] [glossary: tool] -->

---

# Module 4 — Anatomy of a trace

<!-- SCREENSHOT PLACEHOLDER: m4-trace — captured via scripts/capture_screenshots.py -->

- `AgentStep → ToolCall` chains, ending in an outcome node (success/failure, styled red)
- `:TOUCHED` edges → the entities the agent's decision depended on
- `:TOUCHED` vs `:MENTIONS` — dependency vs. mention; find both and compare
- Tool-call inputs/outputs carry the actual SQL and policy text — tomorrow's distillation material

<!-- notes: Pick a completed trace in the graph and reconstruct the story: what was the task, which tools ran in what order, what was the outcome? The :TOUCHED edges are the subtle part — they record which entities the decision depended on, which is different from merely mentioning them. Keep that distinction; module 5 builds on it. [glossary: trace] [glossary: provenance] [glossary: tool] -->

---

# Module 4 — Similar-task retrieval

![diagram](../slides/diagrams/d13-similar-task-retrieval.svg)

- A new ticket embeds near yesterday's trace — retrieval finds the matching procedure
- Retrieved traces prime the agent: tool order, steps skipped, confidence
- The proof is an **ablation**: the same ticket run with retrieval off (control) vs. on (treatment)
- The trace panel shows the behavioral difference side by side

<!-- notes: Claims about memory helping are cheap; this module proves it with an ablation. The same refund ticket runs twice — once with retrieval disabled as the control, once with it on as the treatment — and you watch the agent's behavior differ: fewer steps, the right tool order, no flailing. That's what "the agent remembers how it solved it" actually means. [glossary: agent] [glossary: trace] -->

---

# Module 4 — Live demo: the refund, twice

- Live demo: `make s4-refund` — first refund ticket; the trace is recorded
- Live demo: `make s4-refund-repeat` — the same-shape ticket: control run, then treatment run
- Watch: `lookup_account` → `fetch_policy("refund")` → `issue_refund` — recalled, not re-derived
- Live demo: `make s4-fail` — an over-limit refund that `issue_refund` rejects: the failed trace

<!-- notes: Three beats. First the original refund, recorded as a trace. Then days later, the same-shape ticket — and we run it with retrieval off and on so the difference is undeniable. Finally the deliberate failure: a refund over the policy limit, rejected by the tool. That failed trace is not a bug in the demo — it's the setup for governance in module 5. [glossary: trace] [glossary: tool] -->

---

# Module 4 — The provenance question

- Ask the agent: **"Why did you issue that refund?"**
- Trace the answer: final outcome → steps → tool calls → the `fetch_policy` result the decision relied on → the customer's original message
- This is the eval question modules 2–3 couldn't answer
- Reasoning memory turns "the agent did a thing" into an auditable story

<!-- notes: This is my favorite question of the day. Before reasoning memory, the agent's behavior was a black box; now every outcome walks back through steps and tool calls to the policy text that justified it and the message that started it. For a support org, that's not a nice-to-have — it's the audit trail. [glossary: provenance] [glossary: trace] -->

---

# Module 4 — Exploration brief

- Core questions:
  1. Reconstruct a completed trace: task, tool order, outcome
  2. What did similar-task retrieval change — tool order, steps skipped, confidence?
  3. Find the *failed* trace — what went wrong, and how does the next agent avoid it?
- Stretch: the `:TOUCHED` vs `:MENTIONS` deep-dive; the full provenance walk — module 4 README
- Fell behind? `make module-4` · *(this module's exploration is the designated trim zone)*

<!-- notes: If we're tight on time this is where we compress — the core three questions carry the concepts. The failed trace question matters most for what's coming: what does it mean that failures are first-class memory? Hold that thought for twenty minutes. [glossary: trace] [glossary: provenance] -->

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

- Live demo: `make eval` — the same four questions, one last time
- The board is green: each question became answerable at exactly one module boundary
- *"Do you know who I am?"* → long-term memory · *"What did we discuss?"* → short-term
- *"Have you handled a ticket like this before?"* → reasoning memory → distilled skill

<!-- notes: Full circle. The scorecard that was red in module 1 is green now, and the attribution is clean: each memory layer unlocked exactly the questions it was designed to. If you take one picture today, take this one — it's the argument for layered memory in a single image. -->

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

- `pip install neo4j-agent-memory` (or `uv add`) into your agent's project
- Create a `MemoryClient` pointed at your database (`backend="bolt"`)
- Call `add_message` on each conversation turn
- Inject `get_context` into your agent's instructions — you have short-term memory
- Teardown: `docs/teardown.md` · Resources: **neo4j.com/labs/agent-memory** · GraphAcademy **Context Graphs** course · **github.com/neo4j-labs/agent-memory**

<!-- notes: The whole workshop distilled into four steps you can do before your coffee gets cold on Monday — install, connect, write messages, read context back. Everything beyond that — ontologies, hydration, traces — layers on the same client the same way you saw today. Thank you for spending the afternoon with us; the repo, the glossary, and the module READMEs are yours to keep. [glossary: ontology] [glossary: hydration] [glossary: trace] -->
