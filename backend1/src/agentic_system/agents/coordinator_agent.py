"""
Агент-координатор для Agent-To-Agent архитектуры
"""
import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """
    Агент-координатор, который управляет другими агентами
    и реализует Agent-To-Agent взаимодействие
    """
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        super().__init__()
        self.agents = agents
        self.conversation_history = []
    
    async def process_request(self, file_content: str, question: str, **kwargs) -> str:
        """
        Обрабатывает запрос, координируя работу других агентов
        """
        try:
            # Определяем, какой агент лучше подходит для задачи
            primary_agent = self._select_primary_agent(question)
            
            # Получаем первичный ответ
            primary_response = await primary_agent.process_request(file_content, question, **kwargs)
            
            # Определяем, нужна ли дополнительная обработка
            if self._needs_secondary_agent(question, primary_response):
                secondary_agent = self._select_secondary_agent(question, primary_response)
                
                # Формируем запрос для второго агента
                secondary_question = self._create_secondary_question(question, primary_response)
                
                # Получаем дополнительный ответ
                secondary_response = await secondary_agent.process_request(
                    file_content, secondary_question, **kwargs
                )
                
                # Объединяем ответы
                final_response = self._combine_responses(
                    primary_response, secondary_response, question
                )
                
                # Сохраняем историю взаимодействия
                self._save_interaction_history(
                    question, primary_agent.name, primary_response,
                    secondary_agent.name, secondary_response, final_response
                )
                
                return final_response
            else:
                # Сохраняем простое взаимодействие
                self._save_simple_interaction(question, primary_agent.name, primary_response)
                return primary_response
                
        except Exception as e:
            return f"Ошибка координатора: {str(e)}"
    
    def _select_primary_agent(self, question: str) -> BaseAgent:
        """Выбирает основного агента для обработки вопроса"""
        question_lower = question.lower()
        
        # Логика выбора агента на основе типа вопроса
        if any(word in question_lower for word in ['анализ', 'структура', 'данные', 'статистика']):
            return self.agents.get('pydantic', list(self.agents.values())[0])
        elif any(word in question_lower for word in ['резюме', 'краткое', 'суть', 'основное']):
            return self.agents.get('simple', list(self.agents.values())[0])
        elif any(word in question_lower for word in ['детально', 'подробно', 'глубокий']):
            return self.agents.get('langchain', list(self.agents.values())[0])
        else:
            # По умолчанию используем первого доступного агента
            return list(self.agents.values())[0]
    
    def _needs_secondary_agent(self, question: str, primary_response: str) -> bool:
        """Определяет, нужен ли второй агент"""
        question_lower = question.lower()
        
        # Условия для вызова второго агента
        complex_keywords = ['сравни', 'проанализируй', 'детально', 'всесторонне', 'комплексно']
        
        if any(keyword in question_lower for keyword in complex_keywords):
            return True
        
        # Если первичный ответ короткий, можем добавить детализацию
        if len(primary_response.split()) < 50:
            return True
            
        return False
    
    def _select_secondary_agent(self, question: str, primary_response: str) -> BaseAgent:
        """Выбирает второго агента для дополнительной обработки"""
        # Выбираем агента, отличного от уже использованного
        available_agents = list(self.agents.values())
        
        if len(available_agents) > 1:
            # Возвращаем второго агента
            return available_agents[1]
        else:
            # Если агент только один, возвращаем его же
            return available_agents[0]
    
    def _create_secondary_question(self, original_question: str, primary_response: str) -> str:
        """Создает вопрос для второго агента"""
        return f"""
        Дополни и улучши следующий ответ на вопрос: "{original_question}"
        
        Первичный ответ: {primary_response}
        
        Добавь дополнительные детали, контекст или альтернативные точки зрения.
        """
    
    def _combine_responses(self, primary: str, secondary: str, question: str) -> str:
        """Объединяет ответы от двух агентов"""
        return f"""
🤖 **Комплексный ответ от агентной системы:**

**Основной анализ:**
{primary}

**Дополнительная детализация:**
{secondary}

---
*Ответ подготовлен с использованием Agent-To-Agent архитектуры*
        """.strip()
    
    def _save_interaction_history(self, question: str, agent1_name: str, response1: str,
                                agent2_name: str, response2: str, final_response: str):
        """Сохраняет историю взаимодействия агентов"""
        interaction = {
            "question": question,
            "primary_agent": agent1_name,
            "primary_response": response1,
            "secondary_agent": agent2_name,
            "secondary_response": response2,
            "final_response": final_response,
            "timestamp": self._get_timestamp()
        }
        self.conversation_history.append(interaction)
    
    def _save_simple_interaction(self, question: str, agent_name: str, response: str):
        """Сохраняет простое взаимодействие с одним агентом"""
        interaction = {
            "question": question,
            "primary_agent": agent_name,
            "primary_response": response,
            "final_response": response,
            "timestamp": self._get_timestamp()
        }
        self.conversation_history.append(interaction)
    
    def get_interaction_history(self) -> List[Dict[str, Any]]:
        """Возвращает историю взаимодействий агентов"""
        return self.conversation_history
    
    def clear_history(self):
        """Очищает историю взаимодействий"""
        self.conversation_history.clear()
    
    @property
    def name(self) -> str:
        return "coordinator"
    
    @property
    def description(self) -> str:
        return "Агент-координатор для управления Agent-To-Agent взаимодействием" 