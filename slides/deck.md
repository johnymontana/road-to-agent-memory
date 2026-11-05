---

marp: true
theme: default
style: |
  section.technical { display: grid; grid-template-columns: minmax(0, 1.8fr) minmax(0, 1fr); grid-template-rows: auto auto auto 1fr; column-gap: 28px; row-gap: 12px; align-content: start; align-items: start; padding: 42px 50px 70px; font-size: 22px; }
  section.technical h1 { grid-column: 1 / -1; font-size: 34px; margin: 0; }
  section.technical > p:nth-of-type(1) { grid-column: 1 / -1; grid-row: 2; margin: 0; font-size: 20px; }
  section.technical > p:nth-of-type(2) { grid-column: 1 / -1; grid-row: 3; margin: 0; font-size: 21px; }
  section.technical pre { grid-column: 1; grid-row: 4 / span 5; margin: 0; font-size: 18.5px; line-height: 1.25; }
  section.technical pre code { white-space: pre-wrap; }
  section.technical > p:nth-of-type(n+3) { grid-column: 2; margin: 0; }
  section .references { position: absolute; left: 50px; right: 50px; bottom: 18px; color: #004063; font-size: 16px; line-height: 1.3; }
  section .references p { margin: 0; }
  section .references a { color: #0a6190; text-decoration: underline; }
  section:has(> p > img) { display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.2fr); grid-template-rows: auto 1fr; column-gap: 26px; align-items: start; font-size: 24px; padding: 46px 50px 70px; }
  section:has(> p > img) h1 { grid-column: 1 / -1; font-size: 34px; margin-bottom: 24px; }
  section:has(> p > img) > ul { grid-column: 1; grid-row: 2; }
  section:has(> p > img) > p:has(img) { grid-column: 2; grid-row: 2; align-self: center; margin: 0; }
  section:has(> p > img) img { width: 100%; height: auto; max-height: 450px; object-fit: contain; }
  section.resources { background: #faf8f5; color: #004063; padding: 46px 64px 72px; font-size: 22px; }
  section.resources h1 { font-size: 34px; color: #004063; margin-bottom: 8px; }
  section.resources h2 { font-size: 25px; color: #0a6190; margin: 22px 0 5px; }
  section.resources p { margin: 0 0 8px; line-height: 1.35; }
  section.resources a { color: #0a6190; text-decoration: underline; }
  section.resources .resource-footer { position: absolute; left: 64px; right: 64px; bottom: 22px; font-size: 17px; line-height: 1.3; color: #004063; }
  section.resources .resource-footer p { margin: 0; }
  .m5-code-aside { grid-column: 2; grid-row: 4 / span 5; }
  .m5-code-aside p { margin: 0 0 24px; }
  .m5-demo-aside { grid-column: 2; grid-row: 3 / span 4; }
  .m5-demo-aside p { margin: 0 0 24px; }
  section.m5-steps { font-size: 25px; padding: 46px 56px 70px; }
  section.m5-steps h1 { font-size: 34px; }
  section.m5-steps li { margin-bottom: 24px; }
  section.m5-cards, section.m5-concepts { font-size: 23px; padding: 46px 50px 70px; }
  section.m5-cards h1, section.m5-concepts h1 { font-size: 34px; }
  .m5-card-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 22px; margin: 22px 0; }
  .m5-concept-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px; }
  .m5-card-grid > div, .m5-concept-grid > div { background: #edf4f5; border-top: 4px solid #626dff; border-radius: 14px; padding: 20px; }
  .m5-card-grid h2, .m5-concept-grid h2 { font-size: 25px; color: #004063; margin: 0 0 18px; }
  .m5-card-grid p, .m5-concept-grid p { margin: 14px 0; line-height: 1.35; }
  section.m5-demo { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); column-gap: 28px; grid-template-rows: auto auto 1fr; align-items: start; align-content: start; font-size: 24px; padding: 46px 50px 70px; }
  section.m5-demo h1 { grid-column: 1 / -1; font-size: 34px; }
  section.m5-demo > p:first-of-type { grid-column: 1 / -1; grid-row: 2; margin: 0 0 24px; font-size: 20px; }
  section.m5-demo pre { grid-column: 1; grid-row: 3 / span 4; font-size: 18px; line-height: 1.4; padding: 22px; margin: 0; }
  section.m5-demo > p:nth-of-type(n+2) { grid-column: 2; margin: 0 0 22px; }

---

# Road to Agent Memory

- From stateless chatbot to an agent with persistent memory.
- Neo4j Labs workshop · 2.5 hours · run and explore.
- PydanticAI + `neo4j-agent-memory` + your AuraDB.
- Acme Cloud: a fictional SaaS customer-support desk.

<div class="references">

References: [SDK GitHub](https://github.com/neo4j-labs/agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/)

</div>

<!-- notes: Start each module at module_N/app/agent.py; compare adjacent app/ directories. Agent behavior, memory configuration and guardrails are intentionally local copies. Shared lib supplies HTTP transport, settings, SQLite access, receipts and response envelopes. Participants run and inspect the complete implementations; no coding exercise is required. Source: AGENTS.md; docs/adr/004-folder-per-module-progression.md; README.md. Module 1 is the no-memory control. Memory-enabled support apps 2–5 use AuraDB; optional module-5 hosted workflows use a separate NAMS workspace. -->

---

# What you'll leave with (an honest promise)

- A complete full-stack support app, with one agent implementation per module.
- Short-term, long-term and reasoning memory in your Bolt graph.
- Evidence walks and controlled retrieval scorecards at each layer.
- A tested write → retrieve → supply-history recipe to adapt.
- Run the app, inspect the graph and compare neighboring module folders.

![diagram](../slides/diagrams/d02-three-memory-types.svg)

<div class="references">

References: [Memory docs](https://neo4j.com/labs/agent-memory/) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/)

</div>

<!-- notes: Start each module at module_N/app/agent.py; compare adjacent app/ directories. Agent behavior, memory configuration and guardrails are intentionally local copies. Shared lib supplies HTTP transport, settings, SQLite access, receipts and response envelopes. Participants run and inspect the complete implementations; no coding exercise is required. Source: AGENTS.md; docs/adr/004-folder-per-module-progression.md; README.md. -->

---

# Agenda · 150 min

- **M0** Setup — 15 min
- **M1** Stateless agent — 15 min
- **M2** Short-term memory — 20 min
- **M3** Long-term memory — 40 min
- **M4** Reasoning memory — 30 min
- **M5** Optional hosted skill distillation — 20 min
- Wrap + Monday path — 5 min; buffer — 5 min

Complete NAMS setup in pre-work; code details are reference.

<div class="references">

References: [GraphAcademy: Python](https://graphacademy.neo4j.com/courses/workshop-agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/)

</div>

<!-- notes: Complete NAMS setup in pre-work. Detailed code slides are reference; use the core demo path in module 5’s 20-minute block.  150-minute plan: setup 15, stateless 15, short-term 20, long-term 40, reasoning 30, optional hosted skills 20, wrap 5 and buffer 5. Fit the code walks within these budgets. The non-hosted run-of-show reserves the optional 20 minutes for inspection/troubleshooting. Source: docs/run-of-show.md; current Makefile. -->

---

# Add memory, then build on it

- Expose a failure in what the current agent can remember.
- Add each memory type; compare complete module implementations.
- Build a reusable procedure on top of the resulting memory.
- Run fixed Make recipes and inspect measured evidence.
- Evaluate exact facts, source IDs and action receipts; model results can vary.

![diagram](../slides/diagrams/d03-workshop-arc.svg)

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Lenny’s Memory](https://neo4j.com/blog/developer/meet-lennys-memory-building-context-graphs-for-ai-agents/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

</div>

<!-- notes: Skill distillation builds a reusable procedure on the three memory types; it is not a fourth memory layer.  Start each module at module_N/app/agent.py; compare adjacent app/ directories. Agent behavior, memory configuration and guardrails are intentionally local copies. Shared lib supplies HTTP transport, settings, SQLite access, receipts and response envelopes. Participants run and inspect the complete implementations; no coding exercise is required. Source: AGENTS.md; docs/adr/004-folder-per-module-progression.md; README.md. -->

---

# Module 0 — Your environment

- Codespaces-first: prebuilt 4-core / 8 GB devcontainer.
- FastAPI :8000 + Vite :5173; one shared frontend for every module.
- Connect AuraDB and OpenAI; hosted module-5 workflows add optional NAMS.
- Credentials: `.env` or personal Codespaces secrets.
- Fallback: local clone + VS Code Dev Containers.

![diagram](../slides/diagrams/d04-environment-map.svg)

<div class="references">

References: [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [NAMS console](https://memory.neo4jlabs.com/) · [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Connect to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/)

</div>

<!-- notes: Complete NAMS signup and workspace key setup in pre-work; dedicated setup slides appear before the hosted workflow.  Run make check, then make dev MODULE=1 from the repo root. Codespaces or local Dev Containers use uv and npm. Credentials come from .env or environment secrets. make check probes chat inference, embeddings, SQLite, memory startup and graph transport; it reports median Aura round-trip latency and warns above 150ms. Stop the old server with Ctrl+C before changing MODULE, wait for Ready, then reload port 5173. NAMS is only needed for hosted module-5 workflows. Source: scripts/check_env.py; scripts/dev.sh; lib/settings.py; docs/running-the-app.md. -->

---

# Module 0 — Credential checklist

- Set `NEO4J_URI`, `NEO4J_USERNAME` and `NEO4J_PASSWORD` in `.env`.
- Set `OPENAI_API_KEY` in a personal Codespaces secret or `.env`.
- `NAMS_API_KEY` is needed only for hosted module-5 workflows.
- The devcontainer scaffolds `.env` from `.env.example`; see the pre-work email.

<div class="references">

References: [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: NAMS_API_KEY is used by hosted skill workflows and the module 5 NAMS graph checkbox. The support app retains Bolt.  Run make check, then make dev MODULE=1 from the repo root. Codespaces or local Dev Containers use uv and npm. Credentials come from .env or environment secrets. make check probes chat inference, embeddings, SQLite, memory startup and graph transport; it reports median Aura round-trip latency and warns above 150ms. Stop the old server with Ctrl+C before changing MODULE, wait for Ready, then reload port 5173. NAMS is only needed for hosted module-5 workflows. Source: scripts/check_env.py; scripts/dev.sh; lib/settings.py; docs/running-the-app.md. -->

---

# Module 0 — Smoke test, live

```bash
make check
make dev MODULE=1
```

- Check inference, embeddings, memory startup, graph transport and SQLite seed.
- Wait for **Ready**, then open port 5173 and confirm the module badge.
- Use a second terminal for scenarios. Stop the old server before changing `MODULE`.

<div class="references">

References: [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Run make check, then make dev MODULE=1 from the repo root. Codespaces or local Dev Containers use uv and npm. Credentials come from .env or environment secrets. make check probes chat inference, embeddings, SQLite, memory startup and graph transport; it reports median Aura round-trip latency and warns above 150ms. Stop the old server with Ctrl+C before changing MODULE, wait for Ready, then reload port 5173. NAMS is only needed for hosted module-5 workflows. Source: scripts/check_env.py; scripts/dev.sh; lib/settings.py; docs/running-the-app.md. -->

---

# Module 1 — Two stores, two jobs

- **SQLite is the system of record:** accounts, catalog, current policy and refund writes.
- **Neo4j is memory:** messages, entities and execution records in modules 2–5.
- Module 1 starts without a memory client.
- Memory supplies evidence; current SQL policy authorizes business actions.

![diagram](../slides/diagrams/d01-two-stores.svg)

<div class="references">

References: [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. issue_refund enforces current SQL policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. This diagram describes the architecture as memory is added. SQLite remains the system of record; module 1 uses only its business tools. -->

---

# Module 1 — Meet the agent

- PydanticAI + FastAPI backend; React + NVL frontend.
- Read `module_N/app/agent.py`: every module owns a complete agent.
- Five SQLite tools: `lookup_account`, `search_product_catalog`, `fetch_policy`, `check_service_status`, `issue_refund`.
- Local `guardrails.py` checks case scope and replies; `ReceiptGuard` reuses completed request IDs.
- Refunds require selected customer, selected case and authorization for this message.

<div class="references">

References: [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. issue_refund enforces current SQL policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. -->

---

# The baseline: PydanticAI + business tools

<!-- _class: technical -->

Module 1 · Code · `module_1/app/agent.py`

**Construction + normal chat turn**

```python
self.agent = Agent(
    f"openai:{settings.openai_model}",
    deps_type=ToolDeps,
    tools=SQLITE_TOOLS if business_tools else [],
    output_type=str,
    instructions=INSTRUCTIONS,
)
# Inside _turn: check the selected case.
scope = scope_turn(deps, policy_plan)
result = await self.agent.run(
    message, deps=deps,
    instructions=scope.instructions,
)
```

Five SQL tools; no memory client.

No message_history is supplied.

Local guardrails check scope and action claims.

<div class="references">

References: [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

</div>

<!-- notes: Construction and normal-turn fragments from module_1/app/agent.py. Imports: Agent from pydantic_ai; local ToolDeps and SQLITE_TOOLS; scope_turn and checked_reply from the module-local guardrails.py. INSTRUCTIONS is the actual constructor prompt constant. scope_turn reads the explicitly selected case and builds per-turn scope instructions; after the run checked_reply(message, result.output, deps, scope) verifies action claims against receipts. The full app handles errors and timing. Shared ReceiptGuard.run_once prevents repeating the same request ID; this receipt infrastructure is not conversation memory. Module 1 opens no MemoryClient and uses OpenAI for chat only. Visible browser chat bubbles are not sent back to the model. -->

---

# Module 1 — The failure: statelessness

- Every turn calls `Agent.run` without prior messages or retrieved memory.
- Even the same browser conversation forgets earlier turns.
- A restart is not required to expose the gap.
- Persistent storage plus explicit retrieval supplies the missing context.

![diagram](../slides/diagrams/d05-statelessness.svg)

<div class="references">

References: [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. issue_refund enforces current SQL policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. -->

---

# Module 1 — Live demo: the stateless baseline

```bash
make s1-baseline
```

- First: a self-contained account lookup with an email.
- Then: ask for the email from the previous turn without a new lookup.
- **Refresh graph → Saved replay** shows recorded CLI output.
- Browser chat is separate; module 1 creates no live Neo4j memory.

<div class="references">

References: [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. issue_refund enforces current SQL policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. Saved replay is a projection of recorded CLI output; its message/tool nodes are not native Neo4j memory. Module 1 live memory is empty. Browser and CLI conversations are separate. Source: scripts/run_scenario.py; web/src/components/GraphPanel.jsx. -->

---

# Module 1 — The eval baseline

- Run `make eval MODULE=1`.
- Four probes: exact name/email, unique phrase, grounded signup date, recorded reply.
- Private SQL, unique memory fixtures, disabled business tools.
- Exact values and accepted source IDs determine passing results.
- Open the evaluation panel to read the saved scorecard; a new run requires an explicit start.

<div class="references">

References: [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/)

</div>

<!-- notes: The participant Bolt graph links conversation, entity and reasoning memory. Hosted skill fixtures remain in a separate workspace; a Markdown skill crosses into the fresh agent. No cross-backend graph edges are created. Controlled eval checks exact facts plus accepted source IDs using private SQL and unique namespaces with business tools disabled. It is a retrieval probe, not an overall support-quality grade. The UI loads saved results for the current module; opening it does not invoke a model. Source: scripts/eval.py; web/src/components/EvalScorecard.jsx; module_5/app/fresh_agent.py. Run make eval MODULE=N explicitly. The four fixtures test name/email, unique phrase, SQL-grounded signup date and exact recorded reply. Inspect actual source IDs and unknown/error results. -->

---

# Meet neo4j-agent-memory

- .short_term: conversations and messages — what was said.
- .long_term: entities and preferences — who and what it is about.
- .reasoning: tasks, steps and tool calls — how the agent acted.

MemoryClient stores the graph. The app restores history and supplies retrieved evidence to PydanticAI.

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [SDK GitHub](https://github.com/neo4j-labs/agent-memory)

</div>

<!-- notes: The package persists and retrieves memory; PydanticAI executes the model and tools. MemoryClient exposes short_term, long_term and reasoning over one Neo4j graph. Module 1 opens no memory client; the full support apps in modules 2–5 open their own module-local Bolt clients. Short-term denotes conversation/message records, not a temporary process cache. Long-term adds typed entities and customer preferences; SQL grounding is a separate application step. Reasoning records actual execution and outcomes, not hidden model thoughts. Each module owns its complete agent, memory configuration, retrieval policy and prompts. Hosted module-5 REST workflows are a separate optional service path. -->

---

# Where memory meets PydanticAI

- neo4j-agent-memory writes messages, entities, preferences and execution traces.
- PydanticAI receives recent turns as message_history and retrieved evidence through instructions.
- Write → retrieve → compose → run → persist. Each module owns this integration.

<div class="references">

References: [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

</div>

<!-- notes: This is explicit integration, not an automatic Agent wrapper. A long-lived module-local MemoryClient stores records. Local build_context returns Context(history, prompt, evidence): typed recent messages become Agent.run(message_history=context.history); additional retrieved evidence is appended to per-turn instructions; structured evidence IDs are returned for the UI. Constructing a MemoryClient alone does not give an agent history. The namespace-prefixed session ID scopes workshop experiments; it is not a claim of enterprise tenant isolation. Retrieved evidence is not authority or current SQL policy. Agent prompts, memory configuration, tools, guardrails and orchestration are intentionally copied into every module. Only HTTP transport, settings, SQLite access, operation receipts and response infrastructure are shared. Read app/agent.py first; compare adjacent app folders to see the added concept. -->

---

# Configure and open one memory client

<!-- _class: technical -->

Library introduction · Code · `module_2/app/memory.py`

**Module-local build_settings + open_memory**

```python
config = MemorySettings(
    backend="bolt",
    neo4j={
        "uri": settings.neo4j_uri,
        "username": settings.neo4j_username,
        "password": settings.neo4j_password,
    },
    llm=f"openai/{settings.openai_model}",
    embedding=f"openai/{settings.embedding_model}",
    extraction={"extractor_type": "none"},
)
async with MemoryClient(config) as memory:
    # Reuse this connected client across chat turns.
    ...
```

MemoryClient and MemorySettings are package APIs.

Modules 2–5 open module-local Bolt clients.

The async context owns the connection lifetime.

<div class="references">

References: [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Condensed from module_2/app/memory.py build_settings/open_memory. Imports: MemoryClient and MemorySettings from neo4j_agent_memory. AppSettings reads environment or .env; get_settings exports the configured OpenAI key for package clients. Database and bounded connection/retry settings are omitted only from the display. Pin: neo4j-agent-memory[pydantic-ai,openai]==0.8.0. Module 1 has no MemoryClient and uses OpenAI for chat only. The full support apps in modules 2–5 use module-local Bolt clients and OpenAI for chat and embeddings; modules 3–5 additionally configure LLM extraction. Module 2 sets extractor_type="none". Optional hosted NAMS REST workflows and the module-5 fresh skill consumer are separate paths. This example passes MemorySettings explicitly; backend is a settings field, not a MemoryClient constructor keyword. -->

---

# Module 2 — Concept: short-term memory

- Conversations and messages persist as graph data and survive process restarts.
- `short_term.add_message` creates the conversation on first use.
- Recent turns become typed PydanticAI `message_history`.
- Scoped semantic statements become evidence in instructions.
- Inspect source IDs and `recent_conversation` / `semantic_message` paths.

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Short-term API index](https://neo4j.com/labs/agent-memory/reference/api/short-term/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. -->

---

# Module 2 — Message chains in the graph

- `Conversation` → `HAS_MESSAGE` → `Message`; `NEXT_MESSAGE` links the sequence.
- Message records retain ID, role, content, timestamp and embedding.
- The browser omits vectors and shows a bounded graph subset.
- Select a conversation, inspect properties and follow evidence IDs.

![diagram](../slides/diagrams/d06-message-chains.svg)

<div class="references">

References: [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. Follow HAS_MESSAGE and NEXT_MESSAGE. The browser graph omits embeddings and is a bounded subset (default 200 nodes); inspect the truncation notice. Source: lib/graph.py; web/src/components/GraphPanel.jsx. -->

---

# Persist both sides of a conversation

<!-- _class: technical -->

Module 2 · Code · `module_2/app/agent.py`

**Inside ChatService._turn**

```python
short_term = self.memory.short_term
# add_message creates the Conversation on first use.
user_message = await short_term.add_message(
    session_id, "user", message,
    extract_entities=not self.evaluation,
)
# ... recall; run; check the reply ...
await short_term.add_message(
    session_id, "assistant", reply,
    extract_entities=False,
)
```

Reuse the same session ID after restart.

add_message creates the conversation on first use.

Module 2 disables entity extraction in its settings.

<div class="references">

References: [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

</div>

<!-- notes: Normal persistence path from module_2/app/agent.py ChatService._turn. short_term is self.memory.short_term. The service prefixes session IDs with the workshop namespace. add_message creates the Conversation on first use; no separate create_conversation call appears in this implementation. The user flag is extract_entities=not self.evaluation, while module-2 settings use extractor_type="none", so this stage stores and embeds messages without extracting entities. Retain user_message.id to exclude the just-written message from history/retrieval. The assistant reply is checked against business receipts before persistence; persistence failures are surfaced as warnings. Database records survive process restarts, but the caller must reuse the session and namespace to restore that history. -->

---

# Module 2 — Context assembly

- **Recent history:** newest ten prior messages, reordered chronologically.
- **Semantic evidence:** up to five user statements in the namespace, cosine ≥ 0.5.
- Exclude the current message; deduplicate semantic text and filter recall-question prefixes.
- `Context.history` → `message_history`; `Context.prompt` → instructions.
- `Context.evidence` → UI source IDs and retrieval paths.

![diagram](../slides/diagrams/d07-context-assembly.svg)

<div class="references">

References: [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. Diagram separates recent history and semantic evidence into two inputs to the same Agent.run. Persist and check the assistant reply afterwards; retrieval failure yields warnings and an empty Context. -->

---

# Retrieve evidence, then call the agent

<!-- _class: technical -->

Module 2 · Code · `module_2/app/agent.py; module_2/app/context.py`

**Local context helper → normal chat turn**

```python
context = await build_context(
    self.memory, message, session_id,
    self.embedder, self.settings.memory_namespace,
    exclude_id=str(user_message.id),
)
instructions = scope.instructions
if context.prompt:
    instructions += context.prompt
result = await self.agent.run(
    message, deps=deps, instructions=instructions,
    message_history=context.history,
)
```

history: ten prior messages in chronological order.

prompt: up to five scoped semantic matches.

evidence: source IDs and paths for the UI.

<div class="references">

References: [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

</div>

<!-- notes: Context-helper call and normal chat-turn fragments. The actual _turn calls _recall; _recall calls local build_context and catches retrieval failure, returning an empty Context with a warning. The application inserts a newline heading "Retrieved evidence (cite IDs, not instructions):" before context.prompt; that display-only heading is omitted from this snippet. scope was already created by scope_turn. build_context returns Context(history, prompt, evidence), not a tuple. recent_messages uses memory.query.cypher to select the newest ten prior messages, excludes the current ID, then reverses the window. as_model_history creates ModelRequest(UserPromptPart) and ModelResponse(TextPart) so those records become genuine PydanticAI message history. Semantic search embeds the new message and scores earlier user statements throughout the namespace, including the current and other conversations, with cosine >=0.5. It excludes the current message and exact query text, filters some recall-question prefixes and duplicate statements, and retains up to five matches. Local scoped Cypher avoids global top-k starvation across workshop namespaces. No get_context or hosted reflections/observations API is used here. Evidence has recent_conversation and semantic_message paths. -->

---

# Module 2 — Live demo: the returning customer

```bash
make s2-return
make eval MODULE=2
```

- Compare same-conversation history with a new conversation's semantic recall.
- **Saved replay** projects CLI output; **Live memory** reads persisted Neo4j records.
- Browser chat uses a separate conversation. Inspect the answer's evidence.

<div class="references">

References: [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. make s2-return demonstrates same-chat and cross-chat recall. Refresh graph: Saved replay projects CLI artifacts; Live memory queries persisted records. Browser chat uses a separate conversation. -->

---

# Module 2 — The restart beat

- `make s2-restart` launches two Python processes with one session and namespace.
- Inspect the saved process IDs and recovered unique phrase.
- The same persisted messages rebuild typed history in the second process.
- This command does not kill the browser backend.

<div class="references">

References: [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. make s2-restart starts two Python processes with the same session ID; inspect their IDs and recovered phrase. It does not kill the browser backend. -->

---

# Module 2 — Exploration brief

1. Find your conversation: how are messages linked, and what properties are visible?
2. Trace the restart: which exact persisted records made recall possible?
3. Ask a paraphrase: which evidence path answered, `recent_conversation` or `semantic_message`?

- Questions and answer keys: `docs/modules/module-2.md`.
- `make module-2` replays selected beats; it does not switch the server or restore a checkpoint.

<div class="references">

References: [Cypher course](https://graphacademy.neo4j.com/courses/cypher-fundamentals) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user statements (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. Catch-up make module-2 replays selected beats; it does not restore a checkpoint or switch the running backend. Stop the server, run make dev MODULE=2, wait for readiness and reload. Use docs/modules/module-2.md for question answer keys. -->

---

# Module 3 — Concept: long-term memory

- Messages record what was said; entities describe who and what.
- Retrieve entities and selected-customer preferences across conversations.
- The ontology guides extraction; actual model output can vary.
- Add `search_memory`, `save_preference` and `recall_preferences`.
- Retain typed conversation history from module 2.

<div class="references">

References: [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. -->

---

# Module 3 — Ontology-driven extraction

- Read `module_3/ontology/acme_cloud.yaml`: types, subtypes, relation patterns and aliases.
- The app drops invalid relations; strict mode also filters undeclared entity types.
- Domain labels retain a POLE base type, for example `PERSON` / `CUSTOMER`.
- Instructor validator recipe: `uv run scripts/instructor.py strict`.

![diagram](../slides/diagrams/d08-ontology-extraction.svg)

<div class="references">

References: [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [POLE+O](https://neo4j.com/labs/agent-memory/explanation/poleo-model/) · [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. module_3/lab/compare.py runs independent extractor-only default/custom snapshots from the same transcript hash; no prior chat state, SQL hydration or live Bolt write. Inspect Saved replay. Logical relation labels in the diagram are illustrative; live storage uses RELATED_TO {type:...}. Entity nodes retain POLE base type and domain subtype, e.g. PERSON/CUSTOMER. Invalid relations are dropped; strict mode also filters unknown types. Instructor recipe: uv run scripts/instructor.py strict. -->

---

# Turn on ontology-driven extraction

<!-- _class: technical -->

Module 3 · Code · `module_3/app/memory.py; module_3/app/agent.py`

**Startup configuration + message write**

```python
ontology = load_ontology(
    "module_3/ontology/acme_cloud.yaml"
)
config = build_settings(settings)
# extractor_type="llm"; enrichment.enabled=False
async with MemoryClient(
    config, ontology=ontology
) as memory:
    user_message = await memory.short_term.add_message(
        session_id, "user", message,
        extract_entities=True,
    )
```

YAML guides types, aliases and relation patterns.

add_message extracts MENTIONS links.

SQL hydration supplies authoritative business fields.

<div class="references">

References: [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Startup and normal-message-write fragments; the full app reuses one connected client across turns. Imports: MemoryClient and load_ontology from neo4j_agent_memory; build_settings from module_3/app/memory.py. The default ONTOLOGY=acme_cloud loads the local file; default-poleo loads the generic local file; active passes ontology=None and uses the database active version. An explicit file wins over that version. The actual user flag is extract_entities=not self.evaluation; evaluation skips extraction and hydration. add_message creates the conversation if necessary. Module 3 configures extractor_type="llm", enrichment.enabled=False and the selected validation mode. The app drops invalid relations; strict also filters undeclared entity types. Ontology node labels map POLE types/subtypes (for example PERSON/CUSTOMER) to display labels (Customer). Live extracted entity relations are stored as RELATED_TO with the ontology relation in its type property; the extractor-only Saved replay displays logical relation labels directly. Optional Wikimedia enrichment belongs to module_3/lab/enrichment.py and creates cached Saved replay data, not an automatic live-graph write. -->

---

# Module 3 — Before / after: default vs. custom ontology

- `make s3-default` and `make s3-ontology` use one fixed transcript.
- `module_3/lab/compare.py` runs independent extractor calls.
- No chat history, SQL hydration, graph merging or live Bolt writes.
- Compare transcript hashes, types and logical relations in **Saved replay**.
- Temperature zero does not guarantee identical output.

![diagram](../slides/diagrams/d09-default-custom-ontology.svg)

<div class="references">

References: [POLE+O](https://neo4j.com/labs/agent-memory/explanation/poleo-model/) · [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. module_3/lab/compare.py runs independent extractor-only default/custom snapshots from the same transcript hash; no prior chat state, SQL hydration or live Bolt write. Inspect Saved replay. Logical relation labels in the diagram are illustrative; live storage uses RELATED_TO {type:...}. Entity nodes retain POLE base type and domain subtype, e.g. PERSON/CUSTOMER. Invalid relations are dropped; strict mode also filters unknown types. Instructor recipe: uv run scripts/instructor.py strict. -->

---

# Module 3 — The hybrid pipeline (the design-principle slide)

- **LLM:** entity spans, types, relations and descriptions that require validation.
- **SQLite:** authoritative email, plan and signup date, with `hydrated_from` provenance.
- **Optional Wikimedia lab:** public Organization facts in a local cache and Saved replay.
- The enrichment lab does not write live Neo4j memory or report service health.
- Generated descriptions are not business authority.

![diagram](../slides/diagrams/d10-hybrid-pipeline.svg)

<div class="references">

References: [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. Optional make s3-enrich calls module_3/lab/enrichment.py with a named Wikimedia User-Agent. It writes a local cache and Saved replay Organization projection, never live Neo4j. Cache TTL: success 7 days; other statuses 5 minutes. A provider error is visible and does not block the core lesson. Source facts are public company information, not service monitoring. -->

---

# Ground extracted entities in SQL facts

<!-- _class: technical -->

Module 3 · Code · `module_3/app/hydrate.py`

**Inside checked hydration loop**

```python
# entity and facts passed identity/type checks.
await memory.long_term.add_entity(
    entity["name"], entity["type"],
    subtype=entity.get("subtype"),
    description=facts["description"],
    attributes=facts["attributes"],
    resolve=False, deduplicate=False,
    generate_embedding=False, enrich=False,
)
if writer is not None:
    await writer.set_properties(
        entity["name"], entity["type"],
        facts["attributes"],
    )
```

Current-message mentions; exact SQL names or aliases.

The public upsert refreshes description.

PropertyWriter refreshes flat fields before retrieval.

<div class="references">

References: [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

</div>

<!-- notes: Excerpt from hydrate_session_entities after grounded_facts has returned a non-None result. The agent passes the current user message ID; only entities that message mentions are hydrated. Local lookup_facts performs parameterized SQLite reads. grounded_facts rejects conflicting exact-name/alias matches and incompatible POLE base types (PERSON for customers, OBJECT for products/plans, ORGANIZATION for organizations). The public long_term.add_entity upsert refreshes description; the pinned SDK does not refresh existing flat attributes, so a module-local PropertyWriter uses its own pooled Neo4j driver and opens a short session per write. memory.query.cypher is read-only. No _apply_flat_attributes or _lookup_hydration helper exists in this version. Existing resolved entity names remain unchanged (resolve=False, deduplicate=False). Inspect hydrated_from for SQL provenance; generated descriptions alone are not authoritative. A later mention refreshes facts after a SQL change; this is not automatic CDC. The local instructor plan fixture verifies Pro → Enterprise → Pro without modifying the live participant graph. -->

---

# Module 3 — Entity resolution & aliases

- Declared aliases guide canonical naming; inspect the chosen node and retained aliases.
- `add_entity` merges on name and type; hydration refreshes matched entity facts.
- Follow `MENTIONS` back to the current source message.
- Resolution and extraction can still produce duplicates; inspect actual results.

![diagram](../slides/diagrams/d11-entity-resolution.svg)

<div class="references">

References: [Resolution](https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. -->

---

# Module 3 — Live demo: watch the graph bloom

```bash
make s3-default
make s3-ontology
make s3-enrich  # optional lab
```

- Compare immutable extraction snapshots through **Saved replay**.
- In browser chat, introduce Maya; inspect live `MENTIONS` and SQL-grounded fields.
- Optional enrichment saves a cached replay; inspect provider status and continue if unavailable.

<div class="references">

References: [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. Optional make s3-enrich calls module_3/lab/enrichment.py with a named Wikimedia User-Agent. It writes a local cache and Saved replay Organization projection, never live Neo4j. Cache TTL: success 7 days; other statuses 5 minutes. A provider error is visible and does not block the core lesson. Source facts are public company information, not service monitoring. -->

---

# Module 3 — Under the hood: hydration & enrichment

- Live app: current-message mentions → SQL hydration → recall → answer.
- `grounded_facts` checks exact identity and compatible type; `PropertyWriter` refreshes flat fields.
- Enrichment lives in `module_3/lab/enrichment.py`, outside the agent runtime.
- Wikimedia success cache: seven days; other statuses: five minutes.
- Cache + Saved replay only; no live Neo4j write or service monitoring.

<div class="references">

References: [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. Optional make s3-enrich calls module_3/lab/enrichment.py with a named Wikimedia User-Agent. It writes a local cache and Saved replay Organization projection, never live Neo4j. Cache TTL: success 7 days; other statuses 5 minutes. A provider error is visible and does not block the core lesson. Source facts are public company information, not service monitoring. -->

---

# Expose memory tools to PydanticAI

<!-- _class: technical -->

Module 3 · Code · `module_3/app/agent.py; module_3/app/memory_tools.py`

**Inside ChatService.__init__**

```python
tools = SQLITE_TOOLS if business_tools else []
self.agent = Agent(
    f"openai:{settings.openai_model}",
    deps_type=ToolDeps,
    tools=tools + create_memory_tools(memory),
    output_type=str,
    instructions=(INSTRUCTIONS
        + SHORT_TERM_INSTRUCTIONS
        + LONG_TERM_INSTRUCTIONS),
)
# search_memory(query)
# save_preference(category, preference, context)
# recall_preferences()
```

The local tool factory closes over MemoryClient.

RunContext[ToolDeps] supplies customer and namespace.

Memory tools query mid-turn; SQL tools still govern actions.

<div class="references">

References: [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

</div>

<!-- notes: Construction fragment from module_3/app/agent.py. create_memory_tools is local workshop code, not the package tool registry; it shares the familiar integration tool names but scopes queries to the workshop namespace/customer and records tool receipts. INSTRUCTIONS + SHORT_TERM_INSTRUCTIONS + LONG_TERM_INSTRUCTIONS are the actual constants. The short-term instructions teach evidence use; the long-term instructions request search_memory for account-history requests and save_preference when asked to store a preference. context.py retrieves before the model call; search_memory permits another query during the run. It combines Cypher-scoped user statements and allowlisted entity fields with long_term.get_preferences_for for the selected user. ToolDeps carries the explicitly selected customer, namespace, embedder and current_message_id. recall_preferences has no model-visible topic argument. SQL tools and module-local guardrails still validate current business facts and actions. -->

---

# Save and recall one customer’s preferences

<!-- _class: technical -->

Module 3 · Code · `module_3/app/memory_tools.py; module_3/app/context.py`

**Preference write tool + retrieval helper**

```python
# Inside save_preference, after the customer check:
user = customer_id(deps.namespace, deps.account_email)
stored = await memory.long_term.add_preference(
    f"{user}:{category}", preference,
    context=context, user_identifier=user,
)
# Inside context.search_preferences:
preferences = (
    await memory.long_term.get_preferences_for(
        customer_id(namespace, customer_email)
    )
)
```

User → HAS_PREFERENCE → Preference.

The customer prefixes both category and user identity.

Confirm the returned value and deduplicated flag.

<div class="references">

References: [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

</div>

<!-- notes: Write-tool and retrieval-helper fragments. customer_id is a local helper returning f"{namespace}:{customer_email}". save_preference takes RunContext[ToolDeps], category, preference and optional context. It returns needs_customer before the shown block if no customer is selected. The SDK deduplicates similar preferences within a category across users, so the category is also prefixed with the customer identifier. user_identifier creates (:User)-[:HAS_PREFERENCE]->(:Preference). The receipt uses stored.id/category/preference/context and stored.metadata.get("deduplicated", False); it reports what the SDK actually stored. Retrieval calls the public long_term.get_preferences_for API rather than category-prefix Cypher. search_preferences returns at most ten customer_preference evidence rows and returns an empty list if no customer is selected. The model tool recall_preferences() takes no topic argument. No preference automatically authorizes a business action. -->

---

# Module 3 — Exploration brief (40-min module, tiered)

- **Core:** follow `MENTIONS`, compare extraction snapshots and identify Customer field sources.
- Compare `module_2/app` with `module_3/app`: what new memory behavior appears?
- **Instructor:** negative descriptions, strict validation and local Pro → Enterprise → Pro hydration.
- **Stretch:** select a customer, save a preference and verify the actual stored value and scope.
- Allow 15+ minutes. Questions: `docs/modules/module-3.md`; catch-up: `make module-3`.

<div class="references">

References: [GraphAcademy: Python](https://graphacademy.neo4j.com/courses/workshop-agent-memory) · [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. Catch-up make module-3 replays selected beats; it does not restore a checkpoint or switch the running backend. Stop the server, run make dev MODULE=3, wait for readiness and reload. Use docs/modules/module-3.md for question answer keys. Q7 uses uv run scripts/instructor.py plan: a local fixture checks Pro → Enterprise → Pro; it does not alter a live customer. Preferences require a selected customer and confirmation of the returned stored value. -->

---

# Module 4 — Concept: reasoning memory

- Record tasks, tool calls, executed SQL, exact replies and outcomes.
- Open a trace first; attempt completion after success or failure.
- Retrieve completed executions; the current open trace cannot match itself.
- A declined business request differs from an execution failure.
- Prior procedures are examples; current SQL policy governs action.

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [Reasoning API index](https://neo4j.com/labs/agent-memory/reference/api/reasoning/)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. These are execution receipts with actual SQL, not hidden model thoughts. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. -->

---

# Module 4 — Anatomy of a trace

- `ReasoningTrace` → `HAS_STEP` → `ReasoningStep` → `USES_TOOL` → `ToolCall`.
- `ToolCall` → `INSTANCE_OF` → `Tool`; outcome is a trace property.
- Trace `INITIATED_BY` Message; Step `TOUCHED` explicit case Customer / Plan.
- Inspect actual inputs, outputs and SQL: execution receipts, not hidden model thoughts.

![diagram](../slides/diagrams/d12-trace-anatomy.svg)

<div class="references">

References: [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. These are execution receipts with actual SQL, not hidden model thoughts. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. -->

---

# Open the trace before execution

<!-- _class: technical -->

Module 4 · Code · `module_4/app/agent.py; module_4/app/reasoning.py`

**Condensed normal path in ChatService._turn**

```python
trace = await self.memory.reasoning.start_trace(
    session_id, message,
    metadata={"request_id": request_id,
              "source": "workshop"},
)
scope = scope_turn(deps, policy_plan)
# ... save user message; hydrate; recall context ...
result = await self.agent.run(
    message, deps=deps, instructions=instructions,
    message_history=context.history,
)
reply = checked_reply(
    message, result.output, deps, scope
)
# ... persist reply; record_execution closes trace ...
```

Open the trace before case checks and model execution.

Pass real message history; validate the reply against receipts.

On errors, supply a safe reply and attempt trace completion.

<div class="references">

References: [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/)

</div>

<!-- notes: Condensed normal path from module_4/app/agent.py:161–222. self.memory and self.agent belong to ChatService; deps is ToolDeps and context is Context. scope_turn and checked_reply come from the module-local guardrails.py. start_trace is conditional on record_reasoning and occurs before case checks. Saving the user message extracts entities unless evaluation=True; hydration and retrieval follow. The model receives context.history as real PydanticAI message_history and retrieved evidence/examples through instructions. checked_reply verifies output against deps.collector and scope. Exceptions set execution_ok=False and use failure_reply. The app persists the reply, then calls record_execution with tool_calls=deps.collector, reply, execution_ok, warnings and selected case whenever a trace exists. Completion can fail if storage is unavailable; warnings surface degraded persistence and ReceiptGuard retains local operation receipts for safe request-ID retries. No hidden model thoughts are recorded. -->

---

# Attach observations and provenance

<!-- _class: technical -->

Module 4 · Code · `module_4/app/reasoning.py`

**Inside record_execution: message link + loop**

```python
await memory.reasoning.link_trace_to_message(
    trace.id, str(message.id)
)
output = call["output"]
step = await memory.reasoning.add_step(
    trace.id, action=call["name"],
    observation=json.dumps(output, default=str),
    generate_embedding=False,
)
await memory.reasoning.record_tool_call(
    step.id, call["name"], arguments=call["input"],
    result={"value": output,
            "executed_sql": call.get("sql")},
    message_id=str(message.id), touched_entities=refs,
)
```

INITIATED_BY links a trace to its user message.

TOUCHED links a step to explicit Customer / Plan references.

Capture actual inputs, outputs and SQL; a declined refund has no INSERT.

<div class="references">

References: [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

</div>

<!-- notes: From module_4/app/reasoning.py:95–130. The message link occurs once before the tool_calls loop; step creation and record_tool_call occur for each receipt. output is a presentation alias for call["output"]. The displayed path assumes message exists; real code conditionally links it and passes message_id=None if absent. case_entities builds EntityRef objects from the explicitly selected SQL case Customer and Plan with resolve/deduplicate/enrich/embedding disabled. The call also records rounded duration_ms. Graph: ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool; trace INITIATED_BY Message; ToolCall TRIGGERED_BY Message. touched_entities creates ReasoningStep TOUCHED Entity. Server guard decisions are recorded alongside model tools. The local recorder supports failed runs without AgentRunResult, server checks and exact SQL; SDK integrations.pydantic_ai.record_agent_trace expects a completed result, so it is not used here. -->

---

# Complete the trace with an outcome

<!-- _class: technical -->

Module 4 · Code · `module_4/app/reasoning.py`

**Finally block in record_execution**

```python
outcome = TraceOutcome(
    success=error_kind is None,
    summary=json.dumps({
        "reply": reply,
        "execution_status": (
            "succeeded" if execution_ok else "failed"
        ),
        "business_status": status,
        "warnings": warnings,
    }, default=str),
    error_kind=error_kind,
)
await memory.reasoning.complete_trace(
    trace.id, outcome=outcome
)
```

TraceOutcome is a package model.

A declined refund can execute correctly while trace success=False.

Recording or execution failures also make success=False.

<div class="references">

References: [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

</div>

<!-- notes: Imports: TraceOutcome from neo4j_agent_memory.schema.models and json. Condensed from module_4/app/reasoning.py:107–164. status = business_status(tool_calls) selects the latest issue_refund/refund_policy_guard receipt or no_action. declined means status starts with rejected or equals requires_confirmation. error_kind precedence is recording exception name, execution_error when execution_ok=False, policy_declined, then None. Real code constructs TraceOutcome inside complete_trace; named outcome is presentation-only factoring. The real outcome includes related_entities=refs and metrics execution_succeeded/tool_calls, with no unmeasured policy_compliant assertion. Exact checked reply is retained as JSON. finally attempts completion after execution or recording failure; outages can still prevent storage. -->

---

# Module 4 — Similar-task retrieval

- Completed traces in one namespace; task cosine ≥ 0.45, at most three matches.
- Successful and declined executions can match; no hit is guaranteed.
- Pre-turn examples and mid-turn `search_memory` supply past steps and observations.
- The retrieval toggle disables both routes while normal trace recording continues.
- Controlled ablation also disables extraction, hydration and branch trace writes.

![diagram](../slides/diagrams/d13-similar-task-retrieval.svg)

<div class="references">

References: [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. These are execution receipts with actual SQL, not hidden model thoughts. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. The reasoning_retrieval toggle disables pre-turn examples and mid-turn search_memory procedures; by itself it still records new traces. The controlled make s4-refund-repeat runner additionally sets evaluation=True and record_reasoning=False in both branches: no extraction, hydration or branch trace writes. It uses identical private SQLite copies, separate message scopes and one frozen declined-refund corpus. Compare saved hashes, evidence, tools, tokens, timing and policy compliance. A benefit is not guaranteed. The fixture is module_4/lab/ablation.py; orchestration is scripts/run_scenario.py. -->

---

# Recall completed executions

<!-- _class: technical -->

Module 4 · Code · `module_4/app/reasoning.py; module_4/app/agent.py`

**similar_executions → recall wrapper → agent.run**

```python
# similar_executions: each completed, scoped hit
trace = await memory.reasoning.get_trace_with_steps(
    UUID(row["id"])
)
# ... as_example serializes steps and tool results ...
# Inside ChatService._recall_executions:
examples, evidence = await similar_executions(
    self.memory, message, self.embedder,
    self.reasoning_namespace,
)
# _turn adds examples to instructions before this run:
result = await self.agent.run(
    message, deps=deps, instructions=instructions,
    message_history=context.history,
)
```

Completed traces only: exclude this turn’s open trace.

Scope first; cosine ≥0.45; up to three matches, including declines.

Execution examples guide the model; current SQL policy governs action.

<div class="references">

References: [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

</div>

<!-- notes: Imports: UUID from uuid and local similar_executions. Three scopes: first block inside similar_executions; middle inside ChatService._recall_executions; final block in ChatService._turn. Source: module_4/app/reasoning.py:36–92 and agent.py:187–195,259–271. Namespace Cypher requires completed_at IS NOT NULL before ranking, excluding the trace opened for this turn. It checks task_embedding and selects up to three cosine matches ≥0.45, including completed declines. get_trace_with_steps supplies actual steps, tool arguments/results and outcome; as_example serializes them, and trace IDs join context.evidence. _turn injects nonempty examples labeled Past execution examples (not current policy). SDK get_similar_traces uses global top-k; local query provides exact namespace isolation. reasoning_retrieval=False disables both pre-turn and search_memory procedure retrieval but alone still records traces. The controlled make s4-refund-repeat runner additionally sets record_reasoning=False and evaluation=True in both branches: no branch traces, extraction or hydration; identical private SQL copies, separate message namespaces and one fixed corpus seeded by module_4/lab/ablation.py. Identical outcomes are valid. Retrieval errors surface warnings without necessarily failing the turn. -->

---

# Module 4 — Live demo: record, decline, compare

```bash
make s4-refund
make s4-fail
make s4-refund-repeat
```

- Confirm account and billing case before authorizing a refund.
- Inspect tools and SQL receipts; the over-limit guard declines without escalation.
- Compare frozen-corpus control/treatment runs with identical private SQL copies.
- Check actual evidence, tokens, timing and safety; improvement is not guaranteed.

<div class="references">

References: [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. These are execution receipts with actual SQL, not hidden model thoughts. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. The reasoning_retrieval toggle disables pre-turn examples and mid-turn search_memory procedures; by itself it still records new traces. The controlled make s4-refund-repeat runner additionally sets evaluation=True and record_reasoning=False in both branches: no extraction, hydration or branch trace writes. It uses identical private SQLite copies, separate message scopes and one frozen declined-refund corpus. Compare saved hashes, evidence, tools, tokens, timing and policy compliance. A benefit is not guaranteed. The fixture is module_4/lab/ablation.py; orchestration is scripts/run_scenario.py. -->

---

# Module 4 — The provenance question

- “Why did you issue that refund?”
- Trace → `INITIATED_BY` → Message; Step → `TOUCHED` → Customer / Plan.
- Inspect executed SQL, action receipts and the current policy.
- Server-validation receipts are distinguishable from model-selected tools.

<div class="references">

References: [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. These are execution receipts with actual SQL, not hidden model thoughts. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. -->

---

# Module 4 — Exploration brief

1. Reconstruct actual steps, tools and business outcome.
2. Compare retrieved evidence and measured behavior; identical outcomes are possible.
3. Distinguish policy decline, model exception and degraded persistence.

- Inspect warnings and saved operation receipts before retrying.
- Questions: `docs/modules/module-4.md`; `make module-4` replays selected beats.

<div class="references">

References: [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Cypher course](https://graphacademy.neo4j.com/courses/cypher-fundamentals)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. These are execution receipts with actual SQL, not hidden model thoughts. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. Catch-up make module-4 replays selected beats; it does not restore a checkpoint or switch the running backend. Stop the server, run make dev MODULE=4, wait for readiness and reload. Use docs/modules/module-4.md for question answer keys. The reasoning_retrieval toggle disables pre-turn examples and mid-turn search_memory procedures; by itself it still records new traces. The controlled make s4-refund-repeat runner additionally sets evaluation=True and record_reasoning=False in both branches: no extraction, hydration or branch trace writes. It uses identical private SQLite copies, separate message scopes and one frozen declined-refund corpus. Compare saved hashes, evidence, tools, tokens, timing and policy compliance. A benefit is not guaranteed. The fixture is module_4/lab/ablation.py; orchestration is scripts/run_scenario.py. -->

---

# Module 5 — Build skills on top of agent memory

- Memory records conversations, entities and execution.
- Distillation selects evidence and derives a reusable procedure.
- Inspect the versioned package and its source links.
- A fresh agent loads SKILL.md and uses its own tools.

Setup is pre-work. Detailed code slides are reference; use the core demonstration path within the 20-minute module.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: The module 5 support app retains the full module 4 Bolt/AuraDB memory behavior. Hosted REST workflows seed canonical authored fixtures into a separate NAMS workspace; they do not migrate participant AuraDB data. Skill distillation builds a reusable procedure on top of memory, not a fourth memory store or model-weight training. Source: module_5/app/agent.py; module_5/app/memory.py; module_5/workflows/*.py. Memory supplies context, entity knowledge and recorded actions/outcomes. A distillation run selects evidence and derives a portable procedure with conditions and source links. A receiving agent supplies its own tools and authorization and checks current business policy. Grounding is evidence for inspection, not proof of correctness or suitability. Core 20-minute path: recap concepts, check pre-work, run seed/distill, inspect package/graph, compare fresh-agent modes, demonstrate drift. Signup/setup slides are pre-work; detailed code slides are reference rather than additional timed exercises.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Build procedures on top of agent memory

<!-- _class: m5-concepts -->

<div class="m5-concept-grid"><div><h2>Memory · recorded experience</h2><p>Messages: what was said.</p><p>Entities: who and what it involved.</p><p>Traces: actions, tool results and outcomes.</p></div><div><h2>Skill · reusable procedure</h2><p>Select relevant evidence.</p><p>Derive steps and conditions.</p><p>Retain source links.</p><p>Load instructions in another agent.</p></div></div>

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Memory supplies context, entity knowledge and recorded actions/outcomes. A distillation run selects evidence and derives a portable procedure with conditions and source links. A receiving agent supplies its own tools and authorization and checks current business policy. Grounding is evidence for inspection, not proof of correctness or suitability. No new memory type is introduced. Distillation changes an instruction artifact, not model weights. A raw trace records one execution; a skill generalizes a reusable procedure, while the receiving agent performs a new execution. The workshop fixture is canonical authored history rather than a recording uploaded from the participant app. The module 5 support app retains the full module 4 Bolt/AuraDB memory behavior. Hosted REST workflows seed canonical authored fixtures into a separate NAMS workspace; they do not migrate participant AuraDB data. Skill distillation builds a reusable procedure on top of memory, not a fourth memory store or model-weight training. Source: module_5/app/agent.py; module_5/app/memory.py; module_5/workflows/*.py.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Build reusable procedures on agent memory

- Select memory; generate a scoped procedure.
- Review and publish a versioned package.
- Load SKILL.md in a fresh agent with business tools.
- This changes instructions, not model weights.

![diagram](../slides/diagrams/d19-memory-to-skills.svg)

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Memory supplies context, entity knowledge and recorded actions/outcomes. A distillation run selects evidence and derives a portable procedure with conditions and source links. A receiving agent supplies its own tools and authorization and checks current business policy. Grounding is evidence for inspection, not proof of correctness or suitability. Diagram: selected memory feeds a scoped distillation run; after succeeded the workshop approves, publishes and downloads a versioned package. Fresh agent loads SKILL.md and calls business tools. Approval is submitted automatically by this script; it does not stop for human review. Failed/error/cancelled runs or timeout lead to explicit fallback guidance. Three memory types remain the input foundation.

Diagram detail: Conceptual application pipeline: three existing memory types provide persisted evidence; scope selects relevant evidence, distillation abstracts a procedure, review/package creates a portable versioned artifact, fresh agent consumes the file with current business tools. No edges between foundation nodes are asserted here. Process arrows are not database relationships. No model fine-tuning occurs. Workshop review submission is automated; a production human decision requires a separate policy/workflow.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Module 5 — The app, hosted workspace and consumer

<!-- _class: m5-concepts -->

<div class="m5-concept-grid"><div><h2>Your AuraDB</h2><p>Support apps 2–5 retain Bolt memory.</p><p>Module 1 has no memory client.</p></div><div><h2>Your NAMS workspace</h2><p>Hosted REST workflows and skill graph.</p><p>make nams-seed writes canonical fixtures, not module 4 traces.</p><p>No automatic Bolt migration.</p></div></div>

<div class="references">

References: [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: The module 5 support app retains the full module 4 Bolt/AuraDB memory behavior. Hosted REST workflows seed canonical authored fixtures into a separate NAMS workspace; they do not migrate participant AuraDB data. Skill distillation builds a reusable procedure on top of memory, not a fourth memory store or model-weight training. Source: module_5/app/agent.py; module_5/app/memory.py; module_5/workflows/*.py. The same browser can inspect both stores: normal graph mode uses Bolt; Module 5 NAMS checkbox selects /api/graph/nams, backed by read-only POST /v1/query. The fresh consumer receives a local Markdown artifact, not a client connected to either memory backend.

References · checked 2026-11-04
Backend capabilities: https://neo4j.com/labs/agent-memory/reference/backend-capabilities/
NAMS console: https://memory.neo4jlabs.com/ -->

---

# Open your NAMS workspace

<!-- _class: m5-steps -->

Module 5 · Pre-work

1. **Open the service** — Visit memory.neo4jlabs.com and choose Sign In.

2. **Use a Neo4j account** — Sign in, or choose Sign up. Email and Google are offered.

3. **Open Dashboard** — First login provisions a default workspace and API key.

Complete account setup before the timed module. Keep this workspace for the workshop fixtures.

<div class="references">

References: [NAMS sign in](https://memory.neo4jlabs.com/) · [Setup docs](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Verified public homepage and Neo4j authentication flow on 2026-11-04. Sign In opens login.neo4j.com; sign-in and signup offer email and Continue with Google. No form was submitted. Public NAMS docs state first login creates a user, default workspace and default key. Do not invent a GitHub option, mandatory manual workspace creation or unverified pricing. Exact authenticated post-login controls were not inspected.

References · checked 2026-11-04
NAMS sign in: https://memory.neo4jlabs.com/
Setup docs: https://memory.neo4jlabs.com/docs -->

---

# Create a key for the workshop workspace

<!-- _class: m5-steps -->

Module 5 · Pre-work

1. **Dashboard → API Keys** — Generate a workspace-bound data key for this workspace.

2. **Copy the nams_ key** — Store it in your private .env or personal Codespaces secrets.

3. **Keep the key private** — Keys expire after 90 days. Never paste the value into slides or Git.

Use a workspace data key. Admin keys have broader account-wide privileges.

<div class="references">

References: [API key dashboard](https://memory.neo4jlabs.com/dashboard/api-keys) · [Authentication docs](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Public docs link https://memory.neo4jlabs.com/dashboard/api-keys. Workspace data keys bind access to a selected workspace; admin keys are broader. Keys use nams_ prefix, expire after 90 days and authenticate directly as Bearer. A default key is also provisioned on first login. Do not claim a one-time-only reveal: current docs describe owner-only reveal. Exact authenticated form labels were not observed; the slide uses only verified navigation and semantic instructions. Never display a real credential.

References · checked 2026-11-04
API key dashboard: https://memory.neo4jlabs.com/dashboard/api-keys
Authentication docs: https://memory.neo4jlabs.com/docs -->

---

# Connect the workshop and check capabilities

<!-- _class: m5-demo -->

Module 5 · Pre-work · First two lines: private .env; commands: terminal.

```bash
NAMS_API_KEY=nams_YOUR_WORKSPACE_KEY
NAMS_BASE_URL=https://memory.neo4jlabs.com

make nams-check
make dev MODULE=5

# Second terminal
make nams-seed
make nams-distill
```

<div class="m5-demo-aside"><p>Read the result: workspace reachable and distillation enabled.</p><p>The script prints publish gates.</p><p>If disabled, use WITH_SKILL=fallback to demonstrate consumption.</p></div>

<div class="references">

References: [NAMS docs](https://memory.neo4jlabs.com/docs) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Source: lib/settings.py; module_5/workflows/nams.py; check.py. NAMS_BASE_URL defaults to https://memory.neo4jlabs.com; do not append /v1 because callers add endpoint paths. Use existing private .env or personal Codespaces secrets. Restart any running dev server after changing config: stop it, run make dev MODULE=5, reload browser. nams-check GETs conversations?limit=1 for auth, then skills/capabilities for distillation and thresholds. Auth success with distillation disabled can still return exit0; read the message. Fallback uses artifacts/pre-distilled-skill/SKILL.md and demonstrates consumption only, not live generation.

References · checked 2026-11-04
NAMS docs: https://memory.neo4jlabs.com/docs
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/
After make dev starts, use a second terminal in the repository root for make nams-seed and make nams-distill. -->

---

# Seed a small, inspectable memory corpus

<!-- _class: m5-cards -->

Module 5 · Hosted evidence

<div class="m5-card-grid"><div><h2>4 explicit entities</h2><p>Maya Chen; Northwind Robotics; Acme Cloud Compute; Pro.</p><p>Entity upserts may merge.</p></div><div><h2>1 conversation</h2><p>Create the conversation, then bulk-add four messages.</p><p>Save the returned conversation ID.</p></div><div><h2>2 completed traces</h2><p>Each trace has three steps and tool calls.</p><p>Complete with an outcome and success=True.</p></div></div>

Run make nams-seed · saves DATA_DIR/nams-workspace.json for make nams-distill.

<div class="references">

References: [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: The module 5 support app retains the full module 4 Bolt/AuraDB memory behavior. Hosted REST workflows seed canonical authored fixtures into a separate NAMS workspace; they do not migrate participant AuraDB data. Skill distillation builds a reusable procedure on top of memory, not a fourth memory store or model-weight training. Source: module_5/app/agent.py; module_5/app/memory.py; module_5/workflows/*.py. seed.py creates four explicit entities, one new conversation, four messages and two successful completed traces, each with three steps/tool calls. Service extraction may create additional entities; four is the explicit fixture count, not a total graph-node promise. Tool input/output are JSON-encoded strings. Both traces reference the first user message, and explicit touchedEntityIds/relatedEntityIds point to Maya only. A run writes seed state only after all calls succeed. Repeated seed creates new conversations/traces and the newest saved conversation scopes normal distillation.

References · checked 2026-11-04
NAMS OpenAPI: https://memory.neo4jlabs.com/openapi.json
Live NAMS API: https://memory.neo4jlabs.com/docs -->

---

# Complete the traces before distilling them

<!-- _class: technical m5-code -->

Module 5 · Code reference · `module_5/workflows/seed.py`

**After the steps and tool calls of one trace**

```python
await call(
    http, "POST",
    f"/v1/reasoning/traces/{trace_id}/complete",
    {
        "outcome": trace["outcome"],
        "success": True,
        "relatedEntityIds": [entity_ids["Maya Chen"]],
    },
)
trace_ids.append(trace_id)
# After all traces, save the scope for distillation:
write_json(seed_state_path(settings), {
    "conversationId": conv_id, "traceIds": trace_ids
})
```

<div class="m5-code-aside"><p>A completed successful execution is eligible evidence for the demonstrated procedure.</p><p>The seed record connects the Make targets.</p><p>data/nams-workspace.json stores conversationId and traceIds.</p></div>

<div class="references">

References: [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: The write_json call runs once after the trace loop and after the HTTP client closes; the excerpt labels that boundary. The path follows DATA_DIR, which defaults to data. Seed fails fast on a bad write; tests assert it does not write the state record after failure. Completion payload uses outcome string and success, unlike the Bolt SDK TraceOutcome object. Source lines: 206–219.

References · checked 2026-11-04
NAMS OpenAPI: https://memory.neo4jlabs.com/openapi.json
Live NAMS API: https://memory.neo4jlabs.com/docs -->

---

# Distill one conversation into a versioned skill

<!-- _class: technical m5-code -->

Module 5 · Code reference · `module_5/workflows/distill.py`

**Inside main(redistill), condensed happy path**

```python
seeded = read_json(seed_state_path(settings))
scope = {
    "type": "conversations",
    "conversationIds": [seeded["conversationId"]],
}
request = {"nameHint": SKILL_NAME, "scope": scope}
if existing:
    request["skillId"] = existing["id"]
async with client(settings) as http:
    started = await call(
        http, "POST", "/v1/skills/generate", request
    )
    run = await wait_for_run(http, started["runId"])
```

<div class="m5-code-aside"><p>The normal path scopes to the newest seeded conversation.</p><p>An existing skillId creates another version of the same skill.</p><p>Without a seed record, the script explicitly falls back to workspace scope.</p></div>

<div class="references">

References: [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Imports read_json, seed_state_path, SKILL_NAME, client and call from module-local workflows.nams; wait_for_run is defined in distill.py. existing is selected by GET /v1/skills, matching acme-refund-procedure and preferring the published entry; that lookup is omitted from this condensed snippet and in real code runs inside client before generate. Missing seed produces scope={"type":"workspace"}; no missing-scope request remains. --redistill requires an existing matching skill. wait_for_run GETs runs/{id}, prints status changes, polls every five seconds up to 600 seconds, and returns on succeeded/failed/error/cancelled/error/failCode. main only publishes if status==succeeded. Source lines: 92–117.

References · checked 2026-11-04
NAMS OpenAPI: https://memory.neo4jlabs.com/openapi.json
Live NAMS API: https://memory.neo4jlabs.com/docs -->

---

# Approve, publish and unpack the skill package

<!-- _class: technical m5-code -->

Module 5 · Code reference · `module_5/workflows/distill.py`

**After a succeeded run**

```python
skill_id = run["skillId"]
await call(
    http, "POST", f"/v1/skills/{skill_id}/review",
    {"decision": "approve",
     "feedback": "Approved during the workshop."},
)
await call(
    http, "POST", f"/v1/skills/{skill_id}/publish"
)
package = await http.get(
    f"/v1/skills/{skill_id}/download"
)
package.raise_for_status()
skill_md = unpack(package.content, OUT_DIR)
```

<div class="m5-code-aside"><p>The workshop script submits approval automatically; there is no human pause.</p><p>Download returns a ZIP package.</p><p>Inspect SKILL.md, references/ and provenance.json.</p></div>

<div class="references">

References: [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Approval uses decision=approve with feedback, followed by publish. main prints groundingScore and coverageScore, then makes these calls. OUT_DIR.mkdir occurs before unpack after the HTTP context exits; directory preparation is omitted here. unpack removes one top-level ZIP directory and skips .. members. skill.json separately records skillId, skillVersionId as versionId, and run ID for downstream drift. No human review checkpoint is implemented, even though comments call the API a human-review gate. Source lines: 122–146.

References · checked 2026-11-04
NAMS OpenAPI: https://memory.neo4jlabs.com/openapi.json
Live NAMS API: https://memory.neo4jlabs.com/docs -->

---

# Inspect the downloaded skill package

<!-- _class: m5-cards -->

Module 5 · Portable artifacts

<div class="m5-card-grid"><div><h2>SKILL.md</h2><p>Portable procedure and conditions.</p><p>This is the file the fresh agent loads as instructions.</p></div><div><h2>references/</h2><p>Supporting material shipped in the ZIP.</p><p>The fresh agent does not load these files automatically.</p></div><div><h2>provenance.json</h2><p>Claims and steps map to groundedIn memory IDs.</p><p>These IDs drive the drift demonstration.</p></div></div>

Local skill.json records skillId, versionId and runId; it is a workflow receipt, not a memory store.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: distill.py downloads a ZIP, strips its enclosing skill-name folder and unpacks SKILL.md, references/ and provenance.json into artifacts/distilled. It separately writes skill.json with skillId, versionId from run.skillVersionId, and runId. Fresh-agent consumption reads only SKILL.md; it does not automatically ingest supporting files or verify attestation. Current service deployment determines optional package/attestation fields. Reruns reuse the named skill through skillId and publish a new version.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Inspect the versioned skill graph

- Tick NAMS above the workshop graph, then refresh.
- Follow Skill → SkillVersion → SkillStep → grounded evidence.
- SUPERSEDES connects versions; provenance.json also records claims.
- Use source links to inspect evidence, not to infer correctness.

![diagram](../slides/diagrams/d14-skill-distillation.svg)

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Actual served graph from lib/graph.py NAMS_SKILL_GRAPH: (Skill)-HAS_VERSION→(SkillVersion)-HAS_STEP→(SkillStep)-GROUNDED_IN→(source); versions may SUPERSEDES earlier versions. Source may be Entity, AgentStep or ToolCall. Claims are separately recorded in provenance.json; the UI query does not include SkillClaim nodes. In module5 tick NAMS above the graph; this calls read-only hosted /v1/query through /api/graph/nams. The app filters large documents from properties. Grounding permits source inspection; it does not establish truth or safe execution. The module 5 support app retains the full module 4 Bolt/AuraDB memory behavior. Hosted REST workflows seed canonical authored fixtures into a separate NAMS workspace; they do not migrate participant AuraDB data. Skill distillation builds a reusable procedure on top of memory, not a fourth memory store or model-weight training. Source: module_5/app/agent.py; module_5/app/memory.py; module_5/workflows/*.py.

Diagram detail: Exact served pattern from lib/graph.py: Skill → HAS_VERSION → SkillVersion → HAS_STEP → SkillStep → GROUNDED_IN → evidence; newer version → SUPERSEDES → prior. Evidence nodes are returned with actual labels; “Agent step” names an evidence category, not a guessed label. The workshop query does not require SkillClaim nodes; claim records are in provenance.json. Tick NAMS in the UI.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Quality signals support review

<!-- _class: m5-cards -->

Module 5 · Evaluate the skill

<div class="m5-card-grid"><div><h2>Grounding</h2><p>How much of the procedure has supporting evidence?</p><p>Follow claims and steps to source IDs.</p></div><div><h2>Coverage</h2><p>How much of the selected evidence is represented?</p><p>Inspect omitted cases and conditions.</p></div><div><h2>Review and execution</h2><p>The demo auto-approves publication.</p><p>Inspect the result and test the consumer against current policy.</p></div></div>

High scores and intact source links do not establish correctness, safety or transfer to a new environment.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Memory supplies context, entity knowledge and recorded actions/outcomes. A distillation run selects evidence and derives a portable procedure with conditions and source links. A receiving agent supplies its own tools and authorization and checks current business policy. Grounding is evidence for inspection, not proof of correctness or suitability. nams-check prints deployment groundingThreshold and coverageThreshold; generation prints groundingScore and coverageScore. Avoid hard-coded universal thresholds. The script automatically posts decision=approve and feedback, then publish, without an interactive pause. A production review policy must define who inspects what; a server review state is not proof a human reviewed. Test current SQL policy, account/case authorization and actual execution receipts separately from source provenance.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Give the skill to a fresh PydanticAI agent

<!-- _class: technical m5-code -->

Module 5 · Code reference · `module_5/app/fresh_agent.py`

**Condensed construction + fresh-agent run**

```python
skill = load_skill("on")  # downloaded SKILL.md
instructions = INSTRUCTIONS
instructions += (
    "\n\n## Distilled procedure "
    "(from organizational memory)\n" + skill
)
agent = Agent(
    f"openai:{settings.openai_model}",
    deps_type=ToolDeps,
    tools=list(SQLITE_TOOLS),
    instructions=instructions,
    output_type=str,
)
# deps: private SQLite copy + explicit billing case
result = await agent.run(TICKET, deps=deps)
```

<div class="m5-code-aside"><p>Load SKILL.md into agent instructions.</p><p>No memory client, history or retrieval tools.</p><p>Each mode uses a private SQL copy; issue_refund still checks current policy.</p></div>

<div class="references">

References: [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

</div>

<!-- notes: Imports: Agent from pydantic_ai; INSTRUCTIONS from local app.agent; SQLITE_TOOLS and ToolDeps from local tools. Combines load_skill, create_fresh_agent construction and run_fresh_agent for explicit on mode; real create_fresh_agent appends the heading only if skill is not None. Adjacent literals reproduce the exact heading. Current source: module_5/app/fresh_agent.py:32–85. on requires artifacts/distilled/SKILL.md; fallback explicitly uses artifacts/pre-distilled-skill/SKILL.md; off has no skill. Missing on artifact raises rather than silently becoming a control. run_fresh_agent uses a temporary SQLite copy and clears the Ravi duplicate-compute refund only in that copy, so off/on start from the same open case and the workshop database stays unchanged. ToolDeps supplies Ravi’s account, incident_id and explicit authorization. This direct model demo skips scope_turn/checked_reply and returns model output; issue_refund retains SQL validation. No MemoryClient, message_history or search_memory is installed. One command runs one mode: compare make s5-fresh-agent WITH_SKILL=off and WITH_SKILL=on. Use WITH_SKILL=fallback deliberately for the checked-in fixture. Fewer calls or better outcomes are not guaranteed. The downloaded ZIP also contains references/ and provenance.json, but the receiving agent loads only SKILL.md. Skill distillation transfers an instruction artifact; it does not update model weights.

References · checked 2026-11-04
PydanticAI agents: https://pydantic.dev/docs/ai/core-concepts/agent/
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/ -->

---

# Compare the fresh agent with and without a skill

<!-- _class: m5-demo -->

Module 5 · Live demo

```bash
make s5-fresh-agent \
  WITH_SKILL=off

make s5-fresh-agent \
  WITH_SKILL=on

# Explicit fallback:
make s5-fresh-agent \
  WITH_SKILL=fallback
```

<div class="m5-demo-aside"><p>Run once per mode on a private SQL copy.</p><p>Compare tool receipts and the business outcome.</p><p>No guaranteed improvement; current policy still governs actions.</p></div>

<div class="references">

References: [Skills tutorial](https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: Imports: Agent from pydantic_ai; INSTRUCTIONS from local app.agent; SQLITE_TOOLS and ToolDeps from local tools. Combines load_skill, create_fresh_agent construction and run_fresh_agent for explicit on mode; real create_fresh_agent appends the heading only if skill is not None. Adjacent literals reproduce the exact heading. Current source: module_5/app/fresh_agent.py:32–85. on requires artifacts/distilled/SKILL.md; fallback explicitly uses artifacts/pre-distilled-skill/SKILL.md; off has no skill. Missing on artifact raises rather than silently becoming a control. run_fresh_agent uses a temporary SQLite copy and clears the Ravi duplicate-compute refund only in that copy, so off/on start from the same open case and the workshop database stays unchanged. ToolDeps supplies Ravi’s account, incident_id and explicit authorization. This direct model demo skips scope_turn/checked_reply and returns model output; issue_refund retains SQL validation. No MemoryClient, message_history or search_memory is installed. One command runs one mode: compare make s5-fresh-agent WITH_SKILL=off and WITH_SKILL=on. Use WITH_SKILL=fallback deliberately for the checked-in fixture. Fewer calls or better outcomes are not guaranteed. The downloaded ZIP also contains references/ and provenance.json, but the receiving agent loads only SKILL.md. Skill distillation transfers an instruction artifact; it does not update model weights. Run seed and distill before on. Inspect downloaded package and tick NAMS above the graph. Off has no file; on requires artifacts/distilled/SKILL.md; fallback explicitly loads the checked-in artifact. Missing on artifact raises rather than silently becoming a control. For the quick path, show the code reference without line-by-line explanation.

References · checked 2026-11-04
Skills tutorial: https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/
NAMS console: https://memory.neo4jlabs.com/ -->

---

# Governance follows the evidence

<!-- _class: m5-steps -->

**Change the system of record** — make policy-change updates SQLite; hosted memory is unchanged.

**Delete cited hosted memory** — Read provenance, select policy entities or the most-cited entity, then inspect this skill’s drift.

**Create a new version** — make nams-redistill uses the same skill ID; compare the procedure and changed evidence IDs.

Drift concerns source dependencies. New executions must still check current business policy.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Source: scripts/change_policy.py; module_5/workflows/drift.py; distill.py. policy-change toggles Pro250↔150 and edits refund policy text in SQLite; on lowering it reads current NAMS drift to demonstrate the separate-store boundary. drift.py loads skill.json/provenance.json, counts groundedIn IDs across claims+steps, GETs entities among them, deletes names containing policy or the most-cited entity fallback, then reads only this skillId/drift. It prints returned status and staleClaims/staleSteps with text. The script targets the downloaded skill and the sources recorded in its provenance. Redistill passes existing skillId, yielding a new version; compare text/evidence IDs and rerun the fresh agent. Run policy-change again to restore250.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Follow provenance to the memory a skill uses

<!-- _class: technical m5-code -->

Module 5 · Code reference · `module_5/workflows/drift.py`

**Inside main, after reading skill.json**

```python
provenance = read_json(SKILL_DIR / "provenance.json")
cited = grounding(provenance)
entities = await grounding_entities(http, list(cited))
targets = [e for e in entities
           if "policy" in e["name"].lower()]
if not targets and entities:
    targets = [max(entities,
                   key=lambda e: cited[e["id"]])]
for entity in targets:
    await call(
        http, "DELETE", f"/v1/entities/{entity['id']}"
    )
report = await call(
    http, "GET", f"/v1/skills/{skill_id}/drift"
)
```

<div class="m5-code-aside"><p>Read groundedIn IDs from claims and steps.</p><p>Delete cited policy entities, or the most-cited entity as a fallback.</p><p>Inspect staleClaims, staleSteps and the returned status.</p></div>

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: grounding combines provenance["claims"] and provenance["steps"] and counts each groundedIn node. grounding_entities GETs entities/{id}, keeps 200 responses (other grounding nodes may be messages/steps/tool calls). The actual constant TARGET_HINT="policy" replaces the inline literal shown. Before entering this fragment, the script requires skillId and provenance; if targets remains empty, it exits rather than reporting a successful deletion. It queries only the downloaded skillId, not every workspace skill. Deletes are destructive and should be instructor-led in a disposable workshop workspace. The demonstrated deletion does not edit SQLite. Source lines: 49–68.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Govern the evidence behind a skill

- Read groundedIn IDs from downloaded provenance.
- Delete cited hosted entities; inspect this skill’s drift report.
- Re-distill a new version and compare procedure/evidence changes.
- SQLite policy changes remain a separate store change.

![diagram](../slides/diagrams/d15-governance-loop.svg)

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Source: scripts/change_policy.py; module_5/workflows/drift.py; distill.py. policy-change toggles Pro250↔150 and edits refund policy text in SQLite; on lowering it reads current NAMS drift to demonstrate the separate-store boundary. drift.py loads skill.json/provenance.json, counts groundedIn IDs across claims+steps, GETs entities among them, deletes names containing policy or the most-cited entity fallback, then reads only this skillId/drift. It prints returned status and staleClaims/staleSteps with text. The script targets the downloaded skill and the sources recorded in its provenance. Redistill passes existing skillId, yielding a new version; compare text/evidence IDs and rerun the fresh agent. Run policy-change again to restore250. Diagram should show provenance-selected hosted entity deletion, one skill drift report, new version and verification. Literal service status is drifted; claims and steps are reported as stale. Use circles for any graph entities; process rectangles represent commands, not graph nodes.

Diagram detail: Read skill.json/provenance.json; count groundedIn IDs; resolve entity IDs; delete policy-named cited entities, otherwise most-cited. Ask only the downloaded skillId for its drift report. staleClaims/staleSteps identify lost sources. Re-distillation generates a version of the same skill from current scoped memory, not current SQLite state. make policy-change toggles $250↔$150 and asks drift without synchronizing memory; final invocation restores default. Destructive entity deletion is instructor-led.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Run the drift loop and restore the policy

<!-- _class: m5-demo -->

Module 5 · Instructor-led demo

```bash
make policy-change
make nams-drift
make nams-redistill

make policy-change
# Restores the $250 Pro limit
```

<div class="m5-demo-aside"><p>First: SQLite changes; hosted evidence does not.</p><p>Then: delete cited hosted entities and inspect drifted claims/steps.</p><p>Re-distill a new version; read the diff and source IDs.</p></div>

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Source: scripts/change_policy.py; module_5/workflows/drift.py; distill.py. policy-change toggles Pro250↔150 and edits refund policy text in SQLite; on lowering it reads current NAMS drift to demonstrate the separate-store boundary. drift.py loads skill.json/provenance.json, counts groundedIn IDs across claims+steps, GETs entities among them, deletes names containing policy or the most-cited entity fallback, then reads only this skillId/drift. It prints returned status and staleClaims/staleSteps with text. The script targets the downloaded skill and the sources recorded in its provenance. Redistill passes existing skillId, yielding a new version; compare text/evidence IDs and rerun the fresh agent. Run policy-change again to restore250. nams-drift is destructive: run this instructor-led in a disposable workshop workspace, after inspecting the target provenance. Without target entities it exits and asks for redistillation. The restore command returns SQL Pro limit to250 only when the demo starts at default250. Check printed before/after values; do not assume current policy from a slide. Re-distillation does not synchronize the SQL policy into hosted memory and does not itself prove the new procedure correct.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Hosted capability, explicit boundaries

<!-- _class: m5-concepts -->

<div class="m5-concept-grid"><div><h2>App and consumer</h2><p>Support apps 2–5 retain Bolt memory.</p><p>The fresh consumer reads a portable procedure and uses SQL tools.</p></div><div><h2>Hosted service</h2><p>NAMS provides hosted skill workflows and the skill graph.</p><p>Read capabilities and current contracts; the service evolves independently.</p></div></div>

Teardown: revoke the workshop key; follow docs/teardown.md for hosted data, Codespaces and AuraDB.

<div class="references">

References: [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: The module 5 support app retains the full module 4 Bolt/AuraDB memory behavior. Hosted REST workflows seed canonical authored fixtures into a separate NAMS workspace; they do not migrate participant AuraDB data. Skill distillation builds a reusable procedure on top of memory, not a fourth memory store or model-weight training. Source: module_5/app/agent.py; module_5/app/memory.py; module_5/workflows/*.py. The module README reports a prior live rehearsal of the current Make targets; this slide refresh did not repeat paid or destructive service calls. Offline tests verify current requests against the contract. For delivery, read nams-check output and use explicit fallback if the feature is unavailable. Fallback proves artifact consumption only. Teardown: revoke workshop key, remove disposable hosted data as appropriate, delete Codespace, pause/delete AuraDB per docs/teardown.md.

References · checked 2026-11-04
Backend capabilities: https://neo4j.com/labs/agent-memory/reference/backend-capabilities/
Live NAMS API: https://memory.neo4jlabs.com/docs -->

---

# Module 5 — Exploration brief

<!-- _class: m5-steps -->

1. **Follow a source** — Open provenance.json; trace a claim or step through groundedIn IDs.

2. **Inspect a version** — Tick NAMS in the graph; follow Skill → Version → Step → source.

3. **Explain the drift** — Which source was deleted? Which claims or steps lost evidence?

Compare off/on receipts; inspect a new version and its diff. Catch up: make module-5.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Source: scripts/change_policy.py; module_5/workflows/drift.py; distill.py. policy-change toggles Pro250↔150 and edits refund policy text in SQLite; on lowering it reads current NAMS drift to demonstrate the separate-store boundary. drift.py loads skill.json/provenance.json, counts groundedIn IDs across claims+steps, GETs entities among them, deletes names containing policy or the most-cited entity fallback, then reads only this skillId/drift. It prints returned status and staleClaims/staleSteps with text. The script targets the downloaded skill and the sources recorded in its provenance. Redistill passes existing skillId, yielding a new version; compare text/evidence IDs and rerun the fresh agent. Run policy-change again to restore250. Browser: make dev MODULE=5, select the NAMS checkbox above the graph, refresh after seed/distillation. The query displays Skill, SkillVersion, SkillStep and grounded evidence, plus SUPERSEDES. It does not include SkillClaim nodes; inspect package claims in provenance.json. Discuss raw trace vs reusable procedure vs fresh execution, score limitations and the receiving agent’s current-policy/tool boundary.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Wrap — The eval scoreboard, re-run

- Run `make eval MODULE=N` explicitly; open the panel to read saved results.
- Exact name/email and phrase: seeded messages.
- Signup date: grounded entity fixture. Exact reply: completed trace fixture.
- Private SQL, unique memory, disabled business tools.
- Inspect accepted source IDs; this is a retrieval probe, not an overall quality grade.

<div class="references">

References: [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/)

</div>

<!-- notes: The participant Bolt graph links conversation, entity and reasoning memory. Hosted skill fixtures remain in a separate workspace; a Markdown skill crosses into the fresh agent. No cross-backend graph edges are created. Controlled eval checks exact facts plus accepted source IDs using private SQL and unique namespaces with business tools disabled. It is a retrieval probe, not an overall support-quality grade. The UI loads saved results for the current module; opening it does not invoke a model. Source: scripts/eval.py; web/src/components/EvalScorecard.jsx; module_5/app/fresh_agent.py. Run make eval MODULE=N explicitly. The four fixtures test name/email, unique phrase, SQL-grounded signup date and exact recorded reply. Inspect actual source IDs and unknown/error results. -->

---

# Wrap — Memory is the foundation; skills build on it

- The participant Bolt graph links short-term, long-term and reasoning memory.
- Conversations → messages → mentioned entities; traces → steps → touched entities.
- Hosted skill fixtures stay in a separate NAMS workspace.
- Skill distillation builds reusable procedures on top of memory. A portable SKILL.md crosses into the fresh agent; no cross-backend edges are created.
- Follow source messages, grounded fields and execution receipts.

![diagram](../slides/diagrams/d16-connected-memory.svg)

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

</div>

<!-- notes: The participant Bolt graph links conversation, entity and reasoning memory. Hosted skill fixtures remain in a separate workspace; a Markdown skill crosses into the fresh agent. No cross-backend graph edges are created. Controlled eval checks exact facts plus accepted source IDs using private SQL and unique namespaces with business tools disabled. It is a retrieval probe, not an overall support-quality grade. The UI loads saved results for the current module; opening it does not invoke a model. Source: scripts/eval.py; web/src/components/EvalScorecard.jsx; module_5/app/fresh_agent.py. -->

---

# Wrap — Bolt memory and hosted skill workflows

- **Bolt:** memory-enabled support apps 2–5; your AuraDB and client-side extraction.
- **Module 1:** stateless baseline, without a memory client.
- **Hosted workflows:** separate fixtures, scoped generation, versioned packages and provenance-driven drift.
- **Fresh agent:** downloaded `SKILL.md` + business tools; no memory retrieval.
- Same memory concepts, separate consumption paths and stores.

![diagram](../slides/diagrams/d18-bolt-vs-nams.svg)

<div class="references">

References: [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Connect to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: The participant Bolt graph links conversation, entity and reasoning memory. Hosted skill fixtures remain in a separate workspace; a Markdown skill crosses into the fresh agent. No cross-backend graph edges are created. Controlled eval checks exact facts plus accepted source IDs using private SQL and unique namespaces with business tools disabled. It is a retrieval probe, not an overall support-quality grade. The UI loads saved results for the current module; opening it does not invoke a model. Source: scripts/eval.py; web/src/components/EvalScorecard.jsx; module_5/app/fresh_agent.py. -->

---

# Wrap — Your Monday morning path

- Use the pinned `neo4j-agent-memory[pydantic-ai,openai]` environment and Bolt/OpenAI credentials.
- Construct `MemoryClient(MemorySettings(...))`; write with `short_term.add_message`.
- Run `uv run scripts/monday_memory.py` to write and retrieve one conversation.
- Convert stored roles with `as_model_history`; pass `message_history` to `Agent.run`.
- Put additional semantic, entity or procedure evidence in instructions.

<div class="references">

References: [SDK GitHub](https://github.com/neo4j-labs/agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs)

</div>

<!-- notes: The participant Bolt graph links conversation, entity and reasoning memory. Hosted skill fixtures remain in a separate workspace; a Markdown skill crosses into the fresh agent. No cross-backend graph edges are created. Controlled eval checks exact facts plus accepted source IDs using private SQL and unique namespaces with business tools disabled. It is a retrieval probe, not an overall support-quality grade. The UI loads saved results for the current module; opening it does not invoke a model. Source: scripts/eval.py; web/src/components/EvalScorecard.jsx; module_5/app/fresh_agent.py. uv run scripts/monday_memory.py opens MemoryClient(MemorySettings(...)), writes a unique phrase and queries only that conversation. It asserts and prints retrieved rows, then tells you to convert them using as_model_history and pass message_history to Agent.run; it does not itself call the agent. Other semantic/entity/procedure evidence belongs in instructions. Source: scripts/monday_memory.py; module_2/app/context.py. -->

---

# Resources · Start here

<!-- _class: resources -->

Project and service entry points

## 01 · [GitHub · neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory)

Browse SDK source, examples, issues and contributions. Compare the branch with your installed release.

## 02 · [Official documentation](https://neo4j.com/labs/agent-memory/)

Find concept guides, tutorials and focused API references. Check each example’s version.

## 03 · [NAMS · hosted memory service](https://memory.neo4jlabs.com/)

Open the hosted workspace dashboard and service documentation. Module 5 uses a separate REST workflow.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. Neo4j Agent Memory — GitHub: Python and TypeScript SDK source, examples, issue tracker and contribution entry point. Default branch can advance beyond workshop 0.8.0. Reference: https://github.com/neo4j-labs/agent-memory Neo4j Agent Memory documentation: Official guides, tutorials, concepts and Python/TypeScript API references. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/ NAMS hosted service: Public entry point for the hosted Neo4j Agent Memory Service, its dashboard and service documentation. Verified public entry only. Service behavior, availability, workspace scopes and preview features must be checked in the selected workspace. Module 5's SupportBot still uses Bolt; its separate skill workflow uses hosted REST. Reference: https://memory.neo4jlabs.com/ -->

---

# Resources · Memory concepts

<!-- _class: resources -->

The model behind modules 1–4

## 01 · [Three memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/)

Compare persisted conversation history, durable entity knowledge and recorded task execution.

## 02 · [Why graph memory?](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/)

See how relationships connect messages, entities and execution provenance in one graph.

## 03 · [POLE+O data model](https://neo4j.com/labs/agent-memory/explanation/poleo-model/)

Understand base types and domain subtypes before defining the Acme Cloud ontology.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. Understanding the three memory types: Conversation history, durable knowledge and recorded task execution have distinct retrieval roles. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/explanation/memory-types/ Why Neo4j? Graph memory architecture: How graph relationships join conversations, entities and recorded task traces. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/explanation/graph-architecture/ The POLE+O data model: People, objects, locations, events and organizations provide a common entity model. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/explanation/poleo-model/ -->

---

# Resources · SDK setup and configuration

<!-- _class: resources -->

Pin first; compare versions before copying examples

## 01 · [Pinned Python release · 0.8.0](https://pypi.org/project/neo4j-agent-memory/0.8.0/)

Find the exact workshop release files. Use the repository’s uv.lock and Make recipes.

## 02 · [MemoryClient · lifecycle and stores](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

Check constructor settings, client lifetime, memory accessors and the read-only query surface.

## 03 · [Providers, extraction and schema settings](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

Review LLM, embedding, ontology and resolution configuration; compare with local memory.py.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. Python SDK 0.8.0 — pinned release: Exact workshop package release, downloadable source distribution and wheel. Package description still contains 0.7.0 examples; release files are explicitly 0.8.0. Reference: https://pypi.org/project/neo4j-agent-memory/0.8.0/ MemoryClient API reference: Client lifecycle, memory stores, read-only Cypher interface and ontology precedence. Live examples use BoltSettings; workshop 0.8.0 uses explicit MemorySettings(backend='bolt'). Preserve workshop configuration. Reference: https://neo4j.com/labs/agent-memory/reference/api/memory-client/ Embedding, LLM, schema, extraction and resolution settings: Configure model providers, ontology selection, extraction behavior and entity resolution. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/reference/configuration-providers/ -->

---

# Resources · PydanticAI foundations

<!-- _class: resources -->

Agent construction, tools and dependencies

## 01 · [PydanticAI · agents and instructions](https://pydantic.dev/docs/ai/core-concepts/agent/)

Understand agent construction and the per-run instructions used alongside the base prompt.

## 02 · [PydanticAI · function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/)

Register functions as tools and understand the RunContext dependency boundary.

## 03 · [PydanticAI · typed dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

Follow how runtime services and the selected customer reach tools through ToolDeps.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. PydanticAI — Agents: Construct an agent and provide instructions, tools and per-run context. Rolling documentation; workshop uses locked PydanticAI 2.62.0. Reference: https://pydantic.dev/docs/ai/core-concepts/agent/ PydanticAI — function tools: Register functions as agent tools and use RunContext for typed dependencies. Rolling PydanticAI docs; workshop pins pydantic-ai-slim 2.62.0. Reference: https://pydantic.dev/docs/ai/tools-toolsets/tools/ PydanticAI — dependencies: Pass runtime services and selected customer data into tools through typed dependencies. Rolling PydanticAI docs; workshop pins pydantic-ai-slim 2.62.0. Reference: https://pydantic.dev/docs/ai/core-concepts/dependencies/ -->

---

# Resources · Short-term memory

<!-- _class: resources -->

Persistence, retrieval scope and typed history

## 01 · [Conversation and message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/)

Inspect add_message, conversation creation and retrieval of persisted turns.

## 02 · [Message search and context scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

Read semantic-search scope limits; the workshop deliberately uses namespace-scoped local Cypher.

## 03 · [PydanticAI · messages and history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

Pass typed prior turns through message_history; keep additional retrieved evidence in instructions.

<div class="resource-footer">

[Short-term memory API overview](https://neo4j.com/labs/agent-memory/reference/api/short-term/) · Workshop SDK 0.8.0; compare docs with local code.

</div>

<!-- notes: Verified resources on 2026-11-04. Conversation and message operations: add_message, get_conversation and related persistence operations. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/ Message search and context: Semantic search, similarity metadata and the scope limits of built-in context retrieval. Official page notes Bolt session_id does not isolate semantic search and get_context can include global matches. Workshop local namespace-scoped retrieval is intentional. Reference: https://neo4j.com/labs/agent-memory/reference/api/short-term-search/ PydanticAI — messages and chat history: Pass typed message history to later agent runs; inspect messages returned by an execution. Rolling PydanticAI docs; workshop pins pydantic-ai-slim 2.62.0. Reference: https://pydantic.dev/docs/ai/core-concepts/message-history/ ShortTermMemory API reference Reference: https://neo4j.com/labs/agent-memory/reference/api/short-term/ -->

---

# Resources · Entities and ontologies

<!-- _class: resources -->

Structure, identity and SQL grounding boundaries

## 01 · [Entity and relationship API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/)

Check entity upserts, relationship operations and returned values before extending hydration.

## 02 · [Ontology-driven extraction](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/)

Read YAML types, aliases, descriptions and validation. Workshop extraction uses the LLM path.

## 03 · [Entity resolution and deduplication](https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/)

Study canonical identity, aliases, similarity signals and reviewed duplicate handling.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. Entity and relationship operations: add_entity returns an entity/deduplication pair; entity search and relationship operations. Workshop PropertyWriter is repository code; do not imply it is a neo4j-agent-memory API. Reference: https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/ Drive extraction from an ontology: Define YAML entity labels, descriptions, relationships, aliases and validation constraints. Guide pins 0.7.0 and demonstrates GLiNER 2.5 as well as LLM configuration. Workshop uses an LLM extractor with its checked-in ontologies. Reference: https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/ Entity resolution and deduplication: Canonical entity identity, aliases, similarity matching and duplicate review. Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples. Reference: https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/ -->

---

# Resources · Preferences and integration

<!-- _class: resources -->

Customer scope and application-owned memory policy

## 01 · [Preference and fact API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/)

Inspect add_preference and get_preferences_for; keep explicit customer scope in application code.

## 02 · [How extraction works](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/)

Distinguish candidate extraction, validation and resolution. The broader pipeline is optional background.

## 03 · [Neo4j + PydanticAI integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

Compare the SDK integration with this workshop’s explicit history, tools and local retrieval helpers.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. Preference and fact operations: Save preferences and retrieve them with explicit user and optional entity filters. Preference category and semantic search are not customer authorization boundaries; workshop uses explicit user_identifier. Reference: https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/ How entity extraction works: Compare extraction approaches and distinguish candidate generation, validation and entity resolution. The general multi-stage pipeline is broader than the workshop's configured LLM-only extraction. Reference: https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/ Use Neo4j Agent Memory with PydanticAI: Official integration recipe for retrieving context, exposing memory tools and persisting a turn. Recipe explicitly targets SDK 0.6.0 and shipped MemoryDependency/create_memory_tools. Workshop 0.8.0 deliberately uses local ToolDeps, scoped helpers and typed message_history. Reference: https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/ -->

---

# Resources · Record an execution

<!-- _class: resources -->

Trace lifecycle, observations and outcomes

## 01 · [Trace lifecycle API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

Read start_trace, complete_trace and get_trace_with_steps alongside the module 4 code.

## 02 · [Steps, tool calls and provenance](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/)

Inspect add_step, record_tool_call, message links and Step → TOUCHED → Entity semantics.

## 03 · [TraceOutcome and reasoning models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/)

Check status, outcome and identifier fields; recorded execution is not hidden model reasoning.

<div class="resource-footer">

[Reasoning API overview](https://neo4j.com/labs/agent-memory/reference/api/reasoning/) · Workshop SDK 0.8.0; compare docs with local code.

</div>

<!-- notes: Verified resources on 2026-11-04. Trace lifecycle API: Exact start_trace, complete_trace and get_trace_with_steps contracts for recording and reading an observable task execution. Workshop pins SDK 0.8.0. Module 4 uses explicit application recording around its guards and SQL operations; hosted trace behavior is different. The resource is a focused page, not an unverified fragment. Reference: https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/ Steps, tool calls and message provenance: add_step, record_tool_call and link_trace_to_message; touched_entities links a ReasoningStep to Entity through TOUCHED. Bolt behavior matches the graph concept used in the workshop; do not assume NAMS preserves these optional links or arguments. Reference: https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/ Reasoning models and TraceOutcome: Pydantic fields for ReasoningTrace, ReasoningStep, ToolCall and structured outcomes, including their identifiers and status conventions. Use the workshop's pinned SDK for executable code. The models describe recorded application events and results, not hidden model reasoning. Reference: https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/ ReasoningMemory API index Reference: https://neo4j.com/labs/agent-memory/reference/api/reasoning/ -->

---

# Resources · Retrieve and audit traces

<!-- _class: resources -->

Failures can be useful examples; inspect actual receipts

## 01 · [Trace search and backend differences](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/)

Compare SDK search with the local completed-trace, namespace-scoped retrieval used here.

## 02 · [Record a failed tool call](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/)

Work through a separate Bolt example that records failure, completes an outcome and verifies readback.

## 03 · [Audit execution with TOUCHED](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

Follow step-to-entity dependencies and source messages; check backend support before transferring queries.

<div class="resource-footer">

Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

</div>

<!-- notes: Verified resources on 2026-11-04. Trace search and hosted lifecycle differences: Reference for similar-trace and step search, tool statistics, and the NAMS synthetic trace lifecycle. Workshop similar_executions is local, namespace-scoped Cypher over completed traces followed by SDK get_trace_with_steps. It does not call the SDK get_similar_traces API described here. Reference: https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/ Record and verify a failed tool call: Worked Bolt recipe: start a trace, record a failed tool action, complete its outcome, and verify readback. Online recipe explicitly installs SDK 0.7.0 while the workshop pins 0.8.0. Follow the repo's uv/Make commands for the workshop, not this separate tutorial's environment setup. Reference: https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/ Audit reasoning with TOUCHED edges: Follow recorded steps to referenced entities and connect trace/tool activity to source messages for provenance queries. Guide targets Bolt and SDK 0.7.0. It explicitly warns that Python NAMS drops touched_entities; a callable method is not proof of equivalent hosted persistence. Reference: https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/ -->

---

# Resources · NAMS: service and scope

<!-- _class: resources -->

Hosted contracts evolve independently of the SDK pin

## 01 · [NAMS · live endpoint documentation](https://memory.neo4jlabs.com/docs)

Check request fields, scope, capabilities and hosted lifecycle responses.

## 02 · [Connect Python to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/)

Learn the SDK connection route and hosted conversation identifiers; the workshop uses direct REST workflows.

## 03 · [Bolt vs. NAMS · capability matrix](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/)

Compare supported operations, identifiers and data scope. Similar method names do not imply parity.

<div class="resource-footer">

[NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [API key dashboard](https://memory.neo4jlabs.com/dashboard/api-keys) · Workshop generation uses explicit conversation scope.

</div>

<!-- notes: Verified resources on 2026-11-04. NAMS live API documentation: Current hosted endpoint and request reference, including Skill Generation, capabilities, governance, review, publication and drift. Current workflow sends nameHint and explicit conversations scope, adding skillId for a new version. Missing local seed state warns and falls back to workspace scope. Check the live deployment contract before delivery. Reference: https://memory.neo4jlabs.com/docs Connect Python to NAMS: Configure a workspace key and hosted endpoint, then use the conversation identifier returned by NAMS for scoped message operations. Separate SDK memory connection route. The workshop uses direct HTTPX for hosted skill workflows and authored fixtures, while its support app retains Bolt/AuraDB. Reference: https://neo4j.com/labs/agent-memory/how-to/use-nams/ Bolt vs NAMS capabilities and scope: Compare message, entity, preference, reasoning and extraction operations by backend; understand identifier and retrieval scope boundaries. Reference explicitly describes Python 0.7.0 and TypeScript 0.5.0; workshop pins Python 0.8.0. NAMS is continuously shipped and /v1 is not an SDK version. Treat this as a capability checklist and check the installed version. Reference: https://neo4j.com/labs/agent-memory/reference/backend-capabilities/ NAMS OpenAPI specification Reference: https://memory.neo4jlabs.com/openapi.json NAMS API key dashboard Reference: https://memory.neo4jlabs.com/dashboard/api-keys -->

---

# Resources · Skills and governance

<!-- _class: resources -->

Generation, publication, drift and portable artifacts

## 01 · [Agent Skills · concepts and provenance](https://neo4j.com/labs/agent-memory/explanation/skills/)

Separate distillation, review and consumption. Grounding supports inspection; it does not prove correctness.

## 02 · [Skills API · generate, publish and drift](https://neo4j.com/labs/agent-memory/reference/skills-api/)

Inspect required scopes, run outcomes, review, publication and per-skill drift endpoints.

## 03 · [Distill and download a procedure](https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/)

Follow a separate hosted tutorial through fixture seeding, provenance inspection and SKILL.md download.

<div class="resource-footer">

Hosted preview: inspect the current contract and returned evidence before trusting a generated skill.

</div>

<!-- notes: Verified resources on 2026-11-04. Agent Skills concepts and provenance: Skills distill selected memory into portable procedures. Creation, review and consumption are separate; grounding and integrity do not establish correctness. Preview REST/MCP feature, with no SDK skill accessor or Bolt skill API. A skill is derived from memory, not a fourth memory layer. Receiving application executes it; documented service execution is gated dry-run planning. Reference: https://neo4j.com/labs/agent-memory/explanation/skills/ Skills API: generate, review, publish and drift: Hosted skill endpoints, required scopes, run outcomes, publication, provenance, attestation and drift checks. Current workflow polls succeeded runs, automatically submits decision=approve, publishes and downloads a ZIP. This is not an interactive human review checkpoint. Skills may have deployment-specific gates and attestation. Reference: https://neo4j.com/labs/agent-memory/reference/skills-api/ Distil and download a recorded procedure: Complete official exercise using a simulated refund procedure: seed a fixture, distill, inspect provenance, explicitly publish and verify the downloaded SKILL.md package. Separate SDK 0.7.0 tutorial with a dedicated empty workspace and different request flow. It stops after package verification; it does not demonstrate execution in a receiving agent. Workshop's fresh_agent.py supplies that separate application example. Reference: https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/ -->

---

# Resources · GraphAcademy: Python path

<!-- _class: resources -->

Courses that continue the workshop’s core concepts

## 01 · [Context Graphs: Agent Memory with Neo4j](https://graphacademy.neo4j.com/courses/genai-context-graphs)

Continue with Python memory concepts, POLE+O extraction and queries across the context graph.

## 02 · [Neo4j Agent Memory Workshop](https://graphacademy.neo4j.com/courses/workshop-agent-memory)

Build a PydanticAI learning assistant and implement a custom memory tool.

## 03 · [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals)

Practice graph patterns and filtering before adapting the workshop’s scoped retrieval queries.

<div class="resource-footer">

Free GraphAcademy learning paths. Course exercises use their own repositories and environments.

</div>

<!-- notes: Verified resources on 2026-11-04. Context Graphs: Agent Memory with Neo4j: Self-paced Python course covering short-term, long-term and reasoning memory, POLE+O extraction, and querying the context graph.  Reference: https://graphacademy.neo4j.com/courses/genai-context-graphs Neo4j Agent Memory Workshop: Build a PydanticAI learning assistant with conversation, entity and reasoning memory, then implement a custom memory tool.  Reference: https://graphacademy.neo4j.com/courses/workshop-agent-memory Cypher Fundamentals: Practice matching nodes and relationships, filtering graph results, and creating or updating data with Cypher.  Reference: https://graphacademy.neo4j.com/courses/cypher-fundamentals -->

---

# Resources · Other stacks and releases

<!-- _class: resources -->

Alternative learning paths; verify the selected stack

## 01 · [Agent Memory in 90 Minutes](https://graphacademy.neo4j.com/courses/workshop-agent-memory-90)

Adjacent path: Copilot, MCP and AIP skill distillation; a different workflow from module 5.

## 02 · [Agent Memory Workshop with TypeScript](https://graphacademy.neo4j.com/courses/workshop-agent-memory-ts)

Adjacent path: a Mastra assistant, graph retrieval, context traces and code-enforced guardrails.

## 03 · [SDK release notes](https://github.com/neo4j-labs/agent-memory/releases)

Track published changes before upgrading. Compare release notes, package files and your lockfile.

<div class="resource-footer">

Copilot/AIP and TypeScript/Mastra are adjacent paths, not the Python SupportBot implementation.

</div>

<!-- notes: Verified resources on 2026-11-04. Agent Memory in 90 Minutes: Explore a scaffolded agent, connect Copilot to memory through MCP, build a coding assistant, and distil portable skills with AIP.  Reference: https://graphacademy.neo4j.com/courses/workshop-agent-memory-90 Agent Memory Workshop with TypeScript: Extend a Mastra personal assistant with memory, context traces, graph retrieval and code-enforced guardrails; then build your own agent.  Reference: https://graphacademy.neo4j.com/courses/workshop-agent-memory-ts Neo4j Agent Memory — releases: Published GitHub release notes and change history. Page retrieved lists 0.7.0 as latest; do not label this as the 0.8.0 release. Reference: https://github.com/neo4j-labs/agent-memory/releases -->

---

# Resources · Read: context graphs

<!-- _class: resources -->

Official Neo4j articles for broader design context

## 01 · [Lenny’s Memory · context graphs](https://neo4j.com/blog/developer/meet-lennys-memory-building-context-graphs-for-ai-agents/)

A package introduction and PydanticAI example linking conversations, entities and reasoning traces.

## 02 · [Modeling agent memory](https://neo4j.com/blog/developer/modeling-agent-memory/)

Background on memory models and write strategies. Its older taxonomy differs from this workshop.

## 03 · [When agents share a brain](https://neo4j.com/blog/developer/when-your-agents-share-a-brain-building-multi-agent-memory-with-neo4j/)

Explore a Strands example that shares graph-backed memory across multiple agents.

<div class="resource-footer">

Articles explain concepts and examples; use current API references and the workshop pin for code.

</div>

<!-- notes: Verified resources on 2026-11-04. Meet Lenny’s Memory: Building context graphs for AI agents: Package introduction and PydanticAI demo connecting conversations, entities and reasoning traces into one context graph.  Reference: https://neo4j.com/blog/developer/meet-lennys-memory-building-context-graphs-for-ai-agents/ Modeling agent memory: Conceptual graph models for agent memory, including semantic, episodic and procedural knowledge and trade-offs in when memories are written.  Reference: https://neo4j.com/blog/developer/modeling-agent-memory/ When your agents share a brain: Building multi-agent memory with Neo4j: A Strands multi-agent example shares conversation, entity and reasoning memory through a common Neo4j graph and tool set.  Reference: https://neo4j.com/blog/developer/when-your-agents-share-a-brain-building-multi-agent-memory-with-neo4j/ -->

---

# Resources · Read: integrations and skills

<!-- _class: resources -->

Framework integration, hosted memory and distillation

## 01 · [Microsoft Agent Framework + Neo4j](https://neo4j.com/blog/developer/building-an-ai-agent-with-memory-microsoft-agent-framework-neo4j/)

Explore conversation, preference, entity and trace memory in another agent framework.

## 02 · [A tour of NAMS](https://neo4j.com/blog/genai/a-tour-of-the-neo4j-agent-memory-service-nams/)

See the hosted console and managed memory pipeline accessed through REST or MCP.

## 03 · [From Agent Memory to Portable Skills](https://neo4j.com/blog/genai/from-agent-memory-to-portable-skills/)

Read about scoped distillation, SKILL.md reuse and governance as the source memory changes.

<div class="resource-footer">

Articles explain concepts and examples; use current API references and the workshop pin for code.

</div>

<!-- notes: Verified resources on 2026-11-04. Building an AI agent with memory: Microsoft Agent Framework + Neo4j: A transport-assistant example showing persistent conversations, preferences, entities and trace retrieval through Microsoft Agent Framework integration.  Reference: https://neo4j.com/blog/developer/building-an-ai-agent-with-memory-microsoft-agent-framework-neo4j/ A Tour of the Neo4j Agent Memory Service (NAMS): Walk through the hosted service, its console and managed graph-memory pipeline accessed through REST or MCP.  Reference: https://neo4j.com/blog/genai/a-tour-of-the-neo4j-agent-memory-service-nams/ From Agent Memory to Portable Skills: Explain scoped NAMS skill distillation, evidence-backed SKILL.md packages, fresh-agent reuse and the governance loop for changing memory.  Reference: https://neo4j.com/blog/genai/from-agent-memory-to-portable-skills/ -->
