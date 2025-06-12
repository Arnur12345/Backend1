from typing import Dict, List
from datetime import datetime
import asyncio

from .agents.base_agent import BaseAgent
from .agents.simple_agent import SimpleAgent
from .agents.pydanticai_agent import PydanticAIAgent
from .agents.langchain_agent import LangchainAgent
from .agents.coordinator_agent import CoordinatorAgent
from .file_manager import file_manager


class AgentManager:
    """Менеджер для управления агентами и обработки запросов"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.chat_history: Dict[str, List[Dict]] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Инициализирует доступных агентов"""
        # Базовые агенты
        simple_agent = SimpleAgent()
        pydantic_agent = PydanticAIAgent()
        langchain_agent = LangchainAgent()
        
        # Добавляем базовые агенты
        base_agents = {
            "simple": simple_agent,
            "pydantic": pydantic_agent,
            "langchain": langchain_agent
        }
        
        # Создаем координатор с базовыми агентами
        coordinator = CoordinatorAgent(base_agents)
        
        # Добавляем всех агентов в систему
        self.agents.update(base_agents)
        self.agents["coordinator"] = coordinator
        
        # Устанавливаем координатор как агента по умолчанию для Agent-To-Agent
        self.default_agent = "coordinator"
        
        print(f"Агенты инициализированы. Агент по умолчанию: {self.default_agent}")
        print(f"Доступные агенты: {list(self.agents.keys())}")
    
    async def process_question(self, file_id: str, question: str, user_id: int, agent_type: str = None) -> Dict:
        """Обрабатывает вопрос пользователя"""
        
        # Получаем информацию о файле с проверкой прав доступа
        file_info = file_manager.get_file_info(file_id, user_id)
        if not file_info:
            return {
                "error": "Файл не найден или у вас нет прав доступа",
                "file_id": file_id,
                "question": question,
                "answer": None,
                "response_time": datetime.now(),
                "agent_type": None
            }
        
        # Читаем содержимое файла с проверкой прав доступа
        file_content = file_manager.get_file_content(file_id, user_id)
        if not file_content:
            return {
                "error": "Не удалось прочитать содержимое файла",
                "file_id": file_id,
                "question": question,
                "answer": None,
                "response_time": datetime.now(),
                "agent_type": None
            }
        
        # Всегда используем координатор
        selected_agent = self.agents[self.default_agent]
        
        try:
            # Обрабатываем вопрос через новый API
            answer = await selected_agent.process_request(file_content, question, file_info=file_info)
            
            response = {
                "file_id": file_id,
                "question": question,
                "answer": answer,
                "response_time": datetime.now(),
                "agent_type": selected_agent.name,
                "file_info": {
                    "filename": file_info.get("original_filename"),
                    "file_size": file_info.get("file_size"),
                    "content_type": file_info.get("content_type")
                }
            }
            
            # Сохраняем в историю чата с привязкой к пользователю
            self._save_to_history(file_id, question, answer, selected_agent.name, user_id)
            
            return response
            
        except Exception as e:
            return {
                "error": f"Ошибка при обработке вопроса: {str(e)}",
                "file_id": file_id,
                "question": question,
                "answer": None,
                "response_time": datetime.now(),
                "agent_type": selected_agent.name if 'selected_agent' in locals() else None
            }
    
    def _save_to_history(self, file_id: str, question: str, answer: str, agent_type: str, user_id: int):
        """Сохраняет диалог в историю"""
        # Создаем уникальный ключ для истории пользователя и файла
        history_key = f"{user_id}_{file_id}"
        
        if history_key not in self.chat_history:
            self.chat_history[history_key] = []
        
        self.chat_history[history_key].append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "agent_type": agent_type
        })
        
        # Ограничиваем историю последними 50 сообщениями
        if len(self.chat_history[history_key]) > 50:
            self.chat_history[history_key] = self.chat_history[history_key][-50:]
    
    def get_chat_history(self, file_id: str, user_id: int) -> List[Dict]:
        """Возвращает историю чата для файла пользователя"""
        history_key = f"{user_id}_{file_id}"
        return self.chat_history.get(history_key, [])
    
    def get_available_agents(self) -> List[Dict]:
        """Возвращает список доступных агентов"""
        agents_list = []
        for key, agent in self.agents.items():
            agents_list.append({
                "id": key,
                "name": agent.name,
                "description": agent.description,
                "capabilities": getattr(agent, 'capabilities', [
                    "Анализ текста",
                    "Ответы на вопросы",
                    "Обработка файлов"
                ]),
                "status": "active" if getattr(agent, 'available', True) else "inactive"
            })
        return agents_list
    
    def clear_chat_history(self, file_id: str, user_id: int) -> bool:
        """Очищает историю чата для файла пользователя"""
        history_key = f"{user_id}_{file_id}"
        if history_key in self.chat_history:
            del self.chat_history[history_key]
            return True
        return False
    
    async def chat_with_file(self, file_id: str, question: str, user_id: int, agent_type: str = None) -> str:
        """Простая функция для чата с файлом (для терминала)"""
        response = await self.process_question(file_id, question, user_id, agent_type)
        
        if "error" in response:
            return f"❌ Ошибка: {response['error']}"
        
        return f"🤖 [{response['agent_type']}]: {response['answer']}"


# Глобальный экземпляр менеджера агентов
agent_manager = AgentManager() 