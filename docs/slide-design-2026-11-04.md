# Native deck visual redesign — 2026-11-04

Current code synchronization and validation: [deck-code-sync-2026-11-04.md](deck-code-sync-2026-11-04.md). This document records the earlier review/design baseline.

Applied an individual design treatment to all 75 slides in the existing [native Google Slides deck](https://docs.google.com/presentation/d/1qBsciAQf7s3BUdQleJJ39-4RDKAoqqoVfodPDDg63z8). The work preserves the original slide IDs/order, template layouts, speaker notes, native icons and all 14 code walkthroughs, including their syntax styles.

## Visual system

The existing Neo4j template supplies Syne headings, Public Sans body text, connected-node motifs, logos and the navy/teal foundation. Green denotes conversation memory; yellow denotes entities and grounded fields; blue/purple denotes execution; lavender identifies hosted/portable-skill boundaries. Text labels accompany every color distinction.

- **Graph data:** 45 native circular nodes across the diagram set. A separate centered transparent text surface prevents the restrictive ellipse text inset from breaking schema names. Relationships have full names, directional arrows and meaningful source endpoints.
- **Execution flow:** rounded process cards, clear sequencing and explicit boundaries. Stores, code, properties and workflows retain appropriate containers rather than becoming graph nodes.
- **Technical density:** preserve complete code fragments, source captions, field names, SDK interfaces, namespace scope, SQL authority, outcome semantics and grounding caveats. Diagrams expose properties and provenance alongside topology.
- **Editable delivery:** all presentation additions are native shapes, text and connectors. No diagram or code block was flattened into a screenshot.

## Coverage

| Final slides | Treatment |
| --- | --- |
| 1, 4 | Protected title stack identifier; native agenda numerals converted into aligned stage markers using template colors. |
| 2, 9, 18, 70, 75 | Retained template icons, added aligned technical cards and source/API tags, and separated card copy from footer commands/links. |
| 3, 6, 8, 12, 16, 24, 27, 34, 37, 39, 42, 50, 55, 61, 67, 72, 74 | Rebuilt 17 graph/workflow diagrams with circular records, explicit edge names, stronger topology, property panels and technical contracts. |
| 5, 23, 41, 49, 66 | Kept template connected-node motifs and strengthened the three evidence rows with aligned panels. |
| 7, 15, 22, 32, 48, 60 | Numbered technical concepts plus explicit runtime/SDK surfaces in the section opener's branded panel. |
| 10, 17, 29, 43, 57, 64 | Monospaced terminal recipes, memory-layer outlines and distinct observation/evidence panels. |
| 11, 36, 62, 73 | Preserved template split-screen compositions; added clear system/channel labels and visual separation. |
| 13, 26, 38, 47, 54 | Aligned technical columns with consistent heading/body zones and memory-layer accents. |
| 14, 21, 25, 28, 35, 40, 45, 46, 51, 52, 53, 56, 63, 65 | Retained all code text and token styling. Added scope tabs, API/boundary headings, focused sidebars and memory-layer console accents. |
| 19, 71 | Preserved the template memory wave, widened descriptions and added explicit SDK entry points. |
| 20, 33, 44, 68 | Paired integration/grounding boundary cards; protected disclosure/footer clearances. |
| 30, 58 | Improved restart emphasis and provenance inspection using native branding and a small circular graph. |
| 31, 59, 69 | Aligned exploration tasks into readable evidence rows while retaining template motifs and numbering. |

The conversation chain now uses two rows to fit the complete `HAS_MESSAGE` and `NEXT_MESSAGE` labels without touching nodes. The trace anatomy retains `HAS_STEP`, `USES_TOOL`, `INSTANCE_OF`, `INITIATED_BY` and `TOUCHED`. The wrap explicitly shows `Trace → HAS_STEP → Step → TOUCHED → Entity`, keeping participant Bolt memory and separate hosted fixtures in different containers. Hosted diagrams remain conceptual, with conditional results clearly identified.

## Sources

`slides/visual-design.json` records the brand tokens, all 75 design decisions and complete vector scenes for 17 diagrams. `slides/diagrams/generate_branded_diagrams.py` renders their SVG mirrors. The existing `generate_svgs.py` entry point applies those scenes after its legacy/reference definitions, so a normal regeneration preserves the redesign.

Four additional diagram mirrors cover default/custom ontology, trace anatomy, hosted skill grounding and the connected memory model. Matching references were added to the Markdown deck without replacing ongoing prose changes. The native deck remains authoritative for inherited master artwork, icons, notes and the complete layout.

## Verification

- Rendered and inspected all 75 delivered slides, then verified the collected graph-label, caption and footer repairs. Two consolidated repair passes addressed actual rendering defects, including native ellipse insets and text-box padding.
- Native readback confirms 75 unchanged slide IDs in their original order, unchanged layout references and unchanged presenter notes. Every slide has its intended visual treatment.
- All 14 code blocks retain identical text and syntax-style runs.
- All 45 graph record shapes read back as `ELLIPSE` with equal physical width and height.
- The final slide issue checker reports **zero errors**. Its 29 warnings concern template eyebrow/micro-label roles and are intentional caption typography, inspected visually.
- The offline workshop suite passed: **127 passed, 1 skipped, 4 behavioral tests deselected**. One existing SDK Pydantic deprecation warning remains. No live OpenAI, Neo4j, enrichment or hosted service calls were made for this visual task.
- Both diagram generators pass Ruff; all 17 SVG files parse, regenerate deterministically and match the reviewed scene definitions. `git diff --check` passes.

`slides/visual-design-verification.json` contains the native node inventory, revision, validation scope and SVG hashes. Concurrent application changes were preserved; this work only changes presentation sources, visual tooling and documentation.
