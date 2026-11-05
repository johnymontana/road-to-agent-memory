# Workshop deck resources review — 2026-11-04

> Historical review: the subsequent [Module 5 update](deck-module5-2026-11-04.md) supersedes the counts and NAMS mismatch described below. The current deck has 102 slides and 49 resources. Its snippets use the updated `nameHint` and explicit `scope.type` contract, and approval occurs automatically before publication. See [current verification](../slides/module5-verification.json).

The native Google Slides deck now has 90 slides: the original 75 in their existing order, followed by a 15-slide resources appendix. All additions use editable Google Slides text and shapes, including linked titles, source captions and navigation. The appendix duplicates the inspected Neo4j three-row exploration template, retaining its logo, typography, circular graph motifs and card structure.

## Coverage

The appendix links all 47 verified resources through 45 annotated cards and two additional API overview links. It covers the project repository and releases, the exact SDK 0.8.0 package, conceptual documentation, PydanticAI, message history and search scope, entities and ontologies, preferences, reasoning traces, NAMS, skills and governance, five GraphAcademy courses, and six Neo4j articles.

All 75 original slides now have relevant clickable references and an internal “All resources” link. There are 151 external references across those slides, including focused API links beside all 14 code excerpts. Full titles, URLs, relevance and version notes are also available in speaker notes. The resource slides provide index, previous and next navigation.

The source mirrors are synchronized: [resource catalog](../slides/resources.md), [machine-readable mappings](../slides/resources.json), [Marp source](../slides/deck.md), [rendered HTML](../slides/deck.html), and [technical walkthroughs](../slides/technical-walkthroughs.md). The source presentation contains 58 instructional sections plus 15 resource sections; the native deck has additional diagram slides. All 58 source sections have references.

## Source selection and compatibility

Research used the official [agent-memory repository](https://github.com/neo4j-labs/agent-memory), [Neo4j documentation](https://neo4j.com/labs/agent-memory/), [GraphAcademy](https://graphacademy.neo4j.com/courses/genai-context-graphs), Neo4j blog articles, PydanticAI documentation, PyPI, and the public [NAMS service](https://memory.neo4jlabs.com/). Each catalog entry records its verified URL, purpose and any compatibility caveat. Focused topic pages are used instead of guessed fragment anchors.

The workshop’s SDK 0.8.0 and PydanticAI 2.62.0 pins remain the basis for executable examples. Some online guides use other releases, different client settings, or SDK integration helpers that differ from the workshop’s explicit local history, tools and scoped retrieval. The deck explains these boundaries. GraphAcademy courses using TypeScript/Mastra or Copilot/MCP/AIP are labeled as adjacent learning paths with their own environments.

### NAMS mismatch found during research

The current [live NAMS API documentation](https://memory.neo4jlabs.com/docs) requires `scope.type` for `POST /v1/skills/generate` and lists `nameHint` as the name field. It documents HTTP 400 when `scope.type` is absent. The repository fragment sends `name` and `scope.taskContains`, so it must be reconciled with the current hosted contract before a live module 5 run. The [Skills API reference](https://neo4j.com/labs/agent-memory/reference/skills-api/) is linked alongside the live contract.

The code excerpt remains identical to the repository. Its visible explanation now identifies it as a repository payload, explains the mismatch, and states that the hosted call was not rehearsed. Notes retain the fact that the repository automatically approves a 409 publish gate and retries; this is not a human approval checkpoint. No application code, credentials or hosted workspace state was changed by this resource update.

## Verification

- Native readback confirmed the final 90-slide order, all expected external and internal links, all 47 resource URLs in the appendix, and 181 expected text fields.
- All 14 native code excerpts remain identical. Original speaker notes remain intact before the added references. Existing diagram objects and graph-node shapes are unchanged.
- All 90 native slides were visually inspected using Google Slides LARGE previews. The PDF export reference could not be materialized, so native previews were the fallback. One consolidated repair pass improved six dark-slide caption contrasts and completed the two overview links; all eight repaired slides were inspected again.
- The structural issue checker reported no errors. Its 74 warnings concern existing template micro-labels and intentional source-note text; resource narrative bodies are 13 pt and card titles are 14 pt.
- Marp rebuilt successfully. Browser checks found no section overflow across all 73 local sections. All original code blocks were preserved.
- Offline workshop tests: 139 passed, 1 skipped, 4 deselected. One existing upstream Pydantic deprecation warning remains. No OpenAI, Neo4j, Wikimedia or authenticated NAMS replay was performed for this documentation update.

Detailed results: [resources-verification.json](../slides/resources-verification.json). Native source revision: `DDts8zxWoZw1ng`; delivered revision: `qG5M17j8fBPgPg`.
