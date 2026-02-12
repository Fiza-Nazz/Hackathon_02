# Task 5-9: Deploy and Verify Todo Chatbot on Minikube

## Task 5: Deploy with Helm

### Step 1: Ensure Minikube Docker Environment
```powershell
# Point to Minikube's Docker daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Verify
docker info | Select-String "Name"
```

### Step 2: Test Helm Chart Rendering
```powershell
cd E:\Hackathon_02

# Test template generation (dry-run)
helm template todo-chatbot ./charts/todo-chatbot --debug

# Check for errors in output
```

### Step 3: Install Helm Chart
```powershell
# Install the chart
helm install todo-chatbot ./charts/todo-chatbot --namespace default --create-namespace

# Watch deployment progress
kubectl get all -w
```

### Step 4: Verify Deployment
```powershell
# Check all resources
kubectl get all

# Check pods status
kubectl get pods

# Check services
kubectl get services

# Check ingress
kubectl get ingress

# Check persistent volumes (if any)
kubectl get pv,pvc
```

---

## Task 6: Configure Ingress Access

### Step 1: Enable Ingress Addon (if not already)
```powershell
minikube addons enable ingress

# Verify
minikube addons list | Select-String "ingress"
```

### Step 2: Get Minikube IP
```powershell
# Get IP address
minikube ip

# Example output: 192.168.49.2
```

### Step 3: Update Windows Hosts File
```powershell
# Run PowerShell as Administrator
$minikubeIP = (minikube ip)
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n$minikubeIP todo.local"

# Verify
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"
```

### Step 4: Start Minikube Tunnel (Required on Windows!)
```powershell
# Open a NEW PowerShell window as Administrator
minikube tunnel

# Keep this window open while using the app
# This creates a network route to Ingress
```

### Step 5: Test Access
```powershell
# Test in browser
Start-Process "http://todo.local"

# Or use curl
curl http://todo.local
curl http://todo.local/api
```

---

## Task 7: AI-Assisted Operations with kubectl-ai 🤖

### Installation (if not done in Task 3)
```powershell
npm install -g kubectl-ai

# Configure with Groq
$env:GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

### Usage Examples
```powershell
# Check deployment status
kubectl-ai "check the status of todo-chatbot deployment"

# Debug failing pods
kubectl-ai "why are my pods failing?"

# Scale frontend
kubectl-ai "scale todo-chatbot frontend to 3 replicas"

# Check resource usage
kubectl-ai "show me CPU and memory usage for all pods"

# View logs
kubectl-ai "show me the latest logs from backend pods"

# Check service connectivity
kubectl-ai "can frontend reach backend service?"

# Troubleshooting
kubectl-ai "diagnose issues in my cluster"

# Get recommendations
kubectl-ai "optimize my deployment configuration"
```

### AI-Assisted Debugging
```powershell
# If pods are crash looping
kubectl-ai "my backend pod keeps crashing, what's wrong?"

# If services not accessible
kubectl-ai "why can't I access my frontend service?"

# If ingress not working
kubectl-ai "my ingress is not routing traffic properly"
```

---

## Task 8: Cluster Analysis with kagent/k8sgpt 🤖

### Installation (if not done in Task 3)
```powershell
pip install k8sgpt
```

### Usage Examples
```powershell
# Analyze cluster health
k8sgpt analyze --explain

# Filter by namespace
k8sgpt analyze --namespace default --explain

# Get detailed analysis
k8sgpt analyze --explain --with-doc

# Check specific resources
k8sgpt analyze --filter=Pod --explain
k8sgpt analyze --filter=Service --explain
```

### Alternative: Use kubectl-ai as kagent
```powershell
# Cluster health
kubectl-ai "analyze overall cluster health for todo-chatbot"

# Resource allocation
kubectl-ai "are resources optimally allocated?"

# Security scan
kubectl-ai "check for security issues in my deployment"

# Performance analysis
kubectl-ai "identify performance bottlenecks"

# Cost optimization
kubectl-ai "how can I reduce resource costs?"
```

---

## Task 9: Verification & Testing

### Pod Health Check
```powershell
# Check all pods are running
kubectl get pods

# Expected output:
# NAME                        READY   STATUS    RESTARTS   AGE
# backend-xxx-yyy             1/1     Running   0          5m
# frontend-xxx-yyy            1/1     Running   0          5m
# frontend-xxx-zzz            1/1     Running   0          5m  (if scaled to 2)
# chatbot-xxx-yyy             1/1     Running   0          5m

# Describe pods for details
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> --follow  # tail logs
```

### Service Check
```powershell
# List services
kubectl get services

# Test service endpoints
kubectl get endpoints

# Port-forward for testing (alternative to Ingress)
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/backend 8000:8000
# Visit http://localhost:3000 and http://localhost:8000
```

### Ingress Check
```powershell
# Get ingress details
kubectl get ingress
kubectl describe ingress

# Check ingress controller
kubectl get pods -n ingress-nginx

# Test routes
curl http://todo.local
curl http://todo.local/api
curl http://todo.local/api/health  # if you have a health endpoint
```

### Application Testing
```powershell
# Open in browser
Start-Process "http://todo.local"

# Test frontend
# - Should load Next.js app
# - Check if UI renders correctly

# Test backend API
curl http://todo.local/api/docs  # FastAPI docs (if enabled)
curl http://todo.local/api/tasks  # Your API endpoints

# Test chatbot
# - Use frontend UI to interact with chatbot
# - Verify chatbot responses
```

### Scaling Test
```powershell
# Scale frontend manually
kubectl scale deployment frontend --replicas=3

# Watch pods
kubectl get pods -w

# Verify scaling
kubectl get deployment frontend

# Scale back down
kubectl scale deployment frontend --replicas=2

# AI-assisted scaling
kubectl-ai "scale backend to 2 replicas for better load distribution"
```

### Resource Usage Check
```powershell
# Check node resources
kubectl top nodes

# Check pod resources
kubectl top pods

# Detailed resource view
kubectl describe nodes

# AI analysis
kubectl-ai "show me resource usage across all components"
```

### Load Testing (Optional)
```powershell
# Using Apache Bench (if installed)
ab -n 1000 -c 10 http://todo.local/

# Using curl loop
for ($i=1; $i -le 100; $i++) {
    curl http://todo.local
    Write-Host "Request $i completed"
}
```

---

## Common Issues & Solutions

### Issue: Pods stuck in "Pending" state
```powershell
# Check events
kubectl describe pod <pod-name>

# Common causes:
# 1. Insufficient resources
minikube delete
minikube start --cpus=4 --memory=4096

# 2. Image pull issues
docker images | Select-String "todo-"

# 3. Ask AI
kubectl-ai "why is my pod pending?"
```

### Issue: Pods in "CrashLoopBackOff"
```powershell
# Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # logs from previous crash

# Common causes:
# 1. Missing environment variables
# 2. Database connection issues
# 3. Port already in use

# AI debugging
kubectl-ai "my backend pod is in CrashLoopBackOff, what should I check?"
```

### Issue: Ingress not accessible
```powershell
# Verify Ingress controller
kubectl get pods -n ingress-nginx

# Verify Ingress resource
kubectl get ingress
kubectl describe ingress

# Check hosts file
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"

# **CRITICAL**: Start minikube tunnel
minikube tunnel  # in separate admin PowerShell
```

### Issue: Services can't communicate
```powershell
# Check service endpoints
kubectl get endpoints

# Test from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
# Inside container:
# wget http://backend:8000
# wget http://frontend:3000

# AI diagnosis
kubectl-ai "why can't my frontend communicate with backend?"
```

---

## Helm Management Commands

### List Releases
```powershell
helm list
helm list --all-namespaces
```

### Upgrade Deployment
```powershell
# After making changes to values.yaml
helm upgrade todo-chatbot ./charts/todo-chatbot

# With values override
helm upgrade todo-chatbot ./charts/todo-chatbot --set frontend.replicaCount=3
```

### Rollback Deployment
```powershell
# View history
helm history todo-chatbot

# Rollback to previous version
helm rollback todo-chatbot

# Rollback to specific revision
helm rollback todo-chatbot 2
```

### Uninstall Deployment
```powershell
# Remove deployment
helm uninstall todo-chatbot

# Verify cleanup
kubectl get all
```

---

## Success Criteria Checklist ✅

- [ ] All pods are running (no CrashLoopBackOff)
- [ ] All services are accessible
- [ ] Ingress is configured and working
- [ ] Can access frontend at http://todo.local
- [ ] Can access backend API at http://todo.local/api
- [ ] Chatbot is functional through frontend
- [ ] kubectl-ai commands work
- [ ] Cluster health is good (via kagent/kubectl-ai)
- [ ] Scaling works correctly
- [ ] No critical errors in logs

---

## Documentation for Review

Create a summary document showing:
1. Screenshots of running pods
2. kubectl-ai query examples and outputs
3. Application screenshots
4. Helm deployment output
5. Resource usage stats
6. Any issues faced and how you resolved them (with AI assistance)

This documentation will be used to judge Phase IV completion!

---

**You've completed Phase IV! Congratulations! 🎉**

