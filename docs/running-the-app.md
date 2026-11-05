# Running the app (every module)

These notes apply to every module. Each module README covers only what that
stage adds.

## Two terminals

Run every command from the **repository root**.

To enter Module 2, press Ctrl+C in terminal 1. Start the new backend from the same terminal.

```bash
make dev MODULE=2
```

Leave terminal 1 running. Reload port 5173 and confirm the **Module 2** badge. The same frontend uses the agent served on port 8000. A scenario launches its own module, so a successful terminal run can coexist with an older browser backend.

Run the returning-customer scenario in terminal 2 at the repository root.

```bash
make s2-return
```

Use the corresponding module number, badge and named scenario at each transition. Each module shares the root configuration, SQLite data and workshop AuraDB.

## Browser chat and terminal scenarios

- Browser chat shows its conversation ID and has **New conversation** and
  **Resume** controls. Turn history is kept in browser storage across reloads;
  Neo4j memory persists either way.
- Terminal scenarios (`make s2-return`, ...) print their own dialogue, tool calls
  and timing. They do not add turns to the browser chat.
- For keyboard inspection, open **Inspect nodes by keyboard** in the graph panel. Choose a node to read its labels and properties in the details drawer. Each module guide gives the corresponding graph paths in text.
- To inspect a terminal run, click **Refresh graph → Saved replay** for its saved
  output. Expand a turn under **Execution evidence · Saved replay** for the original prompt, reply, tools, SQL and retrieved evidence. Fixed-transcript extractor runs show the transcript hash and snapshot nodes. For the Neo4j nodes written by memory-enabled scenarios, choose **Live memory**. Choose **Current
  conversation** for browser evidence, or **All stored memory** to see everything.

## Refunds are guarded

A refund needs a selected **Customer**, a selected **Billing case**, and
**Authorize selected refund for this message**. Authorization resets after each turn. PydanticAI’s `prepare_refund` offers `issue_refund` to the model only when all three controls are set. A history question can use `lookup_account` to read earlier refunds. The server re-checks the case identity, the amount, the current SQL plan
limit and that the incident was not already refunded (see `app/guardrails.py`
in any module). Asking for an update reads refund history instead of refunding.
Retrying a request ID returns its saved receipt, so a retry never refunds twice.
There is no escalation tool. Service status values are seeded examples with
timestamps, not a live monitoring feed.

## Evaluation

Run `make eval MODULE=N` with the current module number, or start an isolated evaluation from the UI. Opening the evaluation panel reads saved results. Runs use private SQL data, unique memory fixtures and disabled business tools. A dependency failure preserves completed questions.

| Probe | What is graded | Accepted source |
|---|---|---|
| Named customer lookup | The question supplies the name. Return that exact name and email. | Seeded message or entity ID |
| Conversation phrase | Exact verification phrase from the conversation | Seeded user message ID |
| Account fact | SQL-grounded signup date | Grounded entity ID |
| Prior decision quote | Exact refusal quote from an earlier recorded decision | Trace ID |

A passing response supplies all expected fields (case-folded and whitespace-trimmed) and at least one accepted ID. For example, a correct phrase with the corresponding seeded message ID passes. The same phrase with only an unrelated ID fails the source check. Additional IDs do not all have to be correct for this grader. Read the checks for each probe before interpreting the total. Customer authentication, current refund safety and general procedure execution require separate evidence. [Evaluator](../scripts/eval.py).
