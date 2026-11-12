#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
if [ ! -f data/mart.sqlite3 ]; then
 MART_ADMIN_PASSWORD='MartDemo!2026' MART_CASHIER_PASSWORD='Cashier!2026' .venv/bin/python seed.py
fi
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
