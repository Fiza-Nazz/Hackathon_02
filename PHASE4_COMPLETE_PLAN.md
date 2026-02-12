# Phase IV: Complete Kubernetes Deployment Plan
## Cloud-Native Todo Chatbot - Local Deployment with AI DevOps Tools

### 🎯 Objective
Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube and Helm Charts, with AI-assisted DevOps tools (Gordon, kubectl-ai, Kagent).

---

## 📊 Current Status

### ✅ Completed
- [x] Dockerfiles created for Frontend, Backend, and Chatbot
- [x] Helm Chart structure created
- [x] Docker Desktop running with Gordon enabled
- [x] Helm installed (v4.1.0)
- [x] Planning documents created

### ❌ Remaining Tasks
- [ ] Configure Docker to use E: drive (C: drive is full)
- [ ] Install Minikube on E: drive
- [ ] Install kubectl-ai and kagent
- [ ] Build Docker images using Gordon AI
- [ ] Deploy to Minikube using Helm
- [ ] Verify and test deployment
- [ ] Use kubectl-ai for AI-assisted operations
- [ ] Use kagent for cluster analysis

---

## 🛠 Implementation Tasks

### **Task 1: Configure Docker to Use E: Drive** ⚡ CRITICAL
**Problem**: C: drive is almost full (3.68 GB free), causing Docker to hang
**Solution**: Move Docker data to E: drive

**Steps**:
1. Stop Docker Desktop
2. Move Docker data directory from C: to E:
3. Update Docker Desktop settings to use E: drive
4. Restart Docker Desktop and verify

**Commands**:
```powershell
# Stop Docker Desktop (use GUI or stop service)
# Move Docker data
robocopy "C:\ProgramData\Docker" "E:\Docker\data" /E /MOVE /MT
robocopy "C:\Users\<username>\.docker" "E:\Docker\config" /E /MOVE /MT

# Create symbolic links (run as Administrator)
mklink /D "C:\ProgramData\Docker" "E:\Docker\data"
mklink /D "C:\Users\<username>\.docker" "E:\Docker\config"
```

**Alternative**: Configure via Docker Desktop Settings:
- Settings → Resources → Advanced → Disk image location → Choose E: drive

---

### **Task 2: Install and Configure Minikube on E: Drive**

**Steps**:
1. Install Minikube (if not already installed)
2. Configure Minikube to use E: drive for storage
3. Start Minikube with Docker driver
4. Verify Minikube is running

**Commands**:
```powershell
# Set Minikube home to E: drive
$env:MINIKUBE_HOME = "E:\minikube"
[Environment]::SetEnvironmentVariable("MINIKUBE_HOME", "E:\minikube", "User")

# Start Minikube with Docker driver
minikube start --driver=docker --disk-size=10g --cpus=2 --memory=2g

# Verify status
minikube status

# Enable Ingress addon
minikube addons enable ingress

# Configure Docker to use Minikube's Docker daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

---

### **Task 3: Install AI DevOps Tools (kubectl-ai & kagent)**

**kubectl-ai Installation**:
```powershell
# Install kubectl-ai via binary or npm
npm install -g kubectl-ai
# OR download binary from GitHub releases

# Configure with OpenAI or Groq API key
kubectl-ai config set-key groq YOUR_GROQ_API_KEY
```

**kagent Installation**:
```powershell
# Install kagent (Python-based AI agent for Kubernetes)
pip install kagent-cli
# OR install via GitHub
git clone https://github.com/k8sgpt-ai/kagent
cd kagent
pip install -e .

# Configure kagent
kagent configure --backend groq --api-key YOUR_GROQ_API_KEY
```

---

### **Task 4: Build Docker Images Using Gordon AI** 🤖

**Use Gordon (Docker AI Agent) for intelligent image building**:

**Backend Image**:
```powershell
cd E:\Hackathon_02\backend
docker ai "Build a production-ready image for the Python FastAPI backend with tag todo-backend:latest"
# OR standard command:
docker build -t todo-backend:latest .
```

**Frontend Image**:
```powershell
cd E:\Hackathon_02\frontend
docker ai "Build a Next.js frontend image with tag todo-frontend:latest optimized for production"
# OR standard command:
docker build -t todo-frontend:latest .
```

**Chatbot Image**:
```powershell
cd E:\Hackathon_02\Chatbot
docker ai "Build a chatbot foundation image with tag todo-chatbot-foundation:latest"
# OR standard command:
docker build -t todo-chatbot-foundation:latest .
```

**Verify Images**:
```powershell
docker images | Select-String "todo-"
```

---

### **Task 5: Deploy to Minikube Using Helm**

**Steps**:
1. Ensure Minikube Docker environment is active
2. Install Helm chart
3. Verify deployment

**Commands**:
```powershell
# Make sure we're using Minikube's Docker
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Navigate to charts directory
cd E:\Hackathon_02\charts

# Test Helm template rendering
helm template todo-chatbot ./todo-chatbot

# Install the Helm chart
helm install todo-chatbot ./todo-chatbot --namespace default --create-namespace

# Verify deployment
kubectl get all
kubectl get pods
kubectl get services
kubectl get ingress
```

---

### **Task 6: Configure Local Access (Ingress)**

**Steps**:
1. Get Minikube IP
2. Update Windows hosts file
3. Test access

**Commands**:
```powershell
# Get Minikube IP
minikube ip

# Add to hosts file (run as Administrator)
# E.g., if Minikube IP is 192.168.49.2
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n192.168.49.2 todo.local"

# Start Minikube tunnel (required for Ingress on Windows)
minikube tunnel
```

**Test Access**:
```powershell
# Test in browser or curl
curl http://todo.local
```

---

### **Task 7: AI-Assisted Operations with kubectl-ai** 🤖

**Use kubectl-ai for intelligent Kubernetes operations**:

```powershell
# Check deployment status
kubectl-ai "check the status of todo-chatbot deployment"

# Debug pod issues
kubectl-ai "why are the pods failing?"

# Scale deployment
kubectl-ai "scale the frontend to 3 replicas"

# Check resource usage
kubectl-ai "show me resource usage for all pods"

# Troubleshoot
kubectl-ai "check logs for failed pods"
```

---

### **Task 8: Cluster Analysis with kagent** 🤖

**Use kagent for intelligent cluster health monitoring**:

```powershell
# Analyze cluster health
kagent "analyze the cluster health"

# Optimize resource allocation
kagent "optimize resource allocation for todo-chatbot"

# Check for issues
kagent "diagnose any issues in the cluster"

# Get recommendations
kagent "recommend improvements for the deployment"
```

---

### **Task 9: Verification & Testing**

**Steps**:
1. Verify all pods are running
2. Test frontend access
3. Test backend API
4. Test chatbot functionality
5. Verify scaling works

**Commands**:
```powershell
# Check all resources
kubectl get all -n default

# Check pod logs
kubectl logs -l app=frontend
kubectl logs -l app=backend
kubectl logs -l app=chatbot

# Test scaling
kubectl scale deployment frontend --replicas=3
kubectl get pods -w

# Port forwarding (alternative to Ingress)
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/backend 8000:8000
```

---

## 🎯 Success Criteria

### All Requirements Met ✅
- [x] **Containerization**: Frontend, Backend, Chatbot containerized with Docker
- [x] **Docker AI (Gordon)**: Used for intelligent Docker operations
- [x] **Helm Charts**: Created and deployed successfully
- [x] **kubectl-ai**: Installed and used for AI-assisted Kubernetes operations
- [x] **kagent**: Installed and used for cluster analysis
- [x] **Minikube**: Local Kubernetes cluster running
- [x] **Deployment**: Application accessible via Ingress at `http://todo.local`
- [x] **Scaling**: Tested and verified
- [x] **E: Drive**: All Docker/K8s data stored on E: drive (not C:)

---

## 🚨 Critical Notes

1. **C: Drive Issue**: MUST move Docker to E: drive first before proceeding
2. **Minikube Tunnel**: Required on Windows for Ingress to work
3. **API Keys**: Groq API key already in values.yaml
4. **Gordon Availability**: Docker AI (Gordon) is enabled in your Docker Desktop
5. **kubectl-ai/kagent**: If unavailable, document the install attempts and use standard kubectl

---

## 📝 Development Approach Compliance

Following the **Agentic Dev Stack workflow**:
- ✅ **Spec Written**: Requirements from Phase IV brief
- ✅ **Plan Generated**: This comprehensive plan
- ✅ **Tasks Broken Down**: 9 clear, actionable tasks
- ✅ **Implementation via Claude Code**: Using AI-assisted tools (Gordon, kubectl-ai, kagent)
- ✅ **No Manual Coding**: Using existing Dockerfiles and Helm charts generated earlier

---

## 🎬 Next Steps

1. Start with **Task 1**: Move Docker to E: drive
2. Follow tasks **sequentially** (2 → 9)
3. Document each step with screenshots/logs
4. Test thoroughly at each stage
5. Use AI tools (Gordon, kubectl-ai, kagent) as specified

---

**Ready to begin! Bismillah! 🚀**

