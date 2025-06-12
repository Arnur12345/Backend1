# AI Агентная Система для Работы с Файлами

## Описание

Система позволяет загружать файлы и задавать вопросы различным AI агентам на основе содержимого файлов. Поддерживает несколько типов агентов с разными возможностями.

## Возможности

- 📁 Загрузка файлов (TXT, CSV, JSON, MD, HTML до 10MB)
- 🤖 Выбор из нескольких AI агентов
- 💬 Интерактивный чат с агентами
- 📝 История разговоров для каждого файла
- 🔒 Аутентификация пользователей
- 🌐 Современный веб-интерфейс

## Поддерживаемые агенты

1. **SimpleAgent** - Базовый агент без внешних API
2. **PydanticAIAgent** - Агент с использованием PydanticAI и OpenAI API
3. **LangchainAgent** - Агент с использованием Langchain и OpenAI API

## API Endpoints

### Агентная система
- `POST /agentic/upload` - Загрузка файла
- `GET /agentic/files` - Список загруженных файлов
- `DELETE /agentic/files/{file_id}` - Удаление файла
- `GET /agentic/agents` - Список доступных агентов
- `POST /agentic/ask` - Задать вопрос агенту
- `GET /agentic/chat/{file_id}` - История чата для файла
- `GET /agentic/health` - Проверка здоровья системы

### Аутентификация
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/token` - Получение токена доступа
- `GET /auth/me` - Информация о текущем пользователе

## Установка и запуск

### Backend

1. Установите зависимости:
```bash
cd backend1
pip install -r requirements.txt
```

2. Настройте переменные окружения в `.env`:
```
DATABASE_URL=postgresql+asyncpg://username:password@db:5432/postgresdb
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key  # Опционально для AI агентов
```

3. Запустите миграции:
```bash
alembic upgrade head
```

4. Запустите сервер:
```bash
uvicorn main:app --reload
```

### Frontend

1. Установите зависимости:
```bash
cd frontend
npm install
```

2. Запустите в режиме разработки:
```bash
npm run dev
```

### Docker Compose

Запустите всю систему одной командой:
```bash
docker-compose up -d
```

## Использование

### Веб-интерфейс

1. Откройте http://localhost:3000
2. Зарегистрируйтесь или войдите в систему
3. Перейдите в раздел "AI Агенты"
4. Загрузите файл (перетащите или выберите)
5. Выберите агента
6. Задавайте вопросы в чате

### API

1. Зарегистрируйтесь:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "email": "user@example.com", "password": "password123"}'
```

2. Получите токен:
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

3. Загрузите файл:
```bash
curl -X POST "http://localhost:8000/agentic/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_document.txt"
```

4. Задайте вопрос:
```bash
curl -X POST "http://localhost:8000/agentic/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "FILE_ID", "message": "Что такое FastAPI?", "agent_name": "SimpleAgent"}'
```

### Терминальный интерфейс

Для тестирования доступен CLI интерфейс:
```bash
cd backend1/src
python terminal_chat.py
```

Команды:
- `upload <file_path>` - Загрузить файл
- `list` - Показать файлы
- `select <file_id>` - Выбрать файл
- `agents` - Показать агентов
- `history` - История чата
- `clear` - Очистить экран
- `help` - Помощь
- `exit` - Выход

## Примеры использования

### Анализ документации
Загрузите файл с документацией и задавайте вопросы:
- "Какие основные возможности описаны в документе?"
- "Как установить эту технологию?"
- "Приведи пример кода из документа"

### Анализ данных CSV
Загрузите CSV файл и анализируйте данные:
- "Сколько записей в файле?"
- "Какие колонки есть в данных?"
- "Найди аномалии в данных"

### Обработка JSON
Загрузите JSON файл и работайте со структурой:
- "Какая структура у этого JSON?"
- "Найди все поля типа string"
- "Преобразуй данные в другой формат"

## Архитектура

```
├── backend1/src/
│   ├── agentic_system/          # Агентная система
│   │   ├── agents/              # Реализации агентов
│   │   ├── file_manager.py      # Управление файлами
│   │   ├── agent_manager.py     # Координация агентов
│   │   ├── api.py              # API endpoints
│   │   └── schema.py           # Pydantic модели
│   ├── auth/                   # Аутентификация
│   ├── tasks/                  # Система задач
│   └── main.py                 # Главный файл приложения
├── frontend/src/
│   ├── modules/agentic/        # Модуль агентной системы
│   │   ├── ui/                 # React компоненты
│   │   └── pages/              # Страницы
│   └── lib/                    # API клиент и типы
└── docker-compose.yml          # Docker конфигурация
```

## Конфигурация агентов

Агенты автоматически определяют доступность на основе наличия API ключей:

- **SimpleAgent**: Всегда доступен, работает без внешних API
- **PydanticAIAgent**: Требует OPENAI_API_KEY
- **LangchainAgent**: Требует OPENAI_API_KEY

## Безопасность

- JWT токены для аутентификации
- Валидация типов и размеров файлов
- Изоляция файлов по пользователям
- CORS настройки для фронтенда

## Мониторинг

Проверка здоровья системы:
```bash
curl http://localhost:8000/agentic/health
```

Ответ содержит информацию о:
- Статусе системы
- Количестве доступных агентов
- Количестве файлов
- Состоянии директории загрузок

## Troubleshooting

### Агенты недоступны
- Проверьте наличие OPENAI_API_KEY в переменных окружения
- Убедитесь, что API ключ валидный

### Ошибки загрузки файлов
- Проверьте размер файла (максимум 10MB)
- Убедитесь, что тип файла поддерживается
- Проверьте права доступа к папке uploads/

### Проблемы с базой данных
- Запустите миграции: `alembic upgrade head`
- Проверьте подключение к PostgreSQL
- Убедитесь, что DATABASE_URL корректный

## Разработка

Для добавления нового агента:

1. Создайте класс, наследующий от `BaseAgent`
2. Реализуйте метод `process_query`
3. Добавьте агента в `AgentManager`
4. Обновите конфигурацию доступности

Пример:
```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CustomAgent",
            description="Описание вашего агента"
        )
    
    async def process_query(self, file_content: str, query: str) -> str:
        # Ваша логика обработки
        return "Ответ агента"
``` 