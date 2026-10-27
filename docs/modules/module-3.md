# Module 3 — Long-Term Memory

The biggest module, and the heart of the workshop: the agent stops remembering
*sentences* and starts remembering *things* — who the customer is, what plan they're
on, which products they use — in a knowledge graph shaped by your own ontology.

## What you'll learn

- What an ontology is, and how one YAML document (`ontology/acme_cloud.yaml`) steers what the LLM extracts.
- Why extraction uses the LLM for *structure* (entities, types, relations) but never for *facts*.
- The three-source pipeline for rich entities: LLM structure → SQLite hydration → Wikipedia enrichment.
- How entity resolution and aliases keep "Acme Cloud" and "AcmeCloud" from becoming two nodes.

## Run it

| Command | What it does |
|---|---|
| `make s3-default` | Runs the scenario with the **default POLE+O** entity types — watch the loosely labeled, generic graph it produces. |
| `make s3-ontology` | Re-runs the *same* scenario with the custom Acme Cloud ontology — watch the graph bloom with typed entities and edges. |
| `make s3-enrich` | Runs the scenario that mentions the Stripe integration — extraction creates the entity, Wikipedia enrichment follows seconds later (stretch beat). |

## Explore

Tiers: **Core** for everyone · **Instructor-led** demos (config edits and re-runs the
instructor performs live) · **Stretch** for after the session.

**Core**

1. Find an entity extracted from your conversation. Follow its `:MENTIONS` edge back to the exact message that created it. Why is provenance valuable for a support org?
2. Compare the graph from the default POLE+O run vs. the custom-ontology run on the same scenario. What changed — labels, relationships, precision? Which would you rather build a support workflow on?
3. Click into a `Customer` node's properties. Which came from the LLM (type, subtype, typed relations), which from SQLite hydration (email, plan, signup date), and which from Wikipedia enrichment (`enriched_description`, `wikipedia_url`)? How could you tell the *source* of each property if the panel didn't label them?
4. Compare what the agent knows about the customer now vs. module 2. Which eval questions changed answers?

**Instructor-led**

5. Read the ontology's entity-type descriptions. They're rendered verbatim into the LLM's extraction prompt — why do they include negative cases ("Not the support engineer who answers")? Rewrite one description without its negative cases and re-run — what gets extracted differently?
6. Switch validation to strict and feed the agent an entity type the ontology doesn't declare. What happens — dropped, warned, or stored? When would you choose strict vs. permissive?
7. Watch a hydration upsert: re-run a scenario where the customer's plan was upgraded in SQLite between runs. What changed on the entity node — and what *didn't* (name, type, `:MENTIONS` edges)? Why is MERGE-on-`(name, type)` upsert semantics the right behavior here?

**Stretch**

8. Trigger the alias beat: the customer says "AcmeCloud" after earlier saying "Acme Cloud". The ontology declares the alias — where's the evidence in the graph that they resolved to one node? What would have happened without the alias declaration?
9. Find a typed edge (e.g., `REPORTED`). What do its `support`, `confidence`, and `source_message_ids` properties tell you? Find an edge with `support >= 2` — what does that mean?
10. Query the Neo4j labels: why does a `Customer` land as `(:Entity:Person:Customer {subtype: "CUSTOMER"})`? What is the ontology label vs. the POLE+O anchor, and why keep both?
11. Save a preference via chat ("I prefer email over phone"). Where does it land in the graph, and how does the agent surface it in a later session? How is a preference different from an entity?
12. The LLM could infer properties like an email address — so why do we hydrate every fact from SQLite instead? What failure mode does LLM-invented data invite, and what does the stock `EntityPayload` schema's decision to drop `attributes` tell you about how the library's authors think about this?
13. Find the `Stripe` entity. Which properties are enrichment-written, and why did enrichment work for Stripe but would miss for "Acme Cloud"? When is external enrichment the right tool vs. internal hydration?

## Answer key

1. The `:MENTIONS` edge leads from the entity to the exact `:Message` node whose sentence created it — click through and read the original words. For a support org this is audit-grade trust: every fact the agent asserts can be traced back to who said what and when, which matters for disputes, compliance, and debugging wrong answers.
2. The default run produces loosely labeled generic nodes (`Person`, `Object`), no typed relations, and bare properties; the custom-ontology run produces precise labels (`Customer`, `Plan`, `Incident`) connected by typed edges (`REPORTED`, `SUBSCRIBES_TO`, `AFFECTS`). You'd build on the custom one — a workflow can't route on "an Object mentioned a thing," but it can route on `(:Customer)-[:REPORTED]->(:Incident)`.
3. LLM: the node's type, subtype, and typed relations. SQLite hydration: `email`, `plan`, `signup_date`, `description`. Wikipedia enrichment: `enriched_description`, `wikipedia_url`, `wikidata_id`, `image_url`. Without panel labels you could still tell: hydrated values match real database rows exactly, enrichment fields carry the `enriched_`/`wikipedia_`/`wikidata_` naming, and the LLM never supplies property values at all — its `EntityPayload` schema deliberately excludes them.
4. Module 2 knew *what was said*; now the agent knows *who the customer is* — plan, products, preferences — across sessions. Eval questions like "What do you know about my account?" flip from fail to pass on the scorecard (`make eval`).
5. The descriptions are rendered verbatim into the extraction prompt, and negative cases stop the LLM from over-applying a label to look-alikes — "Not the support engineer who answers" keeps the helpful human on the ticket from being tagged as the `Customer`. Remove the negative cases and re-run, and you'll typically see false positives: the support engineer gets extracted as a Customer.
6. In strict mode, the undeclared entity type is rejected at ingest — dropped with a warning, not stored. Choose strict when data quality matters more than recall (curated knowledge graphs, compliance-sensitive domains); choose permissive while exploring, when you'd rather keep everything and clean up later.
7. After the SQLite plan upgrade, the hydration hook updates the entity's plan properties **in place**; the name, type, and `:MENTIONS` edges are untouched. MERGE on `(name, type)` means "the same real-world thing gets updated, never duplicated" — exactly right when the system of record changes underneath the memory graph.
8. Evidence: a *single* organization node holding both surface forms, with `:MENTIONS` edges arriving from both the "Acme Cloud" message and the "AcmeCloud" message. Without the declared alias, extraction would mint two near-duplicate organization nodes that never merge — and every downstream fact would split across them.
9. `support` counts how many independent mentions back the edge; `confidence` is the extractor's confidence in the relation; `source_message_ids` is the provenance list. An edge with `support >= 2` means two separate mentions asserted the same relationship — corroborated evidence, not a one-off remark.
10. Storage labels anchor every entity to the library's generic POLE+O machinery (`:Entity:Person`), while the ontology type (`Customer`, carried on the node and in `subtype`) keeps your domain meaning precise. Keeping both lets the library's internals work unchanged while your queries stay domain-exact.
11. The preference lands in long-term memory, attached to the customer's entity — a stored fact, not just a chat line. Later sessions surface it through `recall_preferences` and context assembly, so the agent opens the next chat already knowing "email, not phone." A preference is different from an entity: an entity is a *thing in the world*; a preference is a *fact about how to serve someone*.
12. Because the LLM can invent plausible-looking emails or plan tiers — and hallucinated facts in a support agent are worse than no facts (wrong refunds, wrong contact details, confident nonsense). Hydration grounds every fact in the system of record, so if it's on the node, it's in the database. The stock `EntityPayload` dropping `attributes` tells you the library's authors consider fact-filling out of scope for extraction on principle: *structure from the LLM, facts from systems of record*.
13. Stripe's enrichment-written properties are `enriched_description`, `wikipedia_url`, `wikidata_id`, and `image_url`. It worked because Stripe is a real, Wikipedia-notable organization; "Acme Cloud" is fictional, so there's nothing to enrich. Rule of thumb: enrichment for public third parties your database can't know, hydration for anything your own systems of record already do.

## If you fell behind

From the repo root, run:

```
make module-3
```

That replays this module's beats in order (both extraction runs plus the enrichment
scenario) and reproduces the room's current state. If your dev server is still running
an older stage, stop it first with `Ctrl+C`, then restart with `make dev MODULE=3`.

## Glossary

- [Ontology](../glossary.md#ontology) · [POLE+O](../glossary.md#poleo) · [Entity extraction](../glossary.md#entity-extraction) · [Hydration](../glossary.md#hydration) · [Enrichment](../glossary.md#enrichment)
