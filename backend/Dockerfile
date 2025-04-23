# Базовый образ Python
FROM python:3.13-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y postgresql-client

# Копирование исходного кода
WORKDIR /gamers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Копирование остального кода
COPY . .

CMD [ "sh", "./entrypoint.sh" ]