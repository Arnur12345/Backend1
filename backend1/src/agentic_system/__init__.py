from .file_manager import file_manager
from .agent_manager import agent_manager

# API router импортируется отдельно, чтобы избежать циклических зависимостей
def get_router():
    from .api import router
    return router

__all__ = ["file_manager", "agent_manager", "get_router"] 