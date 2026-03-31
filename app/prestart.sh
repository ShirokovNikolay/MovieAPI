#!/usr/bin/env bash

uv run alembic upgrade head

exec "$@"