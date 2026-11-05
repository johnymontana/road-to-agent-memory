# Road to Agent Memory — Makefile
# The sole attendee-facing command surface (ADR 002).
# Canonical spec: WORKSHOP_OUTLINE.md → Repo Plan → Makefile target surface (29 targets).
# One root Makefile; module targets resolve per-folder paths via MODULE (ADR 004).
# `make help` is generated from the SPEC below — CI verifies they agree.

MODULE ?= 1
WITH_SKILL ?= on
ROOT := $(shell pwd)

# ── Canonical target spec (single source of truth — keep in sync with the outline) ──
# setup check seed dev | module-0..5 | s1-baseline s2-return s2-restart s3-default
# s3-ontology s3-enrich s4-refund s4-refund-repeat s4-fail s5-fresh-agent |
# nams-check nams-seed nams-distill nams-drift policy-change nams-redistill |
# eval reset-memory clean

.DEFAULT_GOAL := help
.PHONY: help setup check seed dev \
        module-0 module-1 module-2 module-3 module-4 module-5 \
        s1-baseline s2-return s2-restart s3-default s3-ontology s3-enrich \
        s4-refund s4-refund-repeat s4-fail s5-fresh-agent \
        nams-check nams-seed nams-distill nams-drift policy-change nams-redistill \
        eval reset-memory clean

help: ## Show this command surface
	@echo "Road to Agent Memory — command surface (29 targets)"
	@echo ""
	@echo "  Setup & env : make setup | make check | make seed | make dev [MODULE=N]"
	@echo "  Modules     : make module-0 | module-1 | module-2 | module-3 | module-4 | module-5"
	@echo "  Scenarios   : make s1-baseline | s2-return | s2-restart | s3-default |"
	@echo "                s3-ontology | s3-enrich | s4-refund | s4-refund-repeat |"
	@echo "                s4-fail | s5-fresh-agent"
	@echo "  NAMS (M5)   : make nams-check | nams-seed | nams-distill | nams-drift |"
	@echo "                policy-change | nams-redistill"
	@echo "  Utilities   : make eval [MODULE=N] | reset-memory | clean"

# ── Setup & env ────────────────────────────────────────────────────────────────
setup: ## Install locked Python deps (uv sync) + frontend deps (npm ci)
	uv sync --frozen
	npm --prefix web ci
	uv run scripts/seed_sqlite.py --if-missing

check: ## Smoke test: env vars, AuraDB, OpenAI key, SQLite, (module 5) NAMS
	uv run scripts/check_env.py

seed: ## Seed the Acme Cloud SQLite system of record
	uv run scripts/seed_sqlite.py

dev: ## Run backend (module MODULE) + frontend together. Usage: make dev MODULE=2
	@MODULE=$(MODULE) bash scripts/dev.sh

# ── Module beats (catch-up lanes: run the module's beats in order) ─────────────
module-0: ## Module 0 — verify environment
	$(MAKE) check
	@echo "Now run: make dev MODULE=1"

module-1: ## Module 1 — stateless baseline
	$(MAKE) s1-baseline

module-2: ## Module 2 — short-term memory beats
	$(MAKE) s2-return

module-3: ## Module 3 — long-term memory beats
	$(MAKE) s3-default
	$(MAKE) s3-ontology

module-4: ## Module 4 — reasoning memory beats
	$(MAKE) s4-refund
	$(MAKE) s4-fail
	$(MAKE) s4-refund-repeat

module-5: ## Module 5 — NAMS distillation beats
	$(MAKE) nams-check
	$(MAKE) nams-seed
	$(MAKE) nams-distill
	$(MAKE) s5-fresh-agent

# ── Scenarios (paced/serialized OpenAI calls — ADR 001) ────────────────────────
s1-baseline:       ## M1: billing-issue ticket, no memory
	uv run scripts/run_scenario.py s1-baseline --module 1
s2-return:         ## M2: same-chat and cross-chat message recall
	uv run scripts/run_scenario.py s2-return --module 2
s2-restart:        ## M2: two-process restart with the same conversation
	uv run scripts/run_scenario.py s2-restart --module 2 --restart-beat
s3-default:        ## M3: extraction with default POLE+O types
	uv run scripts/run_scenario.py s3-default --module 3
s3-ontology:       ## M3: fixed transcript with the Acme Cloud ontology
	uv run scripts/run_scenario.py s3-ontology --module 3
s3-enrich:         ## M3 (stretch): explicit cached Wikimedia enrichment (best effort)
	uv run scripts/run_scenario.py s3-enrich --module 3
s4-refund:         ## M4: first refund ticket (recorded as a trace)
	uv run scripts/run_scenario.py s4-refund --module 4
s4-refund-repeat:  ## M4: same-shape ticket — with/without retrieval (ablation pair)
	uv run scripts/run_scenario.py s4-refund-repeat --module 4 --ablation
s4-fail:           ## M4: over-limit refund that issue_refund rejects (failed trace)
	uv run scripts/run_scenario.py s4-fail --module 4
s5-fresh-agent:    ## M5: fresh agent loads the distilled skill, resolves cold
	uv run scripts/fresh_agent.py --with-skill $(WITH_SKILL)

# ── NAMS (module 5) ────────────────────────────────────────────────────────────
nams-check:        ## Verify NAMS key + workspace
	uv run scripts/nams_check.py
nams-seed:         ## Seed canonical reasoning memory into the NAMS workspace
	uv run scripts/seed_nams.py
nams-distill:      ## Trigger skill distillation, poll, publish, download SKILL.md
	uv run scripts/nams_distill.py
nams-drift:        ## Drift beat: delete the refund-policy entity; show flagged claims
	uv run scripts/nams_drift.py
policy-change:     ## Boundary demo: flip the refund limit in SQLite (governance blind spot)
	uv run scripts/change_policy.py
nams-redistill:    ## Re-distill after drift; diff the new SKILL.md
	uv run scripts/nams_distill.py --redistill

# ── Utilities ──────────────────────────────────────────────────────────────────
eval: ## Run the continuity eval-question set; print the scorecard
	uv run scripts/eval.py --module $(MODULE)

reset-memory: ## Wipe the Neo4j memory graph (destructive; asks to confirm)
	uv run scripts/reset_memory.py

clean: ## Remove build artifacts (web/dist, caches; keeps .venv and data)
	rm -rf web/dist .pytest_cache .ruff_cache playwright-report
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
