#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/4] Backend env"
cd "$ROOT_DIR/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true


echo "[2/4] Alembic migrations"
alembic upgrade head

echo "[3/4] Seed demo data"
python scripts/generate_demo_data.py

echo "[4/4] Frontend deps"
cd "$ROOT_DIR/frontend"
npm install
cp -n .env.example .env || true

echo "Done. Run backend/run_dev.py from PyCharm and npm run dev in frontend."
