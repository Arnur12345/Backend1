from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_user_tasks(db: AsyncSession, user_id: int) -> List[Task]:
    result = await db.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate, user_id: int) -> Optional[Task]:
    task = await get_task_by_id(db, task_id, user_id)
    if not task:
        return None
    
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> bool:
    task = await get_task_by_id(db, task_id, user_id)
    if not task:
        return False
    
    await db.delete(task)
    await db.commit()
    return True 