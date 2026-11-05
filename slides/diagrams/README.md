# Diagram sources and verification

The native Google Slides deck uses editable native shapes, arrows and text. These
local SVGs and Excalidraw files are source/reference illustrations; they are not
measured runtime graphs. `generate_svgs.py` regenerates the SVG inventory, applying the reviewed branded
scenes from `slides/visual-design.json` through `generate_branded_diagrams.py`.

For measured non-NAMS graph fallbacks see
`artifacts/screenshots/module-[1-4]-live.png` and the matching JSON source records.
The capture checks the actual running backend and its module badge. CLI extraction
comparisons are immutable Saved replay artifacts with transcript hashes, separate
from the illustrated default/custom diagram.

Non-NAMS illustrations teach per-turn statelessness, Conversation/Message chains,
local recent-plus-semantic context, ontology extraction, separate Customer SQL and
Organization Wikimedia sources, aliases and controlled procedure retrieval.
In the message diagram, each member is linked to its conversation by `HAS_MESSAGE`.
`NEXT_MESSAGE` links consecutive messages. The history query selects conversation
members and sorts them by timestamp and ID. The trace diagram connects a captured
step to the customer and plan selected for its case. Inspect the tool result and
executed SQL to determine which operation changed state.

That earlier non-NAMS replay did not validate the hosted workflows. The current
NAMS illustrations were subsequently reviewed against module 5 code and public
service documentation; see `docs/deck-module5-2026-11-04.md`. They remain schemas,
not captured runtime graphs.
The historical inventory and build phases are retained in IMPLEMENTATION_PLAN.md;
the current delivery contract is docs/run-of-show.md and docs/workshop-fixes-2026-11-01.md.


## Visual design update — 2026-11-04

The 102-slide native deck uses the existing Neo4j template's Syne/Public Sans
hierarchy, navy/teal base, connected-node motifs and memory-layer palette. All
19 diagram compositions have complete scene definitions in
`slides/visual-design.json`; the SVGs mirror those vector primitives.

Graph records are circles with separate centered text surfaces. Native Slides
ellipses have restrictive text insets, so putting the label in its own transparent
textbox prevents broken schema names. Relationships retain their full stored
names and meaningful direction. Workflow stages, API boundaries, code and source
properties remain cards or panels. Never replace a graph node with a box just to
fit its label; expand/reposition the text surface or adjust the composition.

New mirrors cover default/custom ontology, trace anatomy, hosted skill grounding
and the connected memory model. The wrap explicitly shows `Trace → HAS_STEP →
Step → TOUCHED → Entity`; participant Bolt memory and hosted fixtures are separate
containers. These remain illustrative schemas, not measured runtime screenshots.

The native deck is authoritative for full layout, inherited template icons, notes
and branding. SVG mirrors preserve diagram geometry and text as vectors; they do
not recreate the complete template master. See `docs/slide-design-2026-11-04.md`
for coverage and verification.

The module 5 refresh adds `d19-memory-to-skills.svg` and updates the skill,
governance, connected-memory and consumption-model diagrams. The hosted skill
graph now shows `Skill → HAS_VERSION → SkillVersion → HAS_STEP → SkillStep`,
with `GROUNDED_IN` evidence links and `SUPERSEDES` between versions. Distillation
is a derived capability built on the three memory types. Its process arrows are
distinct from stored graph relationships.

The refund evidence figure, `d20-refund-evidence.svg`, shows the three native
nodes used on slide 58. Its white arrows follow the trace through `HAS_STEP` to
the step and `TOUCHED` to the selected case customer or plan. In the anatomy,
versioned-skill and connected-memory figures, a linear description identifies
each source, relationship and target. The same traversal is available in the
Google Slides figure descriptions and in the SVG `<desc>` elements. The
governance figure assigns a separate observation to the SQL limit, hosted drift
report and new skill version.
