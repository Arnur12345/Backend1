# Решение проблем с Docker

## Проблема: Input/Output Error

Если вы видите ошибки типа:
```
write /var/lib/docker/buildkit/containerd-overlayfs/metadata_v2.db: input/output error
```

Это указывает на проблемы с Docker Desktop. Выполните следующие шаги:

### 1. Полная очистка Docker

```powershell
# Остановить все контейнеры
docker-compose down

# Очистить все
docker system prune -a -f --volumes

# Перезапустить Docker Desktop
```

### 2. Если проблема не решена

1. **Закройте Docker Desktop полностью**
2. **Перезагрузите компьютер**
3. **Запустите Docker Desktop заново**

### 3. Альтернативный запуск

Если Docker продолжает давать ошибки, попробуйте запустить сервисы по отдельности:

#### Запуск только базы данных:
```powershell
docker run -d --name postgres-db -p 5433:5432 -e POSTGRES_USER=username -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgresdb postgres:16
```

#### Запуск бэкенда локально:
```powershell
cd 2lecture
# Создайте .env файл с DATABASE_URL=postgresql://username:password@localhost:5433/postgresdb
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

#### Запуск фронтенда локально:
```powershell
cd frontend
npm install
npm run dev
```

## Проблема: Порт 5432 занят

Если видите ошибку:
```
Bind for 0.0.0.0:5432 failed: port is already allocated
```

### Решение:
1. **Остановите локальный PostgreSQL** (если установлен)
2. **Или используйте другой порт** (уже настроено в docker-compose.yml - порт 5433)

## Текущая конфигурация

После всех исправлений:

- **База данных**: PostgreSQL на порту 5433 (внешний)
- **Бэкенд**: FastAPI на порту 8000
- **Фронтенд**: React + Vite на порту 3000

### Доступ к сервисам:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5433

## Команды для запуска

### Обычный запуск:
```powershell
docker-compose up --build
```

### Запуск в фоне:
```powershell
docker-compose up -d --build
```

### Остановка:
```powershell
docker-compose down
```

### Полная очистка и перезапуск:
```powershell
docker-compose down -v
docker system prune -f
docker-compose up --build
``` 