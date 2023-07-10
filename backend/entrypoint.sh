#!/bin/sh

echo "Waiting for psql to start..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.1
done
echo "PostgreSQL started"

if [ "$APP_TYPE" = "HTTP" ]; then
  alembic upgrade head
fi

python main.py

exec "$@"