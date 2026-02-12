# Task 3: Install AI DevOps Tools (kubectl-ai & kagent)

## Goal
Install and configure kubectl-ai and kagent for AI-assisted Kubernetes operations.

## Part A: Install kubectl-ai

### Method 1: NPM Installation (Recommended)
```powershell
# Install kubectl-ai globally via npm
npm install -g kubectl-ai

# Verify installation
kubectl-ai --version
```

### Method 2: Manual Binary Installation
```powershell
# Download latest release from GitHub
# https://github.com/sozercan/kubectl-ai/releases

# Download the Windows binary (kubectl-ai.exe)
# Move to a directory in your PATH, e.g., C:\Windows\System32

# Or create a dedicated directory
New-Item -ItemType Directory -Path "E:\k8s-tools" -Force
# Download kubectl-ai.exe to E:\k8s-tools\
# Add E:\k8s-tools\ to your PATH
```

### Configure kubectl-ai with Groq API
```powershell
# Set Groq as the backend (free and fast!)
kubectl-ai config set-backend groq

# Set your Groq API key
kubectl-ai config set-key groq "YOUR_GROQ_API_KEY"

# Alternatively, use environment variable
$env:GROQ_API_KEY = "YOUR_GROQ_API_KEY"
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "YOUR_GROQ_API_KEY", "User")
```

### Test kubectl-ai
```powershell
# Test with a simple query
kubectl-ai "show me all pods"

# Check cluster status
kubectl-ai "what is the status of my cluster?"
```

---

## Part B: Install kagent

### Option 1: Python pip Installation
```powershell
# Install via pip
pip install k8sgpt

# Note: "kagent" often refers to k8sgpt or similar tools
# k8sgpt is the most popular AI-powered Kubernetes analyzer
```

### Configure k8sgpt (kagent equivalent)
```powershell
# Configure with Groq backend (if supported)
# k8sgpt primarily uses OpenAI, but we can try alternatives

# Set OpenAI-compatible endpoint (for Groq)
$env:OPENAI_API_BASE = "https://api.groq.com/v1"
$env:OPENAI_API_KEY = "YOUR_GROQ_API_KEY"

# Initialize k8sgpt
k8sgpt auth add --backend openai --model llama3-8b-8192

# Analyze cluster
k8sgpt analyze
```

### Alternative: kubectl-ai as kagent
If k8sgpt is not working well with Groq, we can use kubectl-ai for all AI operations:
```powershell
# kubectl-ai can handle all kagent-type queries
kubectl-ai "analyze cluster health"
kubectl-ai "diagnose any issues"
kubectl-ai "recommend resource optimization"
```

---

## Part C: Verification

### Test kubectl-ai
```powershell
# Basic queries
kubectl-ai "list all namespaces"
kubectl-ai "show deployment status"
kubectl-ai "check pod health"

# Advanced queries
kubectl-ai "why is my deployment failing?"
kubectl-ai "scale frontend to 3 replicas"
kubectl-ai "show resource usage across all pods"
```

### Test k8sgpt (kagent)
```powershell
# Analyze cluster
k8sgpt analyze --explain

# Filter by namespace
k8sgpt analyze --namespace default --explain

# Continuous monitoring
k8sgpt analyze --explain --with-doc
```

---

## Troubleshooting

### Issue: kubectl-ai not found
```powershell
# Check if npm global bin is in PATH
npm config get prefix

# Add npm global bin to PATH
# Default location: C:\Users\<username>\AppData\Roaming\npm
```

### Issue: API key not working
```powershell
# Verify environment variable
$env:GROQ_API_KEY

# Test API key directly
curl -X POST "https://api.groq.com/openai/v1/chat/completions" `
  -H "Authorization: Bearer $env:GROQ_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{"messages":[{"role":"user","content":"test"}],"model":"llama3-8b-8192"}'
```

### Issue: k8sgpt not compatible with Groq
**Solution**: Use kubectl-ai for all AI operations. It's more flexible and supports multiple backends including Groq.

---

## Real-World Usage Examples

### Using kubectl-ai for Todo Chatbot Deployment

```powershell
# Check deployment readiness
kubectl-ai "check if todo-chatbot deployment is ready"

# Debug pod issues
kubectl-ai "why is the backend pod crashing?"

# Scale based on load
kubectl-ai "scale frontend deployment to 5 replicas"

# Check resource constraints
kubectl-ai "are there any resource issues in the cluster?"

# View logs intelligently
kubectl-ai "show me error logs from backend pods"

# Network troubleshooting
kubectl-ai "check if frontend can reach backend service"
```

### Using kubectl-ai as kagent (Cluster Analysis)

```powershell
# Health check
kubectl-ai "analyze overall cluster health"

# Resource optimization
kubectl-ai "recommend resource limits for todo-chatbot pods"

# Security scan
kubectl-ai "check for security issues in deployments"

# Performance analysis
kubectl-ai "identify performance bottlenecks"
```

---

## Next Steps

Once AI tools are installed and configured:
1. Build Docker images (Task 4)
2. Deploy to Minikube (Task 5)
3. Use kubectl-ai throughout deployment
4. Monitor and optimize with AI assistance

