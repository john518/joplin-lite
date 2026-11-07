#!/bin/bash
set -e # Exit immediately if any command fails

# Get the project root directory (one level up from the script)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Build the client UI
npm --prefix ui run build

# Run the python desktop application entry point
PYTHONPATH=. PYTHONUNBUFFERED=1 uv run joplin_lite/joplin-lite.py "$@"
