#!/usr/bin/env bash
# One-time bootstrap on a server (DigitalOcean droplet, etc.).
# Run from the repository root after cloning and configuring env files.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> SocraticTutor production setup"
echo "    Root: $ROOT"
echo ""

if [[ ! -f backend/.env ]]; then
  echo "Create backend/.env from backend/.env.example (LLM_API_KEY, JWT_SECRET, etc.)"
  exit 1
fi

if [[ ! -f .env ]] && [[ -f .env.example ]]; then
  echo "Optional: copy .env.example to .env for compose variables (FRONTEND_URL, NEXT_PUBLIC_API_URL)."
fi

if [[ ! -f Caddyfile ]]; then
  echo "Copy Caddyfile.example to Caddyfile and set your domain, then re-run."
  exit 1
fi

echo "==> Building and starting stack (compose + prod overrides)..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

echo "==> Waiting for backend..."
sleep 5

echo "==> Alembic migrations..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T backend uv run alembic upgrade head

echo "==> Rehydrate wiki images (optional; large download — failures are non-fatal)..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T backend uv run python scripts/batch_extract_images.py --rehydrate || true

echo "==> Seed database from content/*/course.json..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T backend uv run python seed.py

echo ""
echo "Done. Visit https://YOURDOMAIN (or http://SERVER_IP:3000 for dev-style access)."
echo "Set FRONTEND_URL and NEXT_PUBLIC_API_URL to your public URL (see DEPLOY.md)."
