#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found; falling back to python"
    PYTHON_EXEC=python
else
    PYTHON_EXEC=python3
fi

echo "Installing dependencies from requirements.txt..."
$PYTHON_EXEC -m pip install --upgrade pip
$PYTHON_EXEC -m pip install -r requirements.txt

echo "Dependencies installed."
