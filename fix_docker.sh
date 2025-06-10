#!/bin/bash

echo "🔧 Исправляем проблемы с Docker..."

# Остановить все контейнеры
echo "1. Останавливаем контейнеры..."
docker-compose down -v 2>/dev/null || true

# Очистить Docker
echo "2. Очищаем Docker кеш..."
docker system prune -af
docker volume prune -f

# Перезапустить Docker (если на Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "3. Перезапускаем Docker..."
    sudo systemctl restart docker
    sleep 5
fi

# Проверить свободное место
echo "4. Проверяем свободное место на диске..."
df -h

echo ""
echo "✅ Docker очищен!"
echo ""
echo "Теперь попробуйте:"
echo "  make dev          # Запуск с Docker"
echo "  make dev-local    # Запуск без Docker"
echo "" 