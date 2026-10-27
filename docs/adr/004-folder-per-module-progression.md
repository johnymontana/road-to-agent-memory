# ADR 004: Folder-per-module progression (self-contained `module_N/` directories)

- **Status:** Accepted
- **Date:** 2026-10-27
- **Context:** How attendees move through the five modules during the live workshop

## Context

Attendees progress through five stages of the same application (stateless → short-term
→ long-term → reasoning → distillation). The original outline specified **git branches
per module** (`module-1` … `module-5`); the adversarial review flagged this as an
operational landmine (REVIEW_FEEDBACK G1: each `git checkout` in a live room is a 3–8
minute synchronization event — dev-server restarts, `.env` survival, dependency diffs —
×4 switches, unbudgeted; H9: branches also quietly expose that the memory layers were
always present, switched on by config).

ADR 002's alternative (feature flags on a single branch driven by `make module-N`)
removes the checkout hazard but hides the code evolution — attendees can't see *what
changed* between stages, which is the workshop's subject matter (review item 16 from
the Designer: "branch-per-module delivery hides the very diffs the workshop is about").

Requirements:

1. No live git checkouts (G1)
2. The per-stage code deltas must be **visible and diffable** — watching the code gain
   a memory layer is the workshop (Designer 16)
3. State (Aura graph, `.env`, venv, SQLite DB) must carry across stages untouched
4. A fallen-behind attendee must reach the room's current stage with one command (G7)

## Decision

**One directory per module, each fully self-contained:**

```
module_1/   # stateless agent — full app code
module_2/   # + short-term memory
module_3/   # + ontology, LLM extraction, hydration, enrichment
module_4/   # + reasoning memory
module_5/   # + NAMS distillation client
```

- Each folder contains the complete app code for its stage — attendees open the folder
  and run it; progression is `cd module_3`, never `git checkout`.
- **Shared state lives at the repo root**: one `.env` (all folders read it), one uv
  venv (`uv sync` once), one `data/acme_cloud.db`, one AuraDB — so memory accumulates
  continuously across folders, which *is* the arc.
- `make module-N` runs that module's beats from its folder (the catch-up lane), and
  `make dev MODULE=3` boots a specific stage — both resolved from the **root Makefile**
  (amended 2026-10-27, plan-review P1: there is one root Makefile using a `MODULE`
  variable for path resolution; module folders contain **no** per-folder Makefiles,
  so the shared root `.env`/`data/`/venv paths never depend on cwd).
- `diff -r module_2/ module_3/` is a first-class teaching artifact — the per-module
  README points at the specific files that gained memory wiring.

## Alternatives considered

| | Verdict |
|---|---|
| **Git branches per module** (original outline) | Rejected — 3–8 min live sync per switch (G1); `.env`/venv/dep breakage risk; progression-by-checkout hides nothing but breaks everything |
| **Feature flags + `make module-N` on one branch** (ADR 002 draft) | Rejected — safe but hides the code deltas that are the workshop's content (Designer 16); flags also mean all five stages' code paths ship live in one binary, enlarging the bug surface |
| **Branches + persistent worktree for env/state** | Rejected — more moving parts than folders, still teaches git mechanics instead of memory |

## Consequences

**Positive:**
- Zero git operations during the live session (G1 eliminated).
- Code evolution is a first-class, diffable artifact — the "progressive" arc is real.
- Root-level shared state means the memory graph grows continuously across modules —
  the narrative and the database agree.
- Catch-up is one command (`make module-N`, run from anywhere via the root Makefile) —
  no branch archaeology (G7).
- Simple for Codespaces: folders are just folders.

**Negative / accepted risks:**
- **Copy drift during development** — five copies of the app diverge unintentionally.
  Mitigation: folders are built sequentially (each derived from the previous), shared
  libraries extracted to a root `lib/` where truly identical, and CI diff-checks the
  intended deltas between adjacent folders.
- **Repo size** — five app copies; acceptable (frontend `node_modules` are not
  duplicated — the root venv/`npm ci` serve all folders).
- The Makefile must resolve paths per module folder (owned in Phase 1 of
  IMPLEMENTATION_PLAN.md).

## Related

- WORKSHOP_OUTLINE.md — Repo Plan
- IMPLEMENTATION_PLAN.md — Phase 1.6, Decision D1 (resolved: this ADR)
- ADR 002 — uv + Makefile tooling (module targets operate on folders)
- REVIEW_FEEDBACK.md — items G1, G7, H9, Designer-16
