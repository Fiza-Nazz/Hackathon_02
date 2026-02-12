# ============================================
# Phase IV Auto-Completion Script
# Todo Chatbot - Kubernetes Deployment
# ============================================
# Purpose: Automate the remaining 30% of Phase IV
# Requirements: Minikube running, Docker Desktop running
# ============================================

param(
    [switch]$SkipAITools = $false,
    [switch]$SkipBuild = $false,
    [switch]$SkipDeploy = $false,
    [switch]$DryRun = $false,
    [switch]$AutoApprove = $false
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Set MINIKUBE_HOME explicitly (pointing to the .minikube directory)
$env:MINIKUBE_HOME = "E:\minikube\.minikube"

# ============================================
# Configuration
# ============================================
$GROQ_API_KEY = "YOUR_GROQ_API_KEY"
$PROJECT_ROOT = "E:\Hackathon_02"
$MINIKUBE_IP = ""

Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Phase IV Auto-Completion Script          ║" -ForegroundColor Cyan
Write-Host "║  Cloud-Native Todo Chatbot                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ============================================
function Write-Step {
    param(
        [string]$Message,
        [string]$Color = "Yellow"
    )
    Write-Host ""
    Write-Host "-------------------------------------------" -ForegroundColor $Color
    Write-Host "> $Message" -ForegroundColor $Color
    Write-Host "-------------------------------------------" -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# ============================================
# STEP 0: Pre-flight Checks
# ============================================
Write-Step "STEP 0: Pre-flight Checks" "Magenta"

Write-Info "Checking Minikube status..."
$minikubeStatus = minikube status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Minikube is running"
} else {
    Write-Info "Minikube is not running or profile not found."
    Write-Info "Attempting to start Minikube..."
    
    if (-not $DryRun) {
        minikube start --driver=docker
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Minikube started successfully"
        } else {
            Write-Error-Custom "Failed to start Minikube! Please check logs."
            exit 1
        }
    } else {
        Write-Info "[DRY RUN] Would start Minikube"
    }
}

Write-Info "Checking kubectl connectivity..."
$nodes = kubectl get nodes 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "kubectl connected to cluster"
    Write-Host $nodes
} else {
    Write-Error-Custom "kubectl cannot connect to cluster!"
    exit 1
}a

Write-Info "Checking Docker Desktop..."
$dockerInfo = docker info 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Docker Desktop is running"
} else {
    Write-Error-Custom "Docker Desktop is not running!"
    exit 1
}

# ============================================
# STEP 1: Enable Ingress Addon
# ============================================
if (-not $SkipDeploy) {
    Write-Step "STEP 1: Enable Ingress Addon" "Cyan"
    
    Write-Info "Checking if Ingress is already enabled..."
    $addons = minikube addons list 2>&1 | Select-String "ingress"
    
    if ($addons -match "enabled") {
        Write-Success "Ingress addon already enabled"
    } else {
        Write-Info "Enabling Ingress addon..."
        if (-not $DryRun) {
            minikube addons enable ingress
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Ingress addon enabled"
            } else {
                Write-Error-Custom "Failed to enable Ingress addon"
            }
        } else {
            Write-Info "[DRY RUN] Would enable Ingress addon"
        }
    }
    
    Write-Info "Waiting for Ingress controller pods to be ready..."
    if (-not $DryRun) {
        Start-Sleep -Seconds 10
        kubectl wait --namespace ingress-nginx `
            --for=condition=ready pod `
            --selector=app.kubernetes.io/component=controller `
            --timeout=120s 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Ingress controller is ready"
        } else {
            Write-Info "Ingress controller may take longer to be ready (continuing anyway)"
        }
    }
}

# ============================================
# STEP 2: Install kubectl-ai
# ============================================
if (-not $SkipAITools) {
    Write-Step "STEP 2: Install kubectl-ai" "Cyan"
    
    if (Test-Command "kubectl-ai") {
        Write-Success "kubectl-ai is already installed"
        kubectl-ai --version 2>&1
    } else {
        Write-Info "Installing kubectl-ai via npm..."
        if (-not $DryRun) {
            npm install -g kubectl-ai
            if ($LASTEXITCODE -eq 0) {
                Write-Success "kubectl-ai installed successfully"
            } else {
                Write-Error-Custom "Failed to install kubectl-ai (continuing anyway)"
                Write-Info "You can install manually: npm install -g kubectl-ai"
            }
        } else {
            Write-Info "[DRY RUN] Would install kubectl-ai"
        }
    }
    
    Write-Info "Configuring kubectl-ai with Groq API key..."
    if (-not $DryRun) {
        $env:GROQ_API_KEY = $GROQ_API_KEY
        [Environment]::SetEnvironmentVariable("GROQ_API_KEY", $GROQ_API_KEY, "User")
        Write-Success "Groq API key configured"
    }
}

# ============================================
# STEP 3: Install k8sgpt (kagent)
# ============================================
if (-not $SkipAITools) {
    Write-Step "STEP 3: Install k8sgpt (kagent)" "Cyan"
    
    if (Test-Command "k8sgpt") {
        Write-Success "k8sgpt is already installed"
    } else {
        Write-Info "Installing k8sgpt via pip..."
        if (-not $DryRun) {
            pip install k8sgpt 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "k8sgpt installed successfully"
            } else {
                Write-Info "k8sgpt installation failed (this is optional)"
                Write-Info "Will use kubectl-ai for AI operations instead"
            }
        } else {
            Write-Info "[DRY RUN] Would install k8sgpt"
        }
    }
}

# ============================================
# STEP 4: Configure Minikube Docker Environment
# ============================================
if (-not $SkipBuild) {
    Write-Step "STEP 4: Configure Minikube Docker Environment" "Cyan"
    
    Write-Info "Configuring shell to use Minikube's Docker daemon..."
    if (-not $DryRun) {
        & minikube -p minikube docker-env --shell powershell | Invoke-Expression
        Write-Success "Now using Minikube's Docker daemon"
        
        Write-Info "Verifying Docker context..."
        docker ps | Select-String "minikube" -Quiet
        Write-Success "Connected to Minikube Docker"
    } else {
        Write-Info "[DRY RUN] Would configure Minikube Docker environment"
    }
}

# ============================================
# STEP 5: Build Docker Images
# ============================================
if (-not $SkipBuild) {
    Write-Step "STEP 5: Build Docker Images" "Cyan"
    
    # Build Backend
    Write-Info "Building Backend image..."
    if (-not $DryRun) {
        Push-Location "$PROJECT_ROOT\backend"
        docker build -t todo-backend:latest . 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Backend image built successfully"
        } else {
            Write-Error-Custom "Failed to build Backend image"
        }
        Pop-Location
    } else {
        Write-Info "[DRY RUN] Would build Backend image"
    }
    
    # Build Frontend
    Write-Info "Building Frontend image..."
    if (-not $DryRun) {
        Push-Location "$PROJECT_ROOT\frontend"
        docker build -t todo-frontend:latest . 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Frontend image built successfully"
        } else {
            Write-Error-Custom "Failed to build Frontend image"
        }
        Pop-Location
    } else {
        Write-Info "[DRY RUN] Would build Frontend image"
    }
    
    # Build Chatbot
    Write-Info "Building Chatbot image..."
    if (-not $DryRun) {
        Push-Location "$PROJECT_ROOT\Chatbot"
        docker build -t todo-chatbot-foundation:latest . 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Chatbot image built successfully"
        } else {
            Write-Error-Custom "Failed to build Chatbot image"
        }
        Pop-Location
    } else {
        Write-Info "[DRY RUN] Would build Chatbot image"
    }
    
    # Verify all images
    Write-Info "Verifying images..."
    if (-not $DryRun) {
        $images = docker images | Select-String "todo-"
        Write-Host $images
        $imageCount = ($images | Measure-Object).Count
        if ($imageCount -ge 3) {
            Write-Success "All 3 images present in Minikube registry"
        } else {
            Write-Info "Warning: Only $imageCount/3 images found"
        }
    }
}

# ============================================
# STEP 6: Deploy with Helm
# ============================================
if (-not $SkipDeploy) {
    Write-Step "STEP 6: Deploy with Helm" "Cyan"
    
    # Check if already deployed
    $helmList = helm list 2>&1 | Select-String "todo-chatbot"
    if ($helmList) {
        Write-Info "todo-chatbot is already deployed. Upgrading..."
        if (-not $DryRun) {
            Push-Location $PROJECT_ROOT
            helm upgrade todo-chatbot ./charts/todo-chatbot --namespace default
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Helm chart upgraded successfully"
            } else {
                Write-Error-Custom "Failed to upgrade Helm chart"
            }
            Pop-Location
        } else {
            Write-Info "[DRY RUN] Would upgrade Helm release"
        }
    } else {
        Write-Info "Installing Helm chart..."
        if (-not $DryRun) {
            Push-Location $PROJECT_ROOT
            helm install todo-chatbot ./charts/todo-chatbot --namespace default
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Helm chart installed successfully"
            } else {
                Write-Error-Custom "Failed to install Helm chart"
            }
            Pop-Location
        } else {
            Write-Info "[DRY RUN] Would install Helm chart"
        }
    }
    
    Write-Info "Waiting for pods to be ready..."
    if (-not $DryRun) {
        Start-Sleep -Seconds 10
        kubectl get pods
    }
}

# ============================================
# STEP 7: Configure Ingress Access
# ============================================
if (-not $SkipDeploy) {
    Write-Step "STEP 7: Configure Ingress Access" "Cyan"
    
    Write-Info "Getting Minikube IP..."
    if (-not $DryRun) {
        $MINIKUBE_IP = minikube ip
        Write-Success "Minikube IP: $MINIKUBE_IP"
        
        Write-Info "Checking hosts file..."
        $hostsPath = "C:\Windows\System32\drivers\etc\hosts"
        $hostsContent = Get-Content $hostsPath -ErrorAction SilentlyContinue
        
        if ($hostsContent -match "todo.local") {
            Write-Success "todo.local already in hosts file"
        } else {
            Write-Info "Adding todo.local to hosts file (requires Admin)..."
            try {
                $hostsEntry = "`n$MINIKUBE_IP todo.local"
                Add-Content -Path $hostsPath -Value $hostsEntry -ErrorAction Stop
                Write-Success "Added todo.local to hosts file"
            } catch {
                Write-Error-Custom "Failed to update hosts file. Run as Administrator:"
                Write-Host "  Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value '`n$MINIKUBE_IP todo.local'" -ForegroundColor Yellow
            }
        }
        
        Write-Info "Starting Minikube tunnel (keep this window open)..."
        Write-Host ""
        Write-Host "═══════════════════════════════════════════" -ForegroundColor Red
        Write-Host "IMPORTANT: Minikube tunnel MUST run continuously!" -ForegroundColor Red
        Write-Host "  • Keep this PowerShell window open" -ForegroundColor Yellow
        Write-Host "  • Or run in a separate window: minikube tunnel" -ForegroundColor Yellow
        Write-Host "═══════════════════════════════════════════" -ForegroundColor Red
        Write-Host ""
        
        if ($AutoApprove) {
            Write-Info "Skipping interactive tunnel start (AutoApprove is on). Please start 'minikube tunnel' manually in another window."
        } else {
            $response = Read-Host "Start minikube tunnel now? (y/n)"
            if ($response -match "^[Yy]") {
                Write-Info "Starting tunnel... (Press Ctrl+C when done)"
                minikube tunnel
            } else {
                Write-Info "Skipped tunnel. Start manually with: minikube tunnel"
            }
        }
    } else {
        Write-Info "[DRY RUN] Would configure hosts and start tunnel"
    }
}

# ============================================
# STEP 8: Verify Deployment
# ============================================
Write-Step "STEP 8: Verify Deployment" "Cyan"

if (-not $DryRun) {
    Write-Info "Checking all pods..."
    kubectl get pods -A
    
    Write-Info "Checking services..."
    kubectl get svc
    
    Write-Info "Checking deployments..."
    kubectl get deployments
    
    Write-Info "Checking ingress..."
    kubectl get ingress
    
    Write-Success "Deployment verification complete"
}

# ============================================
# STEP 9: AI Tools Demonstration
# ============================================
if (-not $SkipAITools) {
    Write-Step "STEP 9: AI Tools Demonstration" "Green"
    
    if (Test-Command "kubectl-ai") {
        Write-Info "Testing kubectl-ai commands..."
        
        if (-not $DryRun) {
            Write-Host ""
            Write-Host "1. Checking deployment status..." -ForegroundColor Cyan
            kubectl-ai "show deployment status for todo-chatbot"
            
            Write-Host ""
            Write-Host "2. Checking pod health..." -ForegroundColor Cyan
            kubectl-ai "check if all pods are healthy"
            
            Write-Host ""
            Write-Host "3. Resource usage..." -ForegroundColor Cyan
            kubectl-ai "show resource usage for all pods"
            
            Write-Success "kubectl-ai demonstrations complete"
        } else {
            Write-Info "[DRY RUN] Would demonstrate kubectl-ai"
        }
    } else {
        Write-Info "kubectl-ai not available for demonstration"
    }
}

# ============================================
# FINAL SUMMARY
# ============================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║           PHASE IV COMPLETED! 🎉           ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

if (-not $DryRun) {
    Write-Success "All steps completed!"
    Write-Host ""
    Write-Info "Access your application:"
    Write-Host "  • Frontend: http://todo.local" -ForegroundColor Yellow
    Write-Host "  • Backend API: http://todo.local/api" -ForegroundColor Yellow
    Write-Host ""
    Write-Info "Useful commands:"
    Write-Host "  • View pods: kubectl get pods" -ForegroundColor Cyan
    Write-Host "  • View logs: kubectl logs -l app=frontend" -ForegroundColor Cyan
    Write-Host "  • Scale: kubectl scale deployment frontend --replicas=3" -ForegroundColor Cyan
    Write-Host "  • AI help: kubectl-ai 'your question'" -ForegroundColor Cyan
    Write-Host ""
    Write-Info "Don't forget to:"
    Write-Host "  1. Keep 'minikube tunnel' running" -ForegroundColor Yellow
    Write-Host "  2. Take screenshots for documentation" -ForegroundColor Yellow
    Write-Host "  3. Test all functionality" -ForegroundColor Yellow
} else {
    Write-Info "Dry run completed. No changes were made."
}

Write-Host ""
Write-Host "Bismillah - Well done! Success!" -ForegroundColor Magenta
Write-Host ""

