#!/usr/bin/env bash
# SAGE — one-command bootstrap for local dev.
#
# Run from the repository root:
#   bash scripts/setup.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[sage] repo root: $ROOT"

# ----- Backend -------------------------------------------------------------
cd "$ROOT/backend"

if [ ! -f .env ]; then
  if [ -f "$ROOT/.env.example" ]; then
    cp "$ROOT/.env.example" .env
    echo "[sage] backend/.env created from .env.example"
  fi
fi

if command -v uv >/dev/null 2>&1; then
  echo "[sage] installing backend deps with uv"
  uv pip install -r requirements.txt
else
  echo "[sage] installing backend deps with pip"
  python3 -m pip install -r requirements.txt
fi

echo "[sage] seeding database"
python3 seed.py

# ----- Frontend ------------------------------------------------------------
cd "$ROOT/frontend"

if [ ! -f .env.local ]; then
  if [ -f .env.local.example ]; then
    cp .env.local.example .env.local
    echo "[sage] frontend/.env.local created from .env.local.example"
  fi
fi

echo "[sage] installing frontend deps"
npm install

cat <<EOF

[sage] Setup complete.

Next:
  Terminal A:  cd backend  && uvicorn app.main:app --reload --port 8000
  Terminal B:  cd frontend && npm run dev

Demo credentials:  demo@sage.ai / demo1234
EOF
