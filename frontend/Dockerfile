# Базовый образ Node.js
FROM node:22.14-alpine AS builder

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходного кода
COPY . .

# Сборка проекта
RUN npm run build

# Этап для nginx
FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Кастомный конфиг для проксирования к backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80