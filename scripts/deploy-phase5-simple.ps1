# Simple Phase 5 Deployment Script
# No emojis, just deployment

Write-Host "Starting Phase 5 Deployment..." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Step 1: Check prerequisites
Write-Host "`nStep 1: Checking prerequisites..." -ForegroundColor Cyan

# Check Docker
Write-Host "  Checking Docker..." -ForegroundColor White
$dockerRunning = docker ps 2>$null
if (-not $dockerRunning) {
    Write-Host "  ERROR: Docker not running" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Docker running" -ForegroundColor Green

# Check kubectl
Write-Host "  Checking kubectl..." -ForegroundColor White
$kubectlVersion = kubectl version --client --short 2>$null
if (-not $kubectlVersion) {
    Write-Host "  ERROR: kubectl not found" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: kubectl installed" -ForegroundColor Green

# Check Dapr
Write-Host "  Checking Dapr..." -ForegroundColor White
if (-not (Test-Path "C:\dapr\dapr.exe")) {
    Write-Host "  ERROR: Dapr not installed" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Dapr installed" -ForegroundColor Green

# Step 2: Initialize Dapr on Kubernetes
Write-Host "`nStep 2: Initializing Dapr on Kubernetes..." -ForegroundColor Cyan
C:\dapr\dapr.exe init -k --wait --timeout 300
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Dapr initialization failed" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Dapr initialized" -ForegroundColor Green

# Step 3: Deploy Kafka
Write-Host "`nStep 3: Deploying Kafka..." -ForegroundColor Cyan
kubectl apply -f k8s/kafka-deployment.yaml
Write-Host "  Waiting for Kafka to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Kafka deployment failed" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Kafka deployed" -ForegroundColor Green

# Step 4: Deploy Dapr Components
Write-Host "`nStep 4: Deploying Dapr Components..." -ForegroundColor Cyan
kubectl apply -f dapr-components/
Write-Host "  OK: Dapr components deployed" -ForegroundColor Green

# Step 5: Deploy Notification Service
Write-Host "`nStep 5: Deploying Notification Service..." -ForegroundColor Cyan
kubectl apply -f k8s/notification-service.yaml
Write-Host "  Waiting for Notification Service..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=notification-service --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "  WARNING: Notification service deployment timeout" -ForegroundColor Yellow
} else {
    Write-Host "  OK: Notification service deployed" -ForegroundColor Green
}

# Step 6: Deploy Recurring Task Service
Write-Host "`nStep 6: Deploying Recurring Task Service..." -ForegroundColor Cyan
kubectl apply -f k8s/recurring-task-service.yaml
Write-Host "  Waiting for Recurring Task Service..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=recurring-task-service --timeout=300s
if ($LASTEXITCODE -ne 0) {
    Write-Host "  WARNING: Recurring task service deployment timeout" -ForegroundColor Yellow
} else {
    Write-Host "  OK: Recurring task service deployed" -ForegroundColor Green
}

# Step 7: Setup Monitoring
Write-Host "`nStep 7: Setting up Monitoring..." -ForegroundColor Cyan
kubectl apply -f k8s/monitoring/prometheus.yaml
kubectl apply -f k8s/monitoring/grafana.yaml
Write-Host "  Waiting for Prometheus..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=300s
Write-Host "  Waiting for Grafana..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=300s
Write-Host "  OK: Monitoring deployed" -ForegroundColor Green

# Step 8: Display Status
Write-Host "`n======================================" -ForegroundColor Green
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

Write-Host "`nDeployment Status:" -ForegroundColor Cyan
kubectl get pods --all-namespaces | Select-String -Pattern "kafka|notification|recurring|prometheus|grafana"

Write-Host "`nServices:" -ForegroundColor Cyan
kubectl get services --all-namespaces | Select-String -Pattern "kafka|notification|recurring|prometheus|grafana"

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Check pod status: kubectl get pods" -ForegroundColor White
Write-Host "  2. View logs: kubectl logs -f <pod-name>" -ForegroundColor White
Write-Host "  3. Access Grafana: kubectl port-forward -n monitoring svc/grafana 3000:3000" -ForegroundColor White
Write-Host "  4. Access Prometheus: kubectl port-forward -n monitoring svc/prometheus 9090:9090" -ForegroundColor White

Write-Host "`nPhase 5 deployment complete!" -ForegroundColor Green
