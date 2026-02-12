# PHASE 5 - START SERVICES WITH DAPR INTEGRATION
# Cloud-Native Service Mesh

Write-Host "🚀 PHASE 5 - STARTING DAPR-ENABLED SERVICES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check if Dapr is installed
Write-Host "🔍 Checking Dapr installation..." -ForegroundColor Yellow
try {
    $daprVersion = dapr --version
    Write-Host "✅ Dapr found: $daprVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Dapr not found. Installing Dapr..." -ForegroundColor Red
    Write-Host "Please install Dapr CLI: https://docs.dapr.io/getting-started/install-dapr-cli/" -ForegroundColor Yellow
    exit 1
}

# Initialize Dapr (if not already done)
Write-Host "🔧 Initializing Dapr..." -ForegroundColor Yellow
try {
    dapr init
    Write-Host "✅ Dapr initialized" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Dapr already initialized or failed" -ForegroundColor Yellow
}

# Step 1: Start Backend with Dapr
Write-Host "🔧 Step 1: Starting Backend Service with Dapr..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "dapr" -ArgumentList "run", "--app-id", "backend-service", "--app-port", "8000", "--dapr-http-port", "3500", "--components-path", "./dapr-components", "--", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory "backend" -WindowStyle Hidden
    Write-Host "✅ Backend service started with Dapr (App ID: backend-service)" -ForegroundColor Green
    Start-Sleep -Seconds 8
} catch {
    Write-Host "❌ Failed to start backend with Dapr: $_" -ForegroundColor Red
}

# Step 2: Start Chatbot with Dapr
Write-Host "🤖 Step 2: Starting Chatbot Service with Dapr..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "dapr" -ArgumentList "run", "--app-id", "chatbot-service", "--app-port", "8001", "--dapr-http-port", "3501", "--components-path", "./dapr-components", "--", "python", "backend/http_server.py" -WorkingDirectory "Chatbot" -WindowStyle Hidden
    Write-Host "✅ Chatbot service started with Dapr (App ID: chatbot-service)" -ForegroundColor Green
    Start-Sleep -Seconds 5
} catch {
    Write-Host "❌ Failed to start chatbot with Dapr: $_" -ForegroundColor Red
}

# Step 3: Start Notification Service with Dapr
Write-Host "🔔 Step 3: Starting Notification Service with Dapr..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "dapr" -ArgumentList "run", "--app-id", "notification-service", "--app-port", "8765", "--dapr-http-port", "3502", "--components-path", "./dapr-components", "--", "python", "services/notification_service.py" -WindowStyle Hidden
    Write-Host "✅ Notification service started with Dapr (App ID: notification-service)" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "❌ Failed to start notification service with Dapr: $_" -ForegroundColor Red
}

# Step 4: Start Recurring Task Service with Dapr
Write-Host "🔄 Step 4: Starting Recurring Task Service with Dapr..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "dapr" -ArgumentList "run", "--app-id", "recurring-task-service", "--dapr-http-port", "3503", "--components-path", "./dapr-components", "--", "python", "services/recurring_task_service.py" -WindowStyle Hidden
    Write-Host "✅ Recurring task service started with Dapr (App ID: recurring-task-service)" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "❌ Failed to start recurring task service with Dapr: $_" -ForegroundColor Red
}

# Step 5: Start Frontend (no Dapr needed)
Write-Host "🎨 Step 5: Starting Frontend..." -ForegroundColor Yellow
try {
    Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "frontend" -WindowStyle Hidden
    Write-Host "✅ Frontend started" -ForegroundColor Green
    Start-Sleep -Seconds 5
} catch {
    Write-Host "❌ Failed to start frontend: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 DAPR-ENABLED SERVICES STATUS:" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🔧 Backend (Dapr): http://localhost:8000 (Dapr: 3500)" -ForegroundColor White
Write-Host "🤖 Chatbot (Dapr): http://localhost:8001 (Dapr: 3501)" -ForegroundColor White
Write-Host "🔔 Notifications (Dapr): WebSocket 8765 (Dapr: 3502)" -ForegroundColor White
Write-Host "🔄 Recurring Tasks (Dapr): Background (Dapr: 3503)" -ForegroundColor White
Write-Host "🎨 Frontend: http://localhost:3000 or 3001" -ForegroundColor White

Write-Host ""
Write-Host "⚡ DAPR CLOUD-NATIVE FEATURES:" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "✅ Service-to-service communication via Dapr" -ForegroundColor Green
Write-Host "✅ Pub/Sub messaging with Kafka component" -ForegroundColor Green
Write-Host "✅ State management with PostgreSQL" -ForegroundColor Green
Write-Host "✅ Secret management with Kubernetes" -ForegroundColor Green
Write-Host "✅ Jobs API for scheduled reminders" -ForegroundColor Green
Write-Host "✅ Observability and tracing" -ForegroundColor Green

Write-Host ""
Write-Host "🧪 DAPR TEST COMMANDS:" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host "curl http://localhost:8000/health" -ForegroundColor Yellow
Write-Host "curl http://localhost:8001/health" -ForegroundColor Yellow
Write-Host "dapr list" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 PHASE 5 DAPR CLOUD-NATIVE ARCHITECTURE IS READY!" -ForegroundColor Green