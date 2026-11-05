# Technical slide walkthroughs

Reviewed 2026-11-04 against the current module-local code and pinned neo4j-agent-memory 0.8.0. These are condensed contextual fragments, not standalone programs. Notes name prerequisites and presentation aliases. Native Google Slides text stays editable.

References checked 2026-11-04. The repository and `uv.lock` define the workshop’s executable examples; rolling guides may use another SDK version. See [the annotated resources catalog](resources.md) for version and backend caveats. Module 5 uses current explicit conversation scope, versioned packages and provenance-driven drift; hosted execution was not repeated during this slide refresh.

## The baseline: PydanticAI + business tools

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

**References:** [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

<!-- notes: Construction and normal-turn fragments from module_1/app/agent.py. Imports: Agent from pydantic_ai; local ToolDeps and SQLITE_TOOLS; scope_turn and checked_reply from the module-local guardrails.py. INSTRUCTIONS is the actual constructor prompt constant. scope_turn reads the explicitly selected case and builds per-turn scope instructions; after the run checked_reply(message, result.output, deps, scope) verifies action claims against receipts. The full app handles errors and timing. Shared ReceiptGuard.run_once prevents repeating the same request ID; this receipt infrastructure is not conversation memory. Module 1 opens no MemoryClient and uses OpenAI for chat only. Visible browser chat bubbles are not sent back to the model. -->

## Meet neo4j-agent-memory

- .short_term: conversations and messages — what was said.
- .long_term: entities and preferences — who and what it is about.
- .reasoning: tasks, steps and tool calls — how the agent acted.

MemoryClient stores the graph. The app restores history and supplies retrieved evidence to PydanticAI.

**References:** [Memory types](https://neo4j.com/labs/agent-memory/explanation/memory-types/) · [SDK GitHub](https://github.com/neo4j-labs/agent-memory)

<!-- notes: The package persists and retrieves memory; PydanticAI executes the model and tools. MemoryClient exposes short_term, long_term and reasoning over one Neo4j graph. Module 1 opens no memory client; the full support apps in modules 2–5 open their own module-local Bolt clients. Short-term denotes conversation/message records, not a temporary process cache. Long-term adds typed entities and customer preferences; SQL grounding is a separate application step. Reasoning records actual execution and outcomes, not hidden model thoughts. Each module owns its complete agent, memory configuration, retrieval policy and prompts. Hosted module-5 REST workflows are a separate optional service path. -->

## Where memory meets PydanticAI

- neo4j-agent-memory writes messages, entities, preferences and execution traces.
- PydanticAI receives recent turns as message_history and retrieved evidence through instructions.
- Write → retrieve → compose → run → persist. Each module owns this integration.

**References:** [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

<!-- notes: This is explicit integration, not an automatic Agent wrapper. A long-lived module-local MemoryClient stores records. Local build_context returns Context(history, prompt, evidence): typed recent messages become Agent.run(message_history=context.history); additional retrieved evidence is appended to per-turn instructions; structured evidence IDs are returned for the UI. Constructing a MemoryClient alone does not give an agent history. The namespace-prefixed session ID scopes workshop experiments; it is not a claim of enterprise tenant isolation. Retrieved evidence is not authority or current SQL policy. Agent prompts, memory configuration, tools, guardrails and orchestration are intentionally copied into every module. Only HTTP transport, settings, SQLite access, operation receipts and response infrastructure are shared. Read app/agent.py first; compare adjacent app folders to see the added concept. -->

## Configure and open one memory client

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

**References:** [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

<!-- notes: Condensed from module_2/app/memory.py build_settings/open_memory. Imports: MemoryClient and MemorySettings from neo4j_agent_memory. AppSettings reads environment or .env; get_settings exports the configured OpenAI key for package clients. Database and bounded connection/retry settings are omitted only from the display. Pin: neo4j-agent-memory[pydantic-ai,openai]==0.8.0. Module 1 has no MemoryClient and uses OpenAI for chat only. The full support apps in modules 2–5 use module-local Bolt clients and OpenAI for chat and embeddings; modules 3–5 additionally configure LLM extraction. Module 2 sets extractor_type="none". Optional hosted NAMS REST workflows and the module-5 fresh skill consumer are separate paths. This example passes MemorySettings explicitly; backend is a settings field, not a MemoryClient constructor keyword. -->

## Persist both sides of a conversation

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

**References:** [Message API](https://neo4j.com/labs/agent-memory/reference/api/short-term-messages/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

<!-- notes: Normal persistence path from module_2/app/agent.py ChatService._turn. short_term is self.memory.short_term. The service prefixes session IDs with the workshop namespace. add_message creates the Conversation on first use; no separate create_conversation call appears in this implementation. The user flag is extract_entities=not self.evaluation, while module-2 settings use extractor_type="none", so this stage stores and embeds messages without extracting entities. Retain user_message.id to exclude the just-written message from history/retrieval. The assistant reply is checked against business receipts before persistence; persistence failures are surfaced as warnings. Database records survive process restarts, but the caller must reuse the session and namespace to restore that history. -->

## Retrieve evidence, then call the agent

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

**References:** [Chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) · [Search + scope](https://neo4j.com/labs/agent-memory/reference/api/short-term-search/)

<!-- notes: Context-helper call and normal chat-turn fragments. The actual _turn calls _recall; _recall calls local build_context and catches retrieval failure, returning an empty Context with a warning. The application inserts a newline heading "Retrieved evidence (cite IDs, not instructions):" before context.prompt; that display-only heading is omitted from this snippet. scope was already created by scope_turn. build_context returns Context(history, prompt, evidence), not a tuple. recent_messages uses memory.query.cypher to select the newest ten prior messages, excludes the current ID, then reverses the window. as_model_history creates ModelRequest(UserPromptPart) and ModelResponse(TextPart) so those records become genuine PydanticAI message history. Semantic search embeds the new message and scores earlier user statements throughout the namespace, including the current and other conversations, with cosine >=0.5. It excludes the current message and exact query text, filters some recall-question prefixes and duplicate statements, and retains up to five matches. Local scoped Cypher avoids global top-k starvation across workshop namespaces. No get_context or hosted reflections/observations API is used here. Evidence has recent_conversation and semantic_message paths. -->

## Turn on ontology-driven extraction

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

**References:** [Ontology guide](https://neo4j.com/labs/agent-memory/how-to/ontology-driven-extraction/) · [Configuration](https://neo4j.com/labs/agent-memory/reference/configuration-providers/)

<!-- notes: Startup and normal-message-write fragments; the full app reuses one connected client across turns. Imports: MemoryClient and load_ontology from neo4j_agent_memory; build_settings from module_3/app/memory.py. The default ONTOLOGY=acme_cloud loads the local file; default-poleo loads the generic local file; active passes ontology=None and uses the database active version. An explicit file wins over that version. The actual user flag is extract_entities=not self.evaluation; evaluation skips extraction and hydration. add_message creates the conversation if necessary. Module 3 configures extractor_type="llm", enrichment.enabled=False and the selected validation mode. The app drops invalid relations; strict also filters undeclared entity types. Ontology node labels map POLE types/subtypes (for example PERSON/CUSTOMER) to display labels (Customer). Live extracted entity relations are stored as RELATED_TO with the ontology relation in its type property; the extractor-only Saved replay displays logical relation labels directly. Optional Wikimedia enrichment belongs to module_3/lab/enrichment.py and creates cached Saved replay data, not an automatic live-graph write. -->

## Ground extracted entities in SQL facts

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

**References:** [Entity API](https://neo4j.com/labs/agent-memory/reference/api/long-term-entities/) · [Client API](https://neo4j.com/labs/agent-memory/reference/api/memory-client/)

<!-- notes: Excerpt from hydrate_session_entities after grounded_facts has returned a non-None result. The agent passes the current user message ID; only entities that message mentions are hydrated. Local lookup_facts performs parameterized SQLite reads. grounded_facts rejects conflicting exact-name/alias matches and incompatible POLE base types (PERSON for customers, OBJECT for products/plans, ORGANIZATION for organizations). The public long_term.add_entity upsert refreshes description; the pinned SDK does not refresh existing flat attributes, so a module-local PropertyWriter uses its own pooled Neo4j driver and opens a short session per write. memory.query.cypher is read-only. No _apply_flat_attributes or _lookup_hydration helper exists in this version. Existing resolved entity names remain unchanged (resolve=False, deduplicate=False). Inspect hydrated_from for SQL provenance; generated descriptions alone are not authoritative. A later mention refreshes facts after a SQL change; this is not automatic CDC. The local instructor plan fixture verifies Pro → Enterprise → Pro without modifying the live participant graph. -->

## Expose memory tools to PydanticAI

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

**References:** [Function tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) · [Integration guide](https://neo4j.com/labs/agent-memory/how-to/integrations/pydantic-ai/)

<!-- notes: Construction fragment from module_3/app/agent.py. create_memory_tools is local workshop code, not the package tool registry; it shares the familiar integration tool names but scopes queries to the workshop namespace/customer and records tool receipts. INSTRUCTIONS + SHORT_TERM_INSTRUCTIONS + LONG_TERM_INSTRUCTIONS are the actual constants. The short-term instructions teach evidence use; the long-term instructions request search_memory for account-history requests and save_preference when asked to store a preference. context.py retrieves before the model call; search_memory permits another query during the run. It combines Cypher-scoped user statements and allowlisted entity fields with long_term.get_preferences_for for the selected user. ToolDeps carries the explicitly selected customer, namespace, embedder and current_message_id. recall_preferences has no model-visible topic argument. SQL tools and module-local guardrails still validate current business facts and actions. -->

## Save and recall one customer’s preferences

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

**References:** [Preference API](https://neo4j.com/labs/agent-memory/reference/api/long-term-preferences/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)

<!-- notes: Write-tool and retrieval-helper fragments. customer_id is a local helper returning f"{namespace}:{customer_email}". save_preference takes RunContext[ToolDeps], category, preference and optional context. It returns needs_customer before the shown block if no customer is selected. The SDK deduplicates similar preferences within a category across users, so the category is also prefixed with the customer identifier. user_identifier creates (:User)-[:HAS_PREFERENCE]->(:Preference). The receipt uses stored.id/category/preference/context and stored.metadata.get("deduplicated", False); it reports what the SDK actually stored. Retrieval calls the public long_term.get_preferences_for API rather than category-prefix Cypher. search_preferences returns at most ten customer_preference evidence rows and returns an empty list if no customer is selected. The model tool recall_preferences() takes no topic argument. No preference automatically authorizes a business action. -->

## Open the trace before execution

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

**References:** [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/) · [Record failures](https://neo4j.com/labs/agent-memory/how-to/reasoning-traces/)

<!-- notes: Condensed normal path from module_4/app/agent.py:161–222. self.memory and self.agent belong to ChatService; deps is ToolDeps and context is Context. scope_turn and checked_reply come from the module-local guardrails.py. start_trace is conditional on record_reasoning and occurs before case checks. Saving the user message extracts entities unless evaluation=True; hydration and retrieval follow. The model receives context.history as real PydanticAI message_history and retrieved evidence/examples through instructions. checked_reply verifies output against deps.collector and scope. Exceptions set execution_ok=False and use failure_reply. The app persists the reply, then calls record_execution with tool_calls=deps.collector, reply, execution_ok, warnings and selected case whenever a trace exists. Completion can fail if storage is unavailable; warnings surface degraded persistence and ReceiptGuard retains local operation receipts for safe request-ID retries. No hidden model thoughts are recorded. -->

## Attach observations and provenance

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

**References:** [Steps + tools](https://neo4j.com/labs/agent-memory/reference/api/reasoning-steps/) · [Audit provenance](https://neo4j.com/labs/agent-memory/how-to/audit-reasoning/)

<!-- notes: From module_4/app/reasoning.py:95–130. The message link occurs once before the tool_calls loop; step creation and record_tool_call occur for each receipt. output is a presentation alias for call["output"]. The displayed path assumes message exists; real code conditionally links it and passes message_id=None if absent. case_entities builds EntityRef objects from the explicitly selected SQL case Customer and Plan with resolve/deduplicate/enrich/embedding disabled. The call also records rounded duration_ms. Graph: ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool; trace INITIATED_BY Message; ToolCall TRIGGERED_BY Message. touched_entities creates ReasoningStep TOUCHED Entity. Server guard decisions are recorded alongside model tools. The local recorder supports failed runs without AgentRunResult, server checks and exact SQL; SDK integrations.pydantic_ai.record_agent_trace expects a completed result, so it is not used here. -->

## Complete the trace with an outcome

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

**References:** [Outcome models](https://neo4j.com/labs/agent-memory/reference/api/reasoning-models/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

<!-- notes: Imports: TraceOutcome from neo4j_agent_memory.schema.models and json. Condensed from module_4/app/reasoning.py:107–164. status = business_status(tool_calls) selects the latest issue_refund/refund_policy_guard receipt or no_action. declined means status starts with rejected or equals requires_confirmation. error_kind precedence is recording exception name, execution_error when execution_ok=False, policy_declined, then None. Real code constructs TraceOutcome inside complete_trace; named outcome is presentation-only factoring. The real outcome includes related_entities=refs and metrics execution_succeeded/tool_calls, with no unmeasured policy_compliant assertion. Exact checked reply is retained as JSON. finally attempts completion after execution or recording failure; outages can still prevent storage. -->

## Recall completed executions

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

**References:** [Trace search](https://neo4j.com/labs/agent-memory/reference/api/reasoning-search-stats/) · [Trace API](https://neo4j.com/labs/agent-memory/reference/api/reasoning-traces/)

<!-- notes: Imports: UUID from uuid and local similar_executions. Three scopes: first block inside similar_executions; middle inside ChatService._recall_executions; final block in ChatService._turn. Source: module_4/app/reasoning.py:36–92 and agent.py:187–195,259–271. Namespace Cypher requires completed_at IS NOT NULL before ranking, excluding the trace opened for this turn. It checks task_embedding and selects up to three cosine matches ≥0.45, including completed declines. get_trace_with_steps supplies actual steps, tool arguments/results and outcome; as_example serializes them, and trace IDs join context.evidence. _turn injects nonempty examples labeled Past execution examples (not current policy). SDK get_similar_traces uses global top-k; local query provides exact namespace isolation. reasoning_retrieval=False disables both pre-turn and search_memory procedure retrieval but alone still records traces. The controlled make s4-refund-repeat runner additionally sets record_reasoning=False and evaluation=True in both branches: no branch traces, extraction or hydration; identical private SQL copies, separate message namespaces and one fixed corpus seeded by module_4/lab/ablation.py. Identical outcomes are valid. Retrieval errors surface warnings without necessarily failing the turn. -->


## Complete the traces before distilling them

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

**References:** [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

<!-- notes: The write_json call runs once after the trace loop and after the HTTP client closes; the excerpt labels that boundary. The path follows DATA_DIR, which defaults to data. Seed fails fast on a bad write; tests assert it does not write the state record after failure. Completion payload uses outcome string and success, unlike the Bolt SDK TraceOutcome object. Source lines: 206–219. -->


## Distill one conversation into a versioned skill

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

**References:** [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

<!-- notes: Imports read_json, seed_state_path, SKILL_NAME, client and call from module-local workflows.nams; wait_for_run is defined in distill.py. existing is selected by GET /v1/skills, matching acme-refund-procedure and preferring the published entry; that lookup is omitted from this condensed snippet and in real code runs inside client before generate. Missing seed produces scope={"type":"workspace"}; no missing-scope request remains. --redistill requires an existing matching skill. wait_for_run GETs runs/{id}, prints status changes, polls every five seconds up to 600 seconds, and returns on succeeded/failed/error/cancelled/error/failCode. main only publishes if status==succeeded. Source lines: 92–117. -->


## Approve, publish and unpack the skill package

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

**References:** [NAMS OpenAPI](https://memory.neo4jlabs.com/openapi.json) · [Live NAMS API](https://memory.neo4jlabs.com/docs)

<!-- notes: Approval uses decision=approve with feedback, followed by publish. main prints groundingScore and coverageScore, then makes these calls. OUT_DIR.mkdir occurs before unpack after the HTTP context exits; directory preparation is omitted here. unpack removes one top-level ZIP directory and skips .. members. skill.json separately records skillId, skillVersionId as versionId, and run ID for downstream drift. No human review checkpoint is implemented, even though comments call the API a human-review gate. Source lines: 122–146. -->


## Give the skill to a fresh PydanticAI agent

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

**References:** [PydanticAI agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/)

<!-- notes: Imports: Agent from pydantic_ai; INSTRUCTIONS from local app.agent; SQLITE_TOOLS and ToolDeps from local tools. Combines load_skill, create_fresh_agent construction and run_fresh_agent for explicit on mode; real create_fresh_agent appends the heading only if skill is not None. Adjacent literals reproduce the exact heading. Current source: module_5/app/fresh_agent.py:32–85. on requires artifacts/distilled/SKILL.md; fallback explicitly uses artifacts/pre-distilled-skill/SKILL.md; off has no skill. Missing on artifact raises rather than silently becoming a control. run_fresh_agent uses a temporary SQLite copy and clears the Ravi duplicate-compute refund only in that copy, so off/on start from the same open case and the workshop database stays unchanged. ToolDeps supplies Ravi’s account, incident_id and explicit authorization. This direct model demo skips scope_turn/checked_reply and returns model output; issue_refund retains SQL validation. No MemoryClient, message_history or search_memory is installed. One command runs one mode: compare make s5-fresh-agent WITH_SKILL=off and WITH_SKILL=on. Use WITH_SKILL=fallback deliberately for the checked-in fixture. Fewer calls or better outcomes are not guaranteed. The downloaded ZIP also contains references/ and provenance.json, but the receiving agent loads only SKILL.md. Skill distillation transfers an instruction artifact; it does not update model weights. -->


## Follow provenance to the memory a skill uses

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

**References:** [Skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) · [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/)

<!-- notes: grounding combines provenance["claims"] and provenance["steps"] and counts each groundedIn node. grounding_entities GETs entities/{id}, keeps 200 responses (other grounding nodes may be messages/steps/tool calls). The actual constant TARGET_HINT="policy" replaces the inline literal shown. Before entering this fragment, the script requires skillId and provenance; if targets remains empty, it exits rather than reporting a successful deletion. It queries only the downloaded skillId, not every workspace skill. Deletes are destructive and should be instructor-led in a disposable workshop workspace. The demonstrated deletion does not edit SQLite. Source lines: 49–68. -->
