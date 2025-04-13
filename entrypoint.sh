#!/bin/sh

export PYTHONPATH="/app:/usr/local/lib/python3.13/site-packages"

echo "Python path: $PYTHONPATH" >&2
echo "Contenido de /app:" >&2
ls -la /app >&2

# Run server
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
