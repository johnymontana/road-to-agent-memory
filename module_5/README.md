# Module 5 — Skill distillation with NAMS

The support app retains the Module 4 agent and its Bolt/AuraDB memory. A separate workflow builds a portable skill on top of selected memory in the hosted Neo4j Agent Memory Service (NAMS). A fresh PydanticAI agent reads the exported procedure into its instructions, then uses its own SQL business tools to handle a similar case.

## Read the code

1. Start at the module-local [support agent](app/agent.py). Compare the support app and the [fresh consumer](app/fresh_agent.py). The consumer’s inputs are its base instructions, the chosen skill mode, an authorized Ravi incident and a private SQLite copy.
2. Follow the [seed workflow](workflows/seed.py). Each run gets a fresh `userId`. It writes five entities (including the Acme Cloud Refund Policy), four messages in one conversation, and two completed traces with steps and tool calls. The seed receipt records the user, policy entity, conversation and trace IDs.
3. Read the [generation and publication workflow](workflows/distill.py). Both initial generation and re-distillation require the conversation ID from the seed receipt. A missing ID stops the command before it contacts NAMS. Use the checked-in skill or seed once in the designated workshop workspace. It polls every five seconds with a 600-second timeout, approves a successful version, publishes and downloads the ZIP. The procedure, references and provenance are under `artifacts/distilled/`. It stages the download, verifies its SKILL.md and run provenance, then installs the version’s package and local `skill.json` receipt together. A repeat can publish a new version of the same named skill.
4. Read the [drift workflow](workflows/drift.py). It gathers `groundedIn` IDs from the downloaded claims and steps, checks them against this run’s seed and published version, and deletes only cited, exact-name refund-policy records in the seed user’s scope. These may include extracted policy records with IDs different from the explicit seed policy. Inspect the returned drift report. If the checks fail, the workflow reports why it skipped deletion.
5. The [shared HTTP client and file helpers](workflows/nams.py) support the NAMS REST calls. The [readiness workflow](workflows/check.py) reads the workspace, the distillation capability, whether the active ontology accepts the seed's plain entities, and whether the downloaded package belongs to this workspace. [Hosted API contract](https://memory.neo4jlabs.com/openapi.json).

## Run the workshop comparison

In terminal 1, stop the prior server, run `make dev MODULE=5`, reload port 5173 and confirm the **Module 5** badge. In terminal 2 follow the [participant guide](../docs/modules/module-5.md) for pre-work, hosted writes, the minute-five decision and the instructor-only governance extension.

| Ready at capstone minute five | Terminal 2 comparison | What to collect |
|---|---|---|
| Downloaded package from the intended workspace | `make s5-fresh-agent WITH_SKILL=off`, then `make s5-fresh-agent WITH_SKILL=on` | Reply, ordered tool names and printed statuses for Ravi’s $49 case. Open the package and compare one evidence ID. |
| No package ready or hosted capability unavailable | `make s5-fresh-agent WITH_SKILL=off`, then `make s5-fresh-agent WITH_SKILL=fallback` | Same output fields. Read the [checked-in procedure](../artifacts/pre-distilled-skill/SKILL.md), then go to the wrap. |

Only the hosted route can use the NAMS graph checkbox with the appropriate workspace and version. Follow **Skill → HAS_VERSION → SkillVersion → HAS_STEP → SkillStep → GROUNDED_IN → evidence**. Read claim records in `provenance.json`.

`make module-5` runs the whole hosted sequence (check, seed, generate/approve/publish and consume). Use a previously downloaded package directly for inspection or consumer comparison. See the [app guide](../docs/running-the-app.md) for the two-terminal workflow.
