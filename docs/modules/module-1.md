# Module 1 — Per-turn stateless baseline

Start at the [full Module 1 agent](../../module_1/app/agent.py). Compare its behavior with the adjacent module using the [code map](../../module_1/README.md). The [app guide](../running-the-app.md) explains replay views, refund authorization and the isolated evaluation.

Terminal 1 at the repository root. Start the app.

```bash
make dev MODULE=1
```

Reload the browser on port 5173 and confirm the **Module 1** badge. In terminal 2 run the lesson commands.

```bash
make s1-baseline
make eval MODULE=1
```

Each `agent.run` starts without message history, even inside one visible browser
conversation. The first prompt includes Maya's exact email; the second explicitly
asks what was just supplied. It should report unknown. SQL tools can still retrieve
business facts when given an identifier; that is not memory.

## Explore and verify

### Q1: Which tool reads current account facts?

Refresh the graph and choose **Saved replay · s1-baseline**. Open the first turn’s `lookup_account` entry and identify a SQL value returned for Maya. Compare the second turn’s reply with the first turn’s input. In the browser’s Current conversation, send both messages again and inspect those separate browser-turn records.

### Q2: Why is the second answer unknown?

No message history is passed to the next model call. The browser bubbles are not model memory.

Use `lookup_account` for refund history. To expose `issue_refund` to the model, select a customer and billing case and authorize that message. SQL checks the action again when the tool runs.

## Read the code

Start with `module_1/app/agent.py`, then local `tools.py`.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
