#!/usr/bin/env python3
"""
Скрипт для запуска frontend сервера
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Переходим в директорию frontend
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Директория frontend не найдена!")
        return 1
    
    os.chdir(frontend_dir)
    print(f"📁 Переходим в директорию: {frontend_dir}")
    
    # Проверяем наличие package.json
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ Файл package.json не найден!")
        return 1
    
    print("🚀 Запускаем React сервер...")
    print("🌐 Сервер будет доступен по адресу: http://localhost:3000")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        # Сначала проверяем, установлены ли зависимости
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Устанавливаем зависимости...")
            subprocess.run(["npm", "install"], check=True)
        
        # Запускаем dev сервер
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Сервер остановлен пользователем")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return 1
    except FileNotFoundError:
        print("❌ npm не найден. Убедитесь, что Node.js установлен.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 