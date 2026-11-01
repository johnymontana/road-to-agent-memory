# Module 5 — Skill Distillation on NAMS

Code-reading map: [module_5/README.md](../../module_5/README.md). Start with
[`module_5/app/agent.py`](../../module_5/app/agent.py); the full agent is local to this lesson.


The payoff: turn one agent's accumulated experience into a portable, versioned
*skill* — then hand it to a fresh agent that has never seen any of the history, and
watch it resolve the ticket cold.

**The seam, made explicit:** your memory from modules 1–4 lives in *your* AuraDB over
the Bolt backend. NAMS is a separate, hosted, managed workspace — `make nams-seed`
loads the canonical history into it. You're not moving your graph; you're seeding a
fresh one.

## What you'll learn

- What NAMS is, and how a hosted memory workspace differs from your own Bolt-backed AuraDB.
- How skill distillation turns many similar traces into a step-by-step SKILL.md with evidence links.
- What grounding and coverage scores tell you about whether to trust a distilled skill.
- The governance loop: how drift is detected when the memory under a skill changes — and its honest blind spot.

## Run it

| Command | What it does |
|---|---|
| `make nams-check` | Verifies your `nams_` API key and workspace are reachable (you created both in pre-work). |
| `make nams-seed` | Seeds your NAMS workspace with the canonical reasoning memory (~1 min) — the refund-procedure history, in realistic agent-loop order. |
| `make nams-distill` | Triggers skill distillation over the accumulated refund-procedure memory. |
| `make s5-fresh-agent` | **The payoff:** a fresh agent — no session history, no prior traces — loads the distilled skill and resolves the refund ticket cold. |
| `make policy-change` | Flips the refund limit in SQLite (the system of record) — watch governance flag *nothing*. |
| `make nams-drift` | Retires the refund policy by deleting its entity from workspace memory — now the skill's evidence links break and drift is flagged. |
| `make nams-redistill` | Re-distills the skill against the current memory, closing the governance loop. |

## Explore

**Core**

1. Open the distilled SKILL.md. Which steps correspond to which observed tool calls? Follow a `GROUNDED_IN` edge from a claim back to its evidence.
2. What do the grounding and coverage scores tell you? What would a low-grounding step mean, and would you trust it?

**Instructor-led**

3. **The drift beat, made concrete:** first `make policy-change` (flips the refund limit in SQLite — the system of record) — what does governance flag? *(Nothing: it watches the memory graph, not your database — the honest boundary.)* Then `make nams-drift` (ops retires the refund policy — the policy **entity is deleted** from the workspace memory): the skill's `GROUNDED_IN` claims lose their source nodes. What does the governance loop flag now? What happens on re-distillation (`make nams-redistill`)? *Stretch variant: instead of deleting the entity, mark a grounding `issue_refund` tool call as failed — same governance view, different provenance story.*

**Stretch**

4. How is a distilled skill different from a hand-written runbook? From a raw trace? What does each optimize for?
5. Who else could load this skill? What does it mean that procedural knowledge is now a portable, versioned artifact rather than trapped in one workspace?
6. Full-circle: which of the three memory types did distillation draw on for this skill? And which store changed in the drift beat — SQLite or Neo4j? Why?

## Answer key

1. Each SKILL.md step maps to a tool-call pattern that recurred across the seeded traces — "look up the account" from `lookup_account` calls, "validate against policy" from `fetch_policy("refund")`, "issue the refund" from `issue_refund`. A `GROUNDED_IN` edge runs from each step/claim node back to the exact traces, tool calls, and entities it was distilled from — every claim has receipts.
2. Grounding measures how much of the skill is backed by evidence edges; coverage measures how much of the evidence the skill actually used. A low-grounding step is an unsupported claim — treat it as a hypothesis to review, not a procedure to run. High grounding with high coverage is what makes a distilled skill trustworthy enough to hand to a fresh agent.
3. `make policy-change` flags **nothing** — governance watches the memory graph, not your database, and that's the honest boundary of the system. `make nams-drift` deletes the refund-policy entity, so the skill's `GROUNDED_IN` claims lose their source nodes — and now drift is flagged: the skill's evidence has gone stale. `make nams-redistill` regenerates the skill against the current memory, producing a new version whose claims are grounded again.
4. A hand-written runbook is authoritative but stale-prone and expensive to maintain; a raw trace is complete evidence but not reusable as instructions. A distilled skill is generated from real executions — fresher than a runbook, more actionable than a trace — and it's versioned, so changes are explicit.
5. Any agent that can read the workspace (or the exported SKILL.md) can load it: a fresh agent, a teammate's agent, a different product's support bot. Procedural knowledge stops being trapped in one agent's chat history and becomes a portable, versioned artifact — one agent's Tuesday becomes everyone's Tuesday.
6. Distillation drew mainly on reasoning memory (the traces and tool calls), plus the long-term entities those traces touched. In the drift beat, *both* stores changed at different steps: SQLite for `make policy-change` (invisible to governance), and the Neo4j/NAMS memory graph for `make nams-drift` (which fired the signal) — because governance watches memory, not systems of record.

## If you fell behind

From the repo root, run:

```
make module-5
```

That replays this module's beats in order (check, seed, distill and fresh-agent payoff) and reproduces the room's current state. If your dev server is still
running an older stage, stop it first with `Ctrl+C`, then restart with
`make dev MODULE=5`. If NAMS itself is unreachable, ask a helper for the fallback path
(`make s5-fresh-agent WITH_SKILL=fallback` loads the pre-distilled skill from `artifacts/pre-distilled-skill/`).

## Glossary

- [Skill distillation](../glossary.md#skill-distillation) · [Grounding score](../glossary.md#grounding-score) · [Coverage score](../glossary.md#coverage-score) · [NAMS](../glossary.md#nams) · [Bolt backend](../glossary.md#bolt-backend)
