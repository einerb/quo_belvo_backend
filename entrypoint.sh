sleep 5

# Rin migrations
alembic upgrade head

# Run Server
exec uvicorn app.main:app --host 0.0.0.0 --port 8080