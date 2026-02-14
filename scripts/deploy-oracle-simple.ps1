# Simple Oracle Cloud Deployment Script
param(
    [Parameter(Mandatory=$false)]
    [string]$CompartmentId = "",
    
    [Parameter(Mandatory=$false)]
    [string]$ClusterId = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-ashburn-1"
)

Write-Host "Oracle Cloud Deployment for Phase 5" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Check if parameters provided
if ([string]::IsNullOrEmpty($CompartmentId) -or [string]::IsNullOrEmpty($ClusterId)) {
    Write-Host "`nERROR: Missing required parameters" -ForegroundColor Red
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\deploy-oracle-simple.ps1 -CompartmentId 'ocid1.compartment...' -ClusterId 'ocid1.cluster...'" -ForegroundColor White
    Write-Host "`nTo get your IDs:" -ForegroundColor Yellow
    Write-Host "  1. Login to Oracle Cloud Console" -ForegroundColor White
    Write-Host "  2. Go to Identity > Compartments (copy Compartment OCID)" -ForegroundColor White
    Write-Host "  3. Go to Developer Services > Kubernetes Clusters (copy Cluster OCID)" -ForegroundColor White
    exit 1
}

# Step 1: Configure kubectl for OKE
Write-Host "`nStep 1: Configuring kubectl for OKE..." -ForegroundColor Cyan
Write-Host "  Creating kubeconfig..." -ForegroundColor White

oci ce cluster create-kubeconfig `
    --cluster-id $ClusterId `
    --file $HOME\.kube\config-oke `
    --region $Region `
    --token-version 2.0.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Failed to create kubeconfig" -ForegroundColor Red
    Write-Host "  Make sure OCI CLI is configured: oci setup config" -ForegroundColor Yellow
    exit 1
}

$env:KUBECONFIG="$HOME\.kube\config-oke"
Write-Host "  OK: kubectl configured for OKE" -ForegroundColor Green

# Verify connection
Write-Host "  Verifying connection..." -ForegroundColor White
kubectl get nodes
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Cannot connect to OKE cluster" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Connected to OKE cluster" -ForegroundColor Green

# Step 2: Create namespace
Write-Host "`nStep 2: Creating namespace..." -ForegroundColor Cyan
kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -
Write-Host "  OK: Namespace created" -ForegroundColor Green

# Step 3: Create secrets
Write-Host "`nStep 3: Creating secrets..." -ForegroundColor Cyan
if ([string]::IsNullOrEmpty($env:DATABASE_URL)) {
    Write-Host "  WARNING: DATABASE_URL not set" -ForegroundColor Yellow
    Write-Host "  Set it with: `$env:DATABASE_URL='postgresql://...'" -ForegroundColor White
} else {
    kubectl create secret generic db-secret `
        --from-literal=connectionString=$env:DATABASE_URL `
        --namespace=todo-chatbot `
        --dry-run=client -o yaml | kubectl apply -f -
    Write-Host "  OK: Database secret created" -ForegroundColor Green
}

# Step 4: Install Dapr
Write-Host "`nStep 4: Installing Dapr..." -ForegroundColor Cyan
C:\dapr\dapr.exe init -k --wait --timeout 300
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Dapr installation failed" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: Dapr installed" -ForegroundColor Green

# Step 5: Deploy Kafka
Write-Host "`nStep 5: Deploying Kafka..." -ForegroundColor Cyan
kubectl apply -f k8s/kafka-deployment.yaml --namespace=todo-chatbot
Write-Host "  Waiting for Kafka..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=kafka --namespace=todo-chatbot --timeout=300s
Write-Host "  OK: Kafka deployed" -ForegroundColor Green

# Step 6: Deploy Dapr Components
Write-Host "`nStep 6: Deploying Dapr Components..." -ForegroundColor Cyan
kubectl apply -f dapr-components/ --namespace=todo-chatbot
Write-Host "  OK: Dapr components deployed" -ForegroundColor Green

# Step 7: Deploy Microservices
Write-Host "`nStep 7: Deploying Microservices..." -ForegroundColor Cyan
kubectl apply -f k8s/notification-service.yaml --namespace=todo-chatbot
kubectl apply -f k8s/recurring-task-service.yaml --namespace=todo-chatbot
Write-Host "  Waiting for services..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host "  OK: Microservices deployed" -ForegroundColor Green

# Step 8: Deploy Monitoring
Write-Host "`nStep 8: Deploying Monitoring..." -ForegroundColor Cyan
kubectl apply -f k8s/monitoring/prometheus.yaml
kubectl apply -f k8s/monitoring/grafana.yaml
Write-Host "  OK: Monitoring deployed" -ForegroundColor Green

# Step 9: Display Status
Write-Host "`n======================================" -ForegroundColor Green
Write-Host "ORACLE CLOUD DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

Write-Host "`nPod Status:" -ForegroundColor Cyan
kubectl get pods --namespace=todo-chatbot

Write-Host "`nServices:" -ForegroundColor Cyan
kubectl get services --namespace=todo-chatbot

Write-Host "`nMonitoring:" -ForegroundColor Cyan
kubectl get pods --namespace=monitoring

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Get LoadBalancer IPs: kubectl get svc --namespace=todo-chatbot" -ForegroundColor White
Write-Host "  2. Configure DNS for your domain" -ForegroundColor White
Write-Host "  3. Setup SSL certificates" -ForegroundColor White
Write-Host "  4. Access Grafana: kubectl port-forward -n monitoring svc/grafana 3000:3000" -ForegroundColor White

Write-Host "`nDeployment to Oracle Cloud complete!" -ForegroundColor Green
