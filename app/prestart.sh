#!/usr/bin/env bash

set -e

ALEMBIC_PATH=$(find . -name "alembic.ini" -type f 2>/dev/null)

if [ -z "$ALEMBIC_PATH" ]; then
    echo "Error: alembic.ini not found"
    exit 1
fi

START_DIR="$PWD"

cd "$(dirname "$ALEMBIC_PATH")"
uv run alembic upgrade head
cd "$START_DIR"

exec "$@"
