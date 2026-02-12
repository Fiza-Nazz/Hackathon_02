# Quick Phase V Deployment Guide

## 🚀 FASTEST PATH TO PUBLISHED URL (15 minutes)

Since Oracle Cloud setup takes time, here's the quickest way to get your Phase V app live:

### Option 1: Vercel + Railway (Recommended)

#### Frontend Deployment (Vercel)
```bash
# Already deployed at: https://frontend-eight-gilt-98.vercel.app
# Update environment variables:
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_CHATBOT_URL=https://your-chatbot.railway.app
```

#### Backend Deployment (Railway)
1. Go to https://railway.app
2. Connect GitHub repo
3. Deploy backend folder
4. Set environment variables:
   - DATABASE_URL (your Neon DB URL)
   - GROQ_API_KEY
   - BETTER_AUTH_SECRET

#### Chatbot Deployment (Railway)
1. Deploy Chatbot folder separately
2. Set same environment variables

### Option 2: Render.com (Free Alternative)

#### Backend on Render
```yaml
# render.yaml
services:
  - type: web
    name: todo-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: todo-db
          property: connectionString
```

### Option 3: Docker + DigitalOcean App Platform

#### Dockerfile for Backend
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🎯 IMMEDIATE ACTION PLAN

1. **Deploy Backend to Railway** (5 min)
2. **Update Frontend env vars** (2 min)  
3. **Deploy Chatbot to Railway** (5 min)
4. **Test published URLs** (3 min)

## 📋 PUBLISHED URLS FORMAT

- **Frontend**: https://todo-chatbot-frontend.vercel.app
- **Backend API**: https://todo-backend-production.up.railway.app
- **Chatbot**: https://todo-chatbot-production.up.railway.app

## ✅ SUCCESS CRITERIA

Phase V complete when:
- ✅ All services running locally
- ✅ Published URLs accessible
- ✅ Frontend connects to deployed backend
- ✅ Chatbot functionality works
- ✅ Demo video recorded

**TOTAL TIME: 15-20 minutes for published URL!**