#!/bin/sh
set -e

echo "Waiting for database to be ready..."
python -c "
import socket
import time
import os

host = os.getenv('DB_HOST', 'localhost')
port = int(os.getenv('DB_PORT', 5432))

for attempt in range(30):
    try:
        socket.create_connection((host, port), timeout=1)
        print('Database is ready!')
        exit(0)
    except (socket.timeout, socket.error):
        if attempt < 29:
            print(f'Attempt {attempt + 1}/30: Waiting for database...')
            time.sleep(1)
        else:
            print('Failed to connect to database')
            exit(1)
"

echo "Running migrations (errors are logged but do not block startup)..."
python -m alembic -c alembic.ini upgrade head 2>&1 || echo "⚠️  Migration warning (app continues)"

echo "Starting FastAPI application..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop uvloop
