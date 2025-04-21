# 🎮 Gamers — приложение для поиска тиммейтов в играх

**Gamers** — это платформа для поиска команд и игроков в популярные онлайн-игры, такие, как Dota 2, CS:GO и другие.
Пользователи могут создавать команды, указывая параметры (игра, количество участников, время сбора), а другие
пользователи могут присоединяться к ним. Также реализованы функции чата для команд, личных сообщений и добавления в
друзья. 🚀

---

## ✨ Основные функции

- **📝 Регистрация и аутентификация**:
    - Регистрация через email и ~~Google OAuth~~.
    - Токены JWT для аутентификации и авторизации.
    - Хеширование паролей с использованием `bcrypt`.

- **🔍 Создание и поиск команд**:
    - Указание игры, количества участников, времени сбора.
    - Фильтрация команд по параметрам через REST API.
    - Возможность создания и удаления команд.

- **💬 Чат**:
    - Автоматическое создание чата для каждой команды.
    - Личные сообщения между пользователями в реальном времени через WebSocket (`starlette`).
    - Хранение истории сообщений в базе данных.

- **👥 Друзья**:
    - Добавление пользователей в друзья.
    - Отображение списка друзей.

---

## 🏗 Архитектура и паттерны проектирования

### Общая архитектура

Проект использует **многослойную архитектуру** (Layered Architecture):

- **Фронтенд**: SPA (Single Page Application) на Vue.js, взаимодействие с бэкендом через REST API и WebSocket.
- **Бэкенд**: RESTful API на FastAPI с асинхронной обработкой запросов.
- **База данных**: PostgreSQL для хранения данных о пользователях, командах, чатах и друзьях.

### 📁 Структура проекта

Проект разделен на 2 основных модуля:

1. **backend**: Логика сервера, API и взаимодействие с базой данных.
2. **frontend**: Клиентская часть на Vue.js.

#### Структура backend

- `app/auth`: Модуль аутентификации (OAuth, JWT).
- `app/chat`: Логика чата (реализация через WebSocket).
- `app/dao`: Слой доступа к данным (Data Access Object).
- `app/game`: Модуль для управления играми.
- `app/team`: Модуль управления командами.
- `app/migration`: Миграции базы данных с использованием Alembic.

#### Структура frontend

- `src/api`: Взаимодействие с REST API бэкенда.
- `src/components`: Переиспользуемые Vue-компоненты.
- `src/router`: Маршрутизация на основе `vue-router`.
- `src/stores`: Хранилище состояния через `pinia`.
- `src/views`: Основные страницы приложения.

### 🛠 Используемые паттерны

- **Repository**: В модуле `dao` для абстракции доступа к базе данных.
- **Dependency Injection**: Использование зависимостей в FastAPI через `Depends`.
- ~~**Observer**: Для обработки событий в реальном времени (чаты через WebSocket).~~
- ~~**Factory**: Для создания объектов (например, в модуле `auth` для генерации токенов).~~

---

## 🧰 Технологии

### Бэкенд

- ![Python](https://img.shields.io/badge/-Python%203.13-3776AB?style=flat&logo=python) Основной язык программирования.
- ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=fastapi) Асинхронный фреймворк для создания
  REST API.
- ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-003087?style=flat) ORM для работы с PostgreSQL.
- ![Alembic](https://img.shields.io/badge/-Alembic-003087?style=flat) Инструмент миграций базы данных.
- ![asyncpg](https://img.shields.io/badge/-asyncpg-003087?style=flat) Асинхронный драйвер для PostgreSQL.
- ![JWT](https://img.shields.io/badge/-JWT%20(python--jose)-000000?style=flat) Для аутентификации и авторизации.
- ![bcrypt](https://img.shields.io/badge/-bcrypt-000000?style=flat) Для хеширования паролей.
- ![Loguru](https://img.shields.io/badge/-Loguru-000000?style=flat) Для логирования.
- ![Uvicorn](https://img.shields.io/badge/-Uvicorn-293742?style=flat) ASGI-сервер для запуска FastAPI.
- ~~![Starlette](https://img.shields.io/badge/-Starlette-293742?style=flat) WebSocket для чатов.~~

### Фронтенд

- ![Vue.js](https://img.shields.io/badge/-Vue.js%203-4FC08D?style=flat&logo=vuedotjs) Основной фреймворк для построения
  интерфейса.
- ![Vue Router](https://img.shields.io/badge/-Vue%20Router-4FC08D?style=flat&logo=vuedotjs) Для клиентской
  маршрутизации.
- ![Pinia](https://img.shields.io/badge/-Pinia-4FC08D?style=flat) Для управления состоянием.
- ![Axios](https://img.shields.io/badge/-Axios-5A29E4?style=flat&logo=axios) Для HTTP-запросов к API.
- ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=flat&logo=vite) Для сборки и горячей перезагрузки.
- ![TailwindCSS](https://img.shields.io/badge/-TailwindCSS-38B2AC?style=flat&logo=tailwindcss) Для стилизации.
- ~~![vue-google-signin-button](https://img.shields.io/badge/-vue--google--signin--button-4285F4?style=flat&logo=google)
  Для интеграции Google OAuth.~~

### Инфраструктура

- ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker) Контейнеризация приложения.
- ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat&logo=postgresql) Реляционная база данных.
- ![Git](https://img.shields.io/badge/-Git-F05032?style=flat&logo=git) Для контроля версий.

---

## 🚀 Установка и запуск

Для создания миграции базы

```bash
cd backend
alembic revision --autogenerate -m "your message"
```

Для применения последней миграции базы

```bash
cd backend
alembic upgrade head
```

### 📋 Требования

- Python 3.13+
- Node.js 18+
- PostgreSQL 15+
- Docker
- Git