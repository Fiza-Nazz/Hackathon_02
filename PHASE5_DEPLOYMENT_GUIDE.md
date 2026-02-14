# Phase 5 Deployment Guide
## Event-Driven Architecture with Kafka + Dapr

### 🎯 Overview
This guide will help you deploy Phase 5 event-driven architecture to Minikube with Kafka messaging and Dapr runtime.

---

## 📋 Prerequisites

✅ **Already Done:**
- Docker Desktop running
- Minikube running
- Phase 4 deployed (backend, frontend, chatbot)

❌ **Need to Install:**
- Dapr CLI
- Kafka (will be deployed to Minikube)

---

## 🚀 Deployment Steps

### Step 1: Install Dapr on Minikube

```powershell
# Run the Dapr installation script
.\scripts\install-dapr.ps1
```

This will:
- Install Dapr CLI (if not already installed)
- Initialize Dapr on Kubernetes
- Deploy Dapr control plane components

**Verify Dapr:**
```powershell
dapr status -k
```

You should see:
- dapr-operator
- dapr-sidecar-injector
- dapr-sentry
- dapr-placement-server

---

### Step 2: Deploy Phase 5 Services

```powershell
# Run the Phase 5 deployment script
.\scripts\deploy-phase5.ps1
```

This will deploy:
1. **Kafka** - Message broker for event streaming
2. **Dapr Components** - Pub/sub and state store configurations
3. **Notification Service** - Handles reminders and real-time updates
4. **Recurring Task Service** - Creates recurring task instances

---

### Step 3: Verify Deployment

```powershell
# Check all pods
kubectl get pods

# Check services
kubectl get services

# Check Dapr components
kubectl get components
```

**Expected Pods:**
- `kafka-xxx` - Running
- `notification-service-xxx` - Running
- `recurring-task-service-xxx` - Running
- `todo-chatbot-backend-xxx` - Running (from Phase 4)
- `todo-chatbot-frontend-xxx` - Running (from Phase 4)
- `todo-chatbot-chatbot-xxx` - Running (from Phase 4)

---

## 🧪 Testing Phase 5 Features

### Test 1: Event Publishing

```powershell
# Create a task (should publish task.created event)
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Event", "priority": "high"}'

# Check Kafka topics
kubectl exec -it <kafka-pod-name> -- rpk topic list

# View events in Kafka
kubectl exec -it <kafka-pod-name> -- rpk topic consume task-events
```

### Test 2: Recurring Tasks

```powershell
# Create a recurring task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly Report",
    "is_recurring": true,
    "recurring_pattern": "weekly",
    "recurring_interval": 1
  }'

# Complete the task
curl -X PATCH http://localhost:8000/api/tasks/{task_id}/complete \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check if new instance was created
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 3: Real-time Updates (WebSocket)

```javascript
// Connect to WebSocket in browser console
const ws = new WebSocket('ws://localhost:8000/ws/tasks/YOUR_USER_ID');

ws.onmessage = (event) => {
  console.log('Real-time update:', JSON.parse(event.data));
};

// Now create/update/delete tasks and watch real-time updates
```

---

## 📊 Monitoring

### View Service Logs

```powershell
# Kafka logs
kubectl logs -f <kafka-pod-name>

# Notification service logs
kubectl logs -f <notification-service-pod-name>

# Recurring task service logs
kubectl logs -f <recurring-task-service-pod-name>

# Backend logs (event publishing)
kubectl logs -f <backend-pod-name>
```

### Check Kafka Topics

```powershell
# List all topics
kubectl exec -it <kafka-pod-name> -- rpk topic list

# View topic details
kubectl exec -it <kafka-pod-name> -- rpk topic describe task-events

# Consume messages from topic
kubectl exec -it <kafka-pod-name> -- rpk topic consume task-events --num 10
```

### Check Dapr Status

```powershell
# Dapr control plane status
dapr status -k

# View Dapr components
kubectl get components

# Check Dapr logs
kubectl logs -n dapr-system -l app=dapr-operator
```

---

## 🔧 Troubleshooting

### Issue: Kafka pod not starting

```powershell
# Check pod status
kubectl describe pod <kafka-pod-name>

# Check logs
kubectl logs <kafka-pod-name>

# Restart pod
kubectl delete pod <kafka-pod-name>
```

### Issue: Services can't connect to Kafka

```powershell
# Verify Kafka service
kubectl get svc kafka

# Test Kafka connectivity from another pod
kubectl run kafka-test --rm -it --image=redpandadata/redpanda:latest -- \
  rpk cluster info --brokers kafka:9092
```

### Issue: Events not being published

```powershell
# Check backend logs for errors
kubectl logs -f <backend-pod-name> | findstr "event"

# Verify event publisher is initialized
kubectl logs <backend-pod-name> | findstr "publisher"
```

### Issue: Dapr components not working

```powershell
# Check component status
kubectl get components

# View component details
kubectl describe component kafka-pubsub

# Check Dapr sidecar logs
kubectl logs <pod-name> -c daprd
```

---

## 📈 Performance Metrics

### Expected Performance:
- **Event Publishing**: < 50ms
- **Event Processing**: < 1 second
- **WebSocket Updates**: < 100ms
- **Kafka Throughput**: 1000+ events/second

### Monitor Performance:

```powershell
# Check Kafka lag
kubectl exec -it <kafka-pod-name> -- rpk group describe todo-service

# Check service resource usage
kubectl top pods
```

---

## 🎯 Phase 5 Completion Checklist

- [ ] Dapr installed on Minikube
- [ ] Kafka deployed and running
- [ ] Notification service deployed
- [ ] Recurring task service deployed
- [ ] Dapr components applied
- [ ] Event publishing working (create, update, delete, complete)
- [ ] Recurring tasks auto-creating
- [ ] WebSocket real-time updates working
- [ ] All services healthy and running

---

## 🚀 Next Steps (Production Deployment)

1. **Oracle Cloud OKE Setup**
   - Create OKE cluster
   - Configure kubectl for OKE
   - Deploy to production

2. **Managed Kafka (Redpanda Cloud)**
   - Sign up for Redpanda Cloud
   - Create cluster
   - Update Kafka connection strings

3. **CI/CD Pipeline**
   - Configure GitHub Actions
   - Set up secrets
   - Enable automated deployments

4. **Monitoring & Observability**
   - Deploy Prometheus
   - Deploy Grafana
   - Configure alerts

---

## 📞 Support

If you encounter issues:
1. Check logs: `kubectl logs -f <pod-name>`
2. Verify connectivity: `kubectl get pods` and `kubectl get svc`
3. Review Dapr status: `dapr status -k`
4. Check Kafka topics: `kubectl exec -it <kafka-pod> -- rpk topic list`

---

**Phase 5 is now ready for deployment! 🎉**
