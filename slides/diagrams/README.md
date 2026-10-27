# Diagram inventory (D-01 … D-18)

Source of truth: `IMPLEMENTATION_PLAN.md` §4.2. Excalidraw sources live beside this
file; exported PNGs are referenced by `slides/deck.md` and the module READMEs.
Color palette (fixed): short-term `#B2F2BB`/`#2F9E44` · long-term `#FFEC99`/`#F08C00` ·
reasoning `#D0BFFF`/`#9C36B5` · Neo4j/store `#A5D8FF`/`#1971C2` · Labs accent `#6366F1` ·
text `#1e1e1e`. Every diagram pairs color with a text label (no color-only meaning).

| # | Title | Content spec (one line) | Used in | Status |
|---|---|---|---|---|
| D-01 | The two stores | SQLite (system of record) vs. Neo4j (memory), agent between them; reused in M1, M3 hydration, M5 drift | Intro + M1 + M5 | **drawn** — `d01-two-stores.excalidraw` |
| D-02 | Three memory types, one knowledge graph | The trinity (short-term / long-term / reasoning) with color legend, converging on one graph | Intro + Wrap | **drawn** — `d02-three-memory-types.excalidraw` |
| D-03 | The workshop arc | Five-module failure→fix ladder with the eval scorecard overlay | Intro | **drawn** — `d03-workshop-arc.excalidraw` |
| D-04 | Environment map | Codespace (FastAPI, Vite, uv, scripts) ↔ AuraDB ↔ OpenAI ↔ NAMS; shows where each credential lives | M0 | to be drawn after Phase 3 exit |
| D-05 | Statelessness | Two identical sessions, no bridge (the M1 failure mode) | M1 | to be drawn after Phase 3 exit |
| D-06 | Message chains | `:Conversation` → `:Message` sequence; restart-survival animation frames | M2 | to be drawn after Phase 3 exit |
| D-07 | Context assembly | `get_context` → dynamic instructions → model call | M2 | to be drawn after Phase 3 exit |
| D-08 | Ontology-driven extraction | Ontology YAML → extraction prompt → typed graph; forbidden relation dropped at ingest | M3 | **drawn** — `d08-ontology-extraction.excalidraw` |
| D-09 | POLE+O vs. custom ontology before/after | Two mini-graphs side by side on the same scenario | M3 | **screenshot, not Excalidraw** — captured via `scripts/capture_screenshots.py` after Phase 3 exit |
| D-10 | The hybrid pipeline | Three sources (LLM structure / SQLite facts / Wikipedia externals) converging on one entity node with provenance-labeled properties | M3 | **drawn** — `d10-hybrid-pipeline.excalidraw` |
| D-11 | Entity resolution | Alias beat: "AcmeCloud" → one node; SAME_AS review edge | M3 | to be drawn after Phase 3 exit |
| D-12 | Reasoning trace anatomy | Task → AgentSteps → ToolCalls → outcome; `:TOUCHED` vs `:MENTIONS` contrast | M4 | **screenshot, not Excalidraw** — captured via `scripts/capture_screenshots.py` after Phase 3 exit |
| D-13 | Similar-task retrieval | New ticket embeds near yesterday's trace; ablation callout (control vs. treatment) | M4 | to be drawn after Phase 3 exit |
| D-14 | Distillation pipeline | Traces+entities+observations → SKILL.md + skill subgraph with `GROUNDED_IN` edges; grounding/coverage scores | M5 | **screenshot, not Excalidraw** — captured via `scripts/capture_screenshots.py` after Phase 3 exit |
| D-15 | Governance loop | Skill goes stale when grounding changes → re-distill (shape finalized after spike 0.6) | M5 | to be drawn after Phase 3 exit (blocked on spike 0.6 confirmation of D4 drift semantics) |
| D-16 | The finale | One agent's experience becomes everyone's skill — fresh agent loading the distilled skill | M5 | to be drawn after Phase 3 exit |
| D-17 | One knowledge graph recap | Single canvas showing all three layers + skill subgraph connected | Wrap | **screenshot, not Excalidraw** — captured via `scripts/capture_screenshots.py` after Phase 3 exit |
| D-18 | Bolt vs. NAMS | Consumption models table rendered as a diagram | Wrap | to be drawn after Phase 3 exit |

## Export convention

`*.excalidraw` → exported PNG (2x, white background) with the same basename, committed
next to the source. The deck references PNGs as `../slides/diagrams/dNN-<name>.png`.
