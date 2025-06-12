from abc import ABC, abstractmethod
from typing import Dict, Any
import asyncio
from datetime import datetime


class BaseAgent(ABC):
    """Базовый класс для всех агентов"""
    
    def __init__(self, name: str = None):
        self._name = name
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Имя агента"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание агента"""
        pass
    
    @abstractmethod
    async def process_request(self, file_content: str, question: str, **kwargs) -> str:
        """Обрабатывает запрос пользователя на основе содержимого файла"""
        pass
    
    # Для обратной совместимости
    async def process_question(self, file_content: str, question: str, file_info: Dict) -> str:
        """Обрабатывает вопрос пользователя (устаревший метод)"""
        return await self.process_request(file_content, question, file_info=file_info)
    
    def _get_timestamp(self) -> str:
        """Возвращает текущую временную метку"""
        return datetime.now().isoformat()
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Возвращает информацию об агенте"""
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        } 