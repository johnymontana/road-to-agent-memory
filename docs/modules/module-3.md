# Module 3 — Structured, grounded long-term memory

Start at the [full Module 3 agent](../../module_3/app/agent.py). Compare its behavior with the adjacent module using the [code map](../../module_3/README.md). The [app guide](../running-the-app.md) explains replay views, refund authorization and the isolated evaluation.

Terminal 1 at the repository root. Stop the old server with Ctrl+C first.

```bash
make dev MODULE=3
```

Reload the browser on port 5173 and confirm the **Module 3** badge. In terminal 2 run the lesson commands.

```bash
make s3-default
make s3-ontology
make eval MODULE=3
```

The default/custom pair sends one fixed transcript through two independent LLM
extractors. No conversation, SQL hydration or old graph participates. Saved replay
snapshots include identical transcript hashes, ontology, model and timing. Shapes may
vary despite temperature zero. They are extractor results, not a comparison of chat agents.

For the full agent, introduce Maya Chen at Northwind Robotics in browser chat.
Extraction runs first, then type-safe SQL hydration of current-message entities,
then retrieval and the answer. `context.py` exposes allowlisted email, plan,
signup_date and employer facts with IDs. Exact aliases preserve resolved names;
ambiguous or incompatible types do not acquire SQL facts. Property writes share one
driver and open a short session each; bounded retries and warnings preserve partial
completion.

Select a Customer before saving preferences. Each preference is linked to a
per-customer `(:User)` and read back with `long_term.get_preferences_for()`. Its
category is prefixed with namespace and email because the library deduplicates
within a category across all users. The receipt shows the actual stored object,
context and deduplication flag. Customer
choices remain separate. Prior preference rows are not a new source of current policy.

In **Current conversation**, follow `User → HAS_PREFERENCE → Preference` for a customer whose email is on an entity mentioned in this conversation. Choosing the customer scopes saving and recall. Use **All stored memory** for broader graph inspection.

`ONTOLOGY=acme_cloud` loads `module_3/ontology/acme_cloud.yaml`; `default-poleo`
loads the local generic file. `ONTOLOGY=active` uses the database version after
`scripts/activate_ontology.py`. Both shell and `.env` settings resolve on restart.
The pinned app filters invalid relations in both modes; `VALIDATION_MODE=strict`
also drops undeclared entity types. The separate instructor validator recipe shows
explicit relation `mode="drop"` versus `mode="raise"`; it is not the app setting.

Optional `s3-enrich` explicitly requests public Organization facts from Wikimedia.
It caches successes for one week and errors for five minutes and saves provider
status as a replay. A 403 is unavailable, not pending. It never enriches fictional
companies automatically or proves Stripe operational status. Continue without it.

## Explore and verify

### Q1: Where did this entity come from?

In browser chat enter “I’m Maya Chen from Northwind Robotics.” Choose **Current conversation**, select the user message, and follow a `MENTIONS` edge. Name the extracted entity. On a matching customer inspect email, plan or signup date and the SQL source marker. If this run produced no matching customer, record what was extracted and compare an instructor’s labeled example.

### Q2: What changed with the ontology?

Compare only the two Saved replay snapshots. Verify transcript hashes before interpreting their types and edges.

### Q3: Which source supplied Customer fields?

Email, plan and signup_date come from SQL hydration; types/relations come from extraction. hydrated_from is a source marker, not per-field temporal lineage.

### Where can I inspect each experiment?

| Input | Output / writes | View |
|---|---|---|
| Fixed transcript and one ontology per run | Two extractor-only replay snapshots with comparable transcript hashes | **Refresh graph → Saved replay · Extractor only** |
| Browser message introducing Maya | Live graph message and any typed mentions. Matching entities can receive SQL-grounded fields. | **Current conversation** and execution evidence |
| Instructor’s invalid relationship | Local validator drops the edge or raises, according to the explicit test mode | Instructor terminal output |
| Optional Wikimedia lookup | Cached provider result/status and saved replay | Optional `make s3-enrich` replay |

### Q4: What changed since module 2?

Structured facts and scoped preferences were added. Cross-conversation messages already existed in module 2.

### Q5: What do negative descriptions do?

Read the YAML and rerun the fixed extractor after a local edit. They guide the model; outputs are variable.

### Q6: How do validation modes differ?

The instructor runs `uv run scripts/instructor.py strict` on a deliberately invalid relationship. The explicit `drop` and `raise` modes show two validator outcomes. The fixed-transcript extractor filters undeclared types and invalid relations before saving its projection. Browser ingestion uses the app’s configured ontology and validation mode to write the live graph. Compare each experiment in its own view.

### Q7: What happens after a plan upgrade?

Run `uv run scripts/instructor.py plan`: a private SQL copy and local writer fixture run the actual hydration function before, after and following restoration of Maya's plan. Assert one entity is updated in place; this fixture is not a live Neo4j graph or automatic CDC.

## Read the code

Start with `module_3/app/agent.py`, then local `tools.py`. Read local `memory.py` and `context.py` for configuration and retrieval. Read `hydrate.py` and `memory_tools.py` for SQL grounding and preferences.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
