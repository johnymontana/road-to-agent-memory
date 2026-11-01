# Module rearchitecture evaluation

Evaluated locally on 2026-11-01 with the installed locked dependencies.
Every module now owns its agent implementation, including local tool definitions.
Memory configuration, ontology, hydration and hosted workflows live in the stage
that introduces them, with complete copies in subsequent stages.

## Results by module

| Module | Offline behavior verified |
| --- | --- |
| 1 | Stateless agent; all five business tools run against temporary, seeded SQLite; no memory client or memory tools. |
| 2 | Conversation creation, user/assistant persistence, context assembly and agent recreation with the same session; extraction disabled; long-term and reasoning context explicitly excluded. |
| 3 | Local ontology selection and connection lifetime; extraction configured; SQL-grounded hydration updates descriptions and flat properties with provenance; search/save/recall tools; reasoning retrieval excluded. |
| 4 | Real library trace recorder processes PydanticAI results; accepted/refused refunds produce successful/failed outcomes; retrieval ablation disables both automatic retrieval and memory-tool retrieval while recording continues. |
| 5 | Complete local reasoning-enabled support agent; separate fresh agent with business tools and on/off/fallback skill selection; missing skills fail clearly; hosted seed/distill/review/publish/download/drift request ordering and HTTP failure handling. |

For all five stages, tests also exercise HTTP health/chat/eval, scenario dispatch,
the registered tools and the existing frontend response shape. An import guard
checks that lessons do not depend on other lessons or the removed shared agent.

The offline tests run real PydanticAI agent loops with deterministic `FunctionModel`
responses, temporary SQLite databases, and memory adapters. Hosted-workflow tests
use HTTP mock transports. These verify local behavior and request choreography;
they do not establish model quality, extraction accuracy, graph persistence or
compatibility with the current hosted NAMS deployment.

## Checks completed

- Offline Python suite: **68 passed**, with live-service tests deselected.
- Live rehearsal: **all six checks passed** across the initial suite and the
  targeted module 3 rerun after fixes. The initial full run had five passes and
  the module 3 hydration failure; the final module 3 run passed.
- Ruff for `lib/`, all five modules, `scripts/` and `tests/`: passed.
- Python compilation and CLI argument-help smoke checks: passed.
- Make dry runs for module 3 and the module 5 default/fallback skill commands: passed.
- Frontend production build: passed, with the existing bundle-size advisory.
- `git diff --check`: passed.

Repository-wide Ruff is not green: four existing E501 violations remain in
`slides/diagrams/generate_svgs.py` (lines 169, 236, 256 and 257). That pre-existing
slide work was not changed as part of this refactor. Pytest also reports one
upstream Pydantic deprecation warning.

## Fixes found during live rehearsal

- Resolved entities can retain a short name such as `Maya`, with `Maya Chen` in
  their aliases. Hydration now checks exact recorded aliases against SQLite,
  preserves the existing node and message links, and refuses conflicting matches.
- Modules 3–5 explicitly require `save_preference` before confirming a requested
  preference write. The rehearsal uses a unique category so the library cannot
  deduplicate its preference onto an earlier run's globally stored email choice.
- Similar-trace retrieval defaults to successful executions in the installed
  library. Modules 4–5 now explicitly include failures in both retrieval paths and
  show success status in retrieved context, making rejected refunds recallable.
- Extraction does not queue third-party enrichment by itself. Organizations with
  no SQLite record now pass through the public entity upsert, which queues the
  optional enrichment provider. They are not counted as SQL-hydrated facts.

Regression tests cover these changes independently in every affected module.

## Live rehearsal

| Stage | Live result |
| --- | --- |
| 1 | Passed: real OpenAI calls the SQLite account tool and answers Pro; no memory client. |
| 2 | Passed: a unique phrase survives memory-client recreation; no entity mentions are extracted. |
| 3 | Passed after fixes: real extraction, Customer labels, exact SQLite email/signup/provenance on resolved entities, explicit preference write, and vector retrieval in a unique category. |
| 4 | Passed: accepted and rejected refunds recorded in Neo4j; failed trace recalled; reasoning context excluded/included with retrieval off/on. |
| 5 support agent | Passed: the same live trace-outcome and retrieval checks against its own implementation. |
| 5 fresh agent | Passed: real OpenAI loads the checked-in fallback skill and issues the eligible refund using local business tools. |

The over-limit tool-rejection branch uses a deterministic `FunctionModel` to force
the actual refund tool call; an unconstrained model can correctly refuse before
calling it. Its trace recording and recall use real Neo4j. The eligible refund,
ordinary support responses, extraction and embeddings use configured OpenAI.

The six checks in `tests/test_behavioral.py` rehearse real model/tool behavior,
conversation persistence across client recreation, extraction/hydration and
preferences, trace outcomes/retrieval in both modules 4 and 5, and the fresh
fallback-skill agent:

```bash
RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
```

They use temporary SQLite data, unique conversation IDs and a unique preference
category, send fictional Acme Cloud support prompts to configured OpenAI services,
and add conversations, entities and traces to configured Neo4j. They do not reset
existing graph data. Rehearsal records remain available for inspection.
The user explicitly authorized the live service calls and graph writes. Optional
enrichment in modules 3–5 also contacted Wikimedia for organization names.
Wikipedia returned **HTTP 403** from this environment, including a direct provider
probe for the public vendor Stripe. Chat and SQL hydration continued despite this
provider error; successful external enrichment could not be verified. No attempt
was made to bypass Wikipedia's access restriction.

Neo4j reported deprecation warnings for the installed library's vector query
procedure. Those searches still executed successfully. A bounded startup probe
opened a real memory client in about 37 seconds; repeated client creation accounts
for a substantial part of the live suite's runtime.

NAMS credentials are not configured in this workspace. The hosted
seed/distill/publish/drift lifecycle still needs a separate rehearsal in a
designated workshop workspace; the fallback skill does not validate that lifecycle.

`make eval MODULE=N` remains a workshop demonstration using keyword signals. It
shares persisted graph data across runs and does not causally isolate memory
layers, so its score is not a substitute for the tests above.
