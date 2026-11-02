# Diagram sources and verification

The native Google Slides deck uses editable native shapes, arrows and text. These
local SVGs and Excalidraw files are source/reference illustrations; they are not
measured runtime graphs. `generate_svgs.py` regenerates the SVG inventory.

For measured non-NAMS graph fallbacks see
`artifacts/screenshots/module-[1-4]-live.png` and the matching JSON source records.
The capture checks the actual running backend and its module badge. CLI extraction
comparisons are immutable Saved replay artifacts with transcript hashes, separate
from the illustrated default/custom diagram.

Non-NAMS illustrations teach per-turn statelessness, Conversation/Message chains,
local recent-plus-semantic context, ontology extraction, separate Customer SQL and
Organization Wikimedia sources, aliases and controlled procedure retrieval. NEXT
in the simplified chain diagram abbreviates the stored NEXT_MESSAGE relationship.
Trace outcome/reply are ReasoningTrace properties; ReasoningSteps link to ToolCalls,
source messages and explicitly touched entities.

NAMS-specific illustrations remain unchanged and were not validated by this replay.
The historical inventory and build phases are retained in IMPLEMENTATION_PLAN.md;
the current delivery contract is docs/run-of-show.md and docs/workshop-fixes-2026-11-01.md.
