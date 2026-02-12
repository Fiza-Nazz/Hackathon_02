# Deploy Todo-Chatbot to Local Minikube
# Usage: ./deploy.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Deployment for Todo Chatbot Phase 4..." -ForegroundColor Green

# 1. Check/Start Minikube
Write-Host "`n📦 Checking Minikube Status..."
$minikubeStatus = minikube status --format='{{.Host}}' 2>$null
if ($minikubeStatus -ne "Running") {
    Write-Host "Minikube is not running. Starting..." -ForegroundColor Yellow
    minikube start --driver=docker --ports=8000,3000,8001
} else {
    Write-Host "Minikube is already running." -ForegroundColor Green
}

# 2. Enable Ingress
Write-Host "`n🌐 Enabling Ingress Addon..."
minikube addons enable ingress

# 3. Environment Setup
Write-Host "`n🔧 Configuring Environment..."
# Ensure we are using Minikube's Docker daemon
# This is crucial for local images
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# 4. Build Images
Write-Host "`n🏗️  Building Docker Images..."
Write-Host "   - Building Frontend..."
docker build -t todo-frontend:latest ./frontend

Write-Host "   - Building Backend..."
docker build -t todo-backend:latest ./backend

Write-Host "   - Building Chatbot Foundation..."
docker build -t todo-chatbot-foundation:latest ./Chatbot

# 5. Helm Deployment
Write-Host "`n⚓ Deploying Helm Chart..."
# Check if release exists
$release = helm list -q --filter 'todo-chatbot'
if ($release) {
    Write-Host "Upgrading existing release..."
    helm upgrade todo-chatbot ./charts/todo-chatbot
} else {
    Write-Host "Installing new release..."
    helm install todo-chatbot ./charts/todo-chatbot
}

# 6. Verification
Write-Host "`n✅ Deployment Commands Sent!"
Write-Host "Running Pods:"
kubectl get pods

Write-Host "`n🌍 Access Information:"
$ip = minikube ip
Write-Host "Minikube IP: $ip"
Write-Host "Add this to your hosts file (C:\Windows\System32\drivers\etc\hosts):"
Write-Host "$ip todo.local"
Write-Host "`nApp URL: http://todo.local"
Write-Host "API URL: http://todo.local/api"
