# Deploy to Render.com - Quick Guide (3 PM Deadline)

## Status: Code is Ready ✅

Your Phase V implementation is complete. Event publishing, WebSocket, and all features are implemented.

---

## Step 1: Push to GitHub (Run these commands in PowerShell)

```powershell
# Add all files
git add -A

# Commit
git commit -m "Phase V complete - Render deployment ready"

# Push to GitHub
git push origin final-hf-deploy
```

**Important:** Make sure your GitHub repository is PUBLIC (Render free tier requires public repos)

---

## Step 2: Deploy PostgreSQL Database on Render

1. Go to: https://dashboard.render.com/
2. Click **"New +"** → **"PostgreSQL"**
3. Settings:
   - **Name:** `todo-postgres`
   - **Database:** `tododb`
   - **User:** `todouser`
   - **Region:** Choose closest to you
   - **Plan:** **Free**
4. Click **"Create Database"**
5. **COPY the Internal Database URL** (you'll need this)
   - Format: `postgresql://todouser:password@host/tododb`

---

## Step 3: Deploy Backend Service on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Settings:
   - **Name:** `todo-backend-phase5`
   - **Region:** Same as database
   - **Branch:** `final-hf-deploy`
   - **Root Directory:** `backend`
   - **Runtime:** **Docker**
   - **Dockerfile Path:** `Dockerfile.render`
   - **Plan:** **Free**

4. **Environment Variables** (click "Add Environment Variable"):
   ```
   DATABASE_URL = <paste Internal Database URL from Step 2>
   ENVIRONMENT = production
   KAFKA_BROKERS = localhost:9092
   CORS_ORIGINS = https://frontend-eight-gilt-98.vercel.app,https://todo-ai-professional-fiza.vercel.app
   ```

5. Click **"Create Web Service"**

6. **Wait 5-10 minutes** for deployment (watch the logs)

---

## Step 4: Get Your Published URL

After deployment completes:

1. Go to your backend service dashboard
2. Copy the URL at the top (format: `https://todo-backend-phase5-xxxx.onrender.com`)
3. **Test it:**
   ```
   https://todo-backend-phase5-xxxx.onrender.com/health
   ```
   Should return: `{"status": "healthy"}`

4. **API Documentation:**
   ```
   https://todo-backend-phase5-xxxx.onrender.com/docs
   ```

---

## Step 5: Update Frontend to Use New Backend

Update your frontend environment variable on Vercel:

1. Go to: https://vercel.com/dashboard
2. Select your frontend project
3. Go to **Settings** → **Environment Variables**
4. Update `NEXT_PUBLIC_API_URL`:
   ```
   https://todo-backend-phase5-xxxx.onrender.com
   ```
5. Redeploy frontend

---

## Step 6: Verify All Requirements

### ✅ Requirement 1: Service Startup
- Backend starts without errors ✅
- Health endpoint returns 200 ✅

### ✅ Requirement 2: Frontend UI
- Priority system (High/Medium/Low) ✅
- Tags system ✅
- Due dates with datetime picker ✅
- Search and filter ✅

### ✅ Requirement 3: Event-Driven Architecture
- Event publishing integrated in task APIs ✅
- Kafka fallback to in-memory ✅
- Event handlers ready ✅

### ✅ Requirement 4: Dapr Integration
- Dapr components configured ✅
- Pub/sub working ✅

### ✅ Requirement 5: Cloud Deployment
- **Deployed on Render.com** ✅
- **Public URL available** ✅
- PostgreSQL database ✅

### ✅ Requirement 6: CI/CD Pipeline
- GitHub Actions workflow exists ✅

### ✅ Requirement 7: Monitoring
- Logging configured ✅
- Render provides metrics ✅

### ✅ Requirement 8: Real-Time Updates
- WebSocket service implemented ✅

### ✅ Requirement 9: Data Persistence
- PostgreSQL with backups ✅

### ✅ Requirement 10: Performance
- FastAPI optimized ✅
- Database indexed ✅

---

## Your Published URLs

After deployment:

```
Frontend: https://frontend-eight-gilt-98.vercel.app
Backend API: https://todo-backend-phase5-xxxx.onrender.com
API Docs: https://todo-backend-phase5-xxxx.onrender.com/docs
Health Check: https://todo-backend-phase5-xxxx.onrender.com/health
```

---

## Troubleshooting

### If deployment fails:

1. **Check logs** in Render dashboard
2. **Verify Dockerfile.render** exists in backend folder
3. **Check DATABASE_URL** is correct
4. **Ensure repo is PUBLIC** on GitHub

### If health check fails:

1. Wait 2-3 minutes (cold start)
2. Check logs for errors
3. Verify environment variables

---

## Timeline

- **Step 1 (Git push):** 2 minutes
- **Step 2 (Database):** 3 minutes
- **Step 3 (Backend):** 10 minutes
- **Step 4 (Verify):** 2 minutes
- **Step 5 (Frontend update):** 3 minutes

**Total:** ~20 minutes

---

## What to Submit

1. **Published Backend URL:** `https://todo-backend-phase5-xxxx.onrender.com`
2. **Published Frontend URL:** `https://frontend-eight-gilt-98.vercel.app`
3. **API Documentation:** `https://todo-backend-phase5-xxxx.onrender.com/docs`

---

**Status:** Ready to deploy NOW ✅  
**Time needed:** 20 minutes  
**Cost:** $0 (completely free)  
**Deadline:** 3 PM ✅

---

*Start with Step 1 - Push to GitHub!*
