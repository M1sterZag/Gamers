#!/bin/sh

# Если backend контейнер не может этот скрипт нужно поменять кодировку этого файла из CRLF на LF (linux система)

# Ждем, пока база данных станет доступной
echo "Waiting for database to be ready..."
until pg_isready -h db -U ${DB_USER}; do
  sleep 2
done

# Применяем миграции
echo "Applying database migrations..."
alembic upgrade head

# Запускаем скрипт для создания администратора
echo "Creating admin user..."
python admin_cli.py --username="$ADMIN_USERNAME" --email="$ADMIN_EMAIL" --password="$ADMIN_PASS"

# Запускаем приложение
echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000