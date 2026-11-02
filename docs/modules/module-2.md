# Module 2 — Conversation and semantic message memory

Start commands from the repository root. Keep `make dev MODULE=2` in one
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

Run `make eval MODULE=2` explicitly. The evaluation lab starts only on POST/action;
opening or reopening it reads results. Each run uses private SQL, unique memory
fixtures and disabled business tools. Exact facts and source IDs are checked. This
is a controlled retrieval probe, not an end-to-end support-quality score or a promise
of monotonic improvement. A dependency error preserves completed questions.

```bash
make dev MODULE=2
# Second terminal:
make s2-return
make s2-restart
make eval MODULE=2
```

The local `context.py` fetches the newest ten prior messages, reorders them
chronologically, and searches prior user statements within the selected namespace.
It excludes the current message and repeated question text. Evidence records identify
`recent_conversation` and `semantic_message`; vectors are omitted from the browser.
Bolt does not provide hosted observations/reflections in this lesson.

`s2-return` first continues one conversation, then asks in another. `s2-restart`
launches two separate Python processes with the same session and namespace. The saved
artifact lists both process IDs. It does not kill your running browser backend.

## Explore and verify

### Q1: Which records persist?

Conversation HAS_MESSAGE Message, plus message ordering links. Inspect IDs and timestamps.

### Q2: What survives restart?

The same named conversation is retrieved by a new process; inspect the saved process IDs.

### Q3: How does a new conversation differ?

Recent history is session-specific; semantic retrieval can find prior user messages in the namespace.

### Q4: Which search path answered?

Inspect recent_conversation versus semantic_message evidence IDs. Paraphrases need semantic similarity; empty evidence is visible.

## Read the code

Start with `module_2/app/agent.py`, then local `tools.py`. Read local `memory.py` and `context.py` for configuration and retrieval.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
