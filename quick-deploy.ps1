# Phase IV Quick Deployment Script
# Run this after Minikube is successfully started

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Phase IV: Todo Chatbot Deployment Quick Start" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Verify Minikube
Write-Host "[1/6] Verifying Minikube status..." -ForegroundColor Yellow
minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Minikube is not running!" -ForegroundColor Red
    Write-Host "Run: minikube start --driver=docker --cpus=2 --memory=3072 --disk-size=10g" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Minikube is running`n" -ForegroundColor Green

# Step 2: Enable Ingress
Write-Host "[2/6] Enabling Ingress addon..." -ForegroundColor Yellow
minikube addons enable ingress
Write-Host "✓ Ingress enabled`n" -ForegroundColor Green

# Step 3: Configure Docker Environment
Write-Host "[3/6] Configuring Docker to use Minikube's daemon..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
Write-Host "✓ Docker environment configured`n" -ForegroundColor Green

# Step 4: Build Docker Images
Write-Host "[4/6] Building Docker images..." -ForegroundColor Yellow
Write-Host "This may take 10-15 minutes...`n" -ForegroundColor Cyan

# Backend
Write-Host "Building Backend image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\backend
docker build -t todo-backend:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Backend build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Backend image built`n" -ForegroundColor Green

# Frontend
Write-Host "Building Frontend image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\frontend
docker build -t todo-frontend:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Frontend build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Frontend image built`n" -ForegroundColor Green

# Chatbot
Write-Host "Building Chatbot image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\Chatbot
docker build -t todo-chatbot-foundation:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Chatbot build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Chatbot image built`n" -ForegroundColor Green

# Verify images
Write-Host "Verifying all images..." -ForegroundColor Cyan
docker images | Select-String "todo-"
Write-Host ""

# Step 5: Deploy with Helm
Write-Host "[5/6] Deploying with Helm..." -ForegroundColor Yellow
Set-Location E:\Hackathon_02
helm install todo-chatbot ./charts/todo-chatbot
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Helm deployment failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Helm chart deployed`n" -ForegroundColor Green

# Wait for pods to be ready
Write-Host "Waiting for pods to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
kubectl get pods

# Step 6: Configure Ingress Access
Write-Host "`n[6/6] Configuring Ingress access..." -ForegroundColor Yellow
$minikubeIP = (minikube ip).Trim()
Write-Host "Minikube IP: $minikubeIP" -ForegroundColor Cyan

# Check if hosts entry exists
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"
$hostsContent = Get-Content $hostsPath -Raw
if ($hostsContent -match "todo.local") {
    Write-Host "✓ Hosts entry already exists`n" -ForegroundColor Green
} else {
    Write-Host "`nTo access the app, add this to your hosts file (run as Administrator):" -ForegroundColor Yellow
    Write-Host "Add-Content -Path $hostsPath -Value `"``n$minikubeIP todo.local`"`n" -ForegroundColor Cyan
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deployment Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

kubectl get all

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Open PowerShell as Administrator and run:" -ForegroundColor Yellow
Write-Host "   minikube tunnel" -ForegroundColor Cyan
Write-Host "`n2. (If not done) Add to hosts file (run as Administrator):" -ForegroundColor Yellow
Write-Host "   Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value `"``n$minikubeIP todo.local`"" -ForegroundColor Cyan
Write-Host "`n3. Open browser and visit:" -ForegroundColor Yellow
Write-Host "   http://todo.local" -ForegroundColor Cyan
Write-Host "`n4. Install kubectl-ai:" -ForegroundColor Yellow
Write-Host "   npm install -g kubectl-ai" -ForegroundColor Cyan
Write-Host "`n5. Try kubectl-ai:" -ForegroundColor Yellow
Write-Host "   kubectl-ai `"check deployment status`"" -ForegroundColor Cyan
Write-Host "`n========================================`n" -ForegroundColor Cyan

Write-Host "Deployment complete! 🎉" -ForegroundColor Green
