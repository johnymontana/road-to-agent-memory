# Run of show — verified non-NAMS workshop

Allocate 130 minutes plus 20 minutes of optional inspection/troubleshooting in a
150-minute slot. Model and database startup vary. Capture current timings before
delivery; stored replay screenshots are a fallback, never live-service evidence.

| Minutes | Activity | Exact command / observation |
| --- | --- | --- |
| 0–15 | Readiness and two stores | `make check`; `make dev MODULE=1`; wait for Ready and module badge. SQL is authoritative; Neo4j is memory. |
| 15–30 | Stateless control | `make s1-baseline`; choose its Saved replay. Self-contained SQL lookup, then intentional per-turn forgetting. `make eval MODULE=1`. |
| 30–50 | Persistent messages | Stop old server; `make dev MODULE=2`. `make s2-return`, `make s2-restart`. Inspect saved process IDs and source messages. `make eval MODULE=2`. |
| 50–65 | Fixed extraction pair | Stop old server; `make dev MODULE=3`. `make s3-default`, `make s3-ontology`. Refresh Saved replay list and compare transcript hashes and outputs. Allow startup, extraction and inspection time. |
| 65–80 | SQL grounding and preferences | In browser chat introduce Maya; inspect MENTIONS and hydrated email/plan/date before the answer. Select Customer for preference save/recall. |
| 80–90 | Guided variations | `uv run scripts/instructor.py strict`; `uv run scripts/instructor.py plan`. Both are reversible, local recipes. Optional `make s3-enrich`: show provider status, skip on unavailable. |
| 90–95 | Buffer | Questions and troubleshooting. Optional `make eval MODULE=3` can run while discussing evidence. |
| 95–110 | Action and declined-case records | Stop server; `make dev MODULE=4`. `make s4-refund`, `make s4-fail`. Select Saved replay for exact SQL/receipts; select Live memory for native trace links. |
| 110–125 | Controlled retrieval | `make s4-refund-repeat`. Same initial SQL hashes; frozen corpus; separate branches. Inspect actual evidence/tools/tokens/timing. `make eval MODULE=4` if time allows. |
| 125–130 | Wrap | What persisted, what was retrieved, which source supplied each fact, what action actually occurred? Run `uv run scripts/monday_memory.py` as the take-home recipe. |

Every CLI eval must name MODULE. Browser chat evidence and CLI Saved replay are
separate views. Saved replay projects recorded output; Live memory queries that
replay's actual Neo4j conversation for MENTIONS/TOUCHED/INITIATED_BY walks. For browser actions select the account and case and authorize that
message. Never resolve ambiguity using the previous speaker's account. Rejection
is a valid policy-compliant business result; it differs from an execution exception.

Catch-up targets replay selected beats; they do not restore checkpoints. Do not
clear shared graph data to catch up. If a dependency fails, inspect warnings and the
operation receipt before retrying. For screenshots, run the real backend first and
use `uv run scripts/capture_screenshots.py --module N`; the command rejects a badge
mismatch. Helpers handle credentials/ports while the facilitator continues with a
stored replay. Optional Wikimedia errors do not block the core lesson.

## Optional NAMS extension — unchanged, not included in this rehearsal

## Module 5 — Skill Distillation on NAMS (2:05–2:25)

| Time | Segment | Instructor does | Attendees do | Make targets | Trim |
|---|---|---|---|---|---|
| 2:05–2:08 | The seam + distillation concept | **Seam narration slide (D2):** "Your Bolt memory lives in *your* AuraDB. NAMS is a fresh, managed workspace — the seed loads the canonical history into it." Then D-14 distillation pipeline | Listen | — | Never cut the seam narration — it's what stops confusion about where the data went |
| 2:08–2:11 | Check + seed | `make nams-check`, then `make nams-seed` (~1 min — see waiting choreography) | Run both | `make nams-check`, `make nams-seed` | — |
| 2:11–2:15 | Distill + inspect | `make nams-distill`; poll while narrating; inspect SKILL.md + the skill subgraph (`GROUNDED_IN` edges, grounding/coverage scores — core Q1–2) | Run `make nams-distill`; open SKILL.md | `make nams-distill` | — |
| 2:15–2:19 | The payoff | `make s5-fresh-agent` — a fresh agent, no history, loads the skill and resolves the refund cold. Let the room feel it | Run `make s5-fresh-agent` | `make s5-fresh-agent` | Protect the payoff; cut the drift beat to narration if needed |
| 2:19–2:25 | Drift & governance | D-15 governance loop. Instructor-led: `make policy-change` → "nothing flagged — it watches the memory graph, not your database"; then `make nams-drift` → drift fires; `make nams-redistill` closes the loop | Follow along | `make policy-change`, `make nams-drift`, `make nams-redistill` | If tight: run `policy-change` + `nams-drift` only; narrate redistillation. Labs/early-access disclosure here |
