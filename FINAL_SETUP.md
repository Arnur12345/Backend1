# Финальная инструкция по настройке проекта

## ⚠️ Проблема с Docker

У вас серьезные проблемы с Docker Desktop (ошибки ввода-вывода). Это требует перезагрузки Docker или системы.

## 🔧 Решение проблемы

### Вариант 1: Перезапуск Docker (Рекомендуется)

1. **Закройте Docker Desktop полностью**
2. **Перезагрузите компьютер**
3. **Запустите Docker Desktop**
4. **Выполните команду:**
   ```powershell
   docker-compose up --build
   ```

### Вариант 2: Локальный запуск (Если Docker не работает)

#### 1. Запуск базы данных
Установите PostgreSQL локально или используйте онлайн сервис.

#### 2. Запуск бэкенда
```powershell
cd 2lecture

# Создайте файл .env
copy env.txt .env
# Отредактируйте .env, установите DATABASE_URL для локальной БД

# Установите зависимости
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Запустите сервер
cd src
uvicorn main:app --reload
```

#### 3. Запуск фронтенда
```powershell
cd frontend
npm install
npm run dev
```

## 📋 Созданные файлы

Я создал следующие файлы для вашего проекта:

### 1. `docker-compose.yml`
- Настроен для 3 сервисов: база данных (порт 5433), бэкенд (порт 8000), фронтенд (порт 3000)
- Исправлен конфликт портов (PostgreSQL на 5433 вместо 5432)

### 2. `frontend/Dockerfile`
- Упрощенный Dockerfile для React + Vite
- Использует Node.js 20-slim
- Исправлены проблемы с rollup

### 3. `DOCKER_TROUBLESHOOTING.md`
- Подробные инструкции по решению проблем с Docker

## 🚀 После исправления Docker

Когда Docker заработает, используйте эти команды:

```powershell
# Запуск всех сервисов
docker-compose up --build

# Доступ к сервисам:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Backend Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5433
```

## 📝 Что нужно сделать

1. **Перезагрузите систему** для исправления Docker
2. **Создайте файл `.env`** в папке `2lecture/`:
   ```env
   DATABASE_URL=postgresql://username:password@db:5432/postgresdb
   SECRET_KEY=your-secret-key-here
   GROQ_API_KEY=your-groq-api-key-here
   DEBUG=True
   ENVIRONMENT=development
   ```
3. **Запустите проект** командой `docker-compose up --build`

## 🔍 Проверка работы

После запуска проверьте:
- ✅ База данных: `docker logs fastapi_struct-db-1`
- ✅ Бэкенд: http://localhost:8000/docs
- ✅ Фронтенд: http://localhost:3000

Проект готов к работе! 🎉 