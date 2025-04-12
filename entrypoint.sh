#!/bin/sh

export PYTHONPATH=/app

sleep 5

# Run migrations
alembic upgrade head

# Run server
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
