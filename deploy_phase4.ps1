# Phase IV Final Deployment Script
$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Phase IV: Reliable Todo Chatbot Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan


# Step 1: Clean Minikube Environment
Write-Host "Checking Docker Status..." -ForegroundColor Yellow
Write-Host "Checking Docker Status..." -ForegroundColor Yellow
docker info >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker Desktop is NOT running (docker info failed)." -ForegroundColor Red
    Write-Host "Please start Docker Desktop manually and wait for it to turn green." -ForegroundColor Red
    exit 1
}
Write-Host "Docker is Running" -ForegroundColor Green

# Step 1: Clean Minikube Environment
Write-Host "[1/8] Cleaning up old Minikube status..." -ForegroundColor Yellow
$env:MINIKUBE_HOME = "E:\minikube"
docker rm -f minikube 2>$null
docker volume prune -f 2>$null
minikube delete 2>$null
Write-Host "Cleanup complete" -ForegroundColor Green

# Step 2: Build Docker Images Locally
Write-Host "[2/8] Building Docker images locally..." -ForegroundColor Yellow

# Backend
Write-Host "Building Backend image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\backend
docker build -t todo-backend:latest .
Write-Host "Backend image built" -ForegroundColor Green

# Frontend
Write-Host "Building Frontend image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\frontend
docker build -t todo-frontend:latest .
Write-Host "Frontend image built" -ForegroundColor Green

# Chatbot
Write-Host "Building Chatbot image..." -ForegroundColor Cyan
Set-Location E:\Hackathon_02\Chatbot
docker build -t todo-chatbot-foundation:latest .
Write-Host "Chatbot image built" -ForegroundColor Green


# Step 3: Start Minikube Fresh (New Profile)
Write-Host "[3/8] Starting Minikube fresh (Profile: minikube-phase4)..." -ForegroundColor Yellow
minikube start -p minikube-phase4 --driver=docker --cpus=2 --memory=3072 --disk-size=10g --ports=80:80
Write-Host "Minikube started" -ForegroundColor Green

# Step 4: Load Images into Minikube
Write-Host "[4/8] Loading images into Minikube..." -ForegroundColor Yellow
minikube -p minikube-phase4 image load todo-backend:latest
minikube -p minikube-phase4 image load todo-frontend:latest
minikube -p minikube-phase4 image load todo-chatbot-foundation:latest
Write-Host "Images loaded into Minikube" -ForegroundColor Green

# Step 5: Enable Ingress
Write-Host "[5/8] Enabling Ingress addon..." -ForegroundColor Yellow
minikube -p minikube-phase4 addons enable ingress
Write-Host "Ingress enabled" -ForegroundColor Green

# Step 6: Deploy with Helm
Write-Host "[6/8] Deploying with Helm..." -ForegroundColor Yellow
Set-Location E:\Hackathon_02
helm upgrade --install todo-chatbot ./charts/todo-chatbot --kube-context minikube-phase4
Write-Host "Helm deployment triggered" -ForegroundColor Green

# Step 7: Wait and Verify
Write-Host "[7/8] Waiting for pods to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 15
kubectl --context minikube-phase4 get pods

# Step 8: Configure Access
Write-Host "[8/8] Access Configuration" -ForegroundColor Yellow
$minikubeIP = (minikube -p minikube-phase4 ip).Trim()
Write-Host "Minikube IP: $minikubeIP" -ForegroundColor Cyan
Write-Host "Add this to your hosts file: $minikubeIP todo.local" -ForegroundColor Yellow
Write-Host "Run 'minikube -p minikube-phase4 tunnel' in a separate Admin shell to access Ingress." -ForegroundColor Yellow

Write-Host "Deployment Script Complete!" -ForegroundColor Green
