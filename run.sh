#!/usr/bin/env bash
# Render a course to PDF. Usage: ./run.sh <slug> [render.py flags...]
# Wraps: uv run --quiet --with markdown --with pygments python build/render.py <slug> ...
set -e
if [ -z "$1" ]; then
    echo "usage: ./run.sh <slug> [render.py flags...]" >&2
    exit 2
fi
cd "$(dirname "$0")"
exec uv run --quiet --with markdown --with pygments python build/render.py "$@"
