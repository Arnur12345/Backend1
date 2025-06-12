from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.api import router as auth_router
from tasks.api import router as tasks_router
from database import get_async_db

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
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Конкретные домены для фронтенда
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
