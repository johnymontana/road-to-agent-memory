# Module 5 — Build a portable skill from agent memory

In the first four modules you met the support agent, accumulated conversation and entity memory, and recorded tool executions. A distillation run can use selected evidence to derive a reusable procedure. A fresh PydanticAI agent can load that procedure and bring its own tools, permissions and current SQLite policy.

The support app continues to use your Bolt/AuraDB memory. A separate hosted NAMS workspace holds the authored workshop fixtures, skill versions and their evidence links. The workflow uses the NAMS HTTP API. Start with the [module code map](../../module_5/README.md).

## Before class

Sign in to the [NAMS console](https://memory.neo4jlabs.com/) and select Sign up if you need a Neo4j account. In the [API Keys dashboard](https://memory.neo4jlabs.com/dashboard/api-keys), choose the workshop workspace and create a workspace-bound data key. Keep the value private in a personal Codespaces secret or your local `.env`. The service origin is `https://memory.neo4jlabs.com`. The [pre-work guide](../prework-email.md) distinguishes private configuration from terminal commands.

Run `make nams-check`. It reads workspace reachability and then checks whether distillation is enabled. It exits successfully only with confirmed distillation and prints the publish thresholds. It then reads the workspace's active ontology, because a custom ontology from another project can reject the workshop seed with HTTP 422, and reports whether a package already in `artifacts/distilled/` belongs to this workspace. If the check fails, follow its fallback command or switch to a workshop workspace without a custom ontology. Stop pre-work here. Seeding, generating and publishing are workshop actions.

## Choose your route

In terminal 1, stop the prior server with Ctrl+C, run `make dev MODULE=5`, reload port 5173 and confirm the **Module 5** badge. Use terminal 2 for the following commands. Both consumer modes need the normal model and seeded SQLite environment.

| What you have | Do this | What you can inspect |
|---|---|---|
| Hosted capability and an existing downloaded package | Open the package directly and run the off/on comparison below. | Local procedure, references, provenance and receipt. A valid key for the same workspace enables hosted graph inspection. |
| Hosted capability, starting fresh | Once in your designated workshop workspace, run the two hosted write commands below. | The seed state, generation status and downloaded package. |
| Hosted access unavailable, capabilities disabled, generation failed, or **no downloaded package by capstone minute five** | Compare off and fallback. Record both rows, then go to the wrap (Google Slides 75 → 82, repo slides [62](../../slides/deck.html#62) → [69](../../slides/deck.html#69)). | The checked-in SKILL.md and your consumer output. Hosted graph, provenance and drift exercises require the hosted route. |

In Google’s HTML view, use browser Find for the comparison or scorecard title when a slide link opens at the start of the deck. These links open the destinations directly in presentation mode. [Slide 75 · Compare a fresh agent on Ravi’s $49 case](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8/present?slide=id.ram_design_049) · [Slide 82 · The controlled retrieval scorecard](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8/present?slide=id.ram_design_054)

### Hosted writes

```bash
make nams-seed
make nams-distill
```

The seed assigns a fresh user ID to five entities and one four-message conversation. The entities represent Maya, Northwind, Compute, Pro and the Acme Cloud Refund Policy. Two completed traces each record three tool steps. The receipt in `DATA_DIR/nams-workspace.json` records `userId`, `policyEntityId`, `conversationId` and `traceIds`. Each seed starts a new run. Generation and re-distillation require the saved `conversationId`. If it is missing, the command stops before sending a generation request. Use the checked-in comparison or seed once in the designated workshop workspace.

The generator uses the saved conversation, polls the run, automatically approves a successful version, publishes, and downloads a ZIP into `artifacts/distilled/`. A matching named skill receives a new version. The local receipt `skill.json` records the skill, version, run and conversation IDs. `make module-5` is a **full hosted replay** that checks, seeds, generates/publishes and runs the consumer. To catch up with an existing package, proceed directly to inspection. When using fallback, go directly to the comparison.

### Compare a fresh agent

**With a downloaded package**

```bash
make s5-fresh-agent WITH_SKILL=off
make s5-fresh-agent WITH_SKILL=on
```

**With the checked-in procedure**

```bash
make s5-fresh-agent WITH_SKILL=off
make s5-fresh-agent WITH_SKILL=fallback
```

Both calls use the same Ravi $49 duplicate Compute charge, an authorized incident, the same business tools and a fresh private SQL copy. The procedure is supplied as instructions in on or fallback mode. The CLI prints the model reply, ordered tool names and a status where the tool returned one.

| Mode used | Ordered tool names | Visible returned status | Does the reply agree? |
|---|---|---|---|
| off | | | |
| on **or** fallback | | | |

A matching pair of outcomes is a valid result. State which procedure the consumer received and which operation you actually observed. The experiment shows how to transfer an instruction artifact between agents on a similar case. A different case or a policy threshold test requires a separate comparison. **Fallback participants finish here and join the wrap.**

## Explore the hosted artifact

1. Open `artifacts/distilled/SKILL.md` and choose one procedure step. Find a supporting ID in the downloaded `provenance.json`. Look under both `claims` and `steps`. The package also includes `references/`. The fresh consumer reads only SKILL.md.
2. In the Module 5 browser, tick **NAMS**. Follow **Skill → HAS_VERSION → SkillVersion → HAS_STEP → SkillStep → GROUNDED_IN → source evidence**. Look for a source entity, agent step or tool call. A newer version can point to its predecessor with SUPERSEDES. Claim entries live in the provenance JSON.
3. Compare generated grounding and coverage scores with one actual link and the procedure text. What supports that step? Which condition was absent from the two similar successful seed traces? Document what a denied or unauthorized case would need to establish in a separate test. Scores help prioritize review. The receiving app’s SQL policy and authorization govern actions.

## Instructor extension — provenance and drift

Participants observe the instructor using a **disposable workshop workspace**. Use a seed and downloaded package from the same run. Confirm the version is still published. Compare the seed’s explicit `policyEntityId` with the package’s `groundedIn` IDs. NAMS can extract additional records named Acme Cloud Refund Policy under that same seed user; a claim or step may cite one of those IDs. The [drift workflow](../../module_5/workflows/drift.py) can delete only exact-name policy records in that seed user’s scope whose IDs the version cites. It first verifies the original policy and hosted conversation. If the evidence or receipts do not match, record the explanation and skip the deletion. An older package can still supply SKILL.md for the consumer comparison.

1. Establish the starting SQL Pro limit using the current policy lookup or SQL row. If it is $250, run `make policy-change` and read the printed **$250 → $150** transition. The lowering path requests drift for the downloaded version when its receipt includes skillId and versionId and the hosted key is available. A legacy or missing version receipt leaves the observation SQL-only. Record the status actually returned. If you start at $150, the demonstration is already in its lowered state.
2. In the verified disposable workspace, run `make nams-drift` once. Record each deleted policy ID and type printed by the command, the current skill’s status, and the stale claims and steps. The report fields are `status`, `staleClaims` and `staleSteps`. Use the downloaded provenance and graph to look up supporting IDs. If nothing is eligible, record the command’s explanation. An SQL policy change and a deleted hosted source are independent events.
3. If time and evidence permit, run `make nams-redistill`. Inspect the new version, SKILL.md diff and evidence IDs. A new version reflects the selected memory. SQLite is the authority for the current limit.
4. Check the current SQL limit. If it is $150, run `make policy-change` once and verify the printed **$150 → $250** restoration. If already $250, stop. This restores the workshop’s SQL default. A deleted hosted policy stays deleted.

**November 4 rehearsal.** Changing SQLite alone left the hosted version current. NAMS cited two same-name policy records in this run, one Object and one Concept. After their deletion, the first version reported two of five claims and one of three steps stale. The new version received full grounding and coverage scores and still referred to $250 while local SQL held $150. Inspect your own package and status.

**Interpretation.** The $49 consumer case is below both $250 and $150. Use the printed SQL change to show the policy edit and the actual NAMS response to show hosted drift. A separate authorized Pro duplicate charge strictly between the two amounts would distinguish policy enforcement. That would be a new fixture.

Finish the wrap and make the keep-or-clean-up decision before following [teardown](../teardown.md). Detailed code, including seed, review, publish and drift payloads, is in the [Module 5 implementation](../../module_5/README.md).
