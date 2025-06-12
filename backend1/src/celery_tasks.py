import random
import asyncio
from datetime import datetime
from celery import current_task
from celery_app import celery_app
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from tasks.crud import TaskDAO
from tasks.schema import TaskCreate

# Список случайных данных для создания задач
RANDOM_TASKS_DATA = [
    {
        "title": "Изучить новую технологию",
        "description": "Потратить время на изучение новой технологии или фреймворка"
    },
    {
        "title": "Написать документацию",
        "description": "Создать подробную документацию для текущего проекта"
    },
    {
        "title": "Провести код-ревью",
        "description": "Проверить код коллег и оставить конструктивные комментарии"
    },
    {
        "title": "Оптимизировать базу данных",
        "description": "Проанализировать и оптимизировать запросы к базе данных"
    },
    {
        "title": "Настроить мониторинг",
        "description": "Внедрить систему мониторинга для отслеживания производительности"
    },
    {
        "title": "Обновить зависимости",
        "description": "Проверить и обновить все зависимости проекта до актуальных версий"
    },
    {
        "title": "Написать тесты",
        "description": "Создать unit и integration тесты для новой функциональности"
    },
    {
        "title": "Рефакторинг кода",
        "description": "Улучшить структуру и читаемость существующего кода"
    },
    {
        "title": "Настроить CI/CD",
        "description": "Автоматизировать процесс сборки и развертывания приложения"
    },
    {
        "title": "Исследовать безопасность",
        "description": "Провести аудит безопасности и устранить найденные уязвимости"
    }
]

# Список пользователей для случайного назначения задач
USER_IDS = [1, 2, 3, 4, 5]  # Предполагаем, что у нас есть пользователи с ID от 1 до 5


@celery_app.task(bind=True)
def example_task(self, name: str):
    """Пример простой задачи"""
    try:
        # Симуляция работы
        import time
        time.sleep(2)
        
        result = f"Задача выполнена для {name} в {datetime.now()}"
        
        # Обновляем прогресс задачи
        self.update_state(
            state='SUCCESS',
            meta={'result': result, 'completed_at': datetime.now().isoformat()}
        )
        
        return result
    except Exception as exc:
        self.update_state(
            state='FAILURE',
            meta={'error': str(exc)}
        )
        raise


@celery_app.task(bind=True)
def send_notification(self, message: str, recipient: str):
    """Задача отправки уведомления"""
    try:
        # Симуляция отправки уведомления
        import time
        time.sleep(1)
        
        result = f"Уведомление '{message}' отправлено получателю {recipient}"
        
        self.update_state(
            state='SUCCESS',
            meta={'result': result, 'sent_at': datetime.now().isoformat()}
        )
        
        return result
    except Exception as exc:
        self.update_state(
            state='FAILURE',
            meta={'error': str(exc)}
        )
        raise


@celery_app.task(bind=True)
def process_data(self, data: dict):
    """Задача обработки данных"""
    try:
        # Симуляция обработки данных
        import time
        time.sleep(3)
        
        processed_data = {
            "original": data,
            "processed_at": datetime.now().isoformat(),
            "items_count": len(data) if isinstance(data, (list, dict)) else 1,
            "status": "processed"
        }
        
        self.update_state(
            state='SUCCESS',
            meta={'result': processed_data}
        )
        
        return processed_data
    except Exception as exc:
        self.update_state(
            state='FAILURE',
            meta={'error': str(exc)}
        )
        raise


@celery_app.task(bind=True)
def create_random_task(self):
    """Периодическая задача для создания случайной задачи каждую минуту"""
    try:
        # Выбираем случайные данные
        random_task_data = random.choice(RANDOM_TASKS_DATA)
        random_user_id = random.choice(USER_IDS)
        
        # Создаем задачу асинхронно
        async def create_task():
            async with AsyncSessionLocal() as session:
                
                task_create = TaskCreate(
                    title=random_task_data["title"],
                    description=random_task_data["description"]
                )
                
                try:
                    new_task = await TaskDAO.create_task(
                        task_data=task_create,
                        user_id=random_user_id,
                        db=session
                    )
                    return {
                        "task_id": new_task.id,
                        "title": new_task.title,
                        "description": new_task.description,
                        "user_id": new_task.user_id,
                        "created_at": new_task.created_at.isoformat()
                    }
                except Exception as e:
                    # Если пользователь не существует, создаем задачу для пользователя 1
                    new_task = await TaskDAO.create_task(
                        task_data=task_create,
                        user_id=1,
                        db=session
                    )
                    return {
                        "task_id": new_task.id,
                        "title": new_task.title,
                        "description": new_task.description,
                        "user_id": new_task.user_id,
                        "created_at": new_task.created_at.isoformat(),
                        "note": f"Создано для пользователя 1 вместо {random_user_id}"
                    }
        
        # Запускаем асинхронную функцию
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(create_task())
        loop.close()
        
        self.update_state(
            state='SUCCESS',
            meta={'result': result}
        )
        
        return result
        
    except Exception as exc:
        error_msg = f"Ошибка при создании случайной задачи: {str(exc)}"
        self.update_state(
            state='FAILURE',
            meta={'error': error_msg}
        )
        raise Exception(error_msg) 