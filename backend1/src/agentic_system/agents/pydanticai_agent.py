import os
import asyncio
from typing import Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from .base_agent import BaseAgent

# Попытка импорта PydanticAI
try:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIModel
    PYDANTIC_AI_AVAILABLE = True
except ImportError:
    PYDANTIC_AI_AVAILABLE = False

load_dotenv()


class Document(BaseModel):
    content: str
    filename: str


class PydanticAIAgent(BaseAgent):
    """PydanticAI агент для работы с загруженными файлами"""
    
    def __init__(self):
        super().__init__()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if PYDANTIC_AI_AVAILABLE and self.openai_api_key:
            try:
                # Устанавливаем API ключ через переменную окружения
                os.environ["OPENAI_API_KEY"] = self.openai_api_key
                self.agent = Agent(
                    model=OpenAIModel('gpt-4o-mini'),
                    system_prompt="""Ты - помощник для анализа файлов. 
                    Используй предоставленное содержимое файла для ответа на вопросы пользователя.
                    Отвечай на русском языке кратко и по существу.
                    Если информации нет в файле, так и скажи."""
                )
                self.available = True
            except Exception as e:
                print(f"Ошибка инициализации PydanticAI агента: {e}")
                self.available = False
        else:
            self.available = False
            if not PYDANTIC_AI_AVAILABLE:
                print("PydanticAI не установлен")
            if not self.openai_api_key:
                print("OPENAI_API_KEY не найден в .env")
    
    @property
    def name(self) -> str:
        return "pydantic"
    
    @property
    def description(self) -> str:
        return "PydanticAI агент с использованием OpenAI GPT-4"
    
    async def process_request(self, file_content: str, question: str, **kwargs) -> str:
        """Обрабатывает запрос с помощью PydanticAI"""
        return await self.process_question(file_content, question, kwargs.get('file_info', {}))
    
    async def process_question(self, file_content: str, question: str, file_info: Dict) -> str:
        """Обрабатывает вопрос с помощью PydanticAI"""
        
        if not self.available:
            return self._fallback_analysis(file_content, question, file_info)
        
        if not file_content:
            return "Не удалось прочитать содержимое файла."
        
        try:
            # Ограничиваем размер контента для API
            max_content_length = 3000
            if len(file_content) > max_content_length:
                file_content = file_content[:max_content_length] + "...\n[Содержимое обрезано]"
            
            filename = file_info.get('original_filename', 'файл')
            
            prompt = f"""
Анализируй содержимое файла "{filename}" и ответь на вопрос пользователя.

СОДЕРЖИМОЕ ФАЙЛА:
{file_content}

ВОПРОС ПОЛЬЗОВАТЕЛЯ: {question}

Дай краткий и точный ответ на основе содержимого файла. Если в файле нет информации для ответа, так и скажи.
"""
            
            result = await self.agent.run(prompt)
            return result.data
            
        except Exception as e:
            print(f"Ошибка при обращении к PydanticAI: {e}")
            return self._fallback_analysis(file_content, question, file_info)
    
    def _fallback_analysis(self, file_content: str, question: str, file_info: Dict) -> str:
        """Простой анализ как fallback"""
        if not file_content:
            return "Не удалось прочитать содержимое файла."
        
        question_lower = question.lower()
        content_lower = file_content.lower()
        
        # Простые паттерны для анализа
        if any(word in question_lower for word in ['сколько', 'количество', 'число']):
            lines = len(file_content.split('\n'))
            words = len(file_content.split())
            chars = len(file_content)
            return f"Статистика файла: {lines} строк, {words} слов, {chars} символов."
        
        elif any(word in question_lower for word in ['что', 'какой', 'какая', 'какое']):
            lines = file_content.split('\n')
            first_lines = lines[:3] if len(lines) >= 3 else lines
            return f"Файл содержит следующую информацию:\n\nПервые строки:\n" + "\n".join(first_lines[:3])
        
        elif any(word in question_lower for word in ['найди', 'найти', 'поиск', 'ищи']):
            # Извлекаем ключевые слова из вопроса
            words = question.split()
            search_terms = [word for word in words if len(word) > 3 and word not in ['найди', 'найти', 'поиск', 'ищи']]
            
            if not search_terms:
                return "Не удалось определить, что искать в файле."
            
            results = []
            lines = file_content.split('\n')
            
            for i, line in enumerate(lines, 1):
                for term in search_terms:
                    if term.lower() in line.lower():
                        results.append(f"Строка {i}: {line.strip()}")
                        break
            
            if results:
                return f"Найдено совпадений: {len(results)}\n\n" + "\n".join(results[:5])
            else:
                return f"Не найдено совпадений для: {', '.join(search_terms)}"
        
        else:
            # Пытаемся найти ключевые слова из вопроса в тексте
            question_words = [word.lower() for word in question.split() if len(word) > 3]
            found_context = []
            
            for line in file_content.split('\n'):
                for word in question_words:
                    if word in line.lower():
                        found_context.append(line.strip())
                        break
            
            if found_context:
                return f"По вашему вопросу найдена следующая информация:\n\n" + "\n".join(found_context[:3])
            else:
                lines = len(file_content.split('\n'))
                words = len(file_content.split())
                return f"Не удалось найти прямого ответа на ваш вопрос в файле. Файл содержит {lines} строк и {words} слов." 