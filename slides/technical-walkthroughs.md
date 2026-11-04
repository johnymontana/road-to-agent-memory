# Technical slide walkthroughs

Added 2026-11-04. These excerpts target the repository’s pinned
`neo4j-agent-memory` 0.8.0 and PydanticAI integration. They are condensed
fragments inside the module-local agent context. Presenter notes identify imports,
preconditions and omitted setup/error handling. All code is native editable text
in the Google Slides deck.

## The baseline: PydanticAI + business tools

Module 1 · Code · Source: `module_1/app/agent.py`

```python
agent = Agent(
    f"openai:{settings.openai_model}",
    deps_type=ToolDeps,
    tools=list(SQLITE_TOOLS),
    instructions=BASE_INSTRUCTIONS,
    output_type=str,
)
result = await agent.run(
    message, deps=deps,
    instructions=BASE_INSTRUCTIONS,
)
```

Five business tools query SQLite.

No MemoryClient, retrieved evidence or message_history is supplied.

Visible chat bubbles do not become model context.

Presenter context: Imports: Agent from pydantic_ai; ToolDeps and SQLITE_TOOLS from this module. This is a condensed excerpt of construction plus one run. settings is AppSettings; deps is the confirmed per-turn ToolDeps. The full app validates case scope, verifies the reply and saves operation receipts. It deliberately passes no conversation history.

## Meet neo4j-agent-memory

- .short_term: conversations and messages — what was said.
- .long_term: entities and preferences — who and what it is about.
- .reasoning: tasks, steps and tool calls — how the agent acted.

Presenter context: The package is the persistence and retrieval layer; PydanticAI runs the agent. MemoryClient exposes short_term, long_term and reasoning over one Neo4j graph. Short-term refers to conversation/message records, not a temporary process cache. Long-term supplies entities, preferences and facts; grounding is a separate app decision. Reasoning is a record of actual execution, not hidden model thoughts. Follow source messages and explicit provenance edges across layers. Pin and dependency extras are explained on the client code slide.

## Where memory meets PydanticAI

- neo4j-agent-memory persists and retrieves evidence, with configured entity extraction.
- PydanticAI runs the model and tools; the lesson chooses what to write, retrieve and inject.
- Write → retrieve → inject → run → record.

Presenter context: The workshop deliberately uses an explicit integration: a long-lived MemoryClient, local retrieval helpers, PydanticAI instructions and tools, and explicit execution recording. Merely constructing a MemoryClient does not give every Agent.run history. A session identifies a conversation; this repo prefixes session IDs with a namespace to scope experiments. Its local namespace convention is not a claim of enterprise tenant isolation. Retrieved examples are evidence, not instructions or current SQL policy. Package configuration is shared infrastructure while each lesson owns its complete agent implementation.

## Configure and open one memory client

Library introduction · Code · Source: `module_2/app/memory.py`

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

MemoryClient and MemorySettings come from neo4j_agent_memory.

Bolt persists memory in your AuraDB.

The async context owns connection lifetime.

Presenter context: This is a condensed version of build_settings/open_memory in module_2/app/memory.py. Imports: from neo4j_agent_memory import MemoryClient, MemorySettings. AppSettings supplies credentials; get_settings exports the OpenAI key read from .env. Database and bounded connection/retry settings are omitted from this display, not from the application. Pin: neo4j-agent-memory[pydantic-ai,openai]==0.8.0. Modules 1–4 use the same OpenAI account for chat, embeddings and later extraction. Do not use MemoryClient(backend="bolt"); it requires the settings object.

## Persist both sides of a conversation

Module 2 · Code · Source: `module_2/app/agent.py`

```python
await memory.short_term.create_conversation(
    session_id
)
user = await memory.short_term.add_message(
    session_id, "user", message,
    extract_entities=False,
)
# ... retrieve evidence; run the agent; verify reply ...
await memory.short_term.add_message(
    session_id, "assistant", reply,
    extract_entities=False,
)
```

Reuse the same session ID after restart.

The SDK stores Conversation and Message records and orders the messages.

Entity extraction is off in module 2.

Presenter context: Condensed from ChatService._turn. memory is the connected MemoryClient; session_id is namespaced by ChatService. The real module passes extract_entities=not self.evaluation for the user message, while its configured extractor_type="none" prevents entity extraction. This slide uses explicit False to show that stage behavior. Preserve the returned user.id to exclude the current message from retrieval. Assistant persistence happens after the business reply has been verified; failures are surfaced as warnings.

## Retrieve evidence, then call the agent

Module 2 · Code · Source: `module_2/app/agent.py; module_2/app/context.py`

```python
context, evidence = await build_context(
    memory, message, session_id,
    embedder, namespace,
    exclude_id=str(user.id),
    customer_email=account_email,
)
instructions = BASE_INSTRUCTIONS
if evidence:
    instructions += "\nRetrieved evidence:\n" + context
result = await agent.run(
    message, deps=deps, instructions=instructions
)
```

build_context is a local helper.

It uses memory.query.cypher for the latest ten prior messages plus scoped semantic matches.

PydanticAI receives evidence through instructions.

Presenter context: Imports: local build_context and OpenAIEmbedder. This is the actual manual integration pattern, not an automatic memory wrapper. The helper excludes the just-written current message, reverses the newest-ten window into chronological order and deduplicates semantic user statements within namespace. It returns structured source IDs and paths; no reflections/observations API is used on Bolt. deps is the local ToolDeps. The real app catches retrieval errors and labels degraded completion rather than claiming memory was used.

## Turn on ontology-driven extraction

Module 3 · Code · Source: `module_3/app/memory.py; module_3/app/agent.py`

```python
ontology = load_ontology(
    "module_3/ontology/acme_cloud.yaml"
)
config = build_settings(settings)
# config.extraction.extractor_type == "llm"
async with MemoryClient(
    config, ontology=ontology
) as memory:
    user = await memory.short_term.add_message(
        session_id, "user", message,
        extract_entities=True,
    )
```

load_ontology comes from the package.

The YAML guides entity types, aliases and relation patterns.

Extraction links message evidence to entities; SQL supplies business fields.

Presenter context: Imports: MemoryClient and load_ontology from neo4j_agent_memory; build_settings from the module-local memory.py. A conversation already exists as in module 2. Module 3 settings select the LLM extractor, while the ontology is passed at client construction. Invalid relations are filtered in the pinned app; strict mode also filters undeclared entity types. User extraction is disabled during controlled eval. Public Wikimedia enrichment is a separate opt-in cached command, not this extraction call.

## Ground extracted entities in SQL facts

Module 3 · Code · Source: `module_3/app/hydrate.py`

```python
facts = _lookup_hydration(db_path, row["name"])
await memory.long_term.add_entity(
    row["name"], row["type"],
    subtype=row.get("subtype"),
    description=facts["description"],
    attributes=facts["attributes"],
    resolve=False, deduplicate=False,
    generate_embedding=False, enrich=False,
)
await _apply_flat_attributes(
    settings, row["name"], row["type"],
    facts["attributes"], writer=writer,
)
```

SQL supplies email, plan and signup date.

The public upsert refreshes stored knowledge. A local writer updates existing flat properties.

Hydrate before assembling context.

Presenter context: This excerpt begins AFTER hydrate_session_entities has checked current-message mentions, compatible POLE/domain types and nonambiguous exact aliases, and AFTER facts has been confirmed non-None. Both underscore helpers are repository code, not MemoryClient methods. _lookup_hydration reads the private SQL system of record. add_entity refreshes description/metadata. The pooled writer executes the local flat-property SET path because the pinned SDK upsert does not refresh those fields on an existing node. Never hydrate a misclassified Organization with Product facts. The deterministic instructor plan recipe tests Pro → Enterprise → Pro on one local fixture entity.

## Expose memory tools to PydanticAI

Module 3 · Code · Source: `module_3/app/agent.py; module_3/app/memory_tools.py`

```python
memory_tools = create_memory_tools(memory)
agent = Agent(
    f"openai:{settings.openai_model}",
    deps_type=ToolDeps,
    tools=[*SQLITE_TOOLS, *memory_tools],
    instructions=BASE_INSTRUCTIONS,
    output_type=str,
)
# Local tools registered for the model:
# search_memory(query)
# save_preference(category, preference, context)
# recall_preferences(topic)
```

The tool factory closes over MemoryClient.

RunContext[ToolDeps] carries the selected customer and namespace.

Business tools still read and validate SQLite.

Presenter context: create_memory_tools is local workshop code. It returns three PydanticAI-compatible functions, not a built-in SDK tool registry. Search combines scoped user statements, allowlisted grounded entity fields and customer preferences via the public query API. The real module also appends MEMORY_INSTRUCTIONS to the base prompt so the agent searches before asking a returning customer to repeat details. The exact BASE_INSTRUCTIONS name here stands for that composed prompt. See the next slide for the package preference write.

## Save a preference for one customer

Module 3 · Code · Source: `module_3/app/memory_tools.py`

```python
d = ctx.deps  # ctx: RunContext[ToolDeps]
saved = await memory.long_term.add_preference(
    f"{d.namespace}:{d.account_email}:contact",
    "Email only", context="Support follow-ups",
    user_identifier=(
        f"{d.namespace}:{d.account_email}"
    ),
)
return {
    "id": str(saved.id),
    "preference": saved.preference,
    "context": saved.context,
}
```

Require a selected customer before this call.

Scope both category and user identity.

Confirm the actual stored value; deduplication may reuse a prior preference.

Presenter context: This is the write path inside the local save_preference tool, with example category/preference values. The full function returns needs_customer before this block when no account is explicitly selected. It also reports saved.metadata.get("deduplicated", False). Retrieval in this repository uses search_preferences through memory.query.cypher, filtering the namespace/email category prefix. The SDK can deduplicate; never tell the customer a different value was saved than the returned object shows. Imports: RunContext from pydantic_ai, local ToolDeps.

## Record the execution and its outcome

Module 4 · Code · Source: `module_4/app/agent.py; module_4/app/reasoning.py`

```python
trace = await memory.reasoning.start_trace(
    session_id, message
)
try:
    result = await agent.run(message, deps=deps)
    # ... verify reply; derive business outcome ...
except Exception:
    execution_ok = False
finally:
    await memory.reasoning.complete_trace(
        trace.id, outcome=TraceOutcome(
            success=execution_ok and not rejected,
            summary=reply,
        ),
    )
```

Open the trace before the model runs.

The real helper completes it in finally, including execution exceptions.

A policy decline differs from an execution error.

Presenter context: Imports: TraceOutcome from neo4j_agent_memory.schema.models and json. Condensed lifecycle across agent.py and finish_execution in reasoning.py. execution_ok, rejected and reply are initialized before this block; the full app also verifies the reply or supplies a safe failure reply. The full success predicate also requires recording_error is None and the actual summary is JSON with exact reply, execution_status and business_status. The full outcome includes error_kind, warnings, related entity references and metrics. It preserves the exact verified reply. Start_trace runs before account reads, message storage and model execution; actual code catches execution failure and still invokes the completion helper. This is an auditable execution record, not exposed hidden chain of thought.

## Attach observations and provenance

Module 4 · Code · Source: `module_4/app/reasoning.py`

```python
await memory.reasoning.link_trace_to_message(
    trace.id, str(user.id)
)
step = await memory.reasoning.add_step(
    trace.id, action=call["name"],
    observation=json.dumps(call["output"]),
    generate_embedding=False,
)
await memory.reasoning.record_tool_call(
    step.id, call["name"], arguments=call["input"],
    result={"value": call["output"],
            "executed_sql": call.get("sql")},
    message_id=str(user.id), touched_entities=refs,
)
```

INITIATED_BY points to the user message.

TOUCHED links a step to explicit Customer / Plan entity references.

Record executed SQL, including rejected requests without an INSERT.

Presenter context: Loop body from finish_execution; user aliases its message parameter. refs is a list of EntityRef(id=str(entity.id)) built from the explicitly selected SQL billing case Customer and Plan, not guessed from model prose. The real call also records rounded duration_ms. SDK relationships are ReasoningTrace HAS_STEP ReasoningStep USES_TOOL ToolCall INSTANCE_OF Tool; tool calls may TRIGGERED_BY Message. The model does not choose these provenance links. Server validation calls are labeled separately from model-selected tools.

## Retrieve a procedure, then prime the agent

Module 4 · Code · Source: `module_4/app/reasoning.py; module_4/app/agent.py`

```python
examples, evidence = await reasoning_examples(
    memory, message, embedder, namespace
)
instructions += "\nPast executions:\n" + examples
result = await agent.run(
    message, deps=deps, instructions=instructions
)
# Inside the local reasoning_examples helper:
trace = await memory.reasoning.get_trace_with_steps(
    UUID(row["id"])
)
```

The local query selects task embeddings within the intended namespace.

The SDK returns the trace and its actual steps/tool observations.

Examples guide the agent; current SQL policy governs action.

Presenter context: Imports: UUID from uuid. reasoning_examples is repository code, not a MemoryClient method. It embeds the task, queries scoped ReasoningTrace.task_embedding with cosine similarity, fetches up to three full traces through get_trace_with_steps, and serializes task, success, parsed outcome, actions, observations and tool arguments/results. Evidence includes trace IDs. The code shown splits call site and helper for one slide; the final SDK call runs inside the helper before the prompt is assembled. The controlled ablation disables extraction, hydration and recording in both branches, using separate messages and a frozen corpus.

## Turn hosted experience into a skill file

Module 5 · Repository workflow · Source: `module_5/workflows/distill.py`

```python
bearer_token = f"Bearer {settings.nams_api_key}"
async with httpx.AsyncClient(
    base_url=settings.nams_base_url,
    headers={"Authorization": bearer_token},
) as http:
    response = await http.post(
        "/v1/skills/generate",
        json={
            "name": "acme-refund-procedure",
            "scope": {"taskContains": "Refund"},
        },
    )
    response.raise_for_status()
```

This repository uses hosted REST for distillation.

The full workflow polls, publishes and downloads SKILL.md.

The hosted workspace is explicitly seeded; Bolt data is not migrated automatically.

Presenter context: Imports: httpx and AppSettings/get_settings. This is the REST transport used by the repository, not a fabricated MemoryClient.skills API. Existing module-5 workflows/check.py and seed.py verify/setup the hosted workspace; distill.py then generates, polls with a bounded timeout, publishes and downloads artifacts/distilled/SKILL.md. This edit validates code against the current repository only; no hosted NAMS endpoint was invoked. Hosted APIs are early access; use the configured-workspace rehearsal before delivery. The next slide shows the concrete PydanticAI consumption seam.

## Give the skill to a fresh PydanticAI agent

Module 5 · Code · Source: `module_5/app/fresh_agent.py`

```python
skill = load_skill("on")  # downloaded SKILL.md
instructions = BASE_INSTRUCTIONS
instructions += "\n\n## Distilled procedure\n" + skill
agent = Agent(
    f"openai:{settings.openai_model}",
    deps_type=ToolDeps,
    tools=list(SQLITE_TOOLS),
    instructions=instructions,
    output_type=str,
)
result = await agent.run(TICKET, deps=deps)
```

load_skill is a local file helper.

The fresh agent receives a portable procedure in its instructions.

It has business tools, with explicit case authorization, and no memory lookup tools.

Presenter context: Imports: Agent from pydantic_ai; local BASE_INSTRUCTIONS, SQLITE_TOOLS and ToolDeps. create_fresh_agent in fresh_agent.py constructs exactly this kind of agent; run_fresh_agent supplies Ravi’s explicit account, billing case and per-turn authorization in ToolDeps. load_skill("on") requires the downloaded artifact; "fallback" explicitly selects the pre-distilled fixture and "off" is the control. No MemoryClient or search_memory is installed on this fresh agent: organizational learning crosses the boundary as Markdown instructions. SQL guards still determine whether any action can execute.

