#!/usr/bin/env bash
set -euo pipefail

run_migrations() {
  echo "Running database migrations..."
  alembic upgrade head
}

if [[ $# -gt 0 ]]; then
  case "$1" in
    uvicorn|gunicorn)
      run_migrations
      exec "$@"
      ;;
    *)
      exec "$@"
      ;;
  esac
else
  run_migrations
  echo "Starting application..."
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi