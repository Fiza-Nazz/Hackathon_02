# Task 4: Build Docker Images Using Gordon AI

## Goal
Build optimized Docker images for Frontend, Backend, and Chatbot using Docker AI (Gordon) or standard Docker CLI.

## Prerequisites
- [x] Minikube running
- [x] Minikube Docker environment configured
- [x] Docker Desktop with Gordon enabled

## Important: Use Minikube's Docker Daemon

To avoid storing images twice and save disk space, build directly in Minikube:

```powershell
# Point Docker CLI to Minikube's Docker daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Verify you're using Minikube's Docker
docker info | Select-String "Name"
# Should show "minikube" somewhere
```

---

## Method 1: Using Gordon (Docker AI) 🤖

### Backend Image
```powershell
cd E:\Hackathon_02\backend

# Ask Gordon to build the image
docker ai "Build a production-ready Python FastAPI backend image with the tag todo-backend:latest using the existing Dockerfile. Optimize for size and security."

# OR simple command
docker ai "build backend image as todo-backend:latest"
```

### Frontend Image
```powershell
cd E:\Hackathon_02\frontend

# Ask Gordon to build
docker ai "Build a Next.js frontend image tagged as todo-frontend:latest from the Dockerfile. Use multi-stage build for optimization."

# OR simple command
docker ai "build frontend image as todo-frontend:latest"
```

### Chatbot Image
```powershell
cd E:\Hackathon_02\Chatbot

# Ask Gordon to build
docker ai "Build a Python chatbot image tagged as todo-chatbot-foundation:latest. Ensure all dependencies are installed correctly."

# OR simple command
docker ai "build chatbot image as todo-chatbot-foundation:latest"
```

---

## Method 2: Standard Docker CLI (If Gordon is unavailable)

### Backend Image
```powershell
cd E:\Hackathon_02\backend
docker build -t todo-backend:latest .
```

### Frontend Image
```powershell
cd E:\Hackathon_02\frontend
docker build -t todo-frontend:latest .
```

### Chatbot Image
```powershell
cd E:\Hackathon_02\Chatbot
docker build -t todo-chatbot-foundation:latest .
```

---

## Method 3: Using Claude Code to Generate Commands (Agentic Dev)

Ask Claude Code:
```
"Generate optimized Docker build commands for my todo-chatbot project with three components: backend (FastAPI), frontend (Next.js), and chatbot (Python)."
```

---

## Verification

### Check Built Images
```powershell
# List all todo-related images
docker images | Select-String "todo-"

# Expected output:
# todo-backend:latest
# todo-frontend:latest
# todo-chatbot-foundation:latest
```

### Inspect Images
```powershell
# Check image size
docker images todo-backend:latest
docker images todo-frontend:latest
docker images todo-chatbot-foundation:latest

# Detailed inspection
docker inspect todo-backend:latest
docker history todo-backend:latest
```

### Test Images Locally (Optional)
```powershell
# Test backend image
docker run -p 8000:8000 todo-backend:latest
# Visit: http://localhost:8000/docs

# Test frontend image
docker run -p 3000:3000 todo-frontend:latest
# Visit: http://localhost:3000

# Stop containers
docker ps -a
docker stop <container_id>
docker rm <container_id>
```

---

## Using Gordon for Advanced Operations 🤖

### Analyze Image Quality
```powershell
docker ai "Analyze the todo-backend:latest image for security vulnerabilities and optimization opportunities"
```

### Get Build Recommendations
```powershell
docker ai "Review my Dockerfile in E:\Hackathon_02\backend and suggest improvements"
```

### Optimize Image Size
```powershell
docker ai "How can I reduce the size of my todo-frontend:latest image?"
```

### Debug Build Failures
```powershell
# If build fails
docker ai "Why did the build fail for todo-backend? Here's the error: [paste error]"
```

---

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"
```powershell
# Ensure Docker Desktop is running
docker ps

# Reconnect to Minikube's Docker
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

### Issue: Build fails with "COPY failed"
```powershell
# Check if files exist
cd E:\Hackathon_02\backend
ls

# Check .dockerignore
cat .dockerignore

# Ensure you're in the correct directory
pwd
```

### Issue: "No space left on device"
```powershell
# Clean up old images and containers
docker system prune -a --volumes

# Check disk usage
docker system df
minikube ssh "df -h"
```

### Issue: Frontend build hangs at "npm install"
```powershell
# Try with more memory
minikube delete
minikube start --driver=docker --cpus=2 --memory=4096 --disk-size=15g

# Or build with no cache
docker build --no-cache -t todo-frontend:latest .
```

### Issue: Gordon (Docker AI) not responding
```powershell
# Verify Gordon is enabled
# Docker Desktop → Settings → Beta features → Toggle "Docker AI"

# Restart Docker Desktop

# If still not working, use standard Docker CLI (Method 2)
```

---

## Build Optimization Tips

### 1. Use Build Cache
```powershell
# Docker automatically uses cache
# To force rebuild:
docker build --no-cache -t todo-backend:latest .
```

### 2. Multi-Stage Builds (Already in Dockerfiles)
- ✅ Backend: Uses multi-stage (builder + runner)
- ✅ Frontend: Uses multi-stage (builder + runner)
- ✅ Chatbot: Uses multi-stage (builder + runner)

### 3. BuildKit (Faster Builds)
```powershell
# Enable BuildKit for faster builds
$env:DOCKER_BUILDKIT = 1
[Environment]::SetEnvironmentVariable("DOCKER_BUILDKIT", "1", "User")

# Build with BuildKit
docker build -t todo-backend:latest .
```

### 4. Build All Images in Parallel
```powershell
# Open 3 PowerShell windows and build simultaneously
# Window 1:
cd E:\Hackathon_02\backend; docker build -t todo-backend:latest .

# Window 2:
cd E:\Hackathon_02\frontend; docker build -t todo-frontend:latest .

# Window 3:
cd E:\Hackathon_02\Chatbot; docker build -t todo-chatbot-foundation:latest .
```

---

## Image Tagging Strategy

### Current Tags
- `todo-backend:latest`
- `todo-frontend:latest`
- `todo-chatbot-foundation:latest`

### Additional Tags (Optional)
```powershell
# Tag with version
docker tag todo-backend:latest todo-backend:v1.0.0

# Tag with commit hash
$commit = (git rev-parse --short HEAD)
docker tag todo-backend:latest todo-backend:$commit
```

---

## Next Steps

Once all images are built:
1. Verify images exist in Minikube's Docker
2. Update Helm values.yaml if needed
3. Deploy to Minikube (Task 5)
4. Use kubectl-ai to monitor deployment

---

## Success Criteria ✅

- [x] All 3 images built successfully
- [x] Images are in Minikube's Docker daemon (not local Docker)
- [x] Image sizes are reasonable (< 500MB each)
- [x] Images can run without errors
- [x] Used Gordon (Docker AI) for at least one operation

---

**Ready to deploy! On to Task 5! 🚀**
