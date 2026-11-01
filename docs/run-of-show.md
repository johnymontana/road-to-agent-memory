# Run of Show — Road to Agent Memory (150 minutes)

Instructor minute-by-minute run sheet. Times assume a 0:00 start. Budget: M0 15 ·
M1 15 · M2 25 · M3 40 · buffer 5 · M4 25 · M5 20 · Wrap 5.

**Golden rules**

- Demos run on make targets, never live typing. Slides and terminal always agree.
- The instructor never leaves the podium to fix an attendee's machine — helpers own
  environment issues (see *Triage policy* below).
- At every module boundary, run the folder-transition script **verbatim** (below).
- Run eval as `make eval MODULE=N`; scenario commands write to AuraDB but print their
  chat/tool results in the terminal. Reload or change the graph filter afterward.
- Code walkthroughs start at `module_N/app/agent.py`, then local `tools.py` and memory files.

---

## Module 0 — Setup (0:00–0:15)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 0:00–0:03 | Welcome & arc | Title slide, "what you'll leave with" (honest run-and-explore promise), D-03 arc diagram | Listen | — | Cut the arc slide to 30 s if late |
| 0:03–0:08 | Environment tour | D-04 environment map (Codespace ↔ AuraDB ↔ OpenAI ↔ NAMS); where each credential lives | Open the Codespaces badge; add Aura credentials to `.env` | — | Skip the credential deep-dive; point at prework email |
| 0:08–0:12 | Smoke test | Run `make check` live; read the green checklist line by line | Run `make check`; raise hand on red | `make check` | If >3 attendees red, hand to helpers and move on — `make module-0` is the catch-up lane |
| 0:12–0:15 | First boot & UI tour | `make dev`; tour the three panels (chat / graph / trace); note the graph panel is *empty* — "remember that" | `make dev`; click around the UI | `make dev` | Cut Q&A; exploration questions live in docs/modules/module-0.md |

## Module 1 — The Stateless Agent (0:15–0:30)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 0:15–0:18 | The two stores | D-01 diagram: SQLite = system of record, Neo4j = memory; "memory doesn't replace systems of record" | Listen | — | — |
| 0:18–0:20 | Meet the agent | Show the five tools; D-05 statelessness framing | Listen | — | Compress to one slide |
| 0:20–0:26 | Live demo | `make s1-baseline` — run the billing ticket, then "return" in a new chat and watch the agent ask who they are. Land the failure | Run `make s1-baseline`; watch the trace panel SQL | `make s1-baseline` | Run only the first half of the scenario; narrate the second |
| 0:26–0:30 | Eval baseline | `make eval` — print the scorecard; this is the "before" picture the wrap refers back to | Run `make eval`; start core exploration questions 1–2 | `make eval` | Skip attendee exploration entirely if behind — questions + answer key are in module-1.md |

**Folder transition (0:30, verbatim):**

> "Everyone: **stop your server first — Ctrl+C in the terminal running `make dev`** —
> then start module 2 with `make dev MODULE=2`. If you skip the Ctrl+C, the old server
> keeps holding ports 5173 and 8000 and the new one fails with 'port already in use'.
> Same dance at every module boundary: Ctrl+C, then `make dev MODULE=N`."

## Module 2 — Short-Term Memory (0:30–0:55)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 0:30–0:35 | Concept | "Short-term ≠ temporary" slide; D-06 message chains; D-07 context assembly | Listen | — | — |
| 0:35–0:42 | Return beat | `make s2-return` — the customer returns in a new chat; the agent knows them | Run `make s2-return`; find the `:Conversation`/`:Message` chain in the graph panel | `make s2-return` | — |
| 0:42–0:48 | Restart beat | `make s2-restart` — kill the backend mid-conversation, restart, continue. "What survived? Exactly the records in AuraDB." | Run `make s2-restart`; core questions 1–3 | `make s2-restart` | Narrate the restart instead of a second run |
| 0:48–0:55 | Paraphrase demo + exploration | Instructor-led: message search with a paraphrase (Q4) — show the vector path answering | Follow along; stretch Q5 in module-2.md | — | Drop the paraphrase demo if >3 min behind; it re-appears in the README |

**Folder transition (0:55):** Ctrl+C, then `make dev MODULE=3`.

## Module 3 — Long-Term Memory (0:55–1:35)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 0:55–1:02 | Concept | Entities vs. messages; D-08 ontology-driven extraction; D-10 hybrid pipeline — "structure from the LLM, facts from SQLite" (the design-principle slide) | Listen | — | Merge D-08/D-10 into one walkthrough |
| 1:02–1:10 | Before/after | `make s3-default` (generic POLE+O soup) then `make s3-ontology` (typed bloom) on the *same* scenario. This is the module's money shot — protect it | Run both; compare graphs (core Q2) | `make s3-default`, `make s3-ontology` | Never cut the before/after; cut concept slides instead |
| 1:10–1:18 | Ontology tour | Walk `module_3/ontology/acme_cloud.yaml`: annotation-guideline descriptions with negative cases, typed relationships, aliases. Instructor-led Q5 (rewrite a description without negative cases, re-run, watch false positives) | Follow along | — | Demo the negative-case edit only, skip the re-run (narrate the expected diff) |
| 1:18–1:25 | Hydration & provenance | Click a `Customer` node: property provenance (core Q3); `:MENTIONS` walk-back (core Q1); instructor-led Q7 hydration upsert (plan upgraded in SQLite between runs) | Core questions 1, 3, 4 | — | Pick *one* of Q5/Q7 to demo live, not both |
| 1:25–1:30 | Strict vs. permissive + enrichment | Instructor-led Q6 (strict mode drops undeclared types). Show the **pre-warmed Stripe node** in passing — "Wikipedia enrichment; stretch material, screenshot in the README" — and move on | Listen | (`make s3-enrich` only if well ahead) | Enrichment is stretch — never run it on the critical path |
| 1:30–1:35 | Eval checkpoint + buffer | `make eval` — the scorecard flips its first long-term answers green | Run `make eval` | `make eval` | — |

**Buffer (1:35–1:40):** planned 5-minute slack. If on time, take questions or let
attendees start core exploration. If behind, absorb it here — module 4's exploration
is the next droppable section.

**Folder transition (1:40):** Ctrl+C, then `make dev MODULE=4`.

## Module 4 — Reasoning Memory (1:40–2:05)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 1:40–1:45 | Concept | D-12 trace anatomy; `:TOUCHED` vs `:MENTIONS`; "the agent's own execution as memory" | Listen | — | — |
| 1:45–1:50 | First trace | `make s4-refund` — the first refund ticket, recorded; walk the trace subgraph | Run `make s4-refund`; core Q1 (reconstruct the story) | `make s4-refund` | — |
| 1:50–1:57 | The ablation payoff | `make s4-refund-repeat` — same-shape ticket twice: retrieval off (control) then on (treatment), side by side in the trace panel. "This is the module's proof." | Run it; core Q2 | `make s4-refund-repeat` | Protect the ablation; cut concept recap |
| 1:57–2:02 | Failure is memory | `make s4-fail` — the over-limit refund rejected; instructor-led Q4 (what went wrong) + Q5 (provenance walk-back: "why did you issue that refund?") | Follow the walk-back in the graph | `make s4-fail` | **Droppable section** — if behind, skip attendee exploration; do Q5 as a 60-second demo or defer to the README |
| 2:02–2:05 | Eval checkpoint | `make eval` — "Have you handled a ticket like this before?" flips green (core Q3) | Run `make eval` | `make eval` | — |

**Folder transition (2:05):** Ctrl+C, then `make dev MODULE=5`.

## Module 5 — Skill Distillation on NAMS (2:05–2:25)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 2:05–2:08 | The seam + distillation concept | **Seam narration slide (D2):** "Your Bolt memory lives in *your* AuraDB. NAMS is a fresh, managed workspace — the seed loads the canonical history into it." Then D-14 distillation pipeline | Listen | — | Never cut the seam narration — it's what stops confusion about where the data went |
| 2:08–2:11 | Check + seed | `make nams-check`, then `make nams-seed` (~1 min — see waiting choreography) | Run both | `make nams-check`, `make nams-seed` | — |
| 2:11–2:15 | Distill + inspect | `make nams-distill`; poll while narrating; inspect SKILL.md + the skill subgraph (`GROUNDED_IN` edges, grounding/coverage scores — core Q1–2) | Run `make nams-distill`; open SKILL.md | `make nams-distill` | — |
| 2:15–2:19 | The payoff | `make s5-fresh-agent` — a fresh agent, no history, loads the skill and resolves the refund cold. Let the room feel it | Run `make s5-fresh-agent` | `make s5-fresh-agent` | Protect the payoff; cut the drift beat to narration if needed |
| 2:19–2:25 | Drift & governance | D-15 governance loop. Instructor-led: `make policy-change` → "nothing flagged — it watches the memory graph, not your database"; then `make nams-drift` → drift fires; `make nams-redistill` closes the loop | Follow along | `make policy-change`, `make nams-drift`, `make nams-redistill` | If tight: run `policy-change` + `nams-drift` only; narrate redistillation. Labs/early-access disclosure here |

## Wrap (2:25–2:30)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 2:25–2:30 | Recap & Monday morning | `make eval` one last time — full board green. D-17 one-graph recap; D-18 Bolt vs. NAMS; "add memory to your own agent in 20 min" + teardown + resources (neo4j.com/labs/agent-memory, GraphAcademy context-graphs course) | Run `make eval`; note docs/teardown.md | `make eval` | If behind, do the eval re-run and point at the READMEs for the rest |

---

## Waiting choreography (what to say during the gaps)

- **NAMS seed (~1 min):** "While this runs, notice the boundary we just drew on the
  slide: nothing is leaving your AuraDB. This script is writing the canonical refund
  history — traces, steps, tool calls, in the order a real agent loop produced them —
  into a fresh managed workspace. In a real deployment this would be your production
  memory accumulating over weeks; we're compressing it into a minute."
- **Distillation poll:** "Distillation is reading every seeded trace and weighing the
  evidence — which tool-call patterns repeated, which entities they touched. When it
  lands, look for two numbers: grounding — how much of the skill has receipts — and
  coverage — how much of the evidence it used. Those two scores are your trust meter."
- **Enrichment async gap (module 3, if shown):** "The Stripe node appeared first — the
  Wikipedia fields follow at Wikimedia's ~2 requests/second rate limit. That's the
  honest shape of async enrichment: structure now, external knowledge seconds later.
  While we wait, look at the hydrated properties — those came from SQLite,
  synchronously, and they carry the demo even if Wikipedia is slow today."

## Fallback decision points

- **NAMS signup or service issues at module 5** → switch to the fallback kit in
  `artifacts/`: play the pre-recorded distillation video, and have attendees run
  `make s5-fresh-agent WITH_SKILL=fallback` (loads the pre-distilled SKILL.md + exported skill subgraph from
  `artifacts/pre-distilled-skill/`). The payoff — fresh agent loading a skill —
  survives a full NAMS outage. Announce it matter-of-factly: "NAMS is early access;
  this is the same artifact, pre-baked."
- **Extraction output diverges from the expected graph (module 3)** → don't live-debug
  prompts. Temperature 0 makes divergence rare; when it happens, point at the
  expected-graph screenshots in the module README and the deck, note "near-deterministic
  ≠ identical," and move on. The golden-graph snapshots in CI are the source of truth.
- **An attendee's environment breaks** → TA triage policy (below).

## Triage policy (instructor + helpers)

- **Helpers own environment issues, end to end.** The instructor never leaves the
  podium and never debugs an individual machine from the front.
- **Park-and-pair rule:** if a helper can't fix an attendee's environment in ~5
  minutes, park it — pair the attendee with a neighbor to follow along — and get them
  current later with `make module-N` (the catch-up lane reproduces the room's state
  from that module's folder in one command).
- Instructor watches for **OpenAI 429s** (whole-room rate bursts): scenario scripts
  pace calls, but if 429s appear, say so out loud — "that's a rate limit, not your
  setup" — and wait one beat before re-running.
