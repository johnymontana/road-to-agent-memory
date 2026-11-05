# Workshop resource links

Verified 2026-11-04. The 102-slide native deck includes a 15-slide appendix with 49 resources. All 87 instructional native slides and all 72 instructional source sections have contextual references. Full mappings: [resources.json](resources.json).

## Open the workshop

[Open workshop in Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) · [Workshop checkout and local setup](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md)

[Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) · [Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md) · [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) · [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md)

**Capstone route** · At minute five without a package, compare off/fallback using the checked-in SKILL.md and continue to the wrap. Native slides 66 → 75 → 82. Repo slides 53 → 62 → 69.

## Topic index

[SDK setup](deck.html#75) · [PydanticAI](deck.html#76) · [Short-term](deck.html#77) · [Long-term](deck.html#78) · [Reasoning](deck.html#80) · [Hosted API](deck.html#82) · [Skills and governance](deck.html#83) · [GraphAcademy](deck.html#84) · [Articles](deck.html#86)

## Using the references

Use the workshop’s pinned SDK 0.8.0 and module-local code for executable examples. Online guides, other frameworks and hosted contracts can differ. Skill distillation is a capability built on memory; it creates a procedure artifact, not a fourth memory type.

## Current module 5 hosted flow

The readiness check precedes any hosted writes. One seed and one generation produce a versioned ZIP; generation approves and publishes automatically. At minute five without a package, compare off with the checked-in skill and continue to the wrap. Hosted provenance and graph exercises require a hosted package and workspace.

Read the [live service API](https://memory.neo4jlabs.com/docs) and [OpenAPI specification](https://memory.neo4jlabs.com/openapi.json). The script posts decision=approve before publish automatically; no interactive human approval pause is implemented. Fresh-agent consumption reads SKILL.md only. Review evidence and current-policy behavior separately.

## Resources · Choose a destination

Project and service entry points

### [Neo4j Agent Memory — GitHub](https://github.com/neo4j-labs/agent-memory)

Browse SDK source, examples, issues and contributions. Compare the branch with your installed release.

Scope / version note: Default branch can advance beyond workshop 0.8.0.

Verification: GitHub repository opened; README explicitly documents Python 0.8.0. Web-verified 2026-11-04.

### [Neo4j Agent Memory documentation](https://neo4j.com/labs/agent-memory/)

Find concept guides, tutorials and focused API references. Check each example’s version.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Official documentation home opened. Web-verified 2026-11-04.

### [NAMS hosted service](https://memory.neo4jlabs.com/)

Open the hosted workspace dashboard and service documentation. Module 5 uses a separate REST workflow.

Scope / version note: Verified public entry only. Service behavior, availability, workspace scopes and preview features must be checked in the selected workspace. Module 5's SupportBot still uses Bolt; its separate skill workflow uses hosted REST.

Verification: Opened the public NAMS homepage on 2026-11-04 and followed its Docs link. No authenticated workflow or service write was attempted.

## Resources · Memory concepts

The model behind modules 1–4

### [Understanding the three memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/)

Compare persisted conversation history, durable entity knowledge and recorded task execution.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened through official explanation index. Web-verified 2026-11-04.

### [Why Neo4j? Graph memory architecture](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/)

See how relationships connect messages, entities and execution provenance in one graph.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened through official explanation index. Web-verified 2026-11-04.

### [The POLE+O data model](https://neo4j.com/labs/agent-memory/explanation/poleo-model/)

Understand base types and domain subtypes before defining the Acme Cloud ontology.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened through official explanation index. Web-verified 2026-11-04.

## Resources · SDK setup and configuration

Pin first; compare versions before copying examples

### [Python SDK 0.8.0 — pinned release](https://pypi.org/project/neo4j-agent-memory/0.8.0/)

Find the exact workshop release files. Use the repository’s uv.lock and Make recipes.

Scope / version note: Package description still contains 0.7.0 examples; release files are explicitly 0.8.0.

Verification: PyPI release files verified as 0.8.0, uploaded 2026-10-22. Web-verified 2026-11-04.

### [MemoryClient API reference](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

Check constructor settings, client lifetime, memory accessors and the read-only query surface.

Scope / version note: Live examples use BoltSettings; workshop 0.8.0 uses explicit MemorySettings(backend='bolt'). Preserve workshop configuration.

Verification: Opened and checked constructor, properties and ontology precedence. Web-verified 2026-11-04.

### [Embedding, LLM, schema, extraction and resolution settings](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

Review LLM, embedding, ontology and resolution configuration; compare with local memory.py.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened via official documentation navigation. Web-verified 2026-11-04.

## Resources · PydanticAI foundations

Agent construction, tools and dependencies

### [PydanticAI — Agents](https://pydantic.dev/docs/ai/core-concepts/agent/)

Understand agent construction and the per-run instructions used alongside the base prompt.

Scope / version note: Rolling documentation; workshop uses locked PydanticAI 2.62.0.

Verification: Opened official Agents link from current PydanticAI navigation (2026-11-04).

### [PydanticAI — function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/)

Register functions as tools and understand the RunContext dependency boundary.

Scope / version note: Rolling PydanticAI docs; workshop pins pydantic-ai-slim 2.62.0.

Verification: Opened ai.pydantic.dev/tools, followed official redirect and checked registration methods. Web-verified 2026-11-04.

### [PydanticAI — dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

Follow how runtime services and the selected customer reach tools through ToolDeps.

Scope / version note: Rolling PydanticAI docs; workshop pins pydantic-ai-slim 2.62.0.

Verification: Opened ai.pydantic.dev/dependencies, followed official redirect and checked deps_type/deps/RunContext. Web-verified 2026-11-04.

## Resources · Short-term memory

Persistence, retrieval scope and typed history

### [Conversation and message operations](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/)

Inspect add_message, conversation creation and retrieval of persisted turns.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened from ShortTermMemory API; checked add_message signature. Web-verified 2026-11-04.

### [Message search and context](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

Read semantic-search scope limits; the workshop deliberately uses namespace-scoped local Cypher.

Scope / version note: Official page notes Bolt session_id does not isolate semantic search and get_context can include global matches. Workshop local namespace-scoped retrieval is intentional.

Verification: Opened and checked search_messages/get_context scope notes. Web-verified 2026-11-04.

### [PydanticAI — messages and chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/)

Pass typed prior turns through message_history; keep additional retrieved evidence in instructions.

Scope / version note: Rolling PydanticAI docs; workshop pins pydantic-ai-slim 2.62.0.

Verification: Opened ai.pydantic.dev/message-history, followed official redirect and checked message_history examples. Web-verified 2026-11-04.

### [ShortTermMemory API reference](https://neo4j.com/labs/agent-memory/reference/api/short-term/)

Conversation storage and backend differences, including implicit Bolt conversation creation.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened API index and checked Bolt/NAMS distinction. Web-verified 2026-11-04.

## Resources · Entities and ontologies

Structure, identity and SQL grounding boundaries

### [Entity and relationship operations](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/)

Check entity upserts, relationship operations and returned values before extending hydration.

Scope / version note: Workshop PropertyWriter is repository code; do not imply it is a neo4j-agent-memory API.

Verification: Opened from LongTermMemory API and checked add_entity semantics. Web-verified 2026-11-04.

### [Drive extraction from an ontology](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/)

Read YAML types, aliases, descriptions and validation. Workshop extraction uses the LLM path.

Scope / version note: Guide pins 0.7.0 and demonstrates GLiNER 2.5 as well as LLM configuration. Workshop uses an LLM extractor with its checked-in ontologies.

Verification: Opened via official how-to index and inspected ontology example. Web-verified 2026-11-04.

### [Entity resolution and deduplication](https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/)

Study canonical identity, aliases, similarity signals and reviewed duplicate handling.

Scope / version note: Rolling documentation may differ from workshop SDK 0.8.0. Use the workshop repository and uv.lock for executable examples.

Verification: Opened through official explanation index. Web-verified 2026-11-04.

## Resources · Preferences and integration

Customer scope and application-owned memory policy

### [Preference and fact operations](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/)

Inspect add_preference and get_preferences_for; keep explicit customer scope in application code.

Scope / version note: Preference category and semantic search are not customer authorization boundaries; workshop uses explicit user_identifier.

Verification: Opened and checked add_preference/get_preferences_for. Web-verified 2026-11-04.

### [How entity extraction works](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/)

Distinguish candidate extraction, validation and resolution. The broader pipeline is optional background.

Scope / version note: The general multi-stage pipeline is broader than the workshop's configured LLM-only extraction.

Verification: Opened via extraction how-to and inspected LLM/client-side extraction sections. Web-verified 2026-11-04.

### [Use Neo4j Agent Memory with PydanticAI](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

Compare the SDK integration with this workshop’s explicit history, tools and local retrieval helpers.

Scope / version note: Recipe explicitly targets SDK 0.6.0 and shipped MemoryDependency/create_memory_tools. Workshop 0.8.0 deliberately uses local ToolDeps, scoped helpers and typed message_history.

Verification: Opened full official integration recipe. Web-verified 2026-11-04.

## Resources · Record an execution

Trace lifecycle, observations and outcomes

### [Trace lifecycle API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

Read start_trace, complete_trace and get_trace_with_steps alongside the module 4 code.

Scope / version note: Workshop pins SDK 0.8.0. Module 4 uses explicit application recording around its guards and SQL operations; hosted trace behavior is different. The resource is a focused page, not an unverified fragment.

Verification: Opened official API page on 2026-11-04; trace method signatures and Bolt/NAMS behavior inspected.

### [Steps, tool calls and message provenance](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/)

Inspect add_step, record_tool_call, message links and Step → TOUCHED → Entity semantics.

Scope / version note: Bolt behavior matches the graph concept used in the workshop; do not assume NAMS preserves these optional links or arguments.

Verification: Opened the actual linked official API page on 2026-11-04 and inspected add_step, record_tool_call and link_trace_to_message.

### [Reasoning models and TraceOutcome](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/)

Check status, outcome and identifier fields; recorded execution is not hidden model reasoning.

Scope / version note: Use the workshop's pinned SDK for executable code. The models describe recorded application events and results, not hidden model reasoning.

Verification: Opened official Models and structured outcomes page on 2026-11-04.

### [ReasoningMemory API index](https://neo4j.com/labs/agent-memory/reference/api/reasoning/)

Entry point to trace lifecycle, step/tool recording, structured outcomes and search references.

Scope / version note: Main signatures target Bolt. NAMS implements a different conversation-level reasoning lifecycle. Persisted observable events should not be described as a model's private chain of thought.

Verification: Opened official ReasoningMemory API reference on 2026-11-04 and followed its focused subpage links.

## Resources · Retrieve and audit traces

Failures can be useful examples; inspect actual receipts

### [Trace search and hosted lifecycle differences](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/)

Compare SDK search with the local completed-trace, namespace-scoped retrieval used here.

Scope / version note: Workshop similar_executions is local, namespace-scoped Cypher over completed traces followed by SDK get_trace_with_steps. It does not call the SDK get_similar_traces API described here.

Verification: Opened official page on 2026-11-04; its search section is explicitly Bolt-only.

### [Record and verify a failed tool call](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/)

Work through a separate Bolt example that records failure, completes an outcome and verifies readback.

Scope / version note: Online recipe explicitly installs SDK 0.7.0 while the workshop pins 0.8.0. Follow the repo's uv/Make commands for the workshop, not this separate tutorial's environment setup.

Verification: Opened official guide on 2026-11-04; verified title, declared Bolt target, failure handling and documented NAMS differences.

### [Audit reasoning with TOUCHED edges](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

Follow step-to-entity dependencies and source messages; check backend support before transferring queries.

Scope / version note: Guide targets Bolt and SDK 0.7.0. It explicitly warns that Python NAMS drops touched_entities; a callable method is not proof of equivalent hosted persistence.

Verification: Opened official guide on 2026-11-04; inspected its explicit Step-to-Entity TOUCHED relationship and message linkage discussion.

## Resources · NAMS: service and scope

Hosted contracts evolve independently of the SDK pin

### [NAMS live API documentation](https://memory.neo4jlabs.com/docs)

Check request fields, scope, capabilities and hosted lifecycle responses.

Scope / version note: Current workflow sends nameHint and explicit conversations scope, adding skillId for a new version. Both generation commands require the saved conversation ID. With a missing receipt, use the checked-in skill or seed the designated workspace. Check the live deployment contract before delivery.

Verification: Opened public docs on 2026-11-04. Skill Generation > POST /v1/skills/generate says scope.type is required; checked its listed request body and 400 response.

### [Connect Python to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/)

Learn the SDK connection route and hosted conversation identifiers; the workshop uses direct REST workflows.

Scope / version note: Separate SDK memory connection route. The workshop uses direct HTTPX for hosted skill workflows and authored fixtures, while its support app retains Bolt/AuraDB.

Verification: Opened official guide on 2026-11-04; checked its hosted key and service-issued conversation-ID requirements.

### [Bolt vs NAMS capabilities and scope](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/)

Compare supported operations, identifiers and data scope. Similar method names do not imply parity.

Scope / version note: Reference explicitly describes Python 0.7.0 and TypeScript 0.5.0; workshop pins Python 0.8.0. NAMS is continuously shipped and /v1 is not an SDK version. Treat this as a capability checklist and check the installed version.

Verification: Opened official reference on 2026-11-04; checked its SDK version statement and messages/entities/preferences/reasoning/extraction capability rows.

### [NAMS OpenAPI specification](https://memory.neo4jlabs.com/openapi.json)

Inspect the exact hosted schemas used by the workshop HTTP workflows.

Scope / version note: The service ships independently of the pinned Python SDK. Use the current deployment contract.

Verification: Official public OpenAPI document checked on 2026-11-04.

### [NAMS API key dashboard](https://memory.neo4jlabs.com/dashboard/api-keys)

After signing in, create a workspace-bound data key and keep it in private configuration.

Scope / version note: Exact link is exposed by public docs. Authenticated creation controls were not inspected; avoid invented button labels.

Verification: Verified as the API Keys destination linked by official NAMS docs on 2026-11-04.

## Resources · Skills and governance

Generation, publication, drift and portable artifacts

### [Agent Skills concepts and provenance](https://neo4j.com/labs/agent-memory/explanation/skills/)

Separate distillation, review and consumption. Grounding supports inspection; it does not prove correctness.

Scope / version note: Preview REST/MCP feature, with no SDK skill accessor or Bolt skill API. A skill is derived from memory, not a fourth memory layer. Receiving application executes it; documented service execution is gated dry-run planning.

Verification: Opened official Agent Skills (Preview) page on 2026-11-04; inspected creation/review/use, GROUNDED_IN, relation to memory and execution limits.

### [Skills API: generate, review, publish and drift](https://neo4j.com/labs/agent-memory/reference/skills-api/)

Inspect required scopes, run outcomes, review, publication and per-skill drift endpoints.

Scope / version note: Current workflow polls succeeded runs, automatically submits decision=approve, publishes and downloads a ZIP. This is not an interactive human review checkpoint. Skills may have deployment-specific gates and attestation.

Verification: Opened official Skills API (Preview) reference on 2026-11-04 and checked REST endpoints, lifecycle/run outcomes, attestation and gate descriptions.

### [Distil and download a recorded procedure](https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/)

Follow a separate hosted tutorial through fixture seeding, provenance inspection and SKILL.md download.

Scope / version note: Separate SDK 0.7.0 tutorial with a dedicated empty workspace and different request flow. It stops after package verification; it does not demonstrate execution in a receiving agent. Workshop's fresh_agent.py supplies that separate application example.

Verification: Followed the official Skills API quickstart link and opened it on 2026-11-04; checked its declared scope, fixture, preview limits and verification outcome.

## Resources · GraphAcademy: Python path

Courses that continue the workshop’s core concepts

### [Context Graphs: Agent Memory with Neo4j](https://graphacademy.neo4j.com/courses/genai-context-graphs)

Continue with Python memory concepts, POLE+O extraction and queries across the context graph.

Verification: Opened official GraphAcademy course page; confirmed title, Python package, learning objectives and module outline.

### [Neo4j Agent Memory Workshop](https://graphacademy.neo4j.com/courses/workshop-agent-memory)

Build a PydanticAI learning assistant and implement a custom memory tool.

Verification: Opened official GraphAcademy course page; confirmed Pydantic AI learning-assistant project, memory layers and custom-tool module.

### [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals)

Practice graph patterns and filtering before adapting the workshop’s scoped retrieval queries.

Verification: Followed prerequisite link from the official memory workshop; opened course page and confirmed read/write query modules.

## Resources · Other stacks and releases

Alternative learning paths; verify the selected stack

### [Agent Memory in 90 Minutes](https://graphacademy.neo4j.com/courses/workshop-agent-memory-90)

Adjacent path: Copilot, MCP and AIP skill distillation; a different workflow from module 5.

Verification: Opened official GraphAcademy course page; confirmed create-context-graph, Copilot/MCP and Agent Instruction Protocol workflow.

### [Agent Memory Workshop with TypeScript](https://graphacademy.neo4j.com/courses/workshop-agent-memory-ts)

Adjacent path: a Mastra assistant, graph retrieval, context traces and code-enforced guardrails.

Verification: Opened official GraphAcademy course page; confirmed TypeScript/Mastra framework and lesson outline.

### [Neo4j Agent Memory — releases](https://github.com/neo4j-labs/agent-memory/releases)

Track published changes before upgrading. Compare release notes, package files and your lockfile.

Scope / version note: Page retrieved lists 0.7.0 as latest; do not label this as the 0.8.0 release.

Verification: GitHub releases page opened. Web-verified 2026-11-04.

## Resources · Read: context graphs

Official Neo4j articles for broader design context

### [Meet Lenny’s Memory: Building context graphs for AI agents](https://neo4j.com/blog/developer/meet-lennys-memory-building-context-graphs-for-ai-agents/)

A package introduction and PydanticAI example linking conversations, entities and reasoning traces.

Published: 2026-02-02.

Verification: Opened official Neo4j article; confirmed H1, author William Lyon, publication date and three-memory-type introduction.

### [Modeling agent memory](https://neo4j.com/blog/developer/modeling-agent-memory/)

Background on memory models and write strategies. Its older taxonomy differs from this workshop.

Published: 2025-03-20.

Verification: Opened official Neo4j article; confirmed H1, author Alex Gilmore, publication date and modeling discussion.

### [When your agents share a brain: Building multi-agent memory with Neo4j](https://neo4j.com/blog/developer/when-your-agents-share-a-brain-building-multi-agent-memory-with-neo4j/)

Explore a Strands example that shares graph-backed memory across multiple agents.

Published: 2026-04-13.

Verification: Opened official Neo4j article; confirmed H1, author William Lyon, publication date and shared-memory architecture.

## Resources · Read: integrations and skills

Framework integration, hosted memory and distillation

### [Building an AI agent with memory: Microsoft Agent Framework + Neo4j](https://neo4j.com/blog/developer/building-an-ai-agent-with-memory-microsoft-agent-framework-neo4j/)

Explore conversation, preference, entity and trace memory in another agent framework.

Published: 2026-04-08.

Verification: Opened official Neo4j article; confirmed H1, author William Lyon, publication date, TfL Explorer architecture and framework integration.

### [A Tour of the Neo4j Agent Memory Service (NAMS)](https://neo4j.com/blog/genai/a-tour-of-the-neo4j-agent-memory-service-nams/)

See the hosted console and managed memory pipeline accessed through REST or MCP.

Published: 2026-06-23.

Verification: Opened official Neo4j article; confirmed H1, author William Lyon, publication date, managed service scope and REST/MCP interfaces.

### [From Agent Memory to Portable Skills](https://neo4j.com/blog/genai/from-agent-memory-to-portable-skills/)

Read about scoped distillation, SKILL.md reuse and governance as the source memory changes.

Published: 2026-08-06.

Verification: Opened official Neo4j article; confirmed H1, author William Lyon, publication date and scoped skill-distillation discussion.

## Reference coverage

| Source section | Topic | Native slide IDs | References |
| --- | --- | --- | --- |
| 1 | Road to Agent Memory | ram_slide_001 | [SDK GitHub](https://github.com/neo4j-labs/agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/) · [GitHub Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) · [local setup](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md) · [Module 1 entry point](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_1/app/agent.py) |
| 2 | What you’ll leave with | ram_design_002, ram_slide_003 | [Memory docs](https://neo4j.com/labs/agent-memory/) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [the baseline agent](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_1/app/agent.py) |
| 3 | Agenda · 150 min | ram_slide_004 | [GraphAcademy: Python](https://graphacademy.neo4j.com/courses/workshop-agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/) · [Facilitator timetable](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/run-of-show.md) |
| 4 | Add memory, then build on it | ram_design_005, ram_slide_006 | [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Lenny’s Memory](https://neo4j.com/blog/developer/meet-lennys-memory-building-context-graphs-for-ai-agents/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) |
| 5 | Module 0 — Your environment | ram_design_007, ram_slide_008 | [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [NAMS console](https://memory.neo4jlabs.com/) · [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Connect to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/) · [Open the workshop in Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) · [workshop checkout and local setup](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md) |
| 6 | Module 0 — Credential checklist | ram_design_009 | [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [NAMS console](https://memory.neo4jlabs.com/) |
| 7 | Module 0 — Smoke test, live | ram_design_010 | [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [Workshop instructions](https://github.com/johnymontana/road-to-agent-memory/blob/main/README.md) · [Open Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory) |
| 8 | Module 1 — Two stores, two jobs | ram_design_011, ram_slide_012 | [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) |
| 9 | Module 1 — Meet the agent | ram_design_013 | [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) |
| 10 | The baseline: PydanticAI + business tools | ram_code_m1 | [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/) · [module_1/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_1/app/agent.py) |
| 11 | Module 1 — The failure: statelessness | ram_design_014, ram_slide_015 | [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) |
| 12 | Module 1 — Live demo: the stateless baseline | ram_design_016 | [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) |
| 13 | Module 1 — The eval baseline | ram_design_017 | [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Grader](https://github.com/johnymontana/road-to-agent-memory/blob/main/scripts/eval.py) · [Module 1 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-1.md) |
| 14 | Meet neo4j-agent-memory | ram_mem_intro | [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [SDK GitHub](https://github.com/neo4j-labs/agent-memory) |
| 15 | Where memory meets PydanticAI | ram_mem_seam | [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/) |
| 16 | Configure and open one memory client | ram_code_client | [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [module_2/app/memory.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/memory.py) |
| 17 | Module 2 — Concept: short-term memory | ram_design_018 | [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Short-term API index](https://neo4j.com/labs/agent-memory/reference/api/short-term/) |
| 18 | Module 2 — Message chains in the graph | ram_design_019, ram_slide_020 | [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) |
| 19 | Persist both sides of a conversation | ram_code_m2_write | [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [module_2/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/agent.py) |
| 20 | Module 2 — Context assembly | ram_design_021, ram_slide_022 | [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) |
| 21 | Retrieve evidence, then call the agent | ram_code_m2_inject | [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [module_2/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/agent.py) · [module_2/app/context.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_2/app/context.py) |
| 22 | Module 2 — Live demo: the returning customer | ram_design_023 | [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md) |
| 23 | Module 2 — The restart beat | ram_design_024 | [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md) |
| 24 | Module 2 — Exploration brief | ram_design_025 | [Cypher course](https://graphacademy.neo4j.com/courses/cypher-fundamentals) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/) · [Module 2 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-2.md) |
| 25 | Module 3 — Concept: long-term memory | ram_design_026 | [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/) |
| 26 | Module 3 — Ontology-driven extraction | ram_design_027, ram_slide_028 | [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [POLE+O](https://neo4j.com/labs/agent-memory/explanation/poleo-model/) · [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/) |
| 27 | Turn on ontology-driven extraction | ram_code_m3_extract | [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [module_3/app/memory.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/memory.py) · [module_3/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/agent.py) |
| 28 | Module 3 — Before / after: default vs. custom ontology | ram_design_029, ram_slide_030 | [POLE+O](https://neo4j.com/labs/agent-memory/explanation/poleo-model/) · [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) |
| 29 | Module 3 — The hybrid pipeline (the design-principle slide) | ram_design_031, ram_slide_032 | [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) |
| 30 | Ground extracted entities in SQL facts | ram_code_m3_ground | [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [module_3/app/hydrate.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/hydrate.py) |
| 31 | Module 3 — Entity resolution & aliases | ram_design_033, ram_slide_034 | [Resolution](https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/) · [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) |
| 32 | Module 3 — Live demo: watch the graph bloom | ram_design_035 | [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Extraction](https://neo4j.com/labs/agent-memory/explanation/extraction-pipeline/) · [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) |
| 33 | Module 3 — Under the hood: hydration & enrichment | ram_design_036 | [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/) · [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) |
| 34 | Expose memory tools to PydanticAI | ram_code_m3_tools | [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/) · [module_3/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/agent.py) · [module_3/app/memory_tools.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/memory_tools.py) |
| 35 | Save and recall one customer’s preferences | ram_code_m3_preferences | [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/) · [module_3/app/memory_tools.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/memory_tools.py) · [module_3/app/context.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_3/app/context.py) |
| 36 | Module 3 — Exploration brief (40-min module, tiered) | ram_design_037 | [GraphAcademy: Python](https://graphacademy.neo4j.com/courses/workshop-agent-memory) · [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/) · [Module 3 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-3.md) |
| 37 | Module 4 — Concept: reasoning memory | ram_design_038 | [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [Reasoning API index](https://neo4j.com/labs/agent-memory/reference/api/reasoning/) |
| 38 | Module 4 — Anatomy of a trace | ram_design_039, ram_slide_040 | [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) |
| 39 | Open the trace before execution | ram_code_m4_lifecycle | [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [module_4/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/agent.py) · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py) |
| 40 | Attach observations and provenance | ram_code_m4_tools | [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py) |
| 41 | Complete the trace with an outcome | ram_code_m4_outcome | [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py) |
| 42 | Module 4 — Similar-task retrieval | ram_design_041, ram_slide_042 | [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) |
| 43 | Recall completed executions | ram_code_m4_recall | [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [module_4/app/reasoning.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/reasoning.py) · [module_4/app/agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_4/app/agent.py) |
| 44 | Module 4 — Live demo: record, decline, compare | ram_design_043 | [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md) |
| 45 | Module 4 — The provenance question | ram_design_044 | [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md) |
| 46 | Module 4 — Exploration brief | ram_design_045 | [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/) · [Cypher course](https://graphacademy.neo4j.com/courses/cypher-fundamentals) · [November 1 comparison log](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/reviews/2026-11-01-workshop-fixes/command-09.log) · [Module 4 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-4.md) |
| 47 | Module 5 — Build skills on top of agent memory | ram_design_046 | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 48 | Build procedures on top of agent memory | ram_m5_concepts | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) |
| 49 | Build reusable procedures on agent memory | ram_m5_pipeline | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) |
| 50 | Module 5 — The app, hosted workspace and consumer | ram_design_048 | [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [NAMS console](https://memory.neo4jlabs.com/) |
| 51 | Open your NAMS workspace | ram_m5_signup | [NAMS sign in](https://memory.neo4jlabs.com/) · [Setup docs](https://memory.neo4jlabs.com/docs) |
| 52 | Create a key for the workshop workspace | ram_m5_key | [API key dashboard](https://memory.neo4jlabs.com/dashboard/api-keys) · [Authentication docs](https://memory.neo4jlabs.com/docs) |
| 53 | Connect the workshop and check capabilities | ram_m5_connect | [NAMS docs](https://memory.neo4jlabs.com/docs) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 54 | Seed a small, inspectable memory corpus | ram_m5_seed | [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 55 | Complete the traces before distilling them | ram_code_m5_seed_complete | [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs) · [module_5/workflows/seed.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/seed.py) |
| 56 | Distill one conversation into a versioned skill | ram_code_m5_distill | [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs) · [module_5/workflows/distill.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/distill.py) |
| 57 | Approve, publish and unpack the skill package | ram_code_m5_publish | [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs) · [module_5/workflows/distill.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/distill.py) |
| 58 | Inspect the downloaded skill package | ram_m5_package | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) |
| 59 | Inspect the versioned skill graph | ram_slide_047 | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 60 | Quality signals support review | ram_m5_evaluate | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) |
| 61 | Give the skill to a fresh PydanticAI agent | ram_code_m5_agent | [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [module_5/app/fresh_agent.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/app/fresh_agent.py) |
| 62 | Compare the fresh agent with and without a skill | ram_design_049 | [Skills tutorial](https://neo4j.com/labs/agent-memory/tutorials/skills-quickstart/) · [NAMS console](https://memory.neo4jlabs.com/) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 63 | Governance follows the evidence | ram_design_050 | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) |
| 64 | Follow provenance to the memory a skill uses | ram_code_m5_drift | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) · [module_5/workflows/drift.py](https://github.com/johnymontana/road-to-agent-memory/blob/main/module_5/workflows/drift.py) |
| 65 | Govern the evidence behind a skill | ram_slide_051 | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) |
| 66 | Run the drift loop and restore the policy | ram_m5_governance_demo | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 67 | Hosted capability, explicit boundaries | ram_design_052 | [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Live NAMS API](https://memory.neo4jlabs.com/docs) |
| 68 | Module 5 — Exploration brief | ram_design_053 | [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) · [Module 5 guide](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/modules/module-5.md) |
| 69 | Wrap — The eval scoreboard, re-run | ram_design_054 | [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) |
| 70 | Wrap — Memory is the foundation; skills build on it | ram_design_055, ram_slide_056 | [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [Graph model](https://neo4j.com/labs/agent-memory/explanation/graph-architecture/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) |
| 71 | Wrap — Which record answers the question? | ram_design_057, ram_slide_058 | [Backend capabilities](https://neo4j.com/labs/agent-memory/reference/backend-capabilities/) · [Connect to NAMS](https://neo4j.com/labs/agent-memory/how-to/use-nams/) · [NAMS console](https://memory.neo4jlabs.com/) |
| 72 | Wrap — Your Monday morning path | ram_design_059 | [SDK GitHub](https://github.com/neo4j-labs/agent-memory) · [Memory docs](https://neo4j.com/labs/agent-memory/) · [GraphAcademy: memory](https://graphacademy.neo4j.com/courses/genai-context-graphs) · [teardown for keys, Codespaces and AuraDB](https://github.com/johnymontana/road-to-agent-memory/blob/main/docs/teardown.md) · [Run the recipe](https://github.com/johnymontana/road-to-agent-memory/blob/main/scripts/monday_memory.py) |
