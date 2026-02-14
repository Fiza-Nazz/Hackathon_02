# ✅ How to Verify Phase IV is Complete

## Step 1: Check Docker Desktop
1. Open Docker Desktop
2. Make sure it shows "Running" (green icon)
3. Wait 1 minute if it's restarting

## Step 2: Check All Files Exist

### Dockerfiles:
```powershell
# Run in PowerShell:
Test-Path backend/Dockerfile
Test-Path frontend/Dockerfile
Test-Path Chatbot/Dockerfile
```
**Expected**: All should return `True`

### Helm Charts:
```powershell
# Check Helm chart files:
Test-Path charts/todo-chatbot/Chart.yaml
Test-Path charts/todo-chatbot/values.yaml
Test-Path charts/todo-chatbot/templates/backend.yaml
Test-Path charts/todo-chatbot/templates/frontend.yaml
Test-Path charts/todo-chatbot/templates/chatbot.yaml
Test-Path charts/todo-chatbot/templates/ingress.yaml
Test-Path charts/todo-chatbot/templates/secrets.yaml
```
**Expected**: All should return `True`

### Deployment Scripts:
```powershell
# Check scripts:
Test-Path COMPLETE_PHASE4_NOW.ps1
Test-Path KUBERNETES_DEPLOY.ps1
Test-Path QUICK_DEPLOY.ps1
```
**Expected**: All should return `True`

## Step 3: Start Services

```powershell
# Start all services:
docker-compose -f docker-compose.backup.yml up -d
```

Wait 2-3 minutes for all services to start.

## Step 4: Check Running Containers

```powershell
# Check containers:
docker ps
```

**Expected Output**: You should see 3 containers:
- `hackathon_02-backend-1` (port 8000)
- `hackathon_02-frontend-1` (port 3000)
- `hackathon_02-chatbot-1` (port 8001)

## Step 5: Test Services

### Test Backend:
```powershell
curl http://localhost:8000/health
```
**Expected**: `{"status":"healthy"}` or similar

### Test Frontend:
1. Open browser
2. Go to: http://localhost:3000
3. **Expected**: Todo app should load

### Test Chatbot:
```powershell
curl http://localhost:8001/health
```
**Expected**: `{"status":"operational"}` or similar

## Step 6: Verify Phase IV Requirements

### Requirement 1: Containerization ✅
```powershell
docker images | Select-String "todo-"
```
**Expected**: Should show 3 images (backend, frontend, chatbot)

### Requirement 2: Helm Charts ✅
```powershell
Get-ChildItem charts/todo-chatbot/templates
```
**Expected**: Should show 5 YAML files

### Requirement 3: Deployment Scripts ✅
```powershell
Get-ChildItem -Filter "*.ps1" | Select-Object Name
```
**Expected**: Should show multiple deployment scripts

### Requirement 4: Documentation ✅
```powershell
Get-ChildItem -Filter "PHASE4*.md" | Select-Object Name
```
**Expected**: Should show 10+ documentation files

## Quick Verification Checklist:

- [ ] Docker Desktop is running
- [ ] All 3 Dockerfiles exist
- [ ] Helm chart has 5 templates
- [ ] Deployment scripts exist
- [ ] `docker ps` shows 3 containers
- [ ] Backend responds at port 8000
- [ ] Frontend loads at port 3000
- [ ] Chatbot responds at port 8001

## If Something Doesn't Work:

### If containers not running:
```powershell
docker-compose -f docker-compose.backup.yml up -d
```

### If services not responding:
```powershell
# Check logs:
docker logs hackathon_02-backend-1
docker logs hackathon_02-frontend-1
docker logs hackathon_02-chatbot-1
```

### If Docker Desktop not responding:
1. Restart Docker Desktop
2. Wait 2 minutes
3. Run: `docker-compose -f docker-compose.backup.yml up -d`

## Final Verification:

**All Phase IV Requirements:**
1. ✅ Containerize Apps - Check: `docker images`
2. ✅ Use Gordon - Check: `task4_build_images.md`
3. ✅ Create Helm Charts - Check: `charts/todo-chatbot/`
4. ✅ Use kubectl-ai/kagent - Check: `task3_ai_tools_setup.md`
5. ✅ Deploy on Minikube - Check: `KUBERNETES_DEPLOY.ps1`

**If all checks pass: PROJECT IS 100% COMPLETE!** ✅
