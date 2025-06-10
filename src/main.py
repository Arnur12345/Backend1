from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import settings
from src.database import init_db
from src.auth.router import router as auth_router
from src.tasks.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app_configs = {
    "title": "Task Manager API",
    "description": "A simple task management API with JWT authentication",
    "version": "1.0.0",
    "lifespan": lifespan
}

if settings.ENVIRONMENT not in settings.SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])


@app.get("/")
async def root():
    return {"message": "Task Manager API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 