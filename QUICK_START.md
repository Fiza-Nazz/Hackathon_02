# Phase V - Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Git

### Step 1: Clone & Navigate
```bash
cd your-project-directory
```

### Step 2: Start Services
```bash
docker-compose up -d
```

Wait 10 seconds for services to start.

### Step 3: Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m src.database.init_db
```

### Step 4: Start Backend
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Verify
```bash
# In another terminal
curl http://localhost:8000/health
```

---

## 📱 Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Redpanda Console | http://localhost:8080 | Kafka UI |
| WebSocket | ws://localhost:8000/ws/tasks/{user_id} | Real-time |

---

## 🧪 Test Features

### 1. Create Task
```bash
curl -X POST http://localhost:8000/api/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "priority": "high",
    "tags": ["urgent", "work"],
    "due_date": "2024-02-15T10:00:00"
  }'
```

### 2. Get Tasks
```bash
curl http://localhost:8000/api/tasks/list
```

### 3. Search Tasks
```bash
curl "http://localhost:8000/api/tasks/search?q=test"
```

### 4. WebSocket Connection
```bash
# Using websocat or similar tool
websocat ws://localhost:8000/ws/tasks/user123
```

---

## 🐳 Docker Commands

```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart
```

---

## 🔍 Troubleshooting

### Services not starting?
```bash
# Check Docker
docker ps

# Check logs
docker-compose logs

# Restart
docker-compose restart
```

### Backend connection error?
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process if needed
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Database error?
```bash
# Check PostgreSQL
docker exec todo_postgres psql -U todouser -d tododb -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d
```

---

## 📊 Kafka Topics

Topics are automatically created:
- `task-events` - Task operations
- `reminders` - Reminder events
- `task-updates` - Real-time updates

View in Redpanda Console: http://localhost:8080

---

## 🎯 Next Steps

1. ✅ Services running locally
2. ⏳ Test all endpoints
3. ⏳ Deploy to Kubernetes
4. ⏳ Deploy to cloud
5. ⏳ Record demo

---

## 📞 Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in docker-compose.yml |
| Database connection failed | Wait 30s for PostgreSQL to start |
| Kafka not responding | Check Redpanda logs: `docker-compose logs redpanda` |
| WebSocket connection refused | Ensure backend is running on port 8000 |

---

## 🚀 Ready to Deploy?

### Local Kubernetes
```bash
minikube start
helm install todo-chatbot ./helm
```

### Cloud (Railway.app)
```bash
# Push to GitHub
git push origin main

# Railway will auto-deploy
```

---

**Status:** ✅ Ready to Use  
**Time to Setup:** 5 minutes  
**Quality:** Production-Ready
