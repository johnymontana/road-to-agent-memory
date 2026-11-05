# Road to Agent Memory final run-through · November 5, 2026

We ran every participant command from the repository root in the order of the run of show, switched the browser backend through Modules 1–5, and drove the website for each module with a headless Chromium (Playwright) against the live `make dev` servers. SQLite, replays and evaluations used the repository `data/` directory; the Bolt agent wrote to the configured AuraDB in fresh replay and evaluation namespaces. The previous rehearsal is [November 4](workshop-rehearsal-2026-11-04.md).

## What to expect in the room

| Stage | Participant action | Observation from this run |
| --- | --- | --- |
| 0 · Setup | `make setup`, `make check`, then `make dev MODULE=1` | Setup reused the existing SQLite data. All required checks passed in 47 s. The median trivial Bolt query took 453 ms. The app printed Ready and the browser showed the Module 1 badge. |
| 1 · Baseline | `make s1-baseline`, open its Saved replay, `make eval MODULE=1` | Maya's lookup returned Northwind Robotics, Pro and a $250 limit; the next turn answered “Unknown”. The browser produced the same pair. The replay's evidence panel showed the two SQL statements. The eval scored 0/4. The scenario took 5 s. |
| 2 · Short-term | `make s2-return`, `make s2-restart`, `make eval MODULE=2` | Both replays recovered “violet comet” in the same conversation and from a new one with a cited message ID. The restart artifact listed two process IDs. In the browser, a new ticket phrase was recalled in the same conversation (recent_conversation and semantic_message) and from a new conversation (semantic_message only). The node inspector showed HAS_MESSAGE and NEXT_MESSAGE. Backend startup took 33 s per process; each turn took 8–12 s. The eval scored 2/4. |
| 3 · Long-term | `make s3-default`, `make s3-ontology`, `make eval MODULE=3`, then browser chat | Both extractor snapshots shared transcript SHA-256 `752d85d09cfa…`. The generic ontology produced six entities and two relations; the Acme Cloud ontology produced seven entities and five relations, including SUBSCRIBES_TO Pro and REPORTED BILL-104. In the browser, “I'm Maya Chen from Northwind Robotics.” produced MENTIONS edges to a Customer entity carrying email, plan, signup_date and `hydrated_from: sqlite:customers`. With Maya selected, a contact preference was stored (receipt with `deduplicated: false`), recalled in a new conversation through customer_preference evidence, and the Current conversation graph showed User → HAS_PREFERENCE → Preference. Without a selected customer, save_preference returned `needs_customer`. Browser turns took 12–28 s. The eval scored 3/4; the fourth answer was prose rather than JSON. |
| 3 · Extensions | `uv run scripts/instructor.py strict`, `uv run scripts/instructor.py plan`, `make s3-enrich` | The validator dropped the invalid relationship in permissive mode and raised in strict mode. The plan fixture moved one local entity Pro → Enterprise → Pro. Enrichment returned the cached Stripe, Inc. description. |
| 4 · Actions | `make s4-refund`, `make s4-fail`, inspect replays and Live memory | Maya's $49 duplicate-charge refund was issued (refund #1); the $400 request was rejected by the server guard with no INSERT. The Live memory view traversed ReasoningTrace → HAS_STEP → ReasoningStep → USES_TOOL → ToolCall → INSTANCE_OF → Tool, with INITIATED_BY to the message and TOUCHED to Maya Chen and Pro. In the browser, Dana's $129 case was issued once; a repeat without authorization and a repeat with authorization both returned the existing receipt. Each replay took 73–76 s; browser refund turns took 19–36 s. |
| 4 · Ablation | `make s4-refund-repeat`, `make eval MODULE=4` | Input SQL hashes matched. Control called lookup_account → search_memory → issue_refund (2,546 input tokens, 16.6 s); treatment retrieved one reasoning trace and called issue_refund alone (2,288 input tokens, 13.5 s). Both answered the Pro policy question with fetch_policy → lookup_account and no action. The command took 156 s. The eval scored 4/4. |
| 5 · Consumer | `make s5-fresh-agent WITH_SKILL=off`, `=on`, `=fallback` | All three issued Ravi's $49 refund on a private SQL copy. Control called lookup_account → issue_refund; the downloaded skill and the checked-in fallback both called lookup_account → fetch_policy → issue_refund. Each run took about 6 s. |
| 5 · Hosted | `make nams-check`, `make nams-seed` | **Not completed in this run.** The configured `NAMS_API_KEY` was bound to a workspace with no skills, no conversations and an active custom ontology from another project (`ridgeline-hardware-context`, review mode, `person` requires `customer_id`). The seed was rejected with HTTP 422. The previously downloaded package (version 1.4.0) lives in a different workspace, so the browser NAMS view was empty. See the changes below. |

The take-home `uv run scripts/monday_memory.py` wrote one phrase and read it back from exactly one message in 38 s.

## What changed during this run

- `make nams-check` previously passed on a workspace that would reject the seed. It now also reads the workspace's active ontology and fails, with the fallback command, when that ontology requires properties on the seed's `person`, `organization` or `custom` entities, or does not declare them under strict validation. It lists whether an `acme-refund-procedure` skill already exists in the workspace and whether the package in `artifacts/distilled/` belongs to it, so a key from the wrong workspace is visible before class.
- `make nams-seed` previously ended in a traceback on HTTP 422. It now exits with the service's message, the active ontology ID, the remedy (a workshop workspace without a custom ontology) and the fallback command. Nothing is written to the receipt.
- The pre-work email, Module 5 guide and README, the run of show and the outline describe the new readings. Six offline tests cover the rejection and the check's ontology and package paths.

## Before the workshop

1. Point `NAMS_API_KEY` at the workshop workspace (the one that holds `acme-refund-procedure`), or create a fresh workspace and key, then run `make nams-check` until it prints the ontology and package lines without a ❌.
2. On a workspace that passes the check, run `make nams-seed`, `make nams-distill` and `make s5-fresh-agent WITH_SKILL=on`, and tick **NAMS** in the Module 5 browser to confirm Skill → HAS_VERSION → SkillVersion → HAS_STEP → SkillStep → GROUNDED_IN. This run could not exercise that path.
3. The governance extension (`make policy-change`, `make nams-drift`, `make nams-redistill`) was not run; it changes the instructor's SQL policy and hosted workspace and was last exercised on November 4.
4. `make seed` restored the SQLite teaching data after this run (no refunds on file). Replays and evaluations from this run remain in `data/` and appear in the Saved replay list until that directory is cleared.

## Verification

- `make check`, every `make sN-*` scenario, `make eval MODULE=1..4`, `make s5-fresh-agent` in all three modes, `make s3-enrich`, both instructor recipes, `make seed`, `make clean` and the take-home script ran from the Makefile.
- All five module badges, graph views (Current conversation, Saved replay, Live memory, memory-layer filter, node inspector with edge navigation), the evidence panel, the refund controls and the Evaluation lab were exercised in Chromium with no page errors and no failed `/api` requests.
- Ruff, the offline suite (171 passed, 1 skipped), the lockfile check and the production frontend build passed.
