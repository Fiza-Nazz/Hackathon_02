# 🚀 DEPLOY PHASE V NOW - GET PUBLISHED URL IN 15 MINUTES

## Step 1: Deploy Backend to Railway (5 minutes)

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Choose backend folder** as root directory
6. **Set Environment Variables**:
   ```
   DATABASE_URL=your_neon_database_url
   GROQ_API_KEY=your_groq_api_key
   BETTER_AUTH_SECRET=your_secret_key
   PORT=8000
   ```
7. **Deploy** - Railway will auto-detect Dockerfile
8. **Copy the generated URL** (e.g., https://backend-production-xxxx.up.railway.app)

## Step 2: Deploy Chatbot to Railway (5 minutes)

1. **New Project** in Railway
2. **Deploy from GitHub repo**
3. **Choose Chatbot folder** as root directory  
4. **Set Environment Variables**:
   ```
   DATABASE_URL=your_neon_database_url
   GROQ_API_KEY=your_groq_api_key
   BETTER_AUTH_SECRET=your_secret_key
   PORT=8001
   ```
5. **Deploy**
6. **Copy the generated URL** (e.g., https://chatbot-production-xxxx.up.railway.app)

## Step 3: Update Frontend Environment (2 minutes)

Update `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=https://your-chatbot-url.up.railway.app
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.up.railway.app
NEXT_PUBLIC_CHATBOT_URL=https://your-chatbot-url.up.railway.app
```

## Step 4: Deploy Frontend to Vercel (3 minutes)

1. **Go to Vercel**: https://vercel.com
2. **Import Project** from GitHub
3. **Select frontend folder**
4. **Deploy** - Vercel will auto-detect Next.js
5. **Copy the generated URL** (e.g., https://todo-chatbot-frontend.vercel.app)

## 🎯 YOUR PUBLISHED URLS

After deployment, you'll have:

- **Frontend (Main App)**: https://your-app.vercel.app
- **Backend API**: https://backend-production-xxxx.up.railway.app
- **Chatbot API**: https://chatbot-production-xxxx.up.railway.app

## ✅ Test Your Deployment

1. **Open Frontend URL**
2. **Create an account**
3. **Add some tasks**
4. **Test chatbot functionality**
5. **Verify all features work**

## 🎬 Record Demo Video

1. **Screen record 90 seconds**
2. **Show task creation, chatbot, priorities, tags**
3. **Demonstrate Phase V features**
4. **Submit with published URL**

## 🏆 PHASE V COMPLETE!

**Published URL**: https://your-app.vercel.app
**Status**: ✅ DEPLOYED AND LIVE
**Time Taken**: ~15 minutes

---

**Alternative: If Railway doesn't work, use Render.com with same steps**