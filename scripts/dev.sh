#!/usr/bin/env bash
# make dev — run the module backend (:8000) + frontend (:5173) together.
set -euo pipefail
MODULE="${MODULE:-1}"

# Check both ports before starting either service. In particular, a local
# devcontainer can already publish these ports on the host machine.
uv run python - <<'PY'
import socket
import sys

busy = False
for port in (8000, 5173):
    with socket.socket() as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind(("0.0.0.0", port))
        except OSError as exc:
            print(f"Cannot start: port {port} is unavailable ({exc}).", file=sys.stderr)
            busy = True
if busy:
    print(
        "Stop the previous make dev first (Ctrl+C). If Docker publishes these "
        "ports, run make dev in the Dev Container terminal, or stop that "
        "container before running on the host.",
        file=sys.stderr,
    )
    sys.exit(1)
PY

pids=()
stop_tree() {
    local pid="$1" child
    for child in $(pgrep -P "$pid" 2>/dev/null || true); do
        stop_tree "$child"
    done
    kill "$pid" 2>/dev/null || true
}
cleanup() {
    local pid
    # Only stop processes launched here, never the caller's process group.
    for pid in "${pids[@]}"; do stop_tree "$pid"; done
    wait 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "▶ Backend :8000 (module ${MODULE})  ·  Frontend :5173"
uv run python -m "module_${MODULE}.app.main" &
backend_pid=$!
pids+=("$backend_pid")
npm --prefix web run dev -- --strictPort &
frontend_pid=$!
pids+=("$frontend_pid")

# Announce readiness only after both HTTP surfaces answer; health polling also
# remains in the browser when a Codespaces tab opens before this point.
(
    for attempt in $(seq 1 180); do
        if curl -fsS http://localhost:8000/api/health >/dev/null 2>&1 && \
           curl -fsS http://localhost:5173/ >/dev/null 2>&1; then
            echo "Ready: http://localhost:5173 (module ${MODULE})"
            exit 0
        fi
        sleep 1
    done
    echo "Startup is taking longer than expected; inspect the service output above."
) &
pids+=("$!")

# Bash 3.2 (macOS) has no wait -n. Stop the peer when either service exits,
# and preserve the exited service's status so make reports startup failures.
while kill -0 "$backend_pid" 2>/dev/null && kill -0 "$frontend_pid" 2>/dev/null; do
    sleep 0.2
done
if ! kill -0 "$backend_pid" 2>/dev/null; then
    wait "$backend_pid"
else
    wait "$frontend_pid"
fi
