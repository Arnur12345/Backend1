# Task Manager API

Современный REST API для управления задачами, построенный на FastAPI с JWT аутентификацией и PostgreSQL.

## Особенности

- 🔐 JWT аутентификация и авторизация
- 📝 CRUD операции для задач
- 🐘 PostgreSQL база данных
- 🚀 Async/await поддержка
- 🐳 Docker и Docker Compose
- 📊 Alembic миграции
- 🔧 Makefile для удобства

## Быстрый старт

### С Docker Compose (рекомендуется)

```bash
# Клонировать репозиторий
git clone <your-repo-url>
cd fastapi_struct

# Запустить все сервисы
make dev

# Или вручную
docker-compose up --build
```

API будет доступен по адресу: http://localhost:8000

### Локальная разработка

```bash
# Установить зависимости
make install

# Запустить PostgreSQL в Docker
docker run -d \
  --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=taskdb \
  -p 5432:5432 \
  postgres:15-alpine

# Применить миграции
alembic upgrade head

# Запустить приложение
uvicorn src.main:app --reload
```

## API Эндпоинты

### Аутентификация
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход в систему
- `GET /auth/me` - Информация о текущем пользователе

### Задачи (требуют аутентификации)
- `POST /api/create_task` - Создать задачу
- `GET /api/get_tasks` - Получить все мои задачи
- `GET /api/tasks/{task_id}` - Получить задачу по ID
- `PUT /api/tasks/{task_id}` - Обновить задачу
- `DELETE /api/tasks/{task_id}` - Удалить задачу

## Makefile команды

```bash
make help          # Показать все доступные команды
make build         # Собрать Docker образы
make up            # Запустить сервисы
make down          # Остановить сервисы
make logs          # Показать логи
make shell         # Войти в контейнер приложения
make db-shell      # Войти в PostgreSQL
make migrate       # Создать новую миграцию
make upgrade       # Применить миграции
make clean         # Очистить контейнеры и volumes
```

## Структура проекта

```
fastapi_struct/
├── src/
│   ├── auth/           # Модуль аутентификации
│   │   ├── models.py   # SQLAlchemy модели
│   │   ├── schemas.py  # Pydantic схемы
│   │   ├── service.py  # Бизнес логика
│   │   ├── router.py   # API роуты
│   │   └── dependencies.py # FastAPI зависимости
│   ├── tasks/          # Модуль задач
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── router.py
│   ├── config.py       # Конфигурация приложения
│   ├── database.py     # Подключение к БД
│   └── main.py         # Точка входа FastAPI
├── alembic/            # Миграции базы данных
├── docker-compose.yml  # Docker Compose конфигурация
├── Dockerfile          # Docker образ
├── Makefile           # Команды для разработки
└── requirements.txt   # Python зависимости
```

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```env
ENVIRONMENT=local
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/taskdb
```

## Примеры использования

### Регистрация пользователя
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword"
  }'
```

### Вход в систему
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

### Создание задачи
```bash
curl -X POST "http://localhost:8000/api/create_task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Моя первая задача",
    "description": "Описание задачи"
  }'
```

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - инструмент для миграций БД
- **PostgreSQL** - реляционная база данных
- **JWT** - токены для аутентификации
- **Docker** - контейнеризация
- **Pydantic** - валидация данных 