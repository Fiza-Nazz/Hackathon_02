# Docker Desktop E: Drive Configuration Guide

## Problem
C: drive is almost full (only 3.68 GB free), causing Docker Desktop to hang.

## Solution
Move Docker Desktop's WSL2 disk image to E: drive.

## Steps

### Option 1: Docker Desktop Settings (Easiest)
1. Open Docker Desktop
2. Go to **Settings** → **Resources** → **Advanced**
3. Look for **"Disk image location"** or **"WSL2 disk location"**
4. Click **"Browse"** and select `E:\Docker`
5. Click **"Apply & Restart"**

### Option 2: Manual WSL2 Export/Import (If Option 1 not available)

```powershell
# 1. Stop Docker Desktop
# Use System Tray → Right-click Docker → Quit Docker Desktop

# 2. Export WSL2 distributions
wsl --list -v
wsl --export docker-desktop E:\Docker\docker-desktop.tar
wsl --export docker-desktop-data E:\Docker\docker-desktop-data.tar

# 3. Unregister old distributions
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data

# 4. Import to E: drive
wsl --import docker-desktop E:\Docker\desktop E:\Docker\docker-desktop.tar --version 2
wsl --import docker-desktop-data E:\Docker\desktop-data E:\Docker\docker-desktop-data.tar --version 2

# 5. Start Docker Desktop again
```

### Option 3: Symbolic Link (Quick Fix)
```powershell
# Stop Docker Desktop first

# Create E:\Docker directory
New-Item -ItemType Directory -Path E:\Docker -Force

# Move WSL2 data (run as Administrator)
# The actual data is in: C:\Users\<username>\AppData\Local\Docker\wsl
Move-Item -Path "$env:LOCALAPPDATA\Docker\wsl" -Destination "E:\Docker\wsl"

# Create symbolic link
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\Docker\wsl" -Target "E:\Docker\wsl"

# Start Docker Desktop
```

## Verification
After configuration:
```powershell
# Check disk usage
docker system df

# Check if Docker can build images
docker build --help
```

## Next Steps
Once Docker is configured on E: drive, proceed to Minikube setup.
































