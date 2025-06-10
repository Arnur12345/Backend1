# 🚀 Быстрый старт

## Запуск за 30 секунд

```bash
# 1. Запустить все сервисы
make dev

# 2. Открыть в браузере
# http://localhost:8000/docs
```

## 🔧 Если Docker не запускается

### Быстрое решение:
```bash
# Windows
fix_docker.bat

# Linux/Mac
./fix_docker.sh

# Или вручную
make fix-docker
```

### Проблема с памятью/диском:
```bash
# Очистить Docker
docker system prune -af
docker volume prune -f

# Windows: перезапустить Docker Desktop
# Linux: sudo systemctl restart docker

# Попробовать снова
make dev
```

### Альтернативный запуск без Docker:
```bash
# 1. Установить PostgreSQL локально
sudo apt install postgresql postgresql-contrib

# 2. Создать базу данных
sudo -u postgres createdb taskdb
sudo -u postgres psql -c "CREATE USER user WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE taskdb TO user;"

# 3. Установить зависимости Python
pip install -r requirements.txt

# 4. Применить миграции
alembic upgrade head

# 5. Запустить приложение
uvicorn src.main:app --reload
```

## Миграции

```bash
# Создать миграцию
make migrate msg="add new field"

# Применить миграции
make upgrade

# Откатить последнюю миграцию
make downgrade
```

## Полезные команды

```bash
make help          # Все команды
make logs          # Логи
make shell         # Войти в контейнер
make db-shell      # Войти в PostgreSQL
make clean         # Очистить все
```

## Тестирование API

### 1. Регистрация
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@test.com", "password": "123456"}'
```

### 2. Логин
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "123456"}'
```

### 3. Создать задачу (с токеном)
```bash
curl -X POST "http://localhost:8000/api/create_task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title": "Моя задача", "description": "Описание"}'
```

### 4. Получить задачи
```bash
curl -X GET "http://localhost:8000/api/get_tasks" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Если что-то сломалось

```bash
make clean    # Удалить все
make dev      # Запустить заново
```

**Готово! 🎉** 