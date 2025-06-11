from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from tasks.crud import TaskDAO
from tasks.schema import TaskCreate, TaskUpdate, TaskResponse
from tasks.exceptions import (
    TaskNotFoundException,
    TaskCreationException,
    TaskUpdateException,
    TaskDeletionException,
    raise_http_exception
)


class TaskService:
    
    @staticmethod
    async def create_task(task_data: TaskCreate, user_id: int, db: AsyncSession) -> TaskResponse:
        """Create a new task for the user"""
        try:
            db_task = await TaskDAO.create_task(task_data, user_id, db)
            return TaskResponse.model_validate(db_task)
        except Exception as e:
            raise_http_exception(TaskCreationException(f"Failed to create task: {str(e)}"))

    @staticmethod
    async def get_user_tasks(user_id: int, db: AsyncSession) -> List[TaskResponse]:
        """Get all tasks for the user"""
        try:
            tasks = await TaskDAO.get_user_tasks(user_id, db)
            return [TaskResponse.model_validate(task) for task in tasks]
        except Exception as e:
            raise_http_exception(TaskNotFoundException(f"Failed to retrieve tasks: {str(e)}"))

    @staticmethod
    async def get_task_by_id(task_id: int, user_id: int, db: AsyncSession) -> TaskResponse:
        """Get a specific task by ID for the user"""
        try:
            task = await TaskDAO.get_user_task_by_id_or_raise(task_id, user_id, db)
            return TaskResponse.model_validate(task)
        except TaskNotFoundException as e:
            raise_http_exception(e)
        except Exception as e:
            raise_http_exception(TaskNotFoundException(f"Failed to retrieve task: {str(e)}"))

    @staticmethod
    async def update_task(task_id: int, user_id: int, task_data: TaskUpdate, db: AsyncSession) -> TaskResponse:
        """Update a task"""
        try:
            updated_task = await TaskDAO.update_task(task_id, user_id, task_data, db)
            return TaskResponse.model_validate(updated_task)
        except TaskNotFoundException as e:
            raise_http_exception(e)
        except Exception as e:
            raise_http_exception(TaskUpdateException(f"Failed to update task: {str(e)}"))

    @staticmethod
    async def delete_task(task_id: int, user_id: int, db: AsyncSession) -> dict:
        """Delete a task"""
        try:
            await TaskDAO.delete_task(task_id, user_id, db)
            return {"message": "Task deleted successfully"}
        except TaskNotFoundException as e:
            raise_http_exception(e)
        except Exception as e:
            raise_http_exception(TaskDeletionException(f"Failed to delete task: {str(e)}"))

    @staticmethod
    async def get_completed_tasks(user_id: int, db: AsyncSession) -> List[TaskResponse]:
        """Get all completed tasks for the user"""
        try:
            tasks = await TaskDAO.get_completed_tasks(user_id, db)
            return [TaskResponse.model_validate(task) for task in tasks]
        except Exception as e:
            raise_http_exception(TaskNotFoundException(f"Failed to retrieve completed tasks: {str(e)}"))

    @staticmethod
    async def get_pending_tasks(user_id: int, db: AsyncSession) -> List[TaskResponse]:
        """Get all pending tasks for the user"""
        try:
            tasks = await TaskDAO.get_pending_tasks(user_id, db)
            return [TaskResponse.model_validate(task) for task in tasks]
        except Exception as e:
            raise_http_exception(TaskNotFoundException(f"Failed to retrieve pending tasks: {str(e)}"))

    @staticmethod
    async def mark_task_completed(task_id: int, user_id: int, db: AsyncSession) -> TaskResponse:
        """Mark a task as completed"""
        try:
            task_update = TaskUpdate(completed=True)
            updated_task = await TaskDAO.update_task(task_id, user_id, task_update, db)
            return TaskResponse.model_validate(updated_task)
        except TaskNotFoundException as e:
            raise_http_exception(e)
        except Exception as e:
            raise_http_exception(TaskUpdateException(f"Failed to mark task as completed: {str(e)}"))

    @staticmethod
    async def mark_task_pending(task_id: int, user_id: int, db: AsyncSession) -> TaskResponse:
        """Mark a task as pending"""
        try:
            task_update = TaskUpdate(completed=False)
            updated_task = await TaskDAO.update_task(task_id, user_id, task_update, db)
            return TaskResponse.model_validate(updated_task)
        except TaskNotFoundException as e:
            raise_http_exception(e)
        except Exception as e:
            raise_http_exception(TaskUpdateException(f"Failed to mark task as pending: {str(e)}")) 