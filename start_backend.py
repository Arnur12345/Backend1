#!/usr/bin/env python3
"""
Скрипт для запуска backend сервера
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Переходим в директорию backend1
    backend_dir = Path(__file__).parent / "backend1"
    
    if not backend_dir.exists():
        print("❌ Директория backend1 не найдена!")
        return 1
    
    os.chdir(backend_dir)
    print(f"📁 Переходим в директорию: {backend_dir}")
    
    # Проверяем наличие src/main.py
    main_file = backend_dir / "src" / "main.py"
    if not main_file.exists():
        print("❌ Файл src/main.py не найден!")
        return 1
    
    print("🚀 Запускаем FastAPI сервер...")
    print("🌐 Сервер будет доступен по адресу: http://localhost:8000")
    print("📚 Документация API: http://localhost:8000/docs")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        # Запускаем uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Сервер остановлен пользователем")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return 1
    except FileNotFoundError:
        print("❌ Python или uvicorn не найден. Убедитесь, что они установлены.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 