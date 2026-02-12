# Quick Phase IV Deployment Script
Write-Host "Phase IV Quick Deploy Starting..." -ForegroundColor Cyan

# Check Docker
docker info >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Start Docker Desktop first!" -ForegroundColor Red
    exit 1
}

# Option 1: Docker Compose (Fastest)
Write-Host "Deploying with Docker Compose..." -ForegroundColor Yellow
docker-compose -f docker-compose.backup.yml up -d

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Chatbot: http://localhost:8001" -ForegroundColor Cyan
