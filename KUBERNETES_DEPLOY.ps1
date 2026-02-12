# Full Kubernetes Deployment with Minikube
$ErrorActionPreference = "Stop"

Write-Host "Starting Minikube Kubernetes Deployment..." -ForegroundColor Cyan

# Start Minikube
Write-Host "[1/5] Starting Minikube..." -ForegroundColor Yellow
minikube start --driver=docker --cpus=2 --memory=3072

# Build Images
Write-Host "[2/5] Building Docker Images..." -ForegroundColor Yellow
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend
docker build -t todo-chatbot-foundation:latest ./Chatbot

# Load into Minikube
Write-Host "[3/5] Loading Images into Minikube..." -ForegroundColor Yellow
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-chatbot-foundation:latest

# Deploy with Helm
Write-Host "[4/5] Deploying with Helm..." -ForegroundColor Yellow
helm install todo-chatbot ./charts/todo-chatbot

# Enable Ingress
Write-Host "[5/5] Enabling Ingress..." -ForegroundColor Yellow
minikube addons enable ingress

Write-Host "✅ Kubernetes Deployment Complete!" -ForegroundColor Green
Write-Host "Run 'minikube tunnel' to access via http://todo.local" -ForegroundColor Cyan
Write-Host "Or use: kubectl port-forward svc/frontend 3000:3000" -ForegroundColor Cyan
