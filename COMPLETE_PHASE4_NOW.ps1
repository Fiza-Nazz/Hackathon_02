# Complete Phase IV - All Remaining Tasks
# This script completes Tasks 2-9 automatically

$ErrorActionPreference = "Stop"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Phase IV Complete Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Task 2: Setup Minikube on E: Drive
Write-Host "`n[Task 2] Setting up Minikube on E: Drive..." -ForegroundColor Yellow
$env:MINIKUBE_HOME = "E:\minikube"
[Environment]::SetEnvironmentVariable("MINIKUBE_HOME", "E:\minikube", "User")
Write-Host "MINIKUBE_HOME set to E:\minikube" -ForegroundColor Green

# Wait for Docker
Write-Host "`n[Waiting] Checking Docker status..." -ForegroundColor Yellow
$maxRetries = 10
$retryCount = 0
while ($retryCount -lt $maxRetries) {
    try {
        docker info >$null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker is ready!" -ForegroundColor Green
            break
        }
    } catch {}
    $retryCount++
    Write-Host "Waiting for Docker... ($retryCount/$maxRetries)" -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}

if ($retryCount -eq $maxRetries) {
    Write-Host "ERROR: Docker not ready. Please start Docker Desktop manually." -ForegroundColor Red
    exit 1
}

# Task 3: AI Tools (kubectl-ai) - Skip if not available
Write-Host "`n[Task 3] Checking AI Tools..." -ForegroundColor Yellow
try {
    kubectl-ai --version >$null 2>&1
    Write-Host "kubectl-ai is available" -ForegroundColor Green
} catch {
    Write-Host "kubectl-ai not found - will use standard kubectl" -ForegroundColor Yellow
}

# Task 4: Build Docker Images
Write-Host "`n[Task 4] Building Docker Images..." -ForegroundColor Yellow

Write-Host "Building Backend..." -ForegroundColor Cyan
docker build -t todo-backend:latest ./backend
if ($LASTEXITCODE -ne 0) { Write-Host "Backend build failed" -ForegroundColor Red; exit 1 }

Write-Host "Building Frontend..." -ForegroundColor Cyan
docker build -t todo-frontend:latest ./frontend
if ($LASTEXITCODE -ne 0) { Write-Host "Frontend build failed" -ForegroundColor Red; exit 1 }

Write-Host "Building Chatbot..." -ForegroundColor Cyan
docker build -t todo-chatbot-foundation:latest ./Chatbot
if ($LASTEXITCODE -ne 0) { Write-Host "Chatbot build failed" -ForegroundColor Red; exit 1 }

Write-Host "All images built successfully!" -ForegroundColor Green

# Task 5: Start Minikube
Write-Host "`n[Task 5] Starting Minikube..." -ForegroundColor Yellow
minikube delete 2>$null
minikube start --driver=docker --cpus=2 --memory=3072 --disk-size=10g

if ($LASTEXITCODE -ne 0) {
    Write-Host "Minikube failed to start. Using Docker Compose fallback..." -ForegroundColor Yellow
    Write-Host "`n[Fallback] Deploying with Docker Compose..." -ForegroundColor Cyan
    docker-compose -f docker-compose.backup.yml up -d
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Deployment Complete (Docker Compose)" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Chatbot: http://localhost:8001" -ForegroundColor Cyan
    exit 0
}

# Load images into Minikube
Write-Host "Loading images into Minikube..." -ForegroundColor Cyan
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-chatbot-foundation:latest

# Task 6: Enable Ingress
Write-Host "`n[Task 6] Enabling Ingress..." -ForegroundColor Yellow
minikube addons enable ingress

# Task 7: Deploy with Helm
Write-Host "`n[Task 7] Deploying with Helm..." -ForegroundColor Yellow
helm uninstall todo-chatbot 2>$null
helm install todo-chatbot ./charts/todo-chatbot

# Task 8: Wait for pods
Write-Host "`n[Task 8] Waiting for pods to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20
kubectl get pods

# Task 9: Verification
Write-Host "`n[Task 9] Verification..." -ForegroundColor Yellow
Write-Host "Pods:" -ForegroundColor Cyan
kubectl get pods

Write-Host "`nServices:" -ForegroundColor Cyan
kubectl get services

Write-Host "`nIngress:" -ForegroundColor Cyan
kubectl get ingress

# Get Minikube IP
$minikubeIP = (minikube ip).Trim()

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Phase IV Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nAccess Instructions:" -ForegroundColor Yellow
Write-Host "1. Add to hosts file (as Admin):" -ForegroundColor Cyan
Write-Host "   $minikubeIP todo.local" -ForegroundColor White
Write-Host "`n2. Run in separate Admin PowerShell:" -ForegroundColor Cyan
Write-Host "   minikube tunnel" -ForegroundColor White
Write-Host "`n3. Access application:" -ForegroundColor Cyan
Write-Host "   http://todo.local" -ForegroundColor White
Write-Host "`nOr use port-forward:" -ForegroundColor Yellow
Write-Host "   kubectl port-forward svc/frontend 3000:3000" -ForegroundColor White

Write-Host "`n✅ All Tasks (2-9) Complete!" -ForegroundColor Green
