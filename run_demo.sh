#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT_DIR"

echo "Starting FastAPI backend..."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
UVICORN_PID=$!

trap 'printf "\nShutting backend...\n"; kill $UVICORN_PID 2>/dev/null' EXIT

echo "Waiting for backend to initialize..."
sleep 2

echo "Launching Streamlit demo..."
streamlit run ui.py --server.headless true --server.port 8501
