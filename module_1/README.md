# Module 1 — The stateless agent

**The idea:** every call to the model starts from nothing. SupportBot is a
PydanticAI agent with five SQL-backed tools and no memory. Tell it your email,
then ask what you just told it: it cannot say.

## Read the code

1. [`app/agent.py`](app/agent.py): the agent and one chat turn. The key line
   is `self.agent.run(message, ...)` with only the new message, and no history.
2. [`app/tools.py`](app/tools.py): five business tools as plain PydanticAI tool
   functions (`RunContext[ToolDeps]`, docstring = tool description).
3. [`app/guardrails.py`](app/guardrails.py) *(skim)*: refund and reply safety
   checks. It is the same in every module and is not about memory.

`app/main.py` plugs the agent into the shared HTTP server (`lib/app_factory.py`).

## Run it

```bash
make dev MODULE=1
# Second terminal:
make s1-baseline
make eval MODULE=1
```

`s1-baseline` sends Maya's exact email in the first message, then asks what was
just supplied. The agent should say it does not know. SQL tools can still look
up business facts when given an identifier, but that is lookup, not memory.

General app notes (browser vs terminal runs, refunds, evaluation) are in
[docs/running-the-app.md](../docs/running-the-app.md). Questions and answers:
[participant guide](../docs/modules/module-1.md).

## Explore and verify

### Q1: Which tool reads current account facts?

`lookup_account` executes SQL; inspect its actual statements and source data in the trace panel.

### Q2: Why is the second answer unknown?

No message history is passed to the next model call. The browser's chat bubbles are not model memory.
