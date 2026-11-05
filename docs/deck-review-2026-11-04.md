# End-to-end deck review — 2026-11-04

Current code synchronization and validation: [deck-code-sync-2026-11-04.md](deck-code-sync-2026-11-04.md). This document records the earlier review/design baseline.

Reviewed and updated the existing native [Google Slides deck](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8) against the lesson-owned implementations, SDK configuration, scenario runners and frontend replay controls. The deck now has 75 slides, including 14 code walkthroughs. Text, code, diagrams and connectors remain native editable Slides objects.

## Technical corrections

| Slides (final order) | Finding and correction | Repository evidence |
| --- | --- | --- |
| 2–10 | Removed the unmeasured 20-minute implementation promise, deterministic-model implication and guaranteed green score progression. The agenda totals 150 minutes including wrap; code walkthroughs belong inside existing budgets. Credentials support `.env` and environment secrets. Smoke checks exercise inference, embeddings, memory and graph transport; start with `make dev MODULE=1`. | `Makefile`, `scripts/check_env.py`, `.devcontainer/post-create.sh`, `lib/settings.py` |
| 13–17 | Statelessness occurs on every model call without supplied history, including within the same visible browser chat. Refunds require explicit selected account/case and authorization; memory is not authorization. Corrected graph refresh/replay instructions. | `module_1/app/agent.py`, `module_1/app/tools.py`, `web/src/components/GraphPanel.jsx` |
| 19–28 | Distinguished persistence from automatic context injection, local helpers from package APIs, and client lifetime from turn lifetime. Match the actual user extraction flag, preserve `user_message.id`, and show write → retrieve → compose instructions → model as a sequence rather than parallel branches. | `module_2/app/agent.py`, `memory.py`, `context.py` |
| 29–30 | Separate recorded CLI projections, persisted live Neo4j memory and browser conversation state. Keep the same named conversation for the restart demonstration. | `lib/app_factory.py`, `module_2/app/agent.py`, replay runner and graph selector |
| 32–42 | Ontology-guided extraction and resolution can vary. LLM descriptions are not authoritative business fields. Show SQL upsert only inside the checked hydration loop; explicitly identify the separate local flat-property writer. Create a conversation before the extraction example. | `module_3/app/memory.py`, `hydrate.py`, `module_3/ontology/acme_cloud.yaml` |
| 45–47 | Include the composed memory instructions. Use actual preference tool arguments and output fields; the local tool serializes a receipt rather than returning the displayed dictionary directly. Q7 is a local hydration upgrade/restore fixture. | `module_3/app/agent.py`, `memory_tools.py`, `scripts/instructor.py` |
| 49–53 | Replace the misleading condensed try/finally lifecycle with three focused stages: open trace, record observations/provenance, complete outcome. Show exact JSON reply/execution/business fields and the recording-error condition. Notes identify omitted metrics, references and error classification. Completion is attempted; an unavailable memory backend can still prevent persistence. | `module_4/app/agent.py`, `reasoning.py` |
| 54–59 | Move SDK trace expansion before the model-call example, label helper/caller scopes, remove guaranteed matching or speedup claims, and distinguish conceptual successful/declined examples from the actual ablation's single fixed declined fixture. Policy text exists when fetched, not in every tool result. | `module_4/app/reasoning.py`, `ablation.py`, `tools.py` |
| 60–69 | Hosted distillation reads canonical authored fixtures, not participant module-4 executions. The full module-5 support app still uses Bolt; separate workflows use REST. Generation/poll/publication/download and file-based fresh-agent consumption are explicit. Drift deletes a search match and inspects a report; no guaranteed stale flag or successful re-distillation is asserted. | `module_5/app/agent.py`, `fresh_agent.py`, `module_5/workflows/seed.py`, `distill.py`, `drift.py` |
| 70–75 | Controlled retrieval checks require facts and source IDs; they are not an overall quality grade. The connected skill graph is conceptual: participant Bolt data and hosted fixtures remain physically separate. Backend comparison now describes the paths the repo actually uses. | `scripts/eval.py`, module-5 workflows, `scripts/monday_memory.py` |

## Flow and readability

The package introduction remains after the module-1 baseline. Each code slide now states its function/scope, gives a source caption, and explains the package/local boundary. Added one outcome slide after provenance recording, retaining the inspected code-slide exemplar and template typography. No main explanation was reduced below the template's narrative floor. Repaired a wrapped Python call and enlarged the backend comparison labels. Kept conceptual diagrams explicitly separate from measured runtime results.

Reviewed every source and delivered slide as connector-rendered thumbnails, with larger code-slide views. The connector PDF render helper had previously failed to materialize its export; thumbnails were the fallback. Re-inspected the four repaired slides. The final issue checker reports zero errors; remaining warnings are intentional template eyebrow/micro-label roles and pre-existing diagram labels, reviewed visually. No clipped text or overlapping content was found in the final inspected layouts.

Synced `slides/deck.md`, structured/human-readable walkthrough sources, and the affected SVG generator/artifacts. Historical rehearsal reports remain unchanged.

## Validation

- **55 passed**: `tests/test_context_contract.py`, `tests/test_hydration_types.py`, `tests/test_module_agents.py`, `tests/test_nams_workflows.py` (one dependency Pydantic deprecation warning).
- **14 code fragments**: parsed as contextual async fragments; displayed package/PydanticAI calls checked against installed signatures (`neo4j-agent-memory==0.8.0`). This verifies syntax and API shape, not that omitted context makes a fragment standalone.
- **Four outcome probes** execute the real `module_4.app.reasoning.finish_execution` against fake storage: ordinary completion, execution failure, policy decline and recording failure. Verified `success`, error classification, exact reply and execution/business statuses.
- **Native readback**: 75 unique slide IDs in expected order; every code block, scope label, sidebar and source caption matches the structured walkthrough source. Both Markdown mirrors contain all 14 final snippets.
- **Visual QA**: all 75 delivered slides inspected; all 14 code slides inspected at larger scale; one consolidated repair pass and four repaired-slide previews verified.
- `git diff --check` passed.

No new OpenAI, Neo4j or hosted NAMS service rehearsal was performed in this deck review. NAMS behavior remains an early-access, configured-workspace rehearsal requirement. The hosted workflow tests use mocked transport; they do not prove hosted schema or governance parity. Generated extraction, task matches, skill quality and model responses remain variable.
