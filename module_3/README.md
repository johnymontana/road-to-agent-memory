# Module 3 — Long-term memory

**The idea:** remember *who and what* the customer talks about, not just the
words. Saving a user message now also extracts the entities it mentions
(`(:Message)-[:MENTIONS]->(:Entity)`), typed by an ontology. Their facts come
from SQLite, never from the LLM: an extracted "Maya Chen" gets her email, plan
and signup date from the system of record. The agent can also save and recall
customer preferences.

## Read the code

```bash
diff -ru module_2/app module_3/app
```

1. [`app/memory.py`](app/memory.py): `extractor_type="llm"` plus an ontology
   from [`ontology/`](ontology/) (`acme_cloud.yaml` or `default-poleo.yaml`).
2. [`app/agent.py`](app/agent.py): `_turn` adds a **ground** step between
   saving the message and recalling.
3. [`app/hydrate.py`](app/hydrate.py): looks up extracted names in SQLite and
   writes the facts onto the entity nodes. Type mismatches and ambiguous aliases
   hydrate nothing.
4. [`app/context.py`](app/context.py): two new retrieval paths,
   **grounded_entity** and **customer_preference**.
5. [`app/memory_tools.py`](app/memory_tools.py): `search_memory`,
   `save_preference` and `recall_preferences`, which the model calls itself.

[`lab/`](lab/) holds the experiments behind the scenario commands. The agent does
not use them: `compare.py` (extract one fixed transcript with each ontology) and
`enrichment.py` (optional Wikimedia lookup).

## Run it

Terminal 1 at the repository root. Stop the old server with Ctrl+C first.

```bash
make dev MODULE=3
```

Reload the browser on port 5173 and confirm the **Module 3** badge. In terminal 2 run the lesson commands.

```bash
make s3-default      # fixed transcript, generic POLE+O ontology
make s3-ontology     # same transcript, Acme Cloud ontology
make eval MODULE=3
```

- **Ontology comparison:** `s3-default`/`s3-ontology` send one fixed transcript
  through two independent extractors. No conversation, hydration or old graph is
  involved. Saved replays record transcript hashes, ontology, model and timing.
  Shapes can vary even at temperature zero.
- **The full agent:** introduce Maya Chen at Northwind Robotics in browser chat.
  Extraction runs first, then hydration of the entities in that message, then
  retrieval and the answer.
- **Preferences:** select a customer before saving one. The receipt shows the
  stored object and whether it was deduplicated. Preferences are linked to a
  per-customer `(:User)` and read back with `long_term.get_preferences_for()`. In **Current conversation**, follow `User → HAS_PREFERENCE → Preference` for a customer whose email is on an entity mentioned in this conversation. Choosing the customer scopes saving and recall. Use **All stored memory** for broader graph inspection.
- **Ontology selection:** `ONTOLOGY=acme_cloud` (default) or `default-poleo`
  loads the local YAML. `ONTOLOGY=active` uses the version stored in AuraDB
  (`scripts/activate_ontology.py`). `VALIDATION_MODE=strict` also drops entity
  types the ontology does not declare. Settings apply on restart.
- **Enrichment (optional):** `s3-enrich` asks Wikimedia for public organization
  facts. It caches successes for a week and errors for five minutes, and never
  enriches fictional companies. A 403 means unavailable; continue without it.

General app notes: [docs/running-the-app.md](../docs/running-the-app.md).
Questions and answers: [participant guide](../docs/modules/module-3.md).

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
