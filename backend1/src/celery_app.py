import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем URL Redis из переменных окружения
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Создаем экземпляр Celery
celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url,
    include=["celery_tasks"]
)

# Настройки Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    task_track_started=True,
    task_serializer_kwargs={
        'ensure_ascii': False
    }
)

# Настройка периодических задач
celery_app.conf.beat_schedule = {
    'create-random-task-every-minute': {
        'task': 'celery_tasks.create_random_task',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}

if __name__ == "__main__":
    celery_app.start() 