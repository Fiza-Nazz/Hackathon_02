# Deploy to Oracle Cloud OKE
param(
    [Parameter(Mandatory=$true)]
    [string]$CompartmentId,
    
    [Parameter(Mandatory=$true)]
    [string]$ClusterId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-ashburn-1"
)

Write-Host "🚀 Deploying Phase 5 to Oracle Cloud OKE..." -ForegroundColor Green

# Step 1: Configure kubectl for OKE
Write-Host "`n[1/6] Configuring kubectl for OKE..." -ForegroundColor Cyan
oci ce cluster create-kubeconfig `
    --cluster-id $ClusterId `
    --file $HOME\.kube\config-oke `
    --region $Region

$env:KUBECONFIG="$HOME\.kube\config-oke"

# Verify connection
kubectl get nodes
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to connect to OKE cluster" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Connected to OKE cluster" -ForegroundColor Green

# Step 2: Create namespace
Write-Host "`n[2/6] Creating namespace..." -ForegroundColor Cyan
kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -

# Step 3: Create secrets
Write-Host "`n[3/6] Creating secrets..." -ForegroundColor Cyan
kubectl create secret generic db-secret `
    --from-literal=connectionString=$env:DATABASE_URL `
    --namespace=todo-chatbot `
    --dry-run=client -o yaml | kubectl apply -f -

# Step 4: Install Dapr
Write-Host "`n[4/6] Installing Dapr..." -ForegroundColor Cyan
C:\dapr\dapr.exe init -k --wait --timeout 300

# Step 5: Deploy Phase 5 services
Write-Host "`n[5/6] Deploying services..." -ForegroundColor Cyan
kubectl apply -f k8s/ --namespace=todo-chatbot
kubectl apply -f dapr-components/ --namespace=todo-chatbot

# Step 6: Wait for deployments
Write-Host "`n[6/6] Waiting for deployments..." -ForegroundColor Cyan
kubectl wait --for=condition=ready pod -l app=kafka --namespace=todo-chatbot --timeout=300s
kubectl wait --for=condition=ready pod -l app=notification-service --namespace=todo-chatbot --timeout=300s

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`n📊 Service Status:" -ForegroundColor Cyan
kubectl get pods --namespace=todo-chatbot
kubectl get services --namespace=todo-chatbot
