from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.api import router as auth_router
from tasks.api import router as tasks_router
from database import get_async_db

# Импорт Celery задач
try:
    from celery_tasks import example_task, send_notification, process_data, create_random_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    print("Celery tasks not available")

# Import models for Alembic
from auth.schema import User
from tasks.models import Task

# Настройка безопасности для Swagger UI
security = HTTPBearer()

app = FastAPI(
    title="FastAPI Task Management",
    description="API для управления задачами с аутентификацией",
    version="1.0.0",
    # Настройка схемы безопасности для Swagger UI
    openapi_tags=[
        {
            "name": "auth",
            "description": "Операции аутентификации и авторизации",
        },
        {
            "name": "tasks", 
            "description": "Операции с задачами (требуют аутентификации)",
        },
        {
            "name": "agentic_system",
            "description": "AI агентная система для работы с файлами",
        }
    ]
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://104.248.131.146:3000"  # Добавляем IP сервера
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["auth"])
app.include_router(tasks_router, tags=["tasks"])

# Импортируем agentic router отдельно
from agentic_system.api import router as agentic_router
app.include_router(agentic_router, tags=["agentic_system"])


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/health")
async def check_health(db: AsyncSession = Depends(get_async_db)):
    try:
        await db.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(
            status_code=500, detail="Database connection failed"
        )

    return {"status": "ok", "database": "connected"}


# Celery эндпоинты
@app.post("/celery/example")
async def run_example_task(name: str):
    """Запустить пример Celery задачи"""
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery не доступен")
    
    task = example_task.delay(name)
    return {
        "task_id": task.id,
        "status": "Task queued",
        "message": f"Пример задачи поставлен в очередь для {name}"
    }


@app.post("/celery/notification")
async def send_notification_task(message: str, recipient: str):
    """Отправить уведомление через Celery"""
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery не доступен")
    
    task = send_notification.delay(message, recipient)
    return {
        "task_id": task.id,
        "status": "Task queued",
        "message": f"Задача уведомления поставлена в очередь для {recipient}"
    }


@app.post("/celery/process")
async def process_data_task(data: dict):
    """Обработать данные через Celery"""
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery не доступен")
    
    task = process_data.delay(data)
    return {
        "task_id": task.id,
        "status": "Task queued",
        "message": "Задача обработки данных поставлена в очередь"
    }


@app.post("/celery/create-random-task")
async def trigger_random_task():
    """Вручную запустить создание случайной задачи"""
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery не доступен")
    
    task = create_random_task.delay()
    return {
        "task_id": task.id,
        "status": "Task queued",
        "message": "Задача создания случайной задачи поставлена в очередь"
    }


@app.get("/celery/task/{task_id}/status")
async def get_task_status(task_id: str):
    """Получить статус Celery задачи"""
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery не доступен")
    
    try:
        from celery.result import AsyncResult
        from celery_app import celery_app
        
        result = AsyncResult(task_id, app=celery_app)
        
        return {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
            "info": result.info if result.state == 'PENDING' else result.result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статуса задачи: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
