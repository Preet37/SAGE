#!/usr/bin/env bash
# SAGE — Full setup script
set -e

SAGE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "Setting up SAGE at: $SAGE_DIR"

# ── Backend ────────────────────────────────────────────────────────
echo ""
echo "1/4 Installing Python dependencies..."
cd "$SAGE_DIR/backend"

if command -v uv &>/dev/null; then
  uv pip install -r requirements.txt
elif command -v pip3 &>/dev/null; then
  python3 -m pip install -r requirements.txt
else
  echo "ERROR: pip or uv not found. Install Python 3.11+ first."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "  ✓ Created backend/.env — edit it with your API keys"
fi

echo ""
echo "2/4 Seeding database..."
python3 seed.py

# ── Frontend ───────────────────────────────────────────────────────
echo ""
echo "3/4 Installing Node dependencies..."
cd "$SAGE_DIR/frontend"

if command -v npm &>/dev/null; then
  npm install
else
  echo "ERROR: npm not found. Install Node.js 20+ first."
  exit 1
fi

if [ ! -f .env.local ]; then
  cp .env.local.example .env.local
  echo "  ✓ Created frontend/.env.local"
fi

echo ""
echo "4/4 Setup complete!"
echo ""
echo "  To start the backend:"
echo "    cd $SAGE_DIR/backend && uvicorn app.main:app --reload --port 8000"
echo ""
echo "  To start the frontend:"
echo "    cd $SAGE_DIR/frontend && npm run dev"
echo ""
echo "  Demo credentials: demo@sage.ai / demo1234"
echo ""
