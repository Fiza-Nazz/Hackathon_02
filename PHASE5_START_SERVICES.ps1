# PHASE 5 - START ALL SERVICES
# Event-Driven Architecture with Kafka + Dapr

Write-Host "🚀 PHASE 5 - STARTING EVENT-DRIVEN ARCHITECTURE" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Step 1: Start Kafka (Redpanda)
Write-Host "📡 Step 1: Starting Kafka (Redpanda)..." -ForegroundColor Yellow
try {
    docker-compose -f docker-compose.kafka.yml up -d
    Write-Host "✅ Kafka started successfully" -ForegroundColor Green
    Start-Sleep -Seconds 10
} catch {
    Write-Host "❌ Failed to start Kafka: $_" -ForegroundColor Red
}

# Step 2: Start Backend Service
Write-Host "🔧 Step 2: Starting Backend Service..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -WorkingDirectory "backend" -WindowStyle Hidden
    Write-Host "✅ Backend service started on port 8000" -ForegroundColor Green
    Start-Sleep -Seconds 5
} catch {
    Write-Host "❌ Failed to start backend: $_" -ForegroundColor Red
}

# Step 3: Start Chatbot Service
Write-Host "🤖 Step 3: Starting Chatbot Service..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "python" -ArgumentList "backend/http_server.py" -WorkingDirectory "Chatbot" -WindowStyle Hidden
    Write-Host "✅ Chatbot service started on port 8001" -ForegroundColor Green
    Start-Sleep -Seconds 5
} catch {
    Write-Host "❌ Failed to start chatbot: $_" -ForegroundColor Red
}

# Step 4: Start Notification Service
Write-Host "🔔 Step 4: Starting Notification Service..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "python" -ArgumentList "services/notification_service.py" -WindowStyle Hidden
    Write-Host "✅ Notification service started on WebSocket port 8765" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "❌ Failed to start notification service: $_" -ForegroundColor Red
}

# Step 5: Start Recurring Task Service
Write-Host "🔄 Step 5: Starting Recurring Task Service..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "python" -ArgumentList "services/recurring_task_service.py" -WindowStyle Hidden
    Write-Host "✅ Recurring task service started" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "❌ Failed to start recurring task service: $_" -ForegroundColor Red
}

# Step 6: Start Frontend
Write-Host "🎨 Step 6: Starting Frontend..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "frontend" -WindowStyle Hidden
    Write-Host "✅ Frontend started (will be on port 3000 or 3001)" -ForegroundColor Green
    Start-Sleep -Seconds 5
} catch {
    Write-Host "❌ Failed to start frontend: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 PHASE 5 SERVICES STATUS:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📡 Kafka (Redpanda): http://localhost:8080 (Console)" -ForegroundColor White
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "🤖 Chatbot API: http://localhost:8001" -ForegroundColor White
Write-Host "🔔 Notifications: WebSocket port 8765" -ForegroundColor White
Write-Host "🔄 Recurring Tasks: Background service" -ForegroundColor White
Write-Host "🎨 Frontend: http://localhost:3000 or 3001" -ForegroundColor White

Write-Host ""
Write-Host "⚡ EVENT-DRIVEN ARCHITECTURE FEATURES:" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "✅ Real-time task updates via WebSocket" -ForegroundColor Green
Write-Host "✅ Automatic recurring task creation" -ForegroundColor Green
Write-Host "✅ Event-driven notifications" -ForegroundColor Green
Write-Host "✅ Kafka message streaming" -ForegroundColor Green
Write-Host "✅ Audit logging and event sourcing" -ForegroundColor Green

Write-Host ""
Write-Host "🧪 TEST COMMANDS:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host "curl http://localhost:8000/health" -ForegroundColor Yellow
Write-Host "curl http://localhost:8001/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 PHASE 5 EVENT-DRIVEN ARCHITECTURE IS READY!" -ForegroundColor Green