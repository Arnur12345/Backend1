from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional

from tasks.models import Task
from tasks.schema import TaskCreate, TaskUpdate
from tasks.exceptions import TaskNotFoundException


class TaskDAO:
    
    @staticmethod
    async def create_task(task_data: TaskCreate, user_id: int, db: AsyncSession) -> Task:
        """Create a new task for a user"""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id,
            completed=False
        )
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def get_task_by_id(task_id: int, db: AsyncSession) -> Optional[Task]:
        """Get task by ID"""
        result = await db.execute(select(Task).filter(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_task_by_id_or_raise(task_id: int, db: AsyncSession) -> Task:
        """Get task by ID or raise exception"""
        task = await TaskDAO.get_task_by_id(task_id, db)
        if not task:
            raise TaskNotFoundException()
        return task

    @staticmethod
    async def get_user_tasks(user_id: int, db: AsyncSession) -> List[Task]:
        """Get all tasks for a specific user"""
        result = await db.execute(
            select(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_user_task_by_id(task_id: int, user_id: int, db: AsyncSession) -> Optional[Task]:
        """Get specific task for a user"""
        result = await db.execute(
            select(Task).filter(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_task_by_id_or_raise(task_id: int, user_id: int, db: AsyncSession) -> Task:
        """Get specific task for a user or raise exception"""
        task = await TaskDAO.get_user_task_by_id(task_id, user_id, db)
        if not task:
            raise TaskNotFoundException()
        return task

    @staticmethod
    async def update_task(task_id: int, user_id: int, task_data: TaskUpdate, db: AsyncSession) -> Task:
        """Update a task"""
        # First check if task exists and belongs to user
        await TaskDAO.get_user_task_by_id_or_raise(task_id, user_id, db)
        
        # Prepare update data
        update_data = {}
        if task_data.title is not None:
            update_data["title"] = task_data.title
        if task_data.description is not None:
            update_data["description"] = task_data.description
        if task_data.completed is not None:
            update_data["completed"] = task_data.completed

        if update_data:
            await db.execute(
                update(Task)
                .where(Task.id == task_id, Task.user_id == user_id)
                .values(**update_data)
            )
            await db.commit()

        # Return updated task
        return await TaskDAO.get_user_task_by_id_or_raise(task_id, user_id, db)

    @staticmethod
    async def delete_task(task_id: int, user_id: int, db: AsyncSession) -> bool:
        """Delete a task"""
        # First check if task exists and belongs to user
        await TaskDAO.get_user_task_by_id_or_raise(task_id, user_id, db)
        
        await db.execute(
            delete(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        await db.commit()
        return True

    @staticmethod
    async def get_completed_tasks(user_id: int, db: AsyncSession) -> List[Task]:
        """Get all completed tasks for a user"""
        result = await db.execute(
            select(Task).filter(Task.user_id == user_id, Task.completed == True)
            .order_by(Task.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_pending_tasks(user_id: int, db: AsyncSession) -> List[Task]:
        """Get all pending tasks for a user"""
        result = await db.execute(
            select(Task).filter(Task.user_id == user_id, Task.completed == False)
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all() 