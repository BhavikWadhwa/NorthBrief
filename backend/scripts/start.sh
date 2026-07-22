#!/bin/sh
set -eu

python -m app.db.prepare
alembic upgrade head
python -m app.seed
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
