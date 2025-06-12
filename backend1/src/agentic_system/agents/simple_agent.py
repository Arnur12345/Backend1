from .base_agent import BaseAgent
from typing import Dict
import re


class SimpleAgent(BaseAgent):
    """Простой агент для анализа текста без использования внешних API"""
    
    def __init__(self):
        super().__init__()
    
    @property
    def name(self) -> str:
        return "simple"
    
    @property
    def description(self) -> str:
        return "Простой агент для базового анализа текста"
    
    async def process_request(self, file_content: str, question: str, **kwargs) -> str:
        """Обрабатывает запрос на основе простого анализа текста"""
        return await self.process_question(file_content, question, kwargs.get('file_info', {}))
    
    async def process_question(self, file_content: str, question: str, file_info: Dict) -> str:
        """Обрабатывает вопрос на основе простого анализа текста"""
        
        if not file_content:
            return "Не удалось прочитать содержимое файла."
        
        question_lower = question.lower()
        content_lower = file_content.lower()
        
        # Простые паттерны для анализа
        if any(word in question_lower for word in ['сколько', 'количество', 'число']):
            return self._count_analysis(file_content, question_lower)
        
        elif any(word in question_lower for word in ['что', 'какой', 'какая', 'какое']):
            return self._content_analysis(file_content, question_lower)
        
        elif any(word in question_lower for word in ['найди', 'найти', 'поиск', 'ищи']):
            return self._search_analysis(file_content, question_lower)
        
        elif any(word in question_lower for word in ['резюме', 'краткое', 'суммарно', 'итог']):
            return self._summary_analysis(file_content)
        
        else:
            return self._general_analysis(file_content, question)
    
    def _count_analysis(self, content: str, question: str) -> str:
        """Анализ для подсчета элементов"""
        lines = len(content.split('\n'))
        words = len(content.split())
        chars = len(content)
        
        if 'строк' in question or 'линий' in question:
            return f"В файле {lines} строк."
        elif 'слов' in question:
            return f"В файле {words} слов."
        elif 'символов' in question or 'букв' in question:
            return f"В файле {chars} символов."
        else:
            return f"Статистика файла: {lines} строк, {words} слов, {chars} символов."
    
    def _content_analysis(self, content: str, question: str) -> str:
        """Анализ содержимого"""
        lines = content.split('\n')
        first_lines = lines[:3] if len(lines) >= 3 else lines
        
        return f"Файл содержит следующую информацию:\n\nПервые строки:\n" + "\n".join(first_lines[:3])
    
    def _search_analysis(self, content: str, question: str) -> str:
        """Поиск в содержимом"""
        # Извлекаем ключевые слова из вопроса
        words = question.split()
        search_terms = [word for word in words if len(word) > 3 and word not in ['найди', 'найти', 'поиск', 'ищи']]
        
        if not search_terms:
            return "Не удалось определить, что искать в файле."
        
        results = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for term in search_terms:
                if term in line.lower():
                    results.append(f"Строка {i}: {line.strip()}")
                    break
        
        if results:
            return f"Найдено совпадений: {len(results)}\n\n" + "\n".join(results[:5])
        else:
            return f"Не найдено совпадений для: {', '.join(search_terms)}"
    
    def _summary_analysis(self, content: str) -> str:
        """Создание краткого резюме"""
        lines = content.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        total_lines = len(lines)
        total_words = len(content.split())
        
        # Берем первые и последние строки
        summary_lines = []
        if non_empty_lines:
            summary_lines.append(f"Начало: {non_empty_lines[0]}")
            if len(non_empty_lines) > 1:
                summary_lines.append(f"Конец: {non_empty_lines[-1]}")
        
        return f"Краткое резюме файла:\n- Всего строк: {total_lines}\n- Всего слов: {total_words}\n\n" + "\n".join(summary_lines)
    
    def _general_analysis(self, content: str, question: str) -> str:
        """Общий анализ для неопределенных вопросов"""
        lines = content.split('\n')
        words = content.split()
        
        # Пытаемся найти ключевые слова из вопроса в тексте
        question_words = [word.lower() for word in question.split() if len(word) > 3]
        found_context = []
        
        for line in lines:
            for word in question_words:
                if word in line.lower():
                    found_context.append(line.strip())
                    break
        
        if found_context:
            return f"По вашему вопросу найдена следующая информация:\n\n" + "\n".join(found_context[:3])
        else:
            return f"Не удалось найти прямого ответа на ваш вопрос в файле. Файл содержит {len(lines)} строк и {len(words)} слов." 