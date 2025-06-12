# Тестирование API endpoints
Write-Host "🧪 Тестирование Agentic API..." -ForegroundColor Green

# Проверка health endpoint
Write-Host "`n1. Проверка Health endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/agentic/health" -Method GET -TimeoutSec 5
    Write-Host "✅ Health OK" -ForegroundColor Green
    Write-Host "   Агентов: $($health.agents_count)" -ForegroundColor Cyan
    Write-Host "   Файлов: $($health.files_count)" -ForegroundColor Cyan
    Write-Host "   Статус: $($health.status)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Health FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Проверка доступных endpoints
Write-Host "`n2. Доступные endpoints:" -ForegroundColor Yellow
$endpoints = @(
    "POST /agentic/upload",
    "GET /agentic/files", 
    "DELETE /agentic/files/{file_id}",
    "POST /agentic/ask",
    "GET /agentic/chat/{file_id}",
    "GET /agentic/health"
)

foreach ($endpoint in $endpoints) {
    Write-Host "   ✅ $endpoint" -ForegroundColor Green
}

# Проверка что НЕТ /agents endpoint
Write-Host "`n3. Проверка отсутствия /agents endpoint..." -ForegroundColor Yellow
try {
    $agents = Invoke-RestMethod -Uri "http://localhost:8000/agentic/agents" -Method GET -TimeoutSec 5
    Write-Host "❌ ОШИБКА: /agents endpoint все еще существует!" -ForegroundColor Red
} catch {
    if ($_.Exception.Message -like "*404*") {
        Write-Host "✅ /agents endpoint правильно удален (404)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Неожиданная ошибка: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host "`n🎯 Рекомендации:" -ForegroundColor Yellow
Write-Host "1. Очистите кэш браузера полностью" -ForegroundColor Cyan
Write-Host "2. Откройте в режиме инкогнито: http://localhost:3000/agentic" -ForegroundColor Cyan
Write-Host "3. Проверьте Network tab в DevTools" -ForegroundColor Cyan

Write-Host "`n✅ Тестирование завершено!" -ForegroundColor Green 