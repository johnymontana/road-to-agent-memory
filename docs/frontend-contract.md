# Frontend ↔ Backend API Contract

The shared frontend (`web/`) talks to whichever module backend is running
(`make dev MODULE=N`, default 1). Backend serves on **:8000**, Vite dev server on
**:5173** (proxy `/api` → `:8000`).

All responses JSON. The frontend never holds secrets; NAMS calls are proxied
through the backend (`/api/graph/nams`), never called directly from the browser.

## Endpoints

### `GET /api/health`
```json
{ "status": "ok", "module": 3, "memory_layers": ["short_term", "long_term"] }
```
`memory_layers` lists which layers are active in the running module (drives UI badges).

### `POST /api/chat`
Request: `{ "message": "string", "session_id": "string | null" }`

Response:
```json
{
  "reply": "string",
  "session_id": "string",
  "tool_calls": [
    { "name": "lookup_account", "input": {"customer_email": "..."}, "output": {...}, "sql": "SELECT ...", "duration_ms": 12 }
  ],
  "context": { "used_memory": true, "summary": "what was injected (short-term/long-term/reasoning), null in module 1" }
}
```
`sql` is the actual parameterized SQL string the tool executed (trace panel shows it).

### `GET /api/graph`
Graph state from the attendee's AuraDB (Bolt side), mapped for NVL:
```json
{
  "nodes": [ { "id": "string", "labels": ["Message"], "properties": { "content": "...", "...": "..." } } ],
  "relationships": [ { "id": "string", "from": "nodeId", "to": "nodeId", "type": "MENTIONS", "properties": {} } ]
}
```
Query params: `?layer=all|short_term|long_term|reasoning` (default `all`).

### `GET /api/graph/nams`  (module 5 only)
Same NVL shape, sourced from the NAMS workspace via REST (skill subgraph incl.
`Skill`/`SkillVersion`/`SkillStep` nodes and `GROUNDED_IN` edges). Returns
`{ "nodes": [], "relationships": [], "unavailable": true }` when NAMS is not configured.

### `GET /api/eval`
Runs the continuity eval-question set against the current agent; returns:
```json
{ "questions": [ { "id": "q1", "question": "...", "expected_from_module": 2, "answered": true, "answer": "..." } ] }
```

## Conventions
- Node `labels` drive graph-panel coloring via the memory-type palette:
  short-term (Conversation/Message) `#B2F2BB` / long-term (Entity*) `#FFEC99` /
  reasoning (ReasoningTrace/ReasoningStep/ToolCall) `#D0BFFF` / skills (Skill*) `#6366F1`.
- Chat is synchronous request/response (no websockets in v1); the trace panel renders
  `tool_calls` from the latest response; the graph panel refetches after each reply.
