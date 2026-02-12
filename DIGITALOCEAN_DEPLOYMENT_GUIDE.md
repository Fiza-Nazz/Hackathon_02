# Phase V - DigitalOcean Kubernetes Deployment Guide

**Status:** 🚀 Ready for Deployment  
**Platform:** DigitalOcean Kubernetes Service (DOKS)  
**Cost:** $200 Free Credits (60 days)  
**Published URL:** Will be provided after deployment

---

## 📋 Prerequisites

- DigitalOcean Account (free, no card needed)
- `doctl` CLI (DigitalOcean CLI)
- `kubectl` installed
- `helm` installed
- GitHub repository with code

---

## 🎯 Step 1: Create DigitalOcean Account

### 1.1 Sign Up (No Card Required)
```
URL: https://www.digitalocean.com/
1. Click "Sign Up"
2. Enter email
3. Create password
4. Verify email
5. Get $200 free credits
```

### 1.2 Create API Token
```
1. Go to: https://cloud.digitalocean.com/account/api/tokens
2. Click "Generate New Token"
3. Name: "todo-chatbot-token"
4. Select: "Read" and "Write"
5. Copy token (save it!)
```

---

## 🔧 Step 2: Install DigitalOcean CLI

### macOS
```bash
brew install doctl
```

### Windows (PowerShell)
```powershell
choco install doctl
```

### Linux
```bash
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-x64.tar.gz
tar xf ~/doctl-1.94.0-linux-x64.tar.gz
sudo mv ~/doctl /usr/local/bin
```

### Verify Installation
```bash
doctl version
```

---

## 🔐 Step 3: Authenticate with DigitalOcean

```bash
doctl auth init

# When prompted:
# 1. Paste your API token
# 2. Press Enter
# 3. Choose default region (e.g., nyc3)
```

Verify authentication:
```bash
doctl account get
```

---

## ☸️ Step 4: Create Kubernetes Cluster

### 4.1 Create DOKS Cluster
```bash
doctl kubernetes cluster create todo-chatbot-cluster \
  --region nyc3 \
  --version latest \
  --node-pool name=default-pool \
  --node-pool size=s-2vcpu-2gb \
  --node-pool count=2 \
  --enable-monitoring \
  --enable-surge-upgrade
```

**Wait 5-10 minutes for cluster to be ready**

### 4.2 Get Cluster Credentials
```bash
doctl kubernetes cluster kubeconfig save todo-chatbot-cluster
```

### 4.3 Verify Cluster Connection
```bash
kubectl cluster-info
kubectl get nodes
```

---

## 📦 Step 5: Install Required Components

### 5.1 Install Dapr
```bash
dapr init -k
kubectl wait --for=condition=ready pod -l app=dapr-operator -n dapr-system --timeout=300s
```

### 5.2 Create Namespace
```bash
kubectl create namespace todo-app
```

### 5.3 Deploy PostgreSQL
```bash
kubectl apply -f k8s/postgres-deployment.yaml -n todo-app
kubectl wait --for=condition=ready pod -l app=postgres -n todo-app --timeout=300s
```

### 5.4 Deploy Redpanda (Kafka)
```bash
kubectl apply -f k8s/redpanda-deployment.yaml -n todo-app
kubectl wait --for=condition=ready pod -l app=redpanda -n todo-app --timeout=300s
```

---

## 🚀 Step 6: Deploy Application

### 6.1 Build and Push Docker Images

```bash
# Login to Docker Hub (or GitHub Container Registry)
docker login

# Build backend image
cd backend
docker build -t your-username/todo-backend:latest .
docker push your-username/todo-backend:latest

# Build chatbot image
cd ../Chatbot
docker build -t your-username/todo-chatbot:latest .
docker push your-username/todo-chatbot:latest
```

### 6.2 Update Kubernetes Manifests
```bash
# Edit k8s/backend-deployment.yaml
# Change image: your-username/todo-backend:latest

# Edit k8s/websocket-deployment.yaml
# Change image: your-username/todo-backend:latest
```

### 6.3 Deploy Services
```bash
kubectl apply -f k8s/backend-deployment.yaml -n todo-app
kubectl apply -f k8s/websocket-deployment.yaml -n todo-app

# Verify deployments
kubectl get pods -n todo-app
kubectl get svc -n todo-app
```

---

## 🌐 Step 7: Setup Ingress & Public URL

### 7.1 Install Nginx Ingress Controller
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer
```

### 7.2 Get Load Balancer IP
```bash
kubectl get svc -n ingress-nginx

# Copy the EXTERNAL-IP (this is your public IP)
```

### 7.3 Create Ingress
```bash
cat > ingress.yaml << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  namespace: todo-app
spec:
  ingressClassName: nginx
  rules:
  - host: todo-chatbot.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-backend
            port:
              number: 8000
EOF

kubectl apply -f ingress.yaml
```

### 7.4 Point Domain to Load Balancer IP
```
1. Go to your domain registrar
2. Add A record:
   - Name: todo-chatbot
   - Value: <LOAD_BALANCER_IP>
   - TTL: 3600
3. Wait 5-10 minutes for DNS to propagate
```

### 7.5 Get Public URL
```bash
# Your public URL will be:
https://todo-chatbot.your-domain.com

# Or use the Load Balancer IP directly:
http://<LOAD_BALANCER_IP>
```

---

## 🔍 Step 8: Verify Deployment

### 8.1 Check All Pods
```bash
kubectl get pods -n todo-app
kubectl get pods -n dapr-system
```

### 8.2 Check Services
```bash
kubectl get svc -n todo-app
```

### 8.3 Check Logs
```bash
# Backend logs
kubectl logs -f deployment/todo-backend -n todo-app

# WebSocket logs
kubectl logs -f deployment/todo-websocket -n todo-app

# Redpanda logs
kubectl logs -f deployment/redpanda -n todo-app
```

### 8.4 Test Health Endpoint
```bash
curl https://todo-chatbot.your-domain.com/health
```

---

## 📊 Step 9: Setup Monitoring

### 9.1 Enable DigitalOcean Monitoring
```bash
doctl kubernetes cluster update todo-chatbot-cluster \
  --enable-monitoring
```

### 9.2 View Metrics
```
1. Go to: https://cloud.digitalocean.com/kubernetes/clusters
2. Select your cluster
3. Click "Monitoring" tab
4. View CPU, Memory, Network metrics
```

---

## 🔄 Step 10: Setup CI/CD with GitHub Actions

### 10.1 Create GitHub Secrets
```
1. Go to: GitHub Repo → Settings → Secrets
2. Add secrets:
   - DOCKER_USERNAME: your-docker-username
   - DOCKER_PASSWORD: your-docker-password
   - DIGITALOCEAN_ACCESS_TOKEN: your-do-token
   - KUBECONFIG: (base64 encoded kubeconfig)
```

### 10.2 Create Deployment Workflow
```bash
cat > .github/workflows/deploy-do.yml << 'EOF'
name: Deploy to DigitalOcean

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push Docker image
      run: |
        docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
        docker build -t ${{ secrets.DOCKER_USERNAME }}/todo-backend:latest ./backend
        docker push ${{ secrets.DOCKER_USERNAME }}/todo-backend:latest
    
    - name: Deploy to DigitalOcean
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > $HOME/.kube/config
        kubectl set image deployment/todo-backend \
          todo-backend=${{ secrets.DOCKER_USERNAME }}/todo-backend:latest \
          -n todo-app
        kubectl rollout status deployment/todo-backend -n todo-app
EOF
```

---

## 📈 Monitoring & Logs

### View Real-time Logs
```bash
kubectl logs -f deployment/todo-backend -n todo-app
```

### View Pod Events
```bash
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Check Resource Usage
```bash
kubectl top nodes
kubectl top pods -n todo-app
```

---

## 🐛 Troubleshooting

### Pods not starting?
```bash
kubectl describe pod <pod-name> -n todo-app
```

### Service not accessible?
```bash
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app
curl http://localhost:8000/health
```

### Ingress not working?
```bash
kubectl describe ingress todo-ingress -n todo-app
kubectl get ingress -n todo-app
```

### Check Dapr status
```bash
dapr status -k
```

---

## 💰 Cost Management

### Monitor Spending
```bash
doctl billing get
```

### Set Billing Alert
```
1. Go to: https://cloud.digitalocean.com/account/billing
2. Set alert at: $150 (to stay within $200 credits)
```

### Delete Resources (if needed)
```bash
# Delete cluster
doctl kubernetes cluster delete todo-chatbot-cluster

# Delete volumes
doctl compute volume list
doctl compute volume delete <volume-id>
```

---

## 🎯 Final Checklist

- [ ] DigitalOcean account created
- [ ] API token generated
- [ ] `doctl` CLI installed and authenticated
- [ ] DOKS cluster created
- [ ] PostgreSQL deployed
- [ ] Redpanda deployed
- [ ] Backend deployed
- [ ] WebSocket deployed
- [ ] Ingress configured
- [ ] Public URL working
- [ ] Health check passing
- [ ] Monitoring enabled
- [ ] CI/CD pipeline configured

---

## 📱 Your Published URLs

After deployment, you'll have:

```
Frontend: https://frontend-eight-gilt-98.vercel.app
Backend API: https://todo-chatbot.your-domain.com
API Docs: https://todo-chatbot.your-domain.com/docs
WebSocket: wss://todo-chatbot.your-domain.com/ws/tasks/{user_id}
```

---

## 🚀 Next Steps

1. ✅ Create DigitalOcean account
2. ✅ Deploy cluster
3. ✅ Deploy services
4. ✅ Get public URL
5. ✅ Test endpoints
6. ✅ Record demo video
7. ✅ Submit project

---

## 📞 Support

- DigitalOcean Docs: https://docs.digitalocean.com/
- Kubernetes Docs: https://kubernetes.io/docs/
- Dapr Docs: https://dapr.io/docs/

---

**Estimated Time:** 30-45 minutes  
**Cost:** $0 (using free credits)  
**Result:** Production-grade deployment with public URL

---

*Last Updated: February 11, 2026*  
*Phase V Version: 2.1.0*
