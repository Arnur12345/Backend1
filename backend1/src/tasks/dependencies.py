from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.models import User
from database import get_async_db


async def get_current_user_for_tasks(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current authenticated user for task operations"""
    return current_user


async def get_db_for_tasks(
    db: AsyncSession = Depends(get_async_db)
) -> AsyncSession:
    """Get database session for task operations"""
    return db 