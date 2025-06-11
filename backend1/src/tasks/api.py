from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from tasks.schema import TaskCreate, TaskUpdate, TaskResponse
from tasks.service import TaskService
from tasks.dependencies import get_current_user_for_tasks, get_db_for_tasks
from auth.models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create_task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Create a new task for the authenticated user"""
    return await TaskService.create_task(task_data, current_user.id, db)


@router.get("/get_tasks", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Get all tasks for the authenticated user"""
    return await TaskService.get_user_tasks(current_user.id, db)


@router.get("/get_task/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Get a specific task by ID for the authenticated user"""
    return await TaskService.get_task_by_id(task_id, current_user.id, db)


@router.put("/update_task/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Update a specific task for the authenticated user"""
    return await TaskService.update_task(task_id, current_user.id, task_data, db)


@router.delete("/delete_task/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Delete a specific task for the authenticated user"""
    return await TaskService.delete_task(task_id, current_user.id, db)


@router.get("/get_completed_tasks", response_model=List[TaskResponse])
async def get_completed_tasks(
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Get all completed tasks for the authenticated user"""
    return await TaskService.get_completed_tasks(current_user.id, db)


@router.get("/get_pending_tasks", response_model=List[TaskResponse])
async def get_pending_tasks(
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Get all pending tasks for the authenticated user"""
    return await TaskService.get_pending_tasks(current_user.id, db)


@router.patch("/mark_completed/{task_id}", response_model=TaskResponse)
async def mark_task_completed(
    task_id: int,
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Mark a task as completed for the authenticated user"""
    return await TaskService.mark_task_completed(task_id, current_user.id, db)


@router.patch("/mark_pending/{task_id}", response_model=TaskResponse)
async def mark_task_pending(
    task_id: int,
    current_user: User = Depends(get_current_user_for_tasks),
    db: AsyncSession = Depends(get_db_for_tasks)
):
    """Mark a task as pending for the authenticated user"""
    return await TaskService.mark_task_pending(task_id, current_user.id, db) 