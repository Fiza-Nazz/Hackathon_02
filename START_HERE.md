# 🚀 START HERE - Quick Test Guide

## Step 1: Start Docker Desktop (1 minute)

1. Open **Docker Desktop**
2. Wait until it shows **"Running"** (green icon)
3. If it's already running, you're good!

---

## Step 2: Start All Services (2 minutes)

Open **PowerShell** in project folder and run:

```powershell
docker-compose -f docker-compose.backup.yml up -d
```

Wait 2-3 minutes for services to start.

---

## Step 3: Check Services are Running

```powershell
docker ps
```

**You should see 3 containers:**
- `hackathon_02-backend-1` 
- `hackathon_02-frontend-1`
- `hackathon_02-chatbot-1`

---

## Step 4: Test in Browser

### Test Frontend (Main App):
1. Open browser
2. Go to: **http://localhost:3000**
3. You should see the Todo app!

### Test Backend API:
- Open: **http://localhost:8000/docs**
- You should see FastAPI documentation

### Test Chatbot:
- Open: **http://localhost:8001/health**
- You should see: `{"status":"operational"}`

---

## Step 5: Test Chatbot in App

1. Go to **http://localhost:3000**
2. Click the **chat icon** (bottom right corner)
3. Type: **"hi"**
4. Chatbot should respond!

---

## Step 6: Verify Phase IV Files

### Check Dockerfiles:
```powershell
dir backend/Dockerfile
dir frontend/Dockerfile
dir Chatbot/Dockerfile
```
All should exist ✅

### Check Helm Charts:
```powershell
dir charts/todo-chatbot/templates
```
Should show 5 YAML files ✅

### Check Deployment Scripts:
```powershell
dir *.ps1
```
Should show multiple .ps1 files ✅

---

## Quick Troubleshooting

### If services not starting:
```powershell
# Stop everything
docker-compose -f docker-compose.backup.yml down

# Start again
docker-compose -f docker-compose.backup.yml up -d
```

### If chatbot not responding:
```powershell
# Check logs
docker logs hackathon_02-chatbot-1
```

### If Docker Desktop not working:
1. Restart Docker Desktop
2. Wait 2 minutes
3. Run Step 2 again

---

## ✅ Success Checklist

- [ ] Docker Desktop is running
- [ ] `docker ps` shows 3 containers
- [ ] http://localhost:3000 loads (Frontend)
- [ ] http://localhost:8000/docs loads (Backend)
- [ ] http://localhost:8001/health responds (Chatbot)
- [ ] Chat widget works on frontend
- [ ] All Dockerfiles exist
- [ ] Helm charts exist (5 templates)
- [ ] Deployment scripts exist

**If all checked: Phase IV is 100% working!** ✅

---

## For Kubernetes/Minikube Testing (Optional)

If you want to test Kubernetes deployment:

```powershell
.\KUBERNETES_DEPLOY.ps1
```

This will:
1. Start Minikube
2. Build images
3. Deploy with Helm
4. Setup Ingress

**Note**: This takes 5-10 minutes.

---

## Need Help?

Check these files:
- `HOW_TO_VERIFY.md` - Detailed verification
- `PHASE4_REQUIREMENTS_FINAL_CHECK.md` - Requirements checklist
- `FINAL_STATUS_SUMMARY.md` - Complete status

---

## 🎯 Quick Summary

**To test everything:**
1. Start Docker Desktop
2. Run: `docker-compose -f docker-compose.backup.yml up -d`
3. Open: http://localhost:3000
4. Test chat widget

**That's it!** 🚀
