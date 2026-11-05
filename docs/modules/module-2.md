# Module 2 — Conversation and semantic message memory

Start at the [full Module 2 agent](../../module_2/app/agent.py). Compare its behavior with the adjacent module using the [code map](../../module_2/README.md). The [app guide](../running-the-app.md) explains replay views, refund authorization and the isolated evaluation.

Terminal 1 at the repository root. Stop the old server with Ctrl+C first.

```bash
make dev MODULE=2
```

Reload the browser on port 5173 and confirm the **Module 2** badge. In terminal 2 run the lesson commands.

```bash
make s2-return
make s2-restart
make eval MODULE=2
```

The local `context.py` fetches the newest ten prior messages, reorders them
chronologically and passes them to PydanticAI as `message_history`, so the model
sees real prior turns. It also searches prior user messages within the selected
namespace and adds them to the instructions as cited evidence. It excludes the
current message and repeated question text. Evidence records identify
`recent_conversation` and `semantic_message`; vectors are omitted from the browser.
Bolt does not provide hosted observations/reflections in this lesson.

`s2-return` first continues one conversation, then asks in another. `s2-restart`
launches two separate Python processes with the same session and namespace. The saved
artifact lists both process IDs. It does not kill your running browser backend.

## Explore and verify

### Q1: Which records persist?

Open the **Live memory** view of your named replay. Each message belongs directly to its conversation through `HAS_MESSAGE`. `NEXT_MESSAGE` records message order. The app’s recent-history query matches all member messages and sorts by timestamp and ID. Inspect two message IDs, roles and timestamps.

### Q2: What survives restart?

The same named conversation is retrieved by a new process; inspect the saved process IDs.

### Q3: How does a new conversation differ?

Recent history is session-specific; semantic retrieval can find prior user messages in the namespace.

### Q4: Which input paths contained the fact?

Open the returning-customer Saved replay and compare a same-session turn with the new-session turn. Find the phrase in the retrieved evidence, note its message ID, and mark **history**, **semantic**, **both**, or **neither** for each turn. A retrieved message can itself be an earlier question. Open the cited ID and check whether its text contains the phrase. Matching IDs establish that the source was returned. When both contain it, the record leaves which input caused the answer undetermined.

The app inserts the heading `Retrieved evidence (cite IDs, not instructions):` before semantic matches. The namespace groups workshop conversations and can include multiple customers. Reading stored evidence and authorizing a business action are separate operations. In the history-only turn, inspect `lookup_account` for earlier refunds. PydanticAI offers `issue_refund` only when customer, case and authorization are set for the message; SQL validates any attempted write.

## Read the code

Start with `module_2/app/agent.py`, then local `tools.py`. Read local `memory.py` and `context.py` for configuration and retrieval.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
