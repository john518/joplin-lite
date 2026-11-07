#!/usr/bin/env bash
set -e # Exit immediately if any command fails

# Get the project root directory (one level up from the script)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Build the client UI
npm --prefix ui run build

# Run the python desktop application entry point.
# This requires different commands for linux and macOS,
# apparently because pywebview runs different on each OS.

# Common variables
export PYTHONPATH="."
export PYTHONUNBUFFERED="1"

# Detect operating system
OS="$(uname -s)"

if [ "$OS" = "Darwin" ]; then
    # echo "Running on macOS via uv..."
    uv run joplin_lite/joplin-lite.py "$@"
elif [ "$OS" = "Linux" ]; then
    # echo "Running on Linux via virtualenv python..."
    ./.venv/bin/python -u joplin_lite/joplin-lite.py "$@"
else
    echo "Unsupported operating system: $OS"
    exit 1
fi
