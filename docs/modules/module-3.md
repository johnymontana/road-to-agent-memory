# Module 3 — Structured, grounded long-term memory

Start commands from the repository root. Keep `make dev MODULE=3` in one
terminal and run the lesson commands in another. Before switching modules, stop
the server with Ctrl+C, launch the next module, and reload the browser.

Browser chat has a visible conversation ID, New conversation and Resume controls.
It preserves turn history locally across reloads; clearing browser storage removes
that local history. Neo4j memory remains persistent. Terminal commands print their
own dialogue, tools and timing. Use **Refresh graph → Saved replay** to inspect their
immutable output projection; choose **Live memory** for the replay's persisted
Neo4j message/entity/trace links. CLI runs do not append turns to browser chat. Choose Current
conversation for browser evidence, or All stored memory deliberately.

Refund actions require a selected Customer and Billing case plus **Authorize selected
refund for this message**. Confirmation resets after each turn. The server checks
case identity, amount, current SQL plan limit and incident uniqueness. Asking for
an update reads refund history. A request ID returns its saved operation receipt on
retry; replaying a billing case cannot create a second refund. No escalation tool
exists. Status values are seeded examples with timestamps, never a live monitoring feed.

Run `make eval MODULE=3` explicitly. The evaluation lab starts only on POST/action;
opening or reopening it reads results. Each run uses private SQL, unique memory
fixtures and disabled business tools. Exact facts and source IDs are checked. This
is a controlled retrieval probe, not an end-to-end support-quality score or a promise
of monotonic improvement. A dependency error preserves completed questions.

```bash
make dev MODULE=3
# Second terminal:
make s3-default
make s3-ontology
make s3-enrich
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
ambiguous or incompatible types do not acquire SQL facts. One pooled writer is
reused; bounded retries and warnings preserve partial completion.

Select a Customer before saving preferences. Categories include namespace and email;
the receipt shows the actual stored object, context and deduplication flag. Customer
choices remain separate. Prior preference rows are not a new source of current policy.

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

Follow Message MENTIONS Entity and inspect that message.

### Q2: What changed with the ontology?

Compare only the two Saved replay snapshots. Verify transcript hashes before interpreting their types and edges.

### Q3: Which source supplied Customer fields?

Email, plan and signup_date come from SQL hydration; types/relations come from extraction. hydrated_from is a source marker, not per-field temporal lineage.

### Q4: What changed since module 2?

Structured facts and scoped preferences were added. Cross-conversation messages already existed in module 2.

### Q5: What do negative descriptions do?

Read the YAML and rerun the fixed extractor after a local edit. They guide the model; outputs are variable.

### Q6: How do validation modes differ?

Run `uv run scripts/instructor.py strict`: permissive drops an invalid relation, strict raises.

### Q7: What happens after a plan upgrade?

Run `uv run scripts/instructor.py plan`: a private SQL copy and local writer fixture run the actual hydration function before, after and following restoration of Maya's plan. Assert one entity is updated in place; this fixture is not a live Neo4j graph or automatic CDC.

## Read the code

Start with `module_3/app/agent.py`, then local `tools.py`. Read local `memory.py` and `context.py` for configuration and retrieval. Read `hydrate.py` and `memory_tools.py` for SQL grounding and preferences.

Each module owns its full agent implementation. Duplicated lesson code is intentional;
shared `lib/` supplies transport, settings, SQL, receipts and factory selection.
