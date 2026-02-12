# Phase V Deployment Guide

## 📋 Prerequisites

- Docker & Docker Compose
- Kubernetes (Minikube for local, OKE for cloud)
- Helm 3.x
- kubectl
- Python 3.11+
- Git

## 🚀 Local Development Setup

### Step 1: Start Services with Docker Compose

```bash
# Start all services (PostgreSQL, Redpanda, etc.)
docker-compose up -d

# Verify services are running
docker-compose ps

# Check logs
docker-compose logs -f
```

### Step 2: Install Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Initialize Database

```bash
cd backend
python -m src.database.init_db
```

### Step 4: Start Backend Service

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Verify Services

```bash
# Backend health check
curl http://localhost:8000/health

# Redpanda console
open http://localhost:8080

# API documentation
open http://localhost:8000/docs
```

## 🐳 Docker Deployment

### Build Backend Image

```bash
cd backend
docker build -t todo-backend:latest .
docker tag todo-backend:latest ghcr.io/your-org/todo-backend:latest
docker push ghcr.io/your-org/todo-backend:latest
```

### Build Chatbot Image

```bash
cd Chatbot
docker build -t todo-chatbot:latest .
docker tag todo-chatbot:latest ghcr.io/your-org/todo-chatbot:latest
docker push ghcr.io/your-org/todo-chatbot:latest
```

## ☸️ Kubernetes Deployment (Minikube)

### Step 1: Start Minikube

```bash
minikube start --cpus=4 --memory=8192 --disk-size=20gb
minikube addons enable ingress
minikube addons enable metrics-server
```

### Step 2: Install Dapr

```bash
dapr init -k
kubectl wait --for=condition=ready pod -l app=dapr-operator -n dapr-system --timeout=300s
```

### Step 3: Deploy Services

```bash
# Create namespace
kubectl create namespace todo-app

# Deploy PostgreSQL
kubectl apply -f k8s/postgres-deployment.yaml -n todo-app

# Deploy Redpanda
kubectl apply -f k8s/redpanda-deployment.yaml -n todo-app

# Wait for dependencies
kubectl wait --for=condition=ready pod -l app=postgres -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=redpanda -n todo-app --timeout=300s

# Deploy Backend
kubectl apply -f k8s/backend-deployment.yaml -n todo-app

# Deploy WebSocket
kubectl apply -f k8s/websocket-deployment.yaml -n todo-app
```

### Step 4: Deploy with Helm

```bash
# Install or upgrade release
helm upgrade --install todo-chatbot ./helm -n todo-app

# Check deployment status
helm status todo-chatbot -n todo-app

# Get service endpoints
kubectl get svc -n todo-app
```

### Step 5: Access Services

```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Port forward to backend
kubectl port-forward -n todo-app svc/todo-backend 8000:8000

# Port forward to WebSocket
kubectl port-forward -n todo-app svc/todo-websocket 8001:8001

# Access services
curl http://localhost:8000/health
```

## ☁️ Cloud Deployment (Oracle OKE)

### Step 1: Create OKE Cluster

```bash
# Using Oracle Cloud CLI
oci ce cluster create \
  --name todo-chatbot-cluster \
  --kubernetes-version v1.28.0 \
  --vcn-id <your-vcn-id> \
  --kubernetes-network-config cidrBlocks=10.0.0.0/16
```

### Step 2: Configure kubectl

```bash
# Get cluster credentials
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-id> \
  --file $HOME/.kube/config
```

### Step 3: Install Dapr on OKE

```bash
dapr init -k
```

### Step 4: Deploy to OKE

```bash
# Create namespace
kubectl create namespace todo-app

# Deploy all services
kubectl apply -f k8s/ -n todo-app

# Deploy with Helm
helm upgrade --install todo-chatbot ./helm -n todo-app
```

### Step 5: Configure Ingress

```bash
# Create ingress for public access
kubectl apply -f k8s/ingress.yaml -n todo-app

# Get public IP
kubectl get ingress -n todo-app
```

## 📊 Monitoring and Logging

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/todo-backend -n todo-app

# WebSocket logs
kubectl logs -f deployment/todo-websocket -n todo-app

# All pod logs
kubectl logs -f -l app=todo-backend -n todo-app
```

### Check Pod Status

```bash
# Get all pods
kubectl get pods -n todo-app

# Describe pod for details
kubectl describe pod <pod-name> -n todo-app

# Get pod events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Resource Usage

```bash
# Check resource usage
kubectl top nodes
kubectl top pods -n todo-app
```

## 🧪 Testing

### Run Unit Tests

```bash
cd backend
pytest tests/unit -v
```

### Run Integration Tests

```bash
cd backend
pytest tests/integration -v
```

### Run End-to-End Tests

```bash
cd backend
pytest tests/e2e -v
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Runs tests on push
2. Builds Docker images
3. Pushes to container registry
4. Deploys to Kubernetes cluster
5. Runs smoke tests

View workflow status: `.github/workflows/phase5-deploy.yml`

## 🐛 Troubleshooting

### Services not starting

```bash
# Check Docker Compose logs
docker-compose logs <service-name>

# Check Kubernetes pod logs
kubectl logs <pod-name> -n todo-app

# Describe pod for errors
kubectl describe pod <pod-name> -n todo-app
```

### Database connection issues

```bash
# Test PostgreSQL connection
psql -h localhost -U todouser -d tododb

# Check PostgreSQL pod
kubectl exec -it postgres-pod -n todo-app -- psql -U todouser -d tododb
```

### Kafka/Redpanda issues

```bash
# Check Redpanda status
docker exec todo_redpanda rpk cluster info

# Check Redpanda console
open http://localhost:8080
```

## 📝 Environment Variables

Create `.env` file in backend directory:

```env
DATABASE_URL=postgresql://todouser:todopass123@localhost:5432/tododb
KAFKA_BROKERS=localhost:19092
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

## 🎯 Success Criteria

- ✅ All services start without errors
- ✅ Health check endpoints return 200
- ✅ Database migrations complete
- ✅ Kafka topics created
- ✅ WebSocket connections working
- ✅ API endpoints responding
- ✅ Frontend can communicate with backend
- ✅ Chatbot MCP tools functional

## 📞 Support

For issues or questions:
1. Check logs: `kubectl logs -f <pod-name> -n todo-app`
2. Check events: `kubectl get events -n todo-app`
3. Review deployment guide
4. Check GitHub issues

---

**Last Updated:** 2024
**Version:** Phase V 2.1.0
