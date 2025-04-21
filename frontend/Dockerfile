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

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]