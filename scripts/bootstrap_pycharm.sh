#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/5] Backend venv and deps"
cd "$ROOT_DIR/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true

cd "$ROOT_DIR"
echo "[2/5] Infra services"
docker compose up -d db redis

echo "[3/5] Migrations"
cd "$ROOT_DIR/backend"
source .venv/bin/activate
alembic upgrade head

echo "[4/5] Demo data"
python scripts/generate_demo_data.py

echo "[5/5] Frontend deps"
cd "$ROOT_DIR/frontend"
npm install
cp -n .env.example .env || true

echo "Done. Open backend/run_dev.py in PyCharm and run; for frontend run npm run dev."
