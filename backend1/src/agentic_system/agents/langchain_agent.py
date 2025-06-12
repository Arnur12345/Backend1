import os
import asyncio
from typing import Dict
from dotenv import load_dotenv
from .base_agent import BaseAgent

# Попытка импорта Langchain
try:
    from langchain.agents import initialize_agent, Tool
    from langchain.chat_models import ChatOpenAI
    from langchain.agents.agent_types import AgentType
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

load_dotenv()


class LangchainAgent(BaseAgent):
    """Langchain агент для работы с загруженными файлами"""
    
    def __init__(self):
        super().__init__()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if LANGCHAIN_AVAILABLE and self.openai_api_key:
            try:
                self._setup_agent()
                self.available = True
            except Exception as e:
                print(f"Ошибка инициализации Langchain агента: {e}")
                self.available = False
        else:
            self.available = False
            if not LANGCHAIN_AVAILABLE:
                print("Langchain не установлен")
            if not self.openai_api_key:
                print("OPENAI_API_KEY не найден в .env")
    
    def _setup_agent(self):
        """Настройка Langchain агента"""
        
        # Создаем инструменты для анализа файла
        def analyze_content(query: str) -> str:
            """Анализирует содержимое файла"""
            return f"Анализ содержимого: {query}"
        
        def search_in_content(query: str) -> str:
            """Ищет информацию в содержимом файла"""
            return f"Поиск в содержимом: {query}"
        
        def count_elements(query: str) -> str:
            """Подсчитывает элементы в файле"""
            return f"Подсчет элементов: {query}"
        
        tools = [
            Tool(
                name="Content Analysis",
                func=analyze_content,
                description="Полезен для общего анализа содержимого файла",
            ),
            Tool(
                name="Content Search",
                func=search_in_content,
                description="Полезен для поиска конкретной информации в файле",
            ),
            Tool(
                name="Element Counter",
                func=count_elements,
                description="Полезен для подсчета строк, слов, символов в файле",
            )
        ]
        
        # Создаём Langchain агента
        self.agent = initialize_agent(
            tools=tools,
            llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=self.openai_api_key),
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )
    
    @property
    def name(self) -> str:
        return "langchain"
    
    @property
    def description(self) -> str:
        return "Langchain агент с использованием OpenAI и инструментов"
    
    async def process_request(self, file_content: str, question: str, **kwargs) -> str:
        """Обрабатывает запрос с помощью Langchain"""
        return await self.process_question(file_content, question, kwargs.get('file_info', {}))
    
    async def process_question(self, file_content: str, question: str, file_info: Dict) -> str:
        """Обрабатывает вопрос с помощью Langchain"""
        
        if not self.available:
            return self._fallback_analysis(file_content, question, file_info)
        
        if not file_content:
            return "Не удалось прочитать содержимое файла."
        
        try:
            # Ограничиваем размер контента для API
            max_content_length = 2000
            if len(file_content) > max_content_length:
                file_content = file_content[:max_content_length] + "...\n[Содержимое обрезано]"
            
            filename = file_info.get('original_filename', 'файл')
            
            # Формируем контекст для агента
            context = f"""
Анализируй содержимое файла "{filename}":

СОДЕРЖИМОЕ ФАЙЛА:
{file_content}

ВОПРОС ПОЛЬЗОВАТЕЛЯ: {question}

Используй доступные инструменты для анализа и ответь на вопрос пользователя на основе содержимого файла.
"""
            
            # Запускаем агента в отдельном потоке, так как он синхронный
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.agent.run, context)
            
            return result
            
        except Exception as e:
            print(f"Ошибка при обращении к Langchain: {e}")
            return self._fallback_analysis(file_content, question, file_info)
    
    def _fallback_analysis(self, file_content: str, question: str, file_info: Dict) -> str:
        """Простой анализ как fallback"""
        if not file_content:
            return "Не удалось прочитать содержимое файла."
        
        question_lower = question.lower()
        
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