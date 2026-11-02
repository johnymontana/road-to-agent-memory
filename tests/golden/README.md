# Historical reference shapes

These JSON files describe the earlier lesson snapshots. `test_golden_format.py`
checks their schema only; it does not certify current behavior or graph state.

Current learning invariants are executable in `tests/test_behavioral.py`: actual
module-local agents, populated FastAPI graph transport, latest-history ordering,
SQL-grounded Customer fields, per-customer preferences, refund identity and
idempotency, and INITIATED_BY/TOUCHED/USES_TOOL/INSTANCE_OF relationships. The
opted-in live job fails if credentials are missing. `tests/test_ui.py` separately
exercises cold Vite SharedWorkers and participant controls.

Capture new scoped evidence with `scripts/capture_golden.py --module N --session ID`;
it writes a snapshot under DATA_DIR, without inventing passing assertions from the
same data it just read.
