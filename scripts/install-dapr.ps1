# Install Dapr on Minikube
Write-Host "🚀 Installing Dapr on Minikube..." -ForegroundColor Green

# Check if Dapr CLI is installed
$daprVersion = dapr --version 2>$null
if (-not $daprVersion) {
    Write-Host "❌ Dapr CLI not found. Installing..." -ForegroundColor Yellow
    
    # Install Dapr CLI
    powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
    
    Write-Host "✅ Dapr CLI installed" -ForegroundColor Green
} else {
    Write-Host "✅ Dapr CLI already installed: $daprVersion" -ForegroundColor Green
}

# Initialize Dapr on Kubernetes
Write-Host "📦 Initializing Dapr on Kubernetes..." -ForegroundColor Cyan
dapr init -k

# Wait for Dapr to be ready
Write-Host "⏳ Waiting for Dapr to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=ready pod -l app=dapr-operator -n dapr-system --timeout=300s
kubectl wait --for=condition=ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
kubectl wait --for=condition=ready pod -l app=dapr-sentry -n dapr-system --timeout=300s
kubectl wait --for=condition=ready pod -l app=dapr-placement-server -n dapr-system --timeout=300s

# Verify Dapr installation
Write-Host "🔍 Verifying Dapr installation..." -ForegroundColor Cyan
dapr status -k

Write-Host "✅ Dapr installed successfully on Minikube!" -ForegroundColor Green
