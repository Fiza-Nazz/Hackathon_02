# Phase 5 Quick Start - Complete Deployment
Write-Host "🚀 Phase 5 Quick Start - Event-Driven Architecture" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check prerequisites
Write-Host "`n✅ Checking prerequisites..." -ForegroundColor Cyan

# Check Docker
$dockerRunning = docker ps 2>$null
if (-not $dockerRunning) {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Docker Desktop running" -ForegroundColor Green

# Check Minikube
$minikubeStatus = minikube status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Minikube is not running. Starting Minikube..." -ForegroundColor Yellow
    minikube start
}
Write-Host "  ✓ Minikube running" -ForegroundColor Green

# Check kubectl
$kubectlVersion = kubectl version --client --short 2>$null
if (-not $kubectlVersion) {
    Write-Host "❌ kubectl not found. Please install kubectl." -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ kubectl installed" -ForegroundColor Green

Write-Host "`n📦 Starting Phase 5 deployment..." -ForegroundColor Cyan

# Step 1: Install Dapr
Write-Host "`n[1/3] Installing Dapr..." -ForegroundColor Yellow
& "$PSScriptRoot\install-dapr.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dapr installation failed" -ForegroundColor Red
    exit 1
}

# Step 2: Deploy Phase 5 services
Write-Host "`n[2/3] Deploying Phase 5 services..." -ForegroundColor Yellow
& "$PSScriptRoot\deploy-phase5.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Phase 5 deployment failed" -ForegroundColor Red
    exit 1
}

# Step 3: Verify deployment
Write-Host "`n[3/3] Verifying deployment..." -ForegroundColor Yellow

Write-Host "`n📊 Pod Status:" -ForegroundColor Cyan
kubectl get pods | Select-String -Pattern "kafka|notification|recurring|backend|frontend|chatbot"

Write-Host "`n📊 Service Status:" -ForegroundColor Cyan
kubectl get services | Select-String -Pattern "kafka|notification|recurring|backend|frontend|chatbot"

Write-Host "`n📊 Dapr Components:" -ForegroundColor Cyan
kubectl get components

Write-Host "`n✅ Phase 5 deployment complete!" -ForegroundColor Green
Write-Host "`n📚 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Read PHASE5_DEPLOYMENT_GUIDE.md for testing instructions" -ForegroundColor White
Write-Host "  2. Test event publishing by creating/updating tasks" -ForegroundColor White
Write-Host "  3. Monitor logs: kubectl logs -f <pod-name>" -ForegroundColor White
Write-Host "  4. Check Kafka topics: kubectl exec -it <kafka-pod> -- rpk topic list" -ForegroundColor White

Write-Host "`n🎉 Phase 5 is ready! Happy coding!" -ForegroundColor Green
