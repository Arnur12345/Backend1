"""
Custom exceptions for the tasks module.
"""
from fastapi import HTTPException, status


class TaskException(Exception):
    """Base exception for task operations"""
    pass


class TaskNotFoundException(TaskException):
    """Exception raised when task is not found"""
    def __init__(self, message: str = "Task not found"):
        self.message = message
        super().__init__(self.message)


class TaskAccessDeniedException(TaskException):
    """Exception raised when user tries to access task they don't own"""
    def __init__(self, message: str = "Access denied to this task"):
        self.message = message
        super().__init__(self.message)


class TaskCreationException(TaskException):
    """Exception raised when task creation fails"""
    def __init__(self, message: str = "Failed to create task"):
        self.message = message
        super().__init__(self.message)


class TaskUpdateException(TaskException):
    """Exception raised when task update fails"""
    def __init__(self, message: str = "Failed to update task"):
        self.message = message
        super().__init__(self.message)


class TaskDeletionException(TaskException):
    """Exception raised when task deletion fails"""
    def __init__(self, message: str = "Failed to delete task"):
        self.message = message
        super().__init__(self.message)


class InvalidTaskDataException(TaskException):
    """Exception raised when task data is invalid"""
    def __init__(self, message: str = "Invalid task data"):
        self.message = message
        super().__init__(self.message)


def raise_http_exception(exception: TaskException) -> None:
    """Convert task exceptions to HTTP exceptions"""
    if isinstance(exception, TaskNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exception.message
        )
    elif isinstance(exception, TaskAccessDeniedException):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exception.message
        )
    elif isinstance(exception, (TaskCreationException, TaskUpdateException, TaskDeletionException)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message
        )
    elif isinstance(exception, InvalidTaskDataException):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exception.message
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

