# Running the app (every module)

These notes apply to every module. Each module README covers only what that
stage adds.

## Two terminals

Run every command from the **repository root**.

```bash
make dev MODULE=N        # terminal 1: backend :8000 (module N) + frontend :5173
make <scenario>          # terminal 2: the module's scenario beats
```

To switch modules, stop the server with Ctrl+C, run `make dev MODULE=N` with the
new number, and reload the browser. Every module shares the root `.env`, the
SQLite database, the virtual environment and your AuraDB.

## Browser chat and terminal scenarios

- Browser chat shows its conversation ID and has **New conversation** and
  **Resume** controls. Turn history is kept in browser storage across reloads;
  Neo4j memory persists either way.
- Terminal scenarios (`make s2-return`, ...) print their own dialogue, tool calls
  and timing. They do not add turns to the browser chat.
- To inspect a terminal run, click **Refresh graph → Saved replay** for its saved
  output, or **Live memory** for the Neo4j nodes it wrote. Choose **Current
  conversation** for browser evidence, or **All stored memory** to see everything.

## Refunds are guarded

A refund needs a selected **Customer**, a selected **Billing case**, and
**Authorize selected refund for this message**. Authorization resets after each
turn. The server re-checks the case identity, the amount, the current SQL plan
limit and that the incident was not already refunded (see `app/guardrails.py`
in any module). Asking for an update reads refund history instead of refunding.
Retrying a request ID returns its saved receipt, so a retry never refunds twice.
There is no escalation tool. Service status values are seeded examples with
timestamps, not a live monitoring feed.

## Evaluation

Run `make eval MODULE=N`, or start an evaluation from the UI. Opening the
evaluation panel only reads saved results. Each run uses a private SQLite copy,
unique memory fixtures and no business tools, and checks exact facts and source
IDs. It is a controlled retrieval probe, not an end-to-end support-quality score.
If a dependency fails, the questions completed so far are kept.
