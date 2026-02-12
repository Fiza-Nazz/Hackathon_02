# PHASE 5 - QUICK START SCRIPT
# Start all services for immediate demo

Write-Host "🚀 PHASE 5 - QUICK START" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# Step 1: Start Backend
Write-Host "🔧 Starting Backend..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -WorkingDirectory "backend" -WindowStyle Hidden
Start-Sleep -Seconds 5

# Step 2: Start Chatbot  
Write-Host "🤖 Starting Chatbot..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "backend/http_server.py" -WorkingDirectory "Chatbot" -WindowStyle Hidden
Start-Sleep -Seconds 3

# Step 3: Start Frontend
Write-Host "🎨 Starting Frontend..." -ForegroundColor Yellow
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "frontend" -WindowStyle Hidden
Start-Sleep -Seconds 5

# Step 4: Start Notification Service
Write-Host "🔔 Starting Notifications..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "services/notification_service.py" -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ ALL PHASE 5 SERVICES STARTED!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "🔧 Backend: http://localhost:8000" -ForegroundColor White
Write-Host "🤖 Chatbot: http://localhost:8001" -ForegroundColor White  
Write-Host "🎨 Frontend: http://localhost:3000 or 3001" -ForegroundColor White
Write-Host "🔔 Notifications: WebSocket 8765" -ForegroundColor White
Write-Host ""
Write-Host "🎯 DEMO READY - PHASE 5 COMPLETE!" -ForegroundColor Green