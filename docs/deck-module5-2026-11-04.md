# Module 5 deck refresh — 2026-11-04

The [native Google Slides deck](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8/edit) now contains 102 slides. Module 5 occupies slides 60–81: 22 slides covering concepts, NAMS pre-work, the current workflows, code, graph structure, evaluation and drift. Twelve native slides were added using existing Neo4j template layouts. All original 90 slide IDs are retained, with the Module 5 sequence reorganized around the current implementation.

Delivered revision: `MFho-EresCn7HA`. Source revision: `qG5M17j8fBPgPg`. The earlier NAMS payload mismatch documented in the resources review is resolved by the updated repository implementation and these slides. That earlier review remains a historical record.

## Teaching sequence

1. Introduce skill distillation as an application built on agent memory. Conversations, entities and execution traces supply evidence; a distillation run derives a reusable procedure with conditions and source links. This is neither a fourth memory store nor training model weights.
2. Explain the two environments. The Module 5 support app retains the module-local Bolt/AuraDB implementation. Separate HTTPX REST workflows seed authored fixtures into NAMS. They do not migrate participant AuraDB data.
3. Complete NAMS signup, workspace/API-key setup and capability checks as pre-work. The 20-minute module uses these slides as setup references rather than additional timed exercises.
4. Seed and inspect the small hosted corpus, complete the traces, and save the conversation scope for generation.
5. Generate a skill version, poll its run, approve and publish it, then inspect the downloaded ZIP and local receipt.
6. Read the versioned skill graph and quality signals. Evaluate the portable procedure with a fresh agent and current SQL tools.
7. Demonstrate provenance-driven hosted drift, distinguish it from a SQLite policy edit, then re-distill and inspect the new version.

Detailed code slides are marked as references. The main demo sequence remains `make nams-check`, `make dev MODULE=5`, then `make nams-seed` and `make nams-distill` in a second terminal, followed by fresh-agent comparisons and the instructor-led drift demonstration.

## Repository accuracy

| Area | Updated explanation |
| --- | --- |
| Seeding | Four explicit entities, one conversation with four messages, and two completed traces with three steps/tool calls each. Tool input/output is JSON-encoded text. Both traces connect to the first message. Entity upserts may merge; rerunning creates new conversations/traces. |
| Saved scope | `DATA_DIR/nams-workspace.json` records `conversationId` and `traceIds`. Generation normally selects that conversation; if the seed state is absent, the script warns and uses workspace scope. |
| Generation | The current payload uses `nameHint` and explicit `scope.type`. A matching named skill supplies `skillId` to generate a new version. Polling uses `started.runId`, checks terminal status and handles failure/timeout. |
| Approval | The workflow automatically submits `decision: "approve"` with feedback before publication. It is not a human review pause. The previous 409-retry description has been removed. |
| Artifacts | The ZIP contains `SKILL.md`, `references/` and `provenance.json`. Local `skill.json` records `skillId`, `versionId` and `runId`; it is a workflow receipt. |
| Fresh agent | Only `SKILL.md` is loaded into instructions. The consumer has its own SQL tools and private SQL copy, with no memory client, message history or retrieval. It does not automatically read the other package files. The refund tool checks current SQL policy. |
| Graph | `Skill → HAS_VERSION → SkillVersion → HAS_STEP → SkillStep → GROUNDED_IN → evidence`. A new version can `SUPERSEDES` a prior version. Claim records are represented in provenance JSON, not invented `SkillClaim` graph nodes. |
| Drift | Read `groundedIn` IDs from this package's claims and steps, fetch the entity subset, choose cited policy entities or a most-cited fallback, delete the actual entity IDs, and inspect this skill's drift status, `staleClaims` and `staleSteps`. The slides identify this as an instructor-led operation in a disposable workshop workspace. |
| Policy change | `make policy-change` toggles the SQL Pro limit between 250 and 150. This does not update hosted memory. Re-distillation creates a new version; it does not synchronize SQLite policy into NAMS. Restore the Pro limit after the demonstration. |
| Quality | Grounding and coverage are review signals. Intact source links or high scores do not establish correctness or guarantee transfer to a new execution environment. |

Five Module 5 code panels now match the current implementation:

- `module_5/workflows/seed.py`: complete traces and persist the conversation scope.
- `module_5/workflows/distill.py`: generate and poll; approve, publish and unpack the versioned package.
- `module_5/app/fresh_agent.py`: load the procedure into the fresh PydanticAI agent.
- `module_5/workflows/drift.py`: follow provenance to cited entity IDs and query drift.

Excerpts are explicitly condensed and their omitted surrounding checks are explained in speaker notes. All 17 deck code panels match the source walkthrough catalog and parse in an async context. Thirteen existing code excerpts were preserved; the old distillation excerpt was replaced and three new code excerpts were added.

## NAMS onboarding and references

New slides explain the public [NAMS console](https://memory.neo4jlabs.com/), Neo4j sign-in/sign-up, the default workspace, the [API Keys dashboard](https://memory.neo4jlabs.com/dashboard/api-keys), workspace-bound data keys, private configuration and capability checks. The public sign-in UI offers email and Google. First-login workspace/key provisioning and key expiry are grounded in the public service documentation. Workspace data keys are distinguished from broader administrative keys.

The setup panel shows a placeholder `NAMS_API_KEY`, the origin-only `NAMS_BASE_URL=https://memory.neo4jlabs.com`, and the terminal commands separately. It tells participants to read both reachability and distillation capability results: a successful process exit alone does not establish that hosted generation is enabled. `WITH_SKILL=fallback` is a consumption demonstration when hosted distillation is unavailable.

No account, API key or hosted data was created during this slide review. The authenticated key-creation form was not inspected, so the slides avoid unverified form/button details. No credential values were read or placed in the deck.

References link the [live API documentation](https://memory.neo4jlabs.com/docs), [public OpenAPI schema](https://memory.neo4jlabs.com/openapi.json), [skill concepts](https://neo4j.com/labs/agent-memory/explanation/skills/) and [Skills API](https://neo4j.com/labs/agent-memory/reference/skills-api/) beside the relevant concepts and snippets. The existing 15-slide resources appendix remains, now covering 49 unique resources. Every one of the 87 native instructional slides has references and an internal resources link.

## Visual design and source synchronization

The slides retain the Neo4j template's palette, typography, logo, motifs and layout language. Native circles represent graph records; boxes represent processing stages. The new memory-to-skill diagram connects all three memory types to evidence selection. The skill/version/step graph, governance loop, connected-memory recap and Bolt/NAMS boundary diagrams now match the code.

All additions are editable native shapes and text. The local mirrors include 18 SVG diagrams, 87 Marp sections (72 instructional and 15 resources), 19 technical walkthrough entries (17 code panels plus two concept entries), and 72 source reference blocks with 162 links. The source deck and rebuilt HTML have the same Module 5 sequence and explanations.

Current artifacts:

- [Marp source](../slides/deck.md) and [rendered HTML](../slides/deck.html)
- [Technical walkthroughs](../slides/technical-walkthroughs.md) and [structured snippets](../slides/technical-walkthroughs.json)
- [Resource catalog](../slides/resources.md) and [native/source mappings](../slides/resources.json)
- [Design record](../slides/visual-design.json) and [diagram mirrors](../slides/diagrams/README.md)
- [Final verification record](../slides/module5-verification.json)

## Verification and limits

- Final native readback verified the exact 102-slide order, 214 expected text fields, 32 updated speaker notes, all 17 code panels, 44 planned Module 5 reference links, all internal link targets and all 49 catalog resources in the appendix.
- Independent review confirmed all 87 native instructional reference mappings, including the twelve new slides. The versioned skill graph has seven circular record nodes.
- All 102 native slides were visually reviewed using Google Slides LARGE previews. The PDF export reference could not be materialized, so native previews were used. Two consolidated repair passes fixed setup-panel wrapping and one resource card's inherited text styling. Final previews were inspected; no unresolved visual defects remain.
- The structural checker reported zero errors. Its 84 warnings were reviewed: 83 concern template captions or diagram micro-labels, and one flags an intentional process arrow.
- Marp rebuilt successfully; browser checks found zero overflow across all 87 sections and all 18 SVG images loaded.
- Offline tests: **141 passed, 1 skipped, 4 deselected**, with one upstream Pydantic configuration deprecation warning (`uv run pytest tests/ -m 'not behavioral' -q`).
- No application code was changed by this deck refresh. No authenticated NAMS, OpenAI, Neo4j or Wikimedia rehearsal was performed. Public onboarding/API review and offline tests do not establish the availability or behavior of a particular participant's hosted workspace.
