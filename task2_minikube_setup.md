# Task 2: Install and Configure Minikube on E: Drive

## Goal
Set up Minikube with all data on E: drive to save C: drive space.

## Prerequisites
- Docker Desktop running (✅ Already done)
- Minikube installed (or we'll install it now)

## Step 1: Set Minikube Home to E: Drive

```powershell
# Create Minikube directory on E: drive
New-Item -ItemType Directory -Path "E:\minikube" -Force
New-Item -ItemType Directory -Path "E:\minikube\.minikube" -Force

# Set environment variable for current session
$env:MINIKUBE_HOME = "E:\minikube"

# Set environment variable permanently (User level)
[Environment]::SetEnvironmentVariable("MINIKUBE_HOME", "E:\minikube", "User")

# Verify
Write-Host "MINIKUBE_HOME set to: $env:MINIKUBE_HOME"
```

## Step 2: Check if Minikube is Installed

```powershell
# Check Minikube version
minikube version

# If not installed, install via Chocolatey or manual download
# Option A: Chocolatey (if installed)
# choco install minikube

# Option B: Direct download (run as Administrator)
# Download from: https://github.com/kubernetes/minikube/releases/latest
```

## Step 3: Start Minikube with Docker Driver

```powershell
# Delete any existing cluster first
minikube delete

# Start Minikube with optimized settings for your system
# Using E: drive via MINIKUBE_HOME
minikube start `
  --driver=docker `
  --cpus=2 `
  --memory=3072 `
  --disk-size=10g `
  --container-runtime=docker `
  --force

# This will:
# - Use Docker driver (leverages your Docker Desktop)
# - Allocate 2 CPUs
# - Allocate 3 GB RAM
# - Create 10 GB disk (stored in E:\minikube\.minikube)
```

## Step 4: Verify Minikube Status

```powershell
# Check status
minikube status

# Check cluster info
kubectl cluster-info

# Check nodes
kubectl get nodes
```

## Step 5: Enable Ingress Addon

```powershell
# Enable Ingress controller for local access
minikube addons enable ingress

# Verify addon
minikube addons list | Select-String "ingress"
```

## Step 6: Configure Docker to Use Minikube's Docker Daemon

**IMPORTANT**: This allows us to build images directly in Minikube!

```powershell
# Set Docker environment to Minikube's daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Verify - you should see Minikube's Docker now
docker ps

# To make this permanent across sessions, add to PowerShell profile
# Add this line to your PowerShell profile:
# & minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

## Verification

```powershell
# 1. Check Minikube is using E: drive
Get-ChildItem E:\minikube\.minikube

# 2. Check Docker is pointing to Minikube
docker info | Select-String "Name"
# Should show "minikube" somewhere

# 3. Check available storage
minikube ssh "df -h"
```

## Troubleshooting

### Issue: Minikube fails to start
```powershell
# Check Docker is running
docker ps

# Try with verbose logging
minikube start --driver=docker -v=7

# Check logs
minikube logs
```

### Issue: WSL2 VM memory issues
```powershell
# Create/edit .wslconfig in your user directory
# C:\Users\<username>\.wslconfig
# Add:
# [wsl2]
# memory=4GB
# processors=2
```

## Next Steps
Once Minikube is running successfully:
1. Install kubectl-ai and kagent (Task 3)
2. Build Docker images (Task 4)
3. Deploy with Helm (Task 5)
