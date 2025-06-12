from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime

from .schema import (
    FileUploadResponse, 
    QuestionRequest, 
    AgentResponse, 
    FileInfo, 
    ChatHistory,
    AgentInfo
)
from .file_manager import file_manager
from .agent_manager import agent_manager
from auth.dependencies import get_current_user
from auth.models import User

router = APIRouter(prefix="/agentic", tags=["agentic_system"])


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Загружает файл для анализа агентами"""
    
    # Проверяем размер файла (максимум 10MB)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Файл слишком большой. Максимальный размер: 10MB"
        )
    
    # Проверяем тип файла
    allowed_types = [
        "text/plain", 
        "text/csv", 
        "application/json",
        "text/markdown",
        "application/pdf",  # Для будущего расширения
        "text/html"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Неподдерживаемый тип файла: {file.content_type}. Поддерживаются: {', '.join(allowed_types)}"
        )
    
    try:
        file_info = await file_manager.save_file(file, current_user.id)
        
        return FileUploadResponse(
            file_id=file_info["file_id"],
            filename=file_info["original_filename"],
            file_size=file_info["file_size"],
            upload_time=datetime.fromisoformat(file_info["upload_time"]),
            content_type=file_info["content_type"],
            message="Файл успешно загружен и готов для анализа"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при загрузке файла: {str(e)}"
        )


@router.post("/ask", response_model=AgentResponse)
async def ask_question(
    request: QuestionRequest,
    agent_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Задает вопрос агенту по загруженному файлу"""
    
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вопрос не может быть пустым"
        )
    
    try:
        response = await agent_manager.process_question(
            file_id=request.file_id,
            question=request.question,
            user_id=current_user.id,
            agent_type=agent_type
        )
        
        if "error" in response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["error"]
            )
        
        return AgentResponse(
            file_id=response["file_id"],
            question=response["question"],
            answer=response["answer"],
            response_time=response["response_time"],
            agent_type=response["agent_type"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обработке вопроса: {str(e)}"
        )


@router.get("/files", response_model=List[FileInfo])
async def list_files(current_user: User = Depends(get_current_user)):
    """Возвращает список всех загруженных файлов пользователя"""
    
    try:
        files = file_manager.list_files(current_user.id)
        return [
            FileInfo(
                file_id=file_info["file_id"],
                filename=file_info["original_filename"],
                file_size=file_info["file_size"],
                upload_time=datetime.fromisoformat(file_info["upload_time"]),
                content_type=file_info["content_type"]
            )
            for file_info in files
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка файлов: {str(e)}"
        )


@router.get("/files/{file_id}", response_model=FileInfo)
async def get_file_info(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Возвращает информацию о конкретном файле"""
    
    file_info = file_manager.get_file_info(file_id, current_user.id)
    if not file_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден"
        )
    
    return FileInfo(
        file_id=file_info["file_id"],
        filename=file_info["original_filename"],
        file_size=file_info["file_size"],
        upload_time=datetime.fromisoformat(file_info["upload_time"]),
        content_type=file_info["content_type"]
    )


@router.get("/chat/{file_id}", response_model=ChatHistory)
async def get_chat_history(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Возвращает историю чата для файла"""
    
    # Проверяем, что файл существует и принадлежит пользователю
    file_info = file_manager.get_file_info(file_id, current_user.id)
    if not file_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден"
        )
    
    history = agent_manager.get_chat_history(file_id, current_user.id)
    
    return ChatHistory(
        file_id=file_id,
        conversations=history
    )


@router.delete("/chat/{file_id}")
async def clear_chat_history(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Очищает историю чата для файла"""
    
    # Проверяем, что файл существует и принадлежит пользователю
    file_info = file_manager.get_file_info(file_id, current_user.id)
    if not file_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден"
        )
    
    success = agent_manager.clear_chat_history(file_id, current_user.id)
    
    return {
        "message": "История чата очищена" if success else "История чата уже пуста",
        "file_id": file_id
    }


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Удаляет файл и связанную с ним историю чата"""
    
    # Проверяем, что файл существует и принадлежит пользователю
    file_info = file_manager.get_file_info(file_id, current_user.id)
    if not file_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден"
        )
    
    try:
        # Удаляем файл
        file_deleted = file_manager.delete_file(file_id, current_user.id)
        
        # Удаляем историю чата
        agent_manager.clear_chat_history(file_id, current_user.id)
        
        if file_deleted:
            return {
                "message": "Файл и история чата успешно удалены",
                "file_id": file_id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении файла"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении файла: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Проверка работоспособности агентной системы"""
    
    try:
        # Проверяем доступность агентов
        agents = agent_manager.get_available_agents()
        
        # Проверяем файловую систему
        files_count = len(file_manager.list_files())
        
        return {
            "status": "healthy",
            "agents_count": len(agents),
            "files_count": files_count,
            "upload_dir_exists": file_manager.upload_dir.exists(),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get("/agents", response_model=List[AgentInfo])
async def get_available_agents(current_user: User = Depends(get_current_user)):
    """Возвращает список доступных агентов"""
    
    try:
        agents = agent_manager.get_available_agents()
        
        return [
            AgentInfo(
                agent_id=agent["id"],
                name=agent["name"],
                description=agent["description"],
                capabilities=agent["capabilities"],
                status=agent.get("status", "active")
            )
            for agent in agents
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка агентов: {str(e)}"
        )


@router.get("/agents-test")
async def get_available_agents_test():
    """Тестовый endpoint для проверки агентов без аутентификации"""
    
    try:
        agents = agent_manager.get_available_agents()
        return {
            "agents": agents,
            "count": len(agents),
            "status": "ok"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        } 