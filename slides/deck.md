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
  .two-terminal { grid-column: 1; grid-row: 3 / span 4; }
  .two-terminal h2, .mode-grid h2 { margin: 8px 0; font-size: 24px; }
  .two-terminal pre { margin: 0 0 15px !important; padding: 12px !important; }
  section.route-comparison { font-size: 23px; padding: 46px 50px 70px; }
  section.route-comparison h1 { margin-top: 0; font-size: 34px; }
  .mode-grid { display: grid; grid-template-columns: 1fr 1.15fr; gap: 28px; }
  .mode-grid > div { border-top: 4px solid #626dff; background: #edf4f5; padding: 18px; border-radius: 14px; }
  .mode-grid pre { padding: 10px; margin: 8px 0; font-size: 17px; }
  section.trace-audit:has(> p > img) { display: flex; flex-direction: column; justify-content: flex-start; gap: 6px; }
  section.trace-audit:has(> p > img) p:has(img) { align-self: center; width: 88%; }
  section.trace-audit:has(> p > img) img { height: 145px; }
  section.resources { background: #faf8f5; color: #004063; padding: 46px 64px 72px; font-size: 22px; }
  section.resources h1 { font-size: 34px; color: #004063; margin-bottom: 8px; }
  section.resources h2 { font-size: 25px; color: #0a6190; margin: 22px 0 5px; }
  section.resources p { margin: 0 0 8px; line-height: 1.35; }
  section.resources a { color: #0a6190; text-decoration: underline; }
  section.resources .resource-footer { position: absolute; left: 64px; right: 64px; bottom: 22px; font-size: 17px; line-height: 1.3; color: #004063; }
  section.resources .resource-footer p { margin: 0; }
  .m5-code-aside { grid-column: 2; grid-row: 4 / span 5; }
  .m5-code-aside p { margin: 0 0 13px; font-size: 21px; line-height: 1.22; }
  .m5-code-aside p:first-child { color: #004063; }
  .m5-concept-grid pre { font-size: 16px; padding: 12px; white-space: pre-wrap; }
  section .resource-footer a { text-decoration: underline; }
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

- Start the Acme Cloud support workshop in [GitHub Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) or use the [local setup](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md).
- Run the agent, compare memory behavior, and inspect the evidence for a refund.
- Read each complete agent in `module_N/app/agent.py`. Follow the [Module 1 entry point](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_1/app/agent.py).
- PydanticAI, neo4j-agent-memory and AuraDB · 150 minutes.

<div class="references">

References: [SDK GitHub](https://github.com/neo4j-labs/agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/)

</div>

<!-- notes: Start each module at module_N/app/agent.py; compare adjacent app/ directories. Agent behavior, memory configuration and guardrails are intentionally local copies. Shared lib supplies HTTP transport, settings, SQLite access, receipts and response envelopes. Participants run and inspect the complete implementations; no coding exercise is required. Source: AGENTS.md; docs/adr/004-folder-per-module-progression.md; README.md. Module 1 is the no-memory control. Memory-enabled support apps 2–5 use AuraDB; optional module-5 hosted workflows use a separate NAMS workspace. -->

---

# What you’ll leave with

- A running app with a complete agent in each module directory.
- Conversation, entity and execution evidence in your Bolt graph.
- A controlled retrieval scorecard and a portable procedure.
- Start at [the baseline agent](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_1/app/agent.py). Compare adjacent module folders as each memory behavior appears.

![Conversation has messages, messages mention entities, and a reasoning trace starts from a message.](diagrams/d02-three-memory-types.svg)

<div class="references">

References: [Memory docs](https://neo4j.com/labs/agent-memory/) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/)

</div>

<!-- notes: Start each module at module_N/app/agent.py; compare adjacent app/ directories. Agent behavior, memory configuration and guardrails are intentionally local copies. Shared lib supplies HTTP transport, settings, SQLite access, receipts and response envelopes. Participants run and inspect the complete implementations; no coding exercise is required. Source: AGENTS.md; docs/adr/004-folder-per-module-progression.md; README.md. -->

---

# Agenda · 150 min

- **0–15** Set up · **15–30** Establish the stateless baseline.
- **30–50** Recover messages · **50–90** Extract and ground entities.
- **90–95** Buffer · **95–125** Record and compare executions.
- **125–145** Build on memory with a skill. At **130**, switch to the checked-in skill if a package is unavailable.
- **145–150** Read the scorecard and choose a take-home path.

[Facilitator timetable](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/run-of-show.md) · [Capstone live route](#47) · [Fallback comparison](#62)

<div class="references">

References: [GraphAcademy: Python](https://graphacademy.neo4j.com/courses/workshop-agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/)

</div>

<!-- notes: Say — The optional capstone has twenty minutes.

Show — At 125 open the service boundary and check whether a package is available. Decide at 130.

If blocked — Use off/fallback, then the wrap. The full non-hosted timetable is in the run of show. -->

---

# Add memory, then build on it

- Expose a failure in what the current agent can remember.
- Add each memory type; compare complete module implementations.
- Build a reusable procedure on top of the resulting memory.
- Run fixed Make recipes and inspect measured evidence.
- Evaluate exact facts, source IDs and action receipts; model results can vary.

![Stateless, short-term, long-term and reasoning memory build toward a portable skill.](../slides/diagrams/d03-workshop-arc.svg)

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Lenny’s Memory](https://neo4j.com/blog/developer/meet-lennys-memory-building-context-graphs-for-ai-agents/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

</div>

<!-- notes: Skill distillation builds a reusable procedure on the three memory types; it is not a fourth memory layer.  Start each module at module_N/app/agent.py; compare adjacent app/ directories. Agent behavior, memory configuration and guardrails are intentionally local copies. Shared lib supplies HTTP transport, settings, SQLite access, receipts and response envelopes. Participants run and inspect the complete implementations; no coding exercise is required. Source: AGENTS.md; docs/adr/004-folder-per-module-progression.md; README.md. -->

---

# Module 0 — Your environment

- [Open the workshop in Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) or use the [workshop checkout and local setup](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md).
- Start in the repository root. Terminal 1 serves the active module on port 5173.
- Terminal 2 runs scenarios and evaluations. Refresh graph to inspect a CLI replay.
- Keep credentials in private .env or personal Codespaces secrets.

![The workshop app connects separately to AuraDB, OpenAI, and the optional hosted NAMS workspace.](diagrams/d04-environment-map.svg)

<div class="references">

References: [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [NAMS console](https://memory.neo4jlabs.com/) · [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Connect to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/)

</div>

<!-- notes: Say — Use the workshop repository and a private configuration for each participant.

Show — Open the readiness instructions and the module-local agent directory.

If blocked — A facilitator can continue the walkthrough with a labeled saved replay. -->

---

# Module 0 — Credential checklist

- Set `NEO4J_URI`, `NEO4J_USERNAME` and `NEO4J_PASSWORD` in `.env`.
- Set `OPENAI_API_KEY` in a personal Codespaces secret or `.env`.
- `NAMS_API_KEY` is needed only for hosted module-5 workflows.
- The devcontainer scaffolds `.env` from `.env.example`; see the pre-work email.

<div class="references">

References: [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: Say — Use the workshop repository and a private configuration for each participant.

Show — Open the readiness instructions and the module-local agent directory.

If blocked — A facilitator can continue the walkthrough with a labeled saved replay. -->

---

# Module 0 — Smoke test, live

<!-- _class: m5-demo -->

From the workshop root · use Terminal 1

```bash
make check
make dev MODULE=1
```

<div class="m5-demo-aside"><p>Wait for Ready. Open port 5173 and confirm the Module 1 badge.</p><p>Keep Terminal 1 running. Open Terminal 2 for scenarios.</p><p>Before switching modules, press Ctrl+C in Terminal 1, start the next module, then reload.</p></div>

<div class="references">

References: [Workshop instructions](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md) · [Open Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Say — The check reports the median Aura query time and readiness of the configured services.

Show — Run make check, start Module 1, open port 5173, and point out the badge.

If blocked — Use the Ports tab to open 5173. If the badge differs, stop the older server and start Module 1. -->

---

# Module 1 — Two stores, two jobs

- **SQLite is the system of record:** accounts, catalog, current policy and refund writes.
- **Neo4j is memory:** messages, entities and execution records in modules 2–5.
- Module 1 starts without a memory client.
- Memory supplies evidence; current SQL policy authorizes business actions.

![The support app acts through SQLite business tools and retrieves supporting memory from Neo4j.](../slides/diagrams/d01-two-stores.svg)

<div class="references">

References: [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. PydanticAI’s prepare_refund exposes the write only when the customer, case and authorization are present. SQL checks policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. This diagram describes the architecture as memory is added. SQLite remains the system of record; module 1 uses only its business tools. -->

---

# Module 1 — Meet the agent

- PydanticAI + FastAPI backend; React + NVL frontend.
- Read `module_N/app/agent.py`: every module owns a complete agent.
- Five SQLite tools: `lookup_account`, `search_product_catalog`, `fetch_policy`, `check_service_status`, `issue_refund`.
- Local `guardrails.py` checks case scope and replies; `ReceiptGuard` reuses completed request IDs.
- PydanticAI offers `issue_refund` only for a selected customer, case and authorized message. SQL rechecks the write.

<div class="references">

References: [Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) · [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. PydanticAI’s prepare_refund exposes the write only when the customer, case and authorization are present. SQL checks policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. -->

---

# The baseline: PydanticAI + business tools

<!-- _class: technical m5-code -->

Module 1 · Code reference · [module_1/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_1/app/agent.py)

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

<div class="m5-code-aside"><p><b>Follow <code>scope_turn(deps, policy_plan)</code></b></p><p>The selected case determines the current-turn scope.</p><p>Four read tools; one conditional write.</p><p>No message_history is supplied.</p><p>prepare_refund checks customer, case and authorization.</p></div>

<div class="references">

References: [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

</div>

<!-- notes: Say — The selected case determines the current-turn scope.

Show — Point to scope_turn(deps, policy_plan) and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Construction and normal-turn fragments from module_1/app/agent.py. Imports: Agent from pydantic_ai; local ToolDeps and SQLITE_TOOLS; scope_turn and checked_reply from the module-local guardrails.py. INSTRUCTIONS is the actual constructor prompt constant. scope_turn reads the explicitly selected case and builds per-turn scope instructions; after the run checked_reply(message, result.output, deps, scope) verifies action claims against receipts. The full app handles errors and timing. Shared ReceiptGuard.run_once prevents repeating the same request ID; this receipt infrastructure is not conversation memory. Module 1 opens no MemoryClient and uses OpenAI for chat only. Visible browser chat bubbles are not sent back to the model. PydanticAI’s Tool prepare hook offers issue_refund only for a selected customer and billing case with authorization for this message. lookup_account reads refund history. The SQL write still validates the case, amount, current plan limit and uniqueness. -->

---

# Module 1 — The failure: statelessness

- Every turn calls `Agent.run` without prior messages or retrieved memory.
- Even the same browser conversation forgets earlier turns.
- A restart is not required to expose the gap.
- Persistent storage plus explicit retrieval supplies the missing context.

![The second Agent.run receives the new message and its case scope. The first turn is absent from its input.](../slides/diagrams/d05-statelessness.svg)

<div class="references">

References: [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/)

</div>

<!-- notes: Module 1 has five SQLite business tools and no memory client or message_history. Browser bubbles are not model context. The local guardrails.py calls scope_turn and checked_reply; safety is present before memory is added. Customer, Billing case and Authorize selected refund for this message provide explicit per-turn scope; authorization resets each turn. PydanticAI’s prepare_refund exposes the write only when the customer, case and authorization are present. SQL checks policy, identity, amount and uniqueness. ReceiptGuard.run_once reuses saved request IDs. No escalation tool exists; service statuses are seeded examples. Source: module_1/app/agent.py; module_1/app/tools.py; module_1/app/guardrails.py; lib/operations.py. -->

---

# Module 1 — Live demo: the stateless baseline

<!-- _class: m5-demo -->

Terminal 2 · browser badge must read Module 1

```bash
make s1-baseline
```

<div class="m5-demo-aside"><p>First, the agent can look up an account using a supplied email. Next, it forgets the email from the earlier turn.</p><p>Refresh graph → Saved replay · s1-baseline. Read both replies and the first tool result.</p></div>

<div class="references">

References: [Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) · [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: In Execution evidence · Saved replay, expand the original turns and inspect the lookup_account result and SQL. Current conversation switches the panel back to browser turns. Say — A self-contained lookup succeeds even before memory is installed.

Show — Compare the lookup and follow-up in the saved replay.

If blocked — Confirm the Module 1 badge and refresh the replay list. -->

---

# Module 1 — The eval baseline

- Run `make eval MODULE=1`. A private SQL copy and uniquely scoped fixtures isolate four retrieval probes.
- **Named customer lookup** receives a name and asks for name + email. A message or entity is an accepted source.
- The remaining probes ask for a conversation phrase, grounded signup date, and **prior decision quote**.
- All expected values and at least one accepted source ID must match. Business tools are disabled.
- Open Evaluation lab to inspect each pass or miss.

<div class="references">

References: [Grader](https://github.com/johnymontana/road-to-agent-memory/blob/main/scripts/eval.py) · [Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/)

</div>

<!-- notes: Say — The four probes check fixture retrieval.

Show — Show a pass with an accepted ID and an otherwise exact value with a missing ID marked failed.

If blocked — Use the grader and a labeled example if no local scorecard is available. -->

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

- The SDK persists messages, entities, preferences and execution traces.
- Recent turns retain roles in PydanticAI message_history. Retrieved user text gets an explicit evidence heading in instructions.
- A workshop namespace groups conversations. Customer authorization is separately checked for the selected action.
- The module-local app composes inputs, runs the model and records the result.

<div class="references">

References: [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

</div>

<!-- notes: This is explicit integration, not an automatic Agent wrapper. A long-lived module-local MemoryClient stores records. Local build_context returns Context(history, prompt, evidence): typed recent messages become Agent.run(message_history=context.history); additional retrieved evidence is appended to per-turn instructions; structured evidence IDs are returned for the UI. Constructing a MemoryClient alone does not give an agent history. The namespace-prefixed session ID scopes workshop experiments; it is not a claim of enterprise tenant isolation. Retrieved evidence is not authority or current SQL policy. Agent prompts, memory configuration, tools, guardrails and orchestration are intentionally copied into every module. Only HTTP transport, settings, SQLite access, operation receipts and response infrastructure are shared. Read app/agent.py first; compare adjacent app folders to see the added concept. -->

---

# Configure and open one memory client

<!-- _class: technical m5-code -->

Library introduction · Code reference · [module_2/app/memory.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/memory.py)

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

<div class="m5-code-aside"><p><b>Follow <code>async with MemoryClient(config)</code></b></p><p>The module reuses one connected client across turns.</p><p>MemoryClient and MemorySettings are package APIs.</p><p>Modules 2–5 open module-local Bolt clients.</p><p>The async context owns the connection lifetime.</p></div>

<div class="references">

References: [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Say — The module reuses one connected client across turns.

Show — Point to async with MemoryClient(config) and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Condensed from module_2/app/memory.py build_settings/open_memory. Imports: MemoryClient and MemorySettings from neo4j_agent_memory. AppSettings reads environment or .env; get_settings exports the configured OpenAI key for package clients. Database and bounded connection/retry settings are omitted only from the display. Pin: neo4j-agent-memory[pydantic-ai,openai]==0.8.0. Module 1 has no MemoryClient and uses OpenAI for chat only. The full support apps in modules 2–5 use module-local Bolt clients and OpenAI for chat and embeddings; modules 3–5 additionally configure LLM extraction. Module 2 sets extractor_type="none". Optional hosted NAMS REST workflows and the module-5 fresh skill consumer are separate paths. This example passes MemorySettings explicitly; backend is a settings field, not a MemoryClient constructor keyword. -->

---

# Module 2 — Concept: short-term memory

- Conversations and messages persist as graph data and survive process restarts.
- `short_term.add_message` creates the conversation on first use.
- Recent turns become typed PydanticAI `message_history`.
- Scoped user messages become evidence in instructions.
- Inspect source IDs and `recent_conversation` / `semantic_message` paths.

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Short-term API index](https://neo4j.com/labs/agent-memory/reference/api/short-term/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user messages (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. -->

---

# Module 2 — Message chains in the graph

- Each Message belongs to the Conversation through its own `HAS_MESSAGE` edge.
- `NEXT_MESSAGE` describes chronological succession.
- Recent-history retrieval matches Conversation → HAS_MESSAGE → Message, orders by timestamp and ID, and reverses the newest window.
- In Live memory, inspect identity, role and content for an actual returned record.

![Each conversation has a membership edge to each stored message. Separate NEXT_MESSAGE edges link messages in sequence.](diagrams/d06-message-chains.svg)

<div class="references">

References: [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Say — Each message belongs directly to its conversation.

Show — Follow HAS_MESSAGE, then compare NEXT_MESSAGE with the query ordering by timestamp and ID.

If blocked — Open the diagram and the linked local history query. -->

---

# Persist both sides of a conversation

<!-- _class: technical m5-code -->

Module 2 · Code reference · [module_2/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/agent.py)

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

<div class="m5-code-aside"><p><b>Follow <code>short_term.add_message</code></b></p><p>Both participants’ turns persist under the same session ID.</p><p>Reuse the same session ID after restart.</p><p>add_message creates the conversation on first use.</p><p>Module 2 disables entity extraction in its settings.</p></div>

<div class="references">

References: [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

</div>

<!-- notes: Say — Both participants’ turns persist under the same session ID.

Show — Point to short_term.add_message and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Normal persistence path from module_2/app/agent.py ChatService._turn. short_term is self.memory.short_term. The service prefixes session IDs with the workshop namespace. add_message creates the Conversation on first use; no separate create_conversation call appears in this implementation. The user flag is extract_entities=not self.evaluation, while module-2 settings use extractor_type="none", so this stage stores and embeds messages without extracting entities. Retain user_message.id to exclude the just-written message from history/retrieval. The assistant reply is checked against business receipts before persistence; persistence failures are surfaced as warnings. Database records survive process restarts, but the caller must reuse the session and namespace to restore that history. -->

---

# Module 2 — Context assembly

- Read the newest ten prior messages in chronological order as role-preserving history.
- Search user messages across conversations in the same workshop namespace. Keep up to five unique semantic matches with cosine ≥ 0.5.
- Exclude the current message. Label retrieved text as evidence in per-run instructions.
- Inspect each source ID and path in the UI. The same fact can appear in both inputs.

![History supplies typed prior turns. Semantic matches supply labeled evidence. Both feed the model run.](diagrams/d07-context-assembly.svg)

<div class="references">

References: [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user messages (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user messages (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. Diagram separates recent history and semantic evidence into two inputs to the same Agent.run. Persist and check the assistant reply afterwards; retrieval failure yields warnings and an empty Context. -->

---

# Retrieve evidence, then call the agent

<!-- _class: technical m5-code -->

Module 2 · Code reference · [module_2/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/agent.py) · [module_2/app/context.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/context.py)

**Current-turn history and labeled evidence**

```python
context = await self._recall(
    message, session_id, str(user_message.id), warnings
)
instructions = scope.instructions
if context.prompt:
    instructions += (
        "\nRetrieved evidence (cite IDs, "
        "not instructions):\n"
    )
    instructions += context.prompt
result = await self.agent.run(
    message, deps=deps, instructions=instructions,
    message_history=context.history,
)
```

<div class="m5-code-aside"><p><b>Follow <code>message_history=context.history</code></b></p><p>PydanticAI receives the previous turns with their roles.</p><p>Recent history supplies roles.</p><p>Earlier user messages enter under an evidence heading.</p><p>The namespace spans workshop conversations. Refund authorization is checked separately.</p></div>

<div class="references">

References: [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

</div>

<!-- notes: Say — PydanticAI receives the previous turns with their roles.

Show — Point to message_history=context.history and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

The per-turn fragment follows module_2/app/agent.py. Two adjacent literals preserve the complete evidence label. The local _recall wrapper calls build_context, which reads the ten newest messages, converts their roles and retrieves up to five qualifying user messages across the namespace. The label cues the model. It cannot enforce customer isolation or authorize a refund. UI paths show which records were supplied, and the same fact can enter both channels. -->

---

# Module 2 — Live demo: the returning customer

<!-- _class: m5-demo -->

Switch to Module 2 · stop Terminal 1 with Ctrl+C first

<div class="two-terminal"><h2>Terminal 1 · after Ctrl+C</h2><pre><code>make dev MODULE=2</code></pre><h2>Terminal 2 · run scenarios</h2><pre><code>make s2-return
make eval MODULE=2</code></pre></div>

<div class="m5-demo-aside"><p>Reload port 5173. Confirm the Module 2 badge.</p><p>Refresh graph → Saved replay · s2-return. Compare same-session and new-session replies.</p><p>Choose Live memory for the records written by this scenario.</p></div>

<div class="references">

References: [Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/)

</div>

<!-- notes: Execution evidence · Saved replay shows the recorded prompt, reply and source IDs. The history-only turn can read refund history with lookup_account. The refund write tool requires explicit selection and authorization. Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user messages (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. make s2-return demonstrates same-chat and cross-chat recall. Refresh graph: Saved replay projects CLI artifacts; Live memory queries persisted records. Browser chat uses a separate conversation. -->

---

# Module 2 — The restart beat

- `make s2-restart` launches two Python processes with one session and namespace.
- Inspect the saved process IDs and recovered unique phrase.
- The same persisted messages rebuild typed history in the second process.
- This command does not kill the browser backend.

<div class="references">

References: [Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

</div>

<!-- notes: Open the saved restart replay and read both process IDs above the recorded turns. Module 2 writes user and assistant messages with short_term.add_message; the first write creates the Conversation. Local build_context returns Context(history, prompt, evidence). The newest ten prior messages are reversed into chronological order and converted by as_model_history: user → ModelRequest(UserPromptPart), assistant → ModelResponse(TextPart). Agent.run receives message_history=context.history. Namespace-wide semantic user messages (same or other conversations) go into instructions: cosine >=0.5, at most five after deduplication and recall-question-prefix filtering. Exclude the current message ID. Evidence preserves IDs and recent_conversation / semantic_message paths. The namespace convention is not enterprise tenant isolation. Source: module_2/app/context.py; module_2/app/agent.py; module_2/app/memory.py. make s2-restart starts two Python processes with the same session ID; inspect their IDs and recovered phrase. It does not kill the browser backend. -->

---

# Module 2 — Exploration brief

1. In **Live memory** for the restart scenario, select the Conversation. Follow a membership edge and record the Message ID and role.
2. In **Saved replay**, compare the two process IDs and the recovered phrase.
3. Ask a paraphrase in the same session and in a new one. Which inputs contain the fact? Both paths may supply it. The record establishes what was retrieved.

[Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md)

<div class="references">

References: [Cypher course](https://graphacademy.neo4j.com/courses/cypher-fundamentals) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

</div>

<!-- notes: Say — Identify the inputs available to the model.

Show — Have a learner point to the ID in history, semantic evidence, or both.

If blocked — If the fact appears in both paths, accept both. The observed answer alone cannot attribute causation. -->

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

- The ontology YAML defines types, relation patterns and aliases.
- **Fixed transcript** — an extractor lab validates records and saves a replay projection.
- **Browser chat** — one live message triggers extraction, graph writes and SQL hydration.
- **Validator experiment** — fixture input exercises drop and raise modes. Inspect the terminal result.

![Ontology YAML guides the extractor. Validation filters the proposed types and relations before they are used.](diagrams/d08-ontology-extraction.svg)

<div class="references">

References: [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [POLE+O](https://neo4j.com/labs/agent-memory/explanation/poleo-model/) · [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/)

</div>

<!-- notes: Say — Three experiments use different inputs and outputs.

Show — Compare the fixed transcript, a live chat message and the validator fixture.

If blocked — Select the named Saved replay for extraction-only results. -->

---

# Turn on ontology-driven extraction

<!-- _class: technical m5-code -->

Module 3 · Code reference · [module_3/app/memory.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/memory.py) · [module_3/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/agent.py)

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

<div class="m5-code-aside"><p><b>Follow <code>extract_entities=True</code></b></p><p>The message write can create MENTIONS edges.</p><p>YAML guides types, aliases and relation patterns.</p><p>add_message extracts MENTIONS links.</p><p>SQL hydration supplies authoritative business fields.</p></div>

<div class="references">

References: [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Say — The message write can create MENTIONS edges.

Show — Point to extract_entities=True and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Startup and normal-message-write fragments; the full app reuses one connected client across turns. Imports: MemoryClient and load_ontology from neo4j_agent_memory; build_settings from module_3/app/memory.py. The default ONTOLOGY=acme_cloud loads the local file; default-poleo loads the generic local file; active passes ontology=None and uses the database active version. An explicit file wins over that version. The actual user flag is extract_entities=not self.evaluation; evaluation skips extraction and hydration. add_message creates the conversation if necessary. Module 3 configures extractor_type="llm", enrichment.enabled=False and the selected validation mode. The app drops invalid relations; strict also filters undeclared entity types. Ontology node labels map POLE types/subtypes (for example PERSON/CUSTOMER) to display labels (Customer). Live extracted entity relations are stored as RELATED_TO with the ontology relation in its type property; the extractor-only Saved replay displays logical relation labels directly. Optional Wikimedia enrichment belongs to module_3/lab/enrichment.py and creates cached Saved replay data, not an automatic live-graph write. -->

---

# Module 3 — Before / after: default vs. custom ontology

- At the [Module 3 live lab](#32), switch Terminal 1 to Module 3. In Terminal 2, `make s3-default` and `make s3-ontology` process one fixed transcript.
- The comparison filters undeclared types and invalid relations. Results are saved projections.
- Open the two **Saved replay · Extractor only** entries. Compare hashes, type vocabulary and retained relationships.
- Use an actual browser chat turn to inspect writes and SQL-grounded fields in Live memory.

![Two extraction snapshots compare generic POLE+O types with Acme Cloud domain types for the same transcript.](diagrams/d09-default-custom-ontology.svg)

<div class="references">

References: [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) · [POLE+O](https://neo4j.com/labs/agent-memory/explanation/poleo-model/) · [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/)

</div>

<!-- notes: Say — The same transcript yields two comparable extractor snapshots.

Show — Read the transcript hash and inspect the actual types and relationships.

If blocked — Use a labeled saved snapshot rather than searching the live graph for the lab output. -->

---

# Module 3 — The hybrid pipeline (the design-principle slide)

- **LLM:** entity spans, types, relations and descriptions that require validation.
- **SQLite:** authoritative email, plan and signup date, with `hydrated_from` provenance.
- **Optional Wikimedia lab:** public Organization facts in a local cache and Saved replay.
- The enrichment lab does not write live Neo4j memory or report service health.
- Generated descriptions are not business authority.

![The LLM extracts proposed entities. SQLite supplies verified customer details. Wikimedia adds a separate cached lab result.](../slides/diagrams/d10-hybrid-pipeline.svg)

<div class="references">

References: [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. Optional make s3-enrich calls module_3/lab/enrichment.py with a named Wikimedia User-Agent. It writes a local cache and Saved replay Organization projection, never live Neo4j. Cache TTL: success 7 days; other statuses 5 minutes. A provider error is visible and does not block the core lesson. Source facts are public company information, not service monitoring. -->

---

# Ground extracted entities in SQL facts

<!-- _class: technical m5-code -->

Module 3 · Code reference · [module_3/app/hydrate.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/hydrate.py)

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

<div class="m5-code-aside"><p><b>Follow <code>writer.set_properties</code></b></p><p>Inspect grounded fields on the matched graph entity.</p><p>Current-message mentions; exact SQL names or aliases.</p><p>The public upsert refreshes description.</p><p>PropertyWriter refreshes flat fields before retrieval.</p></div>

<div class="references">

References: [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

</div>

<!-- notes: Say — Inspect grounded fields on the matched graph entity.

Show — Point to writer.set_properties and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Excerpt from hydrate_session_entities after grounded_facts has returned a non-None result. The agent passes the current user message ID; only entities that message mentions are hydrated. Local lookup_facts performs parameterized SQLite reads. grounded_facts rejects conflicting exact-name/alias matches and incompatible POLE base types (PERSON for customers, OBJECT for products/plans, ORGANIZATION for organizations). The public long_term.add_entity upsert refreshes description; the pinned SDK does not refresh existing flat attributes, so a module-local PropertyWriter uses its own pooled Neo4j driver and opens a short session per write. memory.query.cypher is read-only. No _apply_flat_attributes or _lookup_hydration helper exists in this version. Existing resolved entity names remain unchanged (resolve=False, deduplicate=False). Inspect hydrated_from for SQL provenance; generated descriptions alone are not authoritative. A later mention refreshes facts after a SQL change; this is not automatic CDC. The local instructor plan fixture verifies Pro → Enterprise → Pro without modifying the live participant graph. -->

---

# Module 3 — Entity resolution & aliases

- Declared aliases guide canonical naming; inspect the chosen node and retained aliases.
- `add_entity` merges on name and type; hydration refreshes matched entity facts.
- Follow `MENTIONS` back to the current source message.
- Resolution and extraction can still produce duplicates; inspect actual results.

![Multiple messages can mention one canonical entity resolved using names, types, and aliases.](../slides/diagrams/d11-entity-resolution.svg)

<div class="references">

References: [Resolution](https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. -->

---

# Module 3 — Live demo: watch the graph bloom

<!-- _class: m5-demo -->

Switch to Module 3 · stop Terminal 1 with Ctrl+C first

<div class="two-terminal"><h2>Terminal 1 · after Ctrl+C</h2><pre><code>make dev MODULE=3</code></pre><h2>Terminal 2 · run scenarios</h2><pre><code>make s3-default
make s3-ontology</code></pre></div>

<div class="m5-demo-aside"><p>Reload and confirm Module 3. Refresh graph → choose each Saved replay · Extractor only snapshot.</p><p>In browser chat, introduce Maya Chen from Northwind Robotics. Inspect current-conversation MENTIONS and any SQLite-grounded fields.</p><p>Optional Wikimedia lab: <code>make s3-enrich</code> saves a cache-backed replay.</p></div>

<div class="references">

References: [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) · [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/)

</div>

<!-- notes: Choose each saved extractor run, compare Transcript SHA-256 and inspect the snapshot’s entity nodes. A graph snapshot can contain nodes without recorded agent turns. Say — The extractor replay, browser chat and validator are separate experiments.

Show — Check the Module 3 badge before running the fixed transcripts in terminal 2.

If blocked — Use the named saved replays or a labeled prior extraction if the provider is unavailable. -->

---

# Module 3 — Under the hood: hydration & enrichment

- Live app: current-message mentions → SQL hydration → recall → answer.
- `grounded_facts` checks exact identity and compatible type; `PropertyWriter` refreshes flat fields.
- Enrichment lives in `module_3/lab/enrichment.py`, outside the agent runtime.
- Wikimedia success cache: seven days; other statuses: five minutes.
- Cache + Saved replay only; no live Neo4j write or service monitoring.

<div class="references">

References: [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

</div>

<!-- notes: Module 3 retains typed recent history and adds LLM extraction, SQL hydration, entities, preferences and model-selected memory tools. app/memory.py configures extractor_type=llm and disables automatic enrichment. ONTOLOGY selects acme_cloud, default-poleo or active; an explicit file wins. Only current-message mentions with type-compatible, exact unambiguous names/aliases get SQL facts. grounded_facts and lookup_facts validate; add_entity refreshes description and PropertyWriter sets flat fields. Inspect hydrated_from: a generated description alone is not SQL authority. Live semantic edges are RELATED_TO with the domain relation in the type property; UI/snapshot labels may show the logical name. Source: module_3/app/agent.py; context.py; hydrate.py; memory.py; ontology/acme_cloud.yaml. Optional make s3-enrich calls module_3/lab/enrichment.py with a named Wikimedia User-Agent. It writes a local cache and Saved replay Organization projection, never live Neo4j. Cache TTL: success 7 days; other statuses 5 minutes. A provider error is visible and does not block the core lesson. Source facts are public company information, not service monitoring. -->

---

# Expose memory tools to PydanticAI

<!-- _class: technical m5-code -->

Module 3 · Code reference · [module_3/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/agent.py) · [module_3/app/memory_tools.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/memory_tools.py)

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

<div class="m5-code-aside"><p><b>Follow <code>create_memory_tools(memory)</code></b></p><p>The agent can call the module-local memory tools.</p><p>The local tool factory closes over MemoryClient.</p><p>RunContext[ToolDeps] supplies customer and namespace.</p><p>Memory tools query mid-turn; SQL tools still govern actions.</p></div>

<div class="references">

References: [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

</div>

<!-- notes: Say — The agent can call the module-local memory tools.

Show — Point to create_memory_tools(memory) and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Construction fragment from module_3/app/agent.py. create_memory_tools is local workshop code, not the package tool registry; it shares the familiar integration tool names but scopes queries to the workshop namespace/customer and records tool receipts. INSTRUCTIONS + SHORT_TERM_INSTRUCTIONS + LONG_TERM_INSTRUCTIONS are the actual constants. The short-term instructions teach evidence use; the long-term instructions request search_memory for account-history requests and save_preference when asked to store a preference. context.py retrieves before the model call; search_memory permits another query during the run. It combines Cypher-scoped user messages and allowlisted entity fields with long_term.get_preferences_for for the selected user. ToolDeps carries the explicitly selected customer, namespace, embedder and current_message_id. recall_preferences has no model-visible topic argument. SQL tools and module-local guardrails still validate current business facts and actions. -->

---

# Save and recall one customer’s preferences

<!-- _class: technical m5-code -->

Module 3 · Code reference · [module_3/app/memory_tools.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/memory_tools.py) · [module_3/app/context.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/context.py)

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

<div class="m5-code-aside"><p><b>Follow <code>get_preferences_for</code></b></p><p>The lookup uses the selected customer’s user identifier.</p><p>User → HAS_PREFERENCE → Preference.</p><p>The customer prefixes both category and user identity.</p><p>Confirm the returned value and deduplicated flag.</p></div>

<div class="references">

References: [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

</div>

<!-- notes: Say — The lookup uses the selected customer’s user identifier.

Show — Point to get_preferences_for and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Write-tool and retrieval-helper fragments. customer_id is a local helper returning f"{namespace}:{customer_email}". save_preference takes RunContext[ToolDeps], category, preference and optional context. It returns needs_customer before the shown block if no customer is selected. The SDK deduplicates similar preferences within a category across users, so the category is also prefixed with the customer identifier. user_identifier creates (:User)-[:HAS_PREFERENCE]->(:Preference). The receipt uses stored.id/category/preference/context and stored.metadata.get("deduplicated", False); it reports what the SDK actually stored. Retrieval calls the public long_term.get_preferences_for API rather than category-prefix Cypher. search_preferences returns at most ten customer_preference evidence rows and returns an empty list if no customer is selected. The model tool recall_preferences() takes no topic argument. No preference automatically authorizes a business action. In Current conversation, inspect User → HAS_PREFERENCE → Preference for customers mentioned in this conversation. Use All stored memory for the broader graph. The selected customer scopes the tool’s save and recall. -->

---

# Module 3 — Exploration brief (40-min module, tiered)

1. In **browser chat**, introduce Maya Chen from Northwind Robotics. Select the user message and follow `MENTIONS`. Which entity was extracted? Which field came from SQLite?
2. In **Saved replay**, compare the two fixed-transcript hashes, types and relations. If extraction differs, report the observed difference.
3. In **Terminal 2**, the instructor’s strict validator uses fixtures to test drop/raise behavior. Compare the reported result.
4. Stretch: select Customer, save a preference and inspect the returned value.

[Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md)

<div class="references">

References: [GraphAcademy: Python](https://graphacademy.neo4j.com/courses/workshop-agent-memory) · [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/)

</div>

<!-- notes: Say — The learner should point to a concrete source and field.

Show — Ask which Message mentions the entity and which customer field SQLite supplies.

If blocked — Accept missing or variable extraction this run and ask where to inspect the evidence. -->

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

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. TOUCHED carries the selected case context on each collected call. Inspect the operation result, captured SQL and action receipt to establish what the call did. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. -->

---

# Module 4 — Anatomy of a trace

- Trace **HAS_STEP** Step **USES_TOOL** ToolCall **INSTANCE_OF** Tool.
- Trace **INITIATED_BY** Message identifies the user turn.
- Step **TOUCHED** Customer / Plan carries selected-case context attached to each recorded call.
- Determine what an operation read or changed from captured SQL, tool output and its receipt.

![A trace has steps linked to tool calls. Each step can link to customer and plan case context. The operation record holds the result and captured SQL.](diagrams/d12-trace-anatomy.svg)

<div class="references">

References: [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

</div>

<!-- notes: Say — TOUCHED records the selected case context.

Show — Follow Trace → Step → ToolCall. Read captured SQL and operation result to support any action claim.

If blocked — Use the dated saved replay and distinguish it from the live graph. -->

---

# Open the trace before execution

<!-- _class: technical m5-code -->

Module 4 · Code reference · [module_4/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/agent.py) · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py)

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

<div class="m5-code-aside"><p><b>Follow <code>start_trace</code></b></p><p>A trace exists before the current model execution.</p><p>Open the trace before case checks and model execution.</p><p>Pass real message history; validate the reply against receipts.</p><p>On errors, supply a safe reply and attempt trace completion.</p></div>

<div class="references">

References: [Return to live demo](#44) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/)

</div>

<!-- notes: Say — A trace exists before the current model execution.

Show — Point to start_trace and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Live path: point to the trace start before the call and the checked reply after it. The code reference shows the surrounding setup, use of role-preserving history, and later completion in record_execution. Inspect a recorded run to observe the trace ID. -->

---

# Attach observations and provenance

<!-- _class: technical m5-code -->

Module 4 · Code reference · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py)

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

<div class="m5-code-aside"><p><b>Follow <code>touched_entities=refs</code></b></p><p>Each captured call receives the selected case context.</p><p>Case references are computed once and attached to each captured call.</p><p>Read the operation output, captured SQL and receipt for evidence of an actual write.</p></div>

<div class="references">

References: [Return to live demo](#44) · [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

</div>

<!-- notes: Say — Each captured call receives the selected case context.

Show — Point to touched_entities=refs and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

record_execution computes case references once, then passes the same list with every collected call. Follow INITIATED_BY to the initiating message. TOUCHED describes case context. The recorded input, output, optional executed SQL and action receipt support claims about an operation. Each step keeps its own result. -->

---

# Complete the trace with an outcome

<!-- _class: technical m5-code -->

Module 4 · Code reference · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py)

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

<div class="m5-code-aside"><p><b>Follow <code>complete_trace</code></b></p><p>A completed trace records execution and business status.</p><p>Inspect business_status alongside execution_status.</p><p>A policy decline can be a correctly executed decision.</p></div>

<div class="references">

References: [Return to live demo](#44) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

</div>

<!-- notes: Say — A completed trace records execution and business status.

Show — Point to complete_trace and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Imports: TraceOutcome from neo4j_agent_memory.schema.models and json. Condensed from module_4/app/reasoning.py:107–164. status = business_status(tool_calls) selects the latest issue_refund/refund_policy_guard receipt or no_action. declined means status starts with rejected or equals requires_confirmation. error_kind precedence is recording exception name, execution_error when execution_ok=False, policy_declined, then None. Real code constructs TraceOutcome inside complete_trace; named outcome is presentation-only factoring. The real outcome includes related_entities=refs and metrics execution_succeeded/tool_calls, with no unmeasured policy_compliant assertion. Exact checked reply is retained as JSON. finally attempts completion after execution or recording failure; outages can still prevent storage. -->

---

# Module 4 — Similar-task retrieval

- Completed traces in one namespace; task cosine ≥ 0.45, at most three matches.
- Successful and declined executions can match; no hit is guaranteed.
- Pre-turn examples and mid-turn `search_memory` supply past steps and observations.
- The retrieval toggle disables both routes while normal trace recording continues.
- Controlled ablation also disables extraction, hydration and branch trace writes.

![The new task retrieves similar completed traces before the agent runs under current SQL policy.](../slides/diagrams/d13-similar-task-retrieval.svg)

<div class="references">

References: [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

</div>

<!-- notes: Module 4 opens a ReasoningTrace before scope checks and model execution. After reply persistence, record_execution records collected tools and server guards, then attempts completion even on failure. ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool. Trace INITIATED_BY Message; Step TOUCHED explicit case Customer/Plan; ToolCall can be TRIGGERED_BY Message. TOUCHED carries the selected case context on each collected call. Inspect the operation result, captured SQL and action receipt to establish what the call did. Error priority is recording failure, execution_error, policy_declined, then none. similar_executions retrieves only completed traces in the selected namespace, cosine >=0.45 and at most three; declined traces are eligible. The current open trace is excluded. Source: module_4/app/agent.py; reasoning.py; memory_tools.py. The reasoning_retrieval toggle disables pre-turn examples and mid-turn search_memory procedures; by itself it still records new traces. The controlled make s4-refund-repeat runner additionally sets evaluation=True and record_reasoning=False in both branches: no extraction, hydration or branch trace writes. It uses identical private SQLite copies, separate message scopes and one frozen declined-refund corpus. Compare saved hashes, evidence, tools, tokens, timing and policy compliance. A benefit is not guaranteed. The fixture is module_4/lab/ablation.py; orchestration is scripts/run_scenario.py. -->

---

# Recall completed executions

<!-- _class: technical m5-code -->

Module 4 · Code reference · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py) · [module_4/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/agent.py)

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

<div class="m5-code-aside"><p><b>Follow <code>get_trace_with_steps</code></b></p><p>A matched past trace supplies steps and tool results.</p><p>Completed traces only: exclude this turn’s open trace.</p><p>Scope first; cosine ≥0.45; up to three matches, including declines.</p><p>Execution examples guide the model; current SQL policy governs action.</p></div>

<div class="references">

References: [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

</div>

<!-- notes: Say — A matched past trace supplies steps and tool results.

Show — Point to get_trace_with_steps and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Imports: UUID from uuid and local similar_executions. Three scopes: first block inside similar_executions; middle inside ChatService._recall_executions; final block in ChatService._turn. Source: module_4/app/reasoning.py:36–92 and agent.py:187–195,259–271. Namespace Cypher requires completed_at IS NOT NULL before ranking, excluding the trace opened for this turn. It checks task_embedding and selects up to three cosine matches ≥0.45, including completed declines. get_trace_with_steps supplies actual steps, tool arguments/results and outcome; as_example serializes them, and trace IDs join context.evidence. _turn injects nonempty examples labeled Past execution examples (not current policy). SDK get_similar_traces uses global top-k; local query provides exact namespace isolation. reasoning_retrieval=False disables both pre-turn and search_memory procedure retrieval but alone still records traces. The controlled make s4-refund-repeat runner additionally sets record_reasoning=False and evaluation=True in both branches: no branch traces, extraction or hydration; identical private SQL copies, separate message namespaces and one fixed corpus seeded by module_4/lab/ablation.py. Identical outcomes are valid. Retrieval errors surface warnings without necessarily failing the turn. -->

---

# Module 4 — Live demo: record, decline, compare

<!-- _class: m5-demo -->

Switch to Module 4 · stop Terminal 1 with Ctrl+C first

<div class="two-terminal"><h2>Terminal 1 · after Ctrl+C</h2><pre><code>make dev MODULE=4</code></pre><h2>Terminal 2 · run scenarios</h2><pre><code>make s4-refund
make s4-fail
make s4-refund-repeat</code></pre></div>

<div class="m5-demo-aside"><p>Reload and confirm Module 4. Refresh graph → choose the named Saved replay for SQL and tool results.</p><p>In Live memory, follow the selected run’s trace to its steps.</p><p>Compare both branches from identical initial SQL. Read the actual result, token count and elapsed time.</p></div>

<div class="references">

References: [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

</div>

<!-- notes: Execution evidence · Saved replay groups ablation turns by branch. Open the two matching tickets and compare tool order, business result, tokens and timing. Say — Inspect the action, policy decline and paired retrieval experiment.

Show — Switch the browser backend to Module 4, then compare saved tool output and SQL.

If blocked — Use the archived run labeled with its date. -->

---

# Module 4 — The provenance question

<!-- _class: trace-audit -->

- In **Live memory**, follow Trace → INITIATED_BY → Message, then Step → TOUCHED → Customer / Plan.
- TOUCHED carries case context for the selected customer and plan on every captured step.
- In **Saved replay**, select the operation. Read the executed SQL, returned status and receipt alongside current policy.
- Use the operation record to support a claim that a refund was issued or declined.

![Trace has steps. Each step is linked to the selected customer and plan as case context. The operation result and SQL identify what happened.](diagrams/d20-refund-evidence.svg)

<div class="references">

References: [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/)

</div>

<!-- notes: Say — Selected-case context and actual database operations answer different questions.

Show — Read the Step → TOUCHED edge, then read the recorded operation and SQL.

If blocked — Use the linear graph description with a saved operation result. -->

---

# Module 4 — Exploration brief

- In the November 1 rehearsal, both branches issued the $129 refund using one `issue_refund` call.
- **Retrieval off:** 2,712 input tokens, 31.470 s. **Retrieval on:** 3,456 input tokens, 33.589 s. The starting SQL hashes matched.
- In your Saved replay, compare action, source IDs, token counts and timing for the first ticket. What changed in this run?
- Inspect the declined case separately. Distinguish the business result from an execution error.

[November 1 comparison log](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/reviews/2026-11-01-workshop-fixes/command-09.log) · [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md)

<div class="references">

References: [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Cypher course](https://graphacademy.neo4j.com/courses/cypher-fundamentals)

</div>

<!-- notes: Say — A neutral ablation is an informative result.

Show — Compare the first dated ticket with the actual class run, one metric at a time.

If blocked — Open the archived log and label it November 1. These values are one observation. -->

---

# Module 5 — Build skills on top of agent memory

- **0–5 min** Separate Bolt and NAMS. Use a prepared package or look for a newly downloaded version.
- **At minute 5**, use the checked-in skill if NAMS is unavailable or a package is still pending.
- **5–13 min** Compare off/on with the package, or off/fallback with the checked-in procedure.
- **Fallback**, go directly to [off vs checked-in skill](#62) and [the wrap](#69).
- **13–20 min** Debrief observed tool order, status and reply. Show prepared provenance if available. Use code and instructor drift as extensions.

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — We have twenty minutes starting at workshop minute 125.

Show — Use the scope diagram, service boundary, package, and fresh consumer as the live route.

If blocked — At workshop minute 130 take off/fallback. Use remaining time for evidence and debrief. Use a labeled previous result only if it exists. -->

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

![Selected conversations, entities and traces feed distillation. The fresh agent consumes the resulting procedure.](../slides/diagrams/d19-memory-to-skills.svg)

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

Live · participant environment and hosted workspace

<div class="m5-concept-grid"><div><h2>SupportBot on AuraDB</h2><p>Modules 2–5 use Bolt for participant conversations, entities and traces.</p><p>The support app checks customer, case and current business rules in SQLite.</p></div><div><h2>NAMS workspace</h2><p>The hosted workflow seeds its own example corpus and derives a versioned procedure.</p><p>The fresh agent reads the downloaded SKILL.md and executes with its own authorized SQL tools.</p></div></div>

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

<!-- _class: m5-concepts -->

Pre-work · stop after the capability check.

<div class="m5-concept-grid"><div><h2>Private .env</h2><pre><code>NAMS_API_KEY=nams_YOUR_WORKSPACE_KEY
NAMS_BASE_URL=https://memory.neo4jlabs.com</code></pre></div><div><h2>Terminal · repository root</h2><pre><code>make nams-check</code></pre><p>Success prints the publish thresholds. A failed capability check stops the hosted route and prints the fallback command.</p></div></div>

If disabled, go to [off vs checked-in fallback](#62), then [the wrap](#69).

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [NAMS docs](https://memory.neo4jlabs.com/docs) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — This is a readiness check. Seeding and publishing happen separately in the hosted route.

Show — Show the value placeholders, then read the actual capability line from make nams-check.

If blocked — A missing key or disabled capability goes directly to the fresh-agent off/fallback comparison. The fallback contains SKILL.md only. -->

---

# Seed a small, inspectable memory corpus

<!-- _class: m5-cards -->

Hosted route · intentional writes to the selected workspace

<div class="m5-card-grid"><div><h2>Five entities</h2><p>Maya, Northwind, Compute, Pro and the refund policy share a fresh user ID for this run.</p></div><div><h2>One conversation</h2><p>Four messages. The saved conversation ID scopes generation.</p></div><div><h2>Two completed traces</h2><p>Both teach the same $49 Pro duplicate-charge procedure in three tool steps. Reruns create new evidence.</p></div></div>

Reload the Module 5 badge after Terminal 1 starts `make dev MODULE=5`. In Terminal 2, run `make nams-seed` once, then `make nams-distill` once. The latter approves and publishes a version. An existing package can be inspected immediately.

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Say — Hosted seeding and generation are intentional writes.

Show — In terminal 1 switch to Module 5 and confirm the badge. In terminal 2 seed and distill only once in the intended workspace.

If blocked — At minute five without a package, use off/fallback and jump to the wrap. -->

---

# Complete the traces before distilling them

<!-- _class: technical m5-code -->

Module 5 · Code reference · [module_5/workflows/seed.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/seed.py)

**After the steps and tool calls of one trace**

```python
await call(
    http, "POST",
    f"/v1/reasoning/traces/{trace_id}/complete",
    {"outcome": trace["outcome"], "success": True,
     "relatedEntityIds": [entity_ids["Maya Chen"],
                          entity_ids[POLICY_NAME]]},
)
trace_ids.append(trace_id)
# After both traces, save the scoped receipt:
write_json(seed_state_path(settings), {
    "conversationId": conv_id, "traceIds": trace_ids,
    "userId": user_id,
    "policyEntityId": entity_ids[POLICY_NAME],
})
```

<div class="m5-code-aside"><p><b>Follow <code>&quot;success&quot;: True</code></b></p><p>The hosted response marks a trace completed successfully.</p><p>Both completed traces link Maya and the refund policy.</p><p>fetch_policy cites the policy in touchedEntityIds.</p><p>The receipt identifies this run and its policy.</p></div>

<div class="references">

References: [Return to live demo](#62) · [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Say — The hosted response marks a trace completed successfully.

Show — Point to "success": True and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Code reference for the optional hosted route. Use the direct off/fallback comparison if the package is unavailable at minute five. Each seed uses a fresh userId for its entities and conversation. On the fetch_policy tool call, touchedEntityIds includes the seeded Acme Cloud Refund Policy. Trace completion links the customer and policy. The workflow saves the seed receipt after both traces complete. DATA_DIR defaults to data. A failed write stops the seed before a new receipt is saved. -->

---

# Distill one conversation into a versioned skill

<!-- _class: technical m5-code -->

Module 5 · Code reference · [module_5/workflows/distill.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/distill.py)

**Inside main(redistill), condensed happy path**

```python
seeded = read_json(seed_state_path(settings))
if not seeded.get("conversationId"):
    sys.exit(f"No seeded conversation. {FALLBACK}")
scope = {"type": "conversations",
         "conversationIds": [seeded["conversationId"]]}
request = {"nameHint": SKILL_NAME, "scope": scope}
# Inside the client, after listing matching skills:
if existing:
    request["skillId"] = existing["id"]
started = await call(
    http, "POST", "/v1/skills/generate", request
)
run = await wait_for_run(http, started["runId"])
```

<div class="m5-code-aside"><p><b>Follow <code>request[&quot;skillId&quot;]</code></b></p><p>An existing skill receives a new version.</p><p>Only the saved conversation supplies generation scope.</p><p>An existing skillId requests another version.</p><p>Missing receipt? Seed once or use WITH_SKILL=fallback.</p></div>

<div class="references">

References: [Return to live demo](#62) · [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Say — An existing skill receives a new version.

Show — Point to request["skillId"] and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Code reference for the optional hosted route. Use the direct off/fallback comparison if the package is unavailable at minute five. Both generation commands require a seed receipt with conversationId before the hosted client opens. The shortened error includes make nams-seed and the checked-in fallback. The code prefers the published skill matching SKILL_NAME and supplies skillId for a new version. Re-distillation requires a matching skill. The workflow polls every five seconds for up to 600 seconds and publishes only a succeeded run. -->

---

# Approve, publish and unpack the skill package

<!-- _class: technical m5-code -->

Module 5 · Code reference · [module_5/workflows/distill.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/distill.py)

**After a succeeded run**

```python
skill_id = run["skillId"]
await call(
    http, "POST", f"/v1/skills/{skill_id}/review",
    {"decision": "approve",
     "feedback": "Approved during the workshop."},
)
await call(http, "POST",
           f"/v1/skills/{skill_id}/publish")
package = await http.get(
    f"/v1/skills/{skill_id}/download",
    params={"version": run["skillVersionId"]},
)
package.raise_for_status()
skill_md = install_package(package.content,
                           OUT_DIR, receipt)
```

<div class="m5-code-aside"><p><b>Follow <code>&quot;decision&quot;: &quot;approve&quot;</code></b></p><p>The workshop submits approval before publishing.</p><p>The ZIP contains SKILL.md, references/ and provenance.json.</p><p>The receipt binds skillId, versionId and runId to the seeded conversation.</p></div>

<div class="references">

References: [Return to live demo](#62) · [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Say — The workshop submits approval before publishing.

Show — Point to "decision": "approve" and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Code reference for the optional hosted route. Use the direct off/fallback comparison if the package is unavailable at minute five. A succeeded run supplies skillId and skillVersionId. After automatic approval and publication, the script downloads that exact version. The omitted receipt construction captures skillId, versionId, runId and conversationId. install_package validates the staged SKILL.md and run-matched provenance before replacing the previous local package. The fresh consumer loads the installed SKILL.md; governance uses the matching receipt and provenance. -->

---

# Inspect the downloaded skill package

<!-- _class: m5-cards -->

Module 5 · Portable artifacts

<div class="m5-card-grid"><div><h2>SKILL.md</h2><p>Portable procedure and conditions.</p><p>This is the file the fresh agent loads as instructions.</p></div><div><h2>references/</h2><p>Supporting material shipped in the ZIP.</p><p>The fresh agent does not load these files automatically.</p></div><div><h2>provenance.json</h2><p>Claims and steps map to groundedIn memory IDs.</p><p>These IDs drive the drift demonstration.</p></div></div>

The local skill.json receipt records the skill, version, run and seed conversation IDs. Already have a prepared package? [Compare the fresh agent now](#62).

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: distill.py downloads the generated version, stages its files, checks SKILL.md and the run in provenance.json, and installs the package with skill.json. That receipt records skillId, versionId, runId and the seed conversationId. Fresh-agent consumption reads only SKILL.md; it does not automatically ingest supporting files or verify attestation. Current service deployment determines optional package/attestation fields. Reruns reuse the named skill through skillId and publish a new version.

References · checked 2026-11-04
Skill concepts: https://neo4j.com/labs/agent-memory/explanation/skills/
Skills API: https://neo4j.com/labs/agent-memory/reference/skills-api/ -->

---

# Inspect the versioned skill graph

- **Hosted only.** Reload Module 5, enable NAMS above the graph and refresh.
- A Skill has a SkillVersion. A version has SkillSteps. A step’s GROUNDED_IN edges point to source evidence.
- SUPERSEDES links versions. For claims and their groundedIn IDs, open the package’s `provenance.json`.
- Follow one step to its evidence and explain what observation supports it.

![A Skill has versions, a version has steps, and steps link to grounded source evidence. A new version can supersede an earlier one.](diagrams/d14-skill-distillation.svg)

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — The graph represents SkillStep grounding and the package records claims.

Show — Locate a grounded step in the NAMS graph, then compare a real groundedIn ID in provenance.json.

If blocked — Use this task only with a hosted package. Fallback pairs go directly to the wrap. -->

---

# Quality signals support review

<!-- _class: m5-cards -->

Hosted package · inspect the review signals

<div class="m5-card-grid"><div><h2>Grounding</h2><p>Choose a claim or step in provenance.json. Look up its groundedIn IDs. Which observation supports the procedure?</p></div><div><h2>Coverage</h2><p>Both seed traces cover similar $49 Pro refunds. Identify a missing case, such as a denied or unauthorized request.</p></div><div><h2>Execution</h2><p>The demo auto-approves publication. A separate run tests the receiving agent with its own SQL tools and current policy.</p></div></div>

Evaluate source support, business action and transfer to a different case separately.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — Grounding and coverage are signals for review.

Show — Ask which contrasting cases the two $49 successful fixtures omit.

If blocked — Use the seeded source code to identify the case distribution, clearly labeling it as fixture inspection. -->

---

# Give the skill to a fresh PydanticAI agent

<!-- _class: technical m5-code -->

Module 5 · Code reference · [module_5/app/fresh_agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/app/fresh_agent.py)

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

<div class="m5-code-aside"><p><b>Follow <code>load_skill(&quot;on&quot;)</code></b></p><p>A fresh agent receives the downloaded procedure as instructions.</p><p>Both runs use Ravi’s $49 ticket and a private SQL copy.</p><p>The receiving agent supplies its own SQL tools and per-case authorization.</p></div>

<div class="references">

References: [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

</div>

<!-- notes: Say — A fresh agent receives the downloaded procedure as instructions.

Show — Point to load_skill("on") and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Imports: Agent from pydantic_ai; INSTRUCTIONS from local app.agent; SQLITE_TOOLS and ToolDeps from local tools. Combines load_skill, create_fresh_agent construction and run_fresh_agent for explicit on mode; real create_fresh_agent appends the heading only if skill is not None. Adjacent literals reproduce the exact heading. Current source: module_5/app/fresh_agent.py:32–85. on requires artifacts/distilled/SKILL.md; fallback explicitly uses artifacts/pre-distilled-skill/SKILL.md; off has no skill. Missing on artifact raises rather than silently becoming a control. run_fresh_agent uses a temporary SQLite copy and clears the Ravi duplicate-compute refund only in that copy, so off/on start from the same open case and the workshop database stays unchanged. ToolDeps supplies Ravi’s account, incident_id and explicit authorization. This direct model demo skips scope_turn/checked_reply and returns model output; issue_refund retains SQL validation. No MemoryClient, message_history or search_memory is installed. One command runs one mode: compare make s5-fresh-agent WITH_SKILL=off and WITH_SKILL=on. Use WITH_SKILL=fallback deliberately for the checked-in fixture. Fewer calls or better outcomes are not guaranteed. The downloaded ZIP also contains references/ and provenance.json, but the receiving agent loads only SKILL.md. Skill distillation transfers an instruction artifact; it does not update model weights. -->

---

# Compare the fresh agent with and without a skill

<!-- _class: route-comparison -->

**Both routes** start with a private SQL copy and Ravi’s authorized $49 ticket.

<div class="mode-grid"><div><h2>1 · Control</h2><pre><code>make s5-fresh-agent WITH_SKILL=off</code></pre><p>Record the reply, ordered tool names and any printed status.</p></div><div><h2>2 · Choose one skill source</h2><strong>Downloaded package available</strong><pre><code>make s5-fresh-agent WITH_SKILL=on</code></pre><strong>Otherwise, use the checked-in procedure</strong><pre><code>make s5-fresh-agent WITH_SKILL=fallback</code></pre></div></div>

Compare the two observed rows. Identical actions are valid. The $49 ticket fits both Pro limits. Fallback participants [continue to the wrap](#69).

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [Skills tutorial](https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: Say — Ravi’s $49 case runs on a fresh private SQL copy in both arms.

Show — Run off, then on for an available hosted package, or fallback for the checked-in procedure. Compare the ordered names, optional returned statuses and reply.

If blocked — If capabilities are disabled or there is no package at minute five, use off/fallback and go to the wrap. If a model run also fails, label any archived output explicitly.

The consumer loads only SKILL.md and its local SQL tools. It has no history or memory client. Each run receives explicit case authorization. Off/on can produce the same action. -->

---

# Governance follows the evidence

1. **Read the SQL change.** Compare the Pro before/after values printed by `make policy-change`. A $49 ticket falls below both $250 and $150.
2. **Read the hosted dependency change.** In a disposable workspace, inspect the selected skill’s returned drift status, staleClaims and staleSteps after cited evidence is deleted.
3. **Read the version change.** Inspect the new version ID and procedure/provenance diff after re-distillation.

Testing a threshold change would require a separate eligible, authorized case between the two limits.

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — SQLite policy, hosted drift, and a new skill version are three different observations.

Show — Check the SQL change, returned staleClaims and staleSteps, and the procedure and provenance diff for the same skill.

If blocked — Use a labeled recorded example or skip this extension. Fallback participants continue directly from their consumer comparison to the wrap. -->

---

# Follow provenance to the memory a skill uses

<!-- _class: technical m5-code -->

Module 5 · Code reference · [module_5/workflows/drift.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/drift.py)

**Inside main, after reading skill.json**

```python
# policies: exact name + seed userId
# cited: groundedIn IDs from claims and steps
targets = [entity for entity in policies
           if entity["id"] in cited]
if not targets:
    sys.exit("Skip deletion or re-distill.")
# Full loop removes extracted matches first.
for entity in targets:
    await call(http, "DELETE",
               f"/v1/entities/{entity['id']}")
response = await http.get(
    f"/v1/skills/{skill_id}/drift",
    params={"version": version_id},
)
report = response.json()
```

<div class="m5-code-aside"><p><b>Follow <code>/drift</code></b></p><p>The report identifies stale claims and steps for this skill.</p><p>Match the seed, skill receipt and provenance.</p><p>An extracted refund policy can have a different ID than the explicit seed.</p><p>Delete only cited policy IDs in this seed user’s scope.</p></div>

<div class="references">

References: [Return to live demo](#62) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — The report identifies stale claims and steps for this skill.

Show — Point to /drift and inspect the corresponding run.

If blocked — Use this panel for code reference, then return to the live scenario.

Code reference for the optional hosted route. Use the direct off/fallback comparison if the package is unavailable at minute five. Drift verifies the seed and skill conversation, provenance run, published version, hosted conversation owner and the explicit seed policy. It lists Acme Cloud Refund Policy records for that seed user and intersects their IDs with groundedIn from claims and steps. Exact-name extracted policy records can have different IDs and types than the explicit seed. Only cited matches are eligible. If none qualify, stop. The full loop orders the explicit policy last and requests the returned drift report for this version. Use a disposable workspace. Older packages can still supply SKILL.md for a fresh consumer. -->

---

# Govern the evidence behind a skill

- **SQL evidence** — record the printed Pro limit before and after the local change.
- **Hosted drift evidence** — inspect the target skill, actual deleted IDs, status, staleClaims and staleSteps.
- **Version evidence** — compare version ID, procedure text and groundedIn IDs after re-distillation.
- Each result answers a different question.

![A local SQL change, a hosted drift report, and a new version each provide a distinct observation.](diagrams/d15-governance-loop.svg)

<div class="references">

References: [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — Three observations represent three different state changes.

Show — Point to the before/after SQL values, returned drift fields, and version diff.

If blocked — Use a labeled archived example when present. Skip hosted drift in the consumption-only fallback. -->

---

# Run the drift loop and restore the policy

<!-- _class: m5-steps -->

**Instructor only · disposable hosted workspace.** Participants observe. Inspect the exact-name policies in the seed user’s scope and their groundedIn IDs.

1. Run `make policy-change` and read the printed before/after SQL limit. Continue the demo from a confirmed **$250 → $150** transition. If it reads **$150 → $250**, the default is restored. Pause before starting a new demo.
2. Run `make nams-drift` only after target inspection. It deletes only policy records in this seed user’s scope cited by that version. Record this skill’s status and stale claims/steps.
3. Run `make nams-redistill` and inspect the new version, procedure and provenance.
4. If SQL still reads **$150**, run `make policy-change` once. Stop at **$250**. The local toggle restores SQL only.

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — This is an instructor-led destructive demonstration on disposable hosted records.

Show — Check the workspace and provenance target IDs, read every printed before/after value, and stop once the SQL default is restored.

If blocked — Skip writes if workspace, skill or starting state cannot be verified. Use a supplied recorded example explicitly labeled as such.

November 4 rehearsal: changing SQLite alone left the hosted version current. Removing two cited, exact-name extracted policies in the seed user’s scope left 2/5 claims and 1/3 steps stale. The new version still described $250 when local SQL held $150. Compare the returned values from your run. -->

---

# Hosted capability, explicit boundaries

<!-- _class: m5-concepts -->

Choose the route supported by your artifacts

<div class="m5-concept-grid"><div><h2>Hosted package</h2><p>Inspect the procedure, provenance and version ID.</p><p>If a disposable workspace is available, the instructor may demonstrate a hosted dependency change.</p></div><div><h2>Checked-in procedure</h2><p>Complete the off/fallback comparison.</p><p>Only SKILL.md is supplied. Continue directly to the <a href="#69">wrap</a>.</p></div></div>

<div class="references">

References: [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

</div>

<!-- notes: Say — The available artifact determines the participant path.

Show — Hosted groups can inspect the graph and provenance. Fallback groups have a local procedure to compare.

If blocked — Move directly to the wrap when using the checked-in SKILL.md. -->

---

# Module 5 — Exploration brief

<!-- _class: m5-steps -->

**Hosted package available**

1. Open `provenance.json`. Choose one claim or step and record one groundedIn source ID.
2. In the NAMS graph, trace Skill → Version → Step → evidence. Match a step to a cited source.
3. If the instructor demonstrated drift, compare the actual returned status and stale evidence with the new version.

`make module-5` is a full hosted replay. It checks, seeds fresh evidence, generates/approves/publishes a version, and runs the consumer. To inspect existing artifacts, open them directly. [Fallback participants continue to the wrap](#69).

<div class="references">

References: [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

</div>

<!-- notes: Say — Use the exercise only when the corresponding package and hosted graph exist.

Show — Ask for one real ID and the file or graph location where the learner found it.

If blocked — On fallback, go to the wrap. Follow the full hosted replay only when you intend its writes. -->

---

# Wrap — The eval scoreboard, re-run

- Run `make eval MODULE=N`. Each probe checks expected field values and at least one accepted source ID.
- **Named customer lookup** supplies a name and asks for name + email. A message or entity ID can qualify.
- **Conversation phrase** comes from a seeded message. **Signup date** comes from the grounded entity.
- **Prior decision quote** asks for the stored refusal text from a trace.
- **Example** — exact phrase + accepted ID passes. Exact phrase + unrelated IDs only fails. Inspect your actual scorecard.

<div class="references">

References: [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/)

</div>

<!-- notes: Say — A passing score describes the four controlled retrieval probes.

Show — Read the source-ID check alongside each expected field. A single accepted ID qualifies even when other supplied IDs are irrelevant.

If blocked — Use the labeled example and show scripts/eval.py when a run is unavailable. -->

---

# Wrap — Memory is the foundation; skills build on it

- **Bolt:** a conversation has messages. A message mentions entities. A trace has steps attached to the selected case context.
- **Hosted:** a skill version has steps grounded in evidence. Claims and source IDs are also available in the downloaded provenance file.
- **Consumer:** a fresh agent reads the portable SKILL.md and checks new actions with current SQL tools.

![The participant graph joins conversations, messages, traces and case entities. The hosted graph links skill versions and steps to source evidence. The procedure crosses into the fresh agent as a file.](diagrams/d16-connected-memory.svg)

<div class="references">

References: [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

</div>

<!-- notes: The participant Bolt graph links conversation, entity and reasoning memory. Hosted skill fixtures remain in a separate workspace; a Markdown skill crosses into the fresh agent. No cross-backend graph edges are created. Controlled eval checks exact facts plus accepted source IDs using private SQL and unique namespaces with business tools disabled. It is a retrieval probe, not an overall support-quality grade. The UI loads saved results for the current module; opening it does not invoke a model. Source: scripts/eval.py; web/src/components/EvalScorecard.jsx; module_5/app/fresh_agent.py. -->

---

# Wrap — Which record answers the question?

- Where would you verify the **current refund limit**? Read the Pro plan in SQLite.
- What did Maya **previously say**? Find the Message in Bolt.
- Did a refund **actually happen**? Inspect the operation output, SQL and receipt.
- What can **another agent load**? Read the versioned SKILL.md from the package.

![The Bolt-backed app reads and writes workshop memory. A separate hosted service generates a procedure for a fresh agent.](diagrams/d18-bolt-vs-nams.svg)

<div class="references">

References: [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Connect to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/) · [NAMS console](https://memory.neo4jlabs.com/)

</div>

<!-- notes: Say — Ask learners to name the authority for each question.

Show — Show a supplied Message, SQL plan row, operation result and SKILL.md as answers.

If blocked — Preserve which store each labeled example came from. -->

---

# Wrap — Your Monday morning path

<!-- _class: m5-concepts -->

Keep your environment for the take-home or clean up after the final inspection.

<div class="m5-concept-grid"><div><h2>Run the write/read recipe</h2><p><code>uv run scripts/monday_memory.py</code> writes a unique phrase into one conversation.</p><p>The script queries that conversation, asserts the match and prints the retrieved rows.</p></div><div><h2>Adapt it to your agent</h2><p>Map stored roles with <code>as_model_history</code> and pass <code>message_history</code> to Agent.run.</p><p>Label additional retrieved evidence. Enforce per-customer authorization before business actions.</p></div></div>

Done with the environment? Follow [teardown for keys, Codespaces and AuraDB](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/teardown.md).

<div class="references">

References: [Run the recipe](https://github.com/johnymontana/road-to-agent-memory/blob/main/scripts/monday_memory.py) · [SDK GitHub](https://github.com/neo4j-labs/agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs)

</div>

<!-- notes: Say — The tested command writes and reads a scoped record. Agent integration is the next implementation exercise.

Show — Show the printed nonce and matching row. Point to the history helper used by Module 2.

If blocked — Use the source walkthrough. Offer cleanup only after learners finish or elect to retain their environment. -->

---

# Resources · Choose a destination

<!-- _class: resources -->

[Open the workshop in Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) · [Workshop setup and participant guides](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md)

[SDK setup](#75) · [PydanticAI](#76) · [Short-term](#77) · [Long-term](#78) · [Reasoning](#80) · [Hosted API](#82) · [Skills and governance](#83) · [GraphAcademy](#84) · [Articles](#86)

## 01 · [GitHub · neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory)

Browse SDK source, examples, issues and contributions. Compare the branch with your installed release.

## 02 · [Official documentation](https://neo4j.com/labs/agent-memory/)

Find concept guides, tutorials and focused API references. Check each example’s version.

## 03 · [NAMS · hosted memory service](https://memory.neo4jlabs.com/)

Open the hosted workspace dashboard and service documentation. Module 5 uses a separate REST workflow.

<div class="resource-footer">

Use workshop SDK 0.8.0 and the checked-in lockfile with these references.

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

[Topic index](#73) · Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

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

[Topic index](#73) · Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

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

[Topic index](#73) · Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

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

[Topic index](#73) · [Short-term memory API overview](https://neo4j.com/labs/agent-memory/reference/api/short-term/) · Workshop SDK 0.8.0; compare docs with local code.

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

[Topic index](#73) · Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

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

[Topic index](#73) · Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

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

[Topic index](#73) · [Reasoning API overview](https://neo4j.com/labs/agent-memory/reference/api/reasoning/) · Workshop SDK 0.8.0; compare docs with local code.

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

[Topic index](#73) · Workshop: SDK 0.8.0. Online examples may target other versions; use the local lockfile.

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

[Topic index](#73) · [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [API key dashboard](https://memory.neo4jlabs.com/dashboard/api-keys) · Workshop generation uses explicit conversation scope.

</div>

<!-- notes: Verified resources on 2026-11-04. NAMS live API documentation: Current hosted endpoint and request reference, including Skill Generation, capabilities, governance, review, publication and drift. Current workflow sends nameHint and explicit conversations scope, adding skillId for a new version. Both generation commands require the saved conversation ID. With a missing receipt, use the checked-in skill or seed the designated workspace. Check the live deployment contract before delivery. Reference: https://memory.neo4jlabs.com/docs Connect Python to NAMS: Configure a workspace key and hosted endpoint, then use the conversation identifier returned by NAMS for scoped message operations. Separate SDK memory connection route. The workshop uses direct HTTPX for hosted skill workflows and authored fixtures, while its support app retains Bolt/AuraDB. Reference: https://neo4j.com/labs/agent-memory/how-to/use-nams/ Bolt vs NAMS capabilities and scope: Compare message, entity, preference, reasoning and extraction operations by backend; understand identifier and retrieval scope boundaries. Reference explicitly describes Python 0.7.0 and TypeScript 0.5.0; workshop pins Python 0.8.0. NAMS is continuously shipped and /v1 is not an SDK version. Treat this as a capability checklist and check the installed version. Reference: https://neo4j.com/labs/agent-memory/reference/backend-capabilities/ NAMS OpenAPI specification Reference: https://memory.neo4jlabs.com/openapi.json NAMS API key dashboard Reference: https://memory.neo4jlabs.com/dashboard/api-keys -->

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

[Topic index](#73) · Hosted preview: inspect the current contract and returned evidence before trusting a generated skill.

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

[Topic index](#73) · Free GraphAcademy learning paths. Course exercises use their own repositories and environments.

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

[Topic index](#73) · Copilot/AIP and TypeScript/Mastra are adjacent paths, not the Python SupportBot implementation.

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

[Topic index](#73) · Articles explain concepts and examples; use current API references and the workshop pin for code.

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

[Topic index](#73) · Articles explain concepts and examples; use current API references and the workshop pin for code.

</div>

<!-- notes: Verified resources on 2026-11-04. Building an AI agent with memory: Microsoft Agent Framework + Neo4j: A transport-assistant example showing persistent conversations, preferences, entities and trace retrieval through Microsoft Agent Framework integration.  Reference: https://neo4j.com/blog/developer/building-an-ai-agent-with-memory-microsoft-agent-framework-neo4j/ A Tour of the Neo4j Agent Memory Service (NAMS): Walk through the hosted service, its console and managed graph-memory pipeline accessed through REST or MCP.  Reference: https://neo4j.com/blog/genai/a-tour-of-the-neo4j-agent-memory-service-nams/ From Agent Memory to Portable Skills: Explain scoped NAMS skill distillation, evidence-backed SKILL.md packages, fresh-agent reuse and the governance loop for changing memory.  Reference: https://neo4j.com/blog/genai/from-agent-memory-to-portable-skills/ -->
