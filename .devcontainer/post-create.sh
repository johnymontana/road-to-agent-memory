#!/usr/bin/env bash
# post-create.sh — runs once the codespace belongs to the attendee. User-scoped
# secrets are available now; keep this FAST (the attendee is watching).
set -euo pipefail

# Scaffold .env from the example (never overwrite an existing one). Any value
# already provided as a personal Codespaces secret (e.g. OPENAI_API_KEY) wins
# at runtime — .env is the fallback for Aura credentials and local overrides.
if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env from .env.example — add your AuraDB credentials."
fi

cat <<'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧠  ROAD TO AGENT MEMORY — workshop environment is ready
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Next steps:
    1. Add your AuraDB credentials + OPENAI_API_KEY to .env
       (or set OPENAI_API_KEY as a personal Codespaces secret
        scoped to this repo — it will already be in your shell)
    2. make check    — verify everything connects
    3. make dev      — start the app (the UI opens automatically)

  Every workshop action is a make target. Try `make help`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
