$ErrorActionPreference = "Continue"

# Configuration
$env:MINIKUBE_HOME = "E:\minikube\.minikube"
$GROQ_API_KEY = "YOUR_GROQ_API_KEY"
$env:GROQ_API_KEY = $GROQ_API_KEY
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", $GROQ_API_KEY, "User")

function Log-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Log-Error { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }
function Log-Success { param($msg) Write-Host "[SUCCESS] $msg" -ForegroundColor Green }

Log-Info "Starting Phase 4 Completion Script (Clean Version)..."

# 1. Minikube Check/Start
Log-Info "Checking Minikube..."
$status = minikube status 2>&1
if ($LASTEXITCODE -ne 0) {
    Log-Info "Minikube not running. Starting..."
    minikube start --driver=docker
    if ($LASTEXITCODE -ne 0) {
        Log-Error "Failed to start Minikube."
        exit 1
    }
}
Log-Success "Minikube is running."

# 2. Enable Ingress
Log-Info "Enabling Ingress..."
minikube addons enable ingress

# 3. Install kubectl-ai
Log-Info "Installing kubectl-ai..."
npm install -g kubectl-ai
if ($LASTEXITCODE -ne 0) { Log-Error "kubectl-ai install failed (ignoring)"; }

# 4. Configure Docker Env
Log-Info "Configuring Minikube Docker Env..."
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# 5. Build Images
Log-Info "Building Images..."
# Backend
cd E:\Hackathon_02\backend
Log-Info "Building Backend..."
docker build -t todo-backend:latest .
# Frontend
cd E:\Hackathon_02\frontend
Log-Info "Building Frontend..."
docker build -t todo-frontend:latest .
# Chatbot
cd E:\Hackathon_02\Chatbot
Log-Info "Building Chatbot..."
docker build -t todo-chatbot-foundation:latest .

# 6. Deploy Helm
cd E:\Hackathon_02
Log-Info "Deploying Helm Chart..."
helm upgrade --install todo-chatbot ./charts/todo-chatbot --namespace default

# 7. Configure Hosts (Guidelines only as script requires Admin)
$ip = minikube ip
Log-Info "Minikube IP is: $ip"
Log-Info "Please manually add '$ip todo.local' to C:\Windows\System32\drivers\etc\hosts if not present."
Log-Info "Running: Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value '`n$ip todo.local'"
try {
    Add-Content -Path "C:\Windows\System32\drivers\etc\hosts" -Value "`n$ip todo.local" -ErrorAction SilentlyContinue
    Log-Success "Added to hosts file."
} catch {
    Log-Info "Could not write to hosts file (requires Admin). Please do it manually."
}

# 8. Verify
Log-Info "Verifying Deployment..."
kubectl get pods
kubectl get svc
kubectl get ingress

# 9. AI Demo
Log-Info "Demonstrating AI Tools..."
kubectl-ai "show deployment status"

# 10. Tunnel Reminder
Log-Info "IMPORTANT: You must run 'minikube tunnel' in a separate window to access http://todo.local"
Log-Success "Phase 4 Script Completed!"

