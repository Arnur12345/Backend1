#!/usr/bin/env python3
"""
Терминальный интерфейс для тестирования агентной системы
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

# Добавляем путь к src в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic_system.agent_manager import agent_manager
from agentic_system.file_manager import file_manager


class TerminalChat:
    def __init__(self):
        self.current_file_id: Optional[str] = None
        self.current_filename: Optional[str] = None
    
    def print_banner(self):
        """Выводит баннер приложения"""
        print("=" * 60)
        print("🤖 АГЕНТНАЯ СИСТЕМА АНАЛИЗА ФАЙЛОВ")
        print("=" * 60)
        print("Команды:")
        print("  upload <путь_к_файлу>  - Загрузить файл")
        print("  list                   - Показать загруженные файлы")
        print("  select <file_id>       - Выбрать файл для чата")
        print("  agents                 - Показать доступных агентов")
        print("  history                - Показать историю чата")
        print("  clear                  - Очистить историю чата")
        print("  help                   - Показать эту справку")
        print("  exit                   - Выйти")
        print("=" * 60)
    
    async def upload_file(self, file_path: str) -> bool:
        """Загружает файл в систему"""
        if not os.path.exists(file_path):
            print(f"❌ Файл не найден: {file_path}")
            return False
        
        try:
            # Создаем фейковый UploadFile объект
            class FakeUploadFile:
                def __init__(self, file_path: str):
                    self.filename = os.path.basename(file_path)
                    self.content_type = self._get_content_type(file_path)
                    self._file_path = file_path
                
                def _get_content_type(self, file_path: str) -> str:
                    ext = Path(file_path).suffix.lower()
                    if ext == '.txt':
                        return 'text/plain'
                    elif ext == '.csv':
                        return 'text/csv'
                    elif ext == '.json':
                        return 'application/json'
                    elif ext == '.md':
                        return 'text/markdown'
                    elif ext == '.html':
                        return 'text/html'
                    else:
                        return 'text/plain'
                
                async def read(self) -> bytes:
                    with open(self._file_path, 'rb') as f:
                        return f.read()
            
            fake_file = FakeUploadFile(file_path)
            file_info = await file_manager.save_file(fake_file)
            
            print(f"✅ Файл загружен успешно!")
            print(f"   ID: {file_info['file_id']}")
            print(f"   Имя: {file_info['original_filename']}")
            print(f"   Размер: {file_info['file_size']} байт")
            
            # Автоматически выбираем загруженный файл
            self.current_file_id = file_info['file_id']
            self.current_filename = file_info['original_filename']
            print(f"📁 Файл '{self.current_filename}' выбран для чата")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке файла: {e}")
            return False
    
    def list_files(self):
        """Показывает список загруженных файлов"""
        files = file_manager.list_files()
        
        if not files:
            print("📂 Нет загруженных файлов")
            return
        
        print("📂 Загруженные файлы:")
        print("-" * 80)
        for file_info in files:
            status = "🟢 [ВЫБРАН]" if file_info['file_id'] == self.current_file_id else "⚪"
            print(f"{status} ID: {file_info['file_id'][:8]}...")
            print(f"    Имя: {file_info['original_filename']}")
            print(f"    Размер: {file_info['file_size']} байт")
            print(f"    Загружен: {file_info['upload_time']}")
            print("-" * 80)
    
    def select_file(self, file_id: str):
        """Выбирает файл для чата"""
        # Поддерживаем короткий ID (первые 8 символов)
        if len(file_id) == 8:
            files = file_manager.list_files()
            for file_info in files:
                if file_info['file_id'].startswith(file_id):
                    file_id = file_info['file_id']
                    break
        
        file_info = file_manager.get_file_info(file_id)
        if not file_info:
            print(f"❌ Файл с ID {file_id} не найден")
            return
        
        self.current_file_id = file_id
        self.current_filename = file_info['original_filename']
        print(f"📁 Файл '{self.current_filename}' выбран для чата")
    
    def show_agents(self):
        """Показывает доступных агентов"""
        agents = agent_manager.get_available_agents()
        
        print("🤖 Доступные агенты:")
        print("-" * 50)
        for agent in agents:
            status = "✅" if agent.get('available', True) else "❌"
            default = "⭐ [ПО УМОЛЧАНИЮ]" if agent['key'] == agent_manager.default_agent else ""
            print(f"{status} {agent['name']} ({agent['key']}) {default}")
            print(f"    Тип: {agent['type']}")
        print("-" * 50)
    
    def show_history(self):
        """Показывает историю чата"""
        if not self.current_file_id:
            print("❌ Сначала выберите файл")
            return
        
        history = agent_manager.get_chat_history(self.current_file_id)
        
        if not history:
            print("📝 История чата пуста")
            return
        
        print(f"📝 История чата для файла '{self.current_filename}':")
        print("=" * 80)
        
        for i, msg in enumerate(history, 1):
            print(f"[{i}] {msg['timestamp']}")
            print(f"👤 Вопрос: {msg['question']}")
            print(f"🤖 [{msg['agent_type']}]: {msg['answer']}")
            print("-" * 80)
    
    def clear_history(self):
        """Очищает историю чата"""
        if not self.current_file_id:
            print("❌ Сначала выберите файл")
            return
        
        success = agent_manager.clear_chat_history(self.current_file_id)
        if success:
            print("✅ История чата очищена")
        else:
            print("ℹ️ История чата уже пуста")
    
    async def ask_question(self, question: str, agent_type: str = None):
        """Задает вопрос агенту"""
        if not self.current_file_id:
            print("❌ Сначала выберите файл")
            return
        
        print(f"🤔 Обрабатываю вопрос...")
        
        try:
            response = await agent_manager.process_question(
                file_id=self.current_file_id,
                question=question,
                agent_type=agent_type
            )
            
            if "error" in response:
                print(f"❌ Ошибка: {response['error']}")
                return
            
            print(f"🤖 [{response['agent_type']}]: {response['answer']}")
            
        except Exception as e:
            print(f"❌ Ошибка при обработке вопроса: {e}")
    
    async def run(self):
        """Основной цикл терминального интерфейса"""
        self.print_banner()
        
        while True:
            try:
                # Показываем текущий файл в промпте
                if self.current_file_id:
                    prompt = f"📁 {self.current_filename[:20]}... > "
                else:
                    prompt = "🤖 > "
                
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Парсим команду
                parts = user_input.split(' ', 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == 'exit':
                    print("👋 До свидания!")
                    break
                
                elif command == 'help':
                    self.print_banner()
                
                elif command == 'upload':
                    if not args:
                        print("❌ Укажите путь к файлу: upload <путь_к_файлу>")
                    else:
                        await self.upload_file(args)
                
                elif command == 'list':
                    self.list_files()
                
                elif command == 'select':
                    if not args:
                        print("❌ Укажите ID файла: select <file_id>")
                    else:
                        self.select_file(args)
                
                elif command == 'agents':
                    self.show_agents()
                
                elif command == 'history':
                    self.show_history()
                
                elif command == 'clear':
                    self.clear_history()
                
                else:
                    # Если это не команда, то это вопрос
                    await self.ask_question(user_input)
            
            except KeyboardInterrupt:
                print("\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")


async def main():
    """Точка входа"""
    chat = TerminalChat()
    await chat.run()


if __name__ == "__main__":
    asyncio.run(main()) 