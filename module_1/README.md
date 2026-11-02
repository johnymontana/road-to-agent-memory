# Module 1 — Per-turn stateless baseline

Start commands from the repository root. Keep `make dev MODULE=1` in one
terminal and run the lesson commands in another. Before switching modules, stop
the server with Ctrl+C, launch the next module, and reload the browser.

Browser chat has a visible conversation ID, New conversation and Resume controls.
It preserves turn history locally across reloads; clearing browser storage removes
that local history. Neo4j memory remains persistent. Terminal commands print their
own dialogue, tools and timing. Use **Refresh graph → Saved replay** to inspect their
immutable output projection; choose **Live memory** for the replay's persisted
Neo4j message/entity/trace links. CLI runs do not append turns to browser chat. Choose Current
conversation for browser evidence, or All stored memory deliberately.

Refund actions require a selected Customer and Billing case plus **Authorize selected
refund for this message**. Confirmation resets after each turn. The server checks
case identity, amount, current SQL plan limit and incident uniqueness. Asking for
an update reads refund history. A request ID returns its saved operation receipt on
retry; replaying a billing case cannot create a second refund. No escalation tool
exists. Status values are seeded examples with timestamps, never a live monitoring feed.

Run `make eval MODULE=1` explicitly. The evaluation lab starts only on POST/action;
opening or reopening it reads results. Each run uses private SQL, unique memory
fixtures and disabled business tools. Exact facts and source IDs are checked. This
is a controlled retrieval probe, not an end-to-end support-quality score or a promise
of monotonic improvement. A dependency error preserves completed questions.

```bash
make dev MODULE=1
# Second terminal:
make s1-baseline
make eval MODULE=1
```

Each `agent.run` starts without message history, even inside one visible browser
conversation. The first prompt includes Maya's exact email; the second explicitly
asks what was just supplied. It should report unknown. SQL tools can still retrieve
business facts when given an identifier; that is not memory.

See the [participant guide](../docs/modules/module-1.md) for the same questions and answer key.

## Explore and verify

### Q1: Which tool reads current account facts?

`lookup_account` executes SQL; inspect its actual statements and source data.

### Q2: Why is the second answer unknown?

No message history is passed to the next model call. The browser bubbles are not model memory.

## Read the code

Start with `module_1/app/agent.py`, then local `tools.py`.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
