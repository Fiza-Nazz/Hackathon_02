# PHASE4_DEPLOY.ps1 - Automated Kubernetes Deployment Script
# Project: Cloud-Native Todo Chatbot

$ErrorActionPreference = "Stop"

Write-Host "--- PHASE 4 KUBERNETES DEPLOYMENT STARTING ---" -ForegroundColor Cyan

# 1. Start Minikube cluster
Write-Host "[1/8] Starting Minikube cluster..." -ForegroundColor Yellow
minikube start --driver=docker

# 2. Enable Ingress addon
Write-Host "[2/8] Enabling Ingress addon..." -ForegroundColor Yellow
minikube addons enable ingress

# 3. Build Docker images inside Minikube's Docker environment
Write-Host "[3/8] Building Docker images inside Minikube environment..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "Building todo-backend..."
docker build -t todo-backend:latest ./backend
Write-Host "Building todo-frontend..."
docker build -t todo-frontend:latest ./frontend
Write-Host "Building todo-chatbot-foundation..."
docker build -t todo-chatbot-foundation:latest ./Chatbot

# 4. Deploy using Helm chart
Write-Host "[4/8] Deploying application using Helm..." -ForegroundColor Yellow
helm upgrade --install todo-chatbot ./charts/todo-chatbot

# 5. Verify pods are running
Write-Host "[5/8] Verifying pod status..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
kubectl get pods

# 6. Verify replicas
Write-Host "[6/8] Verifying frontend replicas (should be 2)..." -ForegroundColor Yellow
kubectl get deployment todo-chatbot-frontend

# 7. Configure /etc/hosts (Info Only)
$MINIKUBE_IP = minikube ip
Write-Host "[7/8] Configuration Information:" -ForegroundColor Green
Write-Host "Add the following line to C:\Windows\System32\drivers\etc\hosts:"
Write-Host "$MINIKUBE_IP todo.local"

# 8. Check Ingress and Enable Direct Access
Write-Host "[8/8] Configuring Application Access..." -ForegroundColor Yellow

# Ensure Ingress is active
kubectl get ingress

# Setup robust port-forwarding for Windows users
Write-Host "Setting up direct access tunnel to default port 8080..." -ForegroundColor Cyan

# Kill any existing port-forwards to avoid conflicts
Get-Process kubectl -ErrorAction SilentlyContinue | Stop-Process -Force

# Start port-forward in background
Start-Process kubectl -ArgumentList "port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80 --address 0.0.0.0" -NoNewWindow
Start-Sleep -Seconds 5

Write-Host "--- DEPLOYMENT SCRIPT COMPLETED ---" -ForegroundColor Cyan
Write-Host "================================================================"
Write-Host "SUCCESS! Application is now accessible at: http://localhost:8080"
Write-Host "================================================================"
Write-Host "(Keep this window open to maintain the connection)"



