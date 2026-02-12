# Phase IV Reliable Deployment Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Phase IV: Reliable Todo Chatbot Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Clean Minikube Environment
Write-Host "[1/7] Cleaning up old Minikube status..." -ForegroundColor Yellow
$env:MINIKUBE_HOME = "E:\minikube"
docker rm -f minikube 2>$null
docker volume prune -f 2>$null
minikube delete 2>$null
Write-Host "✓ Cleanup complete`n" -ForegroundColor Green

# Step 2: Build Docker Images Locally (More Reliable)
Write-Host "[2/7] Building Docker images locally..." -ForegroundColor Yellow

# Backend
Write-Host "Building Backend image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\backend
docker build -t todo-backend:latest .
if ($LASTEXITCODE -ne 0) { throw "Backend build failed!" }
Write-Host "✓ Backend image built`n" -ForegroundColor Green

# Frontend
Write-Host "Building Frontend image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\frontend
docker build -t todo-frontend:latest .
if ($LASTEXITCODE -ne 0) { throw "Frontend build failed!" }
Write-Host "✓ Frontend image built`n" -ForegroundColor Green

# Chatbot
Write-Host "Building Chatbot image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\Chatbot
docker build -t todo-chatbot-foundation:latest .
if ($LASTEXITCODE -ne 0) { throw "Chatbot build failed!" }
Write-Host "✓ Chatbot image built`n" -ForegroundColor Green

# Step 3: Start Minikube Fresh
Write-Host "[3/7] Starting Minikube fresh (Docker driver)..." -ForegroundColor Yellow
minikube start --driver=docker --cpus=2 --memory=3072 --disk-size=10g --ports=80:80
if ($LASTEXITCODE -ne 0) { throw "Minikube start failed!" }
Write-Host "✓ Minikube started`n" -ForegroundColor Green

# Step 4: Load Images into Minikube
Write-Host "[4/7] Loading images into Minikube..." -ForegroundColor Yellow
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-chatbot-foundation:latest
Write-Host "✓ Images loaded into Minikube`n" -ForegroundColor Green

# Step 5: Enable Ingress
Write-Host "[5/7] Enabling Ingress addon..." -ForegroundColor Yellow
minikube addons enable ingress
Write-Host "✓ Ingress enabled`n" -ForegroundColor Green

# Step 6: Deploy with Helm
Write-Host "[6/7] Deploying with Helm..." -ForegroundColor Yellow
Set-Location E:\Hackathon_02
helm install todo-chatbot ./charts/todo-chatbot
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Helm install failed, trying upgrade..." -ForegroundColor Yellow
    helm upgrade --install todo-chatbot ./charts/todo-chatbot
}
Write-Host "✓ Helm deployment triggered`n" -ForegroundColor Green

# Wait
Write-Host "Waiting for pods to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 15
kubectl get pods

# Step 7: Configure Access
Write-Host "`n[7/7] Access Configuration" -ForegroundColor Yellow
$minikubeIP = (minikube ip).Trim()
Write-Host "Minikube IP: $minikubeIP" -ForegroundColor Cyan
Write-Host "Add this to your hosts file: $minikubeIP todo.local" -ForegroundColor Yellow
Write-Host "Run 'minikube tunnel' in a separate Admin shell to access Ingress." -ForegroundColor Yellow

# Step 8: Verify AI Tool
Write-Host "`n[8/7] Verifying AI Tool (kubectl-ai)..." -ForegroundColor Yellow
if (Test-Path "E:\kubectl-ai\kubectl-ai.exe") {
    & "E:\kubectl-ai\kubectl-ai.exe" --version
    Write-Host "✓ kubectl-ai found at E:\kubectl-ai\kubectl-ai.exe" -ForegroundColor Green
} else {
    Write-Host "⚠ kubectl-ai not found at E:\kubectl-ai\kubectl-ai.exe" -ForegroundColor Red
}

Write-Host "`nDeployment Script Complete! 🎉" -ForegroundColor Green
