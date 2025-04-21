#!/bin/sh

# Ждем, пока база данных станет доступной
echo "Waiting for database to be ready..."
until pg_isready -h db -U ${DB_USER}; do
  sleep 2
done

# Применяем миграции
echo "Applying database migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000