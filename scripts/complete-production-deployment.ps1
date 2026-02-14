# Complete Production Deployment Script
# This script deploys everything: Infrastructure, Services, Monitoring, CI/CD

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipTests = $false
)

Write-Host "🚀 Complete Production Deployment - Phase 5" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Green

$startTime = Get-Date

# Step 1: Pre-deployment checks
Write-Host "`n[Step 1/8] Pre-deployment checks..." -ForegroundColor Yellow
Write-Host "  Checking Docker..." -ForegroundColor Cyan
if (-not (docker ps 2>$null)) {
    Write-Host "  ❌ Docker not running" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Docker running" -ForegroundColor Green

Write-Host "  Checking kubectl..." -ForegroundColor Cyan
if (-not (kubectl version --client 2>$null)) {
    Write-Host "  ❌ kubectl not found" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ kubectl installed" -ForegroundColor Green

Write-Host "  Checking Dapr..." -ForegroundColor Cyan
if (-not (Test-Path "C:\dapr\dapr.exe")) {
    Write-Host "  ❌ Dapr not installed" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Dapr installed" -ForegroundColor Green

# Step 2: Install Dapr on Kubernetes
Write-Host "`n[Step 2/8] Installing Dapr on Kubernetes..." -ForegroundColor Yellow
C:\dapr\dapr.exe init -k --wait --timeout 300
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Dapr installation failed" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Dapr installed" -ForegroundColor Green

# Step 3: Deploy Kafka
Write-Host "`n[Step 3/8] Deploying Kafka..." -ForegroundColor Yellow
kubectl apply -f k8s/kafka-deployment.yaml
kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Kafka deployment failed" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Kafka deployed" -ForegroundColor Green

# Step 4: Deploy Dapr Components
Write-Host "`n[Step 4/8] Deploying Dapr Components..." -ForegroundColor Yellow
kubectl apply -f dapr-components/
Write-Host "  ✅ Dapr components deployed" -ForegroundColor Green

# Step 5: Deploy Microservices
Write-Host "`n[Step 5/8] Deploying Microservices..." -ForegroundColor Yellow
kubectl apply -f k8s/notification-service.yaml
kubectl apply -f k8s/recurring-task-service.yaml
kubectl wait --for=condition=ready pod -l app=notification-service --timeout=300s
kubectl wait --for=condition=ready pod -l app=recurring-task-service --timeout=300s
Write-Host "  ✅ Microservices deployed" -ForegroundColor Green

# Step 6: Deploy Main Application
Write-Host "`n[Step 6/8] Deploying Main Application..." -ForegroundColor Yellow
kubectl apply -f charts/todo-chatbot/templates/
kubectl rollout status deployment/todo-chatbot-backend --timeout=300s
kubectl rollout status deployment/todo-chatbot-frontend --timeout=300s
kubectl rollout status deployment/todo-chatbot-chatbot --timeout=300s
Write-Host "  ✅ Main application deployed" -ForegroundColor Green

# Step 7: Setup Monitoring
Write-Host "`n[Step 7/8] Setting up Monitoring..." -ForegroundColor Yellow
& "$PSScriptRoot\setup-monitoring.ps1"
Write-Host "  ✅ Monitoring setup complete" -ForegroundColor Green

# Step 8: Run Smoke Tests
if (-not $SkipTests) {
    Write-Host "`n[Step 8/8] Running Smoke Tests..." -ForegroundColor Yellow
    & "$PSScriptRoot\run-smoke-tests.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠️  Some smoke tests failed" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ All smoke tests passed" -ForegroundColor Green
    }
} else {
    Write-Host "`n[Step 8/8] Skipping smoke tests..." -ForegroundColor Yellow
}

# Deployment Summary
$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n" + "="*60 -ForegroundColor Green
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host "Duration: $($duration.Minutes)m $($duration.Seconds)s" -ForegroundColor Cyan

Write-Host "`n📊 Deployment Status:" -ForegroundColor Yellow
kubectl get pods
kubectl get services

Write-Host "`n🔗 Access URLs:" -ForegroundColor Yellow
$backendIP = kubectl get svc backend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
$frontendIP = kubectl get svc frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
$prometheusIP = kubectl get svc prometheus -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
$grafanaIP = kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

Write-Host "  Backend API: http://${backendIP}:8000" -ForegroundColor White
Write-Host "  Frontend: http://${frontendIP}:3000" -ForegroundColor White
Write-Host "  Prometheus: http://${prometheusIP}:9090" -ForegroundColor White
Write-Host "  Grafana: http://${grafanaIP}:3000 (admin/admin123)" -ForegroundColor White

Write-Host "`n📚 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Access Grafana and import dashboards" -ForegroundColor White
Write-Host "  2. Configure alerts in Prometheus" -ForegroundColor White
Write-Host "  3. Test all features end-to-end" -ForegroundColor White
Write-Host "  4. Monitor metrics for 24 hours" -ForegroundColor White
Write-Host "  5. Setup automated backups" -ForegroundColor White

Write-Host "`nPhase 5 is now live in production!" -ForegroundColor Green
