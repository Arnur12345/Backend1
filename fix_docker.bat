@echo off
echo 🔧 Исправляем проблемы с Docker...

echo 1. Останавливаем контейнеры...
docker-compose down -v 2>nul

echo 2. Очищаем Docker кеш...
docker system prune -af
docker volume prune -f

echo 3. Перезапускаем Docker Desktop...
taskkill /f /im "Docker Desktop.exe" 2>nul
timeout /t 3 >nul
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
timeout /t 10 >nul

echo.
echo ✅ Docker очищен!
echo.
echo Теперь попробуйте:
echo   make dev          # Запуск с Docker
echo   make dev-local    # Запуск без Docker
echo. 