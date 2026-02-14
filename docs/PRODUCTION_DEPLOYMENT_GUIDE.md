# Production Deployment Guide
## Complete Phase 5 Production Deployment

---

## 🎯 Overview
This guide covers complete production deployment of Phase 5 Todo Chatbot with:
- Oracle Cloud OKE deployment
- CI/CD pipeline setup
- Monitoring with Prometheus & Grafana
- Security best practices
- High availability configuration

---

## 📋 Pre-Deployment Checklist

### Infrastructure
- [ ] Oracle Cloud account created
- [ ] OCI CLI installed and configured
- [ ] OKE cluster created
- [ ] Container registry configured
- [ ] Domain name registered (optional)

### Secrets & Configuration
- [ ] Database connection string
- [ ] API keys and tokens
- [ ] SSL certificates
- [ ] Environment variables

### CI/CD
- [ ] GitHub repository configured
- [ ] GitHub secrets added
- [ ] CI/CD pipeline tested

---

## 🚀 Deployment Steps

### Phase 1: Infrastructure Setup (30 minutes)

#### 1.1 Create OKE Cluster
```powershell
# Set variables
$COMPARTMENT_ID = "ocid1.compartment.oc1..xxx"
$REGION = "us-ashburn-1"

# Create cluster
oci ce cluster create `
  --compartment-id $COMPARTMENT_ID `
  --name todo-chatbot-prod `
  --kubernetes-version v1.28.2 `
  --vcn-id <VCN_OCID>
```

#### 1.2 Configure kubectl
```powershell
# Get kubeconfig
oci ce cluster create-kubeconfig `
  --cluster-id <CLUSTER_OCID> `
  --file $HOME\.kube\config-prod `
  --region $REGION

$env:KUBECONFIG="$HOME\.kube\config-prod"
kubectl get nodes
```


### Phase 2: Security Configuration (20 minutes)

#### 2.1 Create Kubernetes Secrets
```powershell
# Database secret
kubectl create secret generic db-secret `
  --from-literal=connectionString="postgresql://user:pass@host:5432/db" `
  --namespace=default

# API keys
kubectl create secret generic api-keys `
  --from-literal=openai-key="sk-xxx" `
  --from-literal=jwt-secret="your-secret-key" `
  --namespace=default

# Container registry credentials
kubectl create secret docker-registry ocir-secret `
  --docker-server=<region>.ocir.io `
  --docker-username='<tenancy>/<username>' `
  --docker-password='<auth-token>' `
  --namespace=default
```

#### 2.2 Configure Network Policies
```powershell
kubectl apply -f k8s/security/network-policies.yaml
```

### Phase 3: Deploy Core Services (30 minutes)

#### 3.1 Install Dapr
```powershell
C:\dapr\dapr.exe init -k --wait --timeout 300
dapr status -k
```

#### 3.2 Deploy Kafka
```powershell
kubectl apply -f k8s/kafka-deployment.yaml
kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s
```

#### 3.3 Deploy Dapr Components
```powershell
kubectl apply -f dapr-components/
```

#### 3.4 Deploy Microservices
```powershell
kubectl apply -f k8s/notification-service.yaml
kubectl apply -f k8s/recurring-task-service.yaml
```

#### 3.5 Deploy Main Application
```powershell
helm upgrade --install todo-chatbot ./charts/todo-chatbot `
  --set image.tag=latest `
  --set replicaCount=3 `
  --set resources.requests.memory=512Mi `
  --set resources.requests.cpu=250m
```

### Phase 4: Monitoring Setup (15 minutes)

#### 4.1 Deploy Prometheus & Grafana
```powershell
.\scripts\setup-monitoring.ps1
```

#### 4.2 Import Grafana Dashboards
```powershell
# Access Grafana
$GRAFANA_IP = kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
Write-Host "Grafana: http://$GRAFANA_IP:3000"

# Login: admin / admin123
# Import dashboard from k8s/monitoring/grafana-dashboard.json
```

### Phase 5: CI/CD Pipeline Setup (20 minutes)

#### 5.1 Configure GitHub Secrets
Go to GitHub repository → Settings → Secrets and add:
- `KUBE_CONFIG`: Base64 encoded kubeconfig
- `DATABASE_URL`: Production database URL
- `OPENAI_API_KEY`: OpenAI API key
- `DOCKER_REGISTRY`: Container registry URL

#### 5.2 Test CI/CD Pipeline
```powershell
# Push to main branch to trigger deployment
git add .
git commit -m "Deploy to production"
git push origin main

# Monitor deployment
gh run watch
```


---

## 🔒 Security Best Practices

### 1. Network Security
- Enable network policies
- Use private subnets for databases
- Configure firewall rules
- Enable DDoS protection

### 2. Secret Management
- Use Kubernetes secrets
- Rotate secrets regularly
- Never commit secrets to Git
- Use OCI Vault for sensitive data

### 3. Access Control
- Enable RBAC
- Use service accounts
- Implement least privilege
- Enable audit logging

### 4. Container Security
- Scan images for vulnerabilities
- Use minimal base images
- Run as non-root user
- Enable Pod Security Policies

---

## 📊 Monitoring & Alerting

### Key Metrics to Monitor
1. **Application Metrics**
   - API response time (target: < 200ms)
   - Error rate (target: < 1%)
   - Request throughput
   - Active users

2. **Infrastructure Metrics**
   - CPU usage (alert: > 80%)
   - Memory usage (alert: > 85%)
   - Disk usage (alert: > 90%)
   - Network traffic

3. **Kafka Metrics**
   - Message throughput
   - Consumer lag (alert: > 1000)
   - Broker health
   - Topic partition count

4. **Database Metrics**
   - Connection pool usage
   - Query performance
   - Replication lag
   - Storage usage

### Alerting Rules
```yaml
# Example Prometheus alert rules
groups:
  - name: todo-chatbot-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
      
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
        for: 5m
        annotations:
          summary: "High memory usage"
```

---

## 🔄 Backup & Disaster Recovery

### Database Backups
```powershell
# Automated daily backups
kubectl create cronjob db-backup `
  --image=postgres:16-alpine `
  --schedule="0 2 * * *" `
  --restart=OnFailure `
  -- pg_dump -h $DB_HOST -U $DB_USER $DB_NAME > /backups/backup-$(date +%Y%m%d).sql
```

### Disaster Recovery Plan
1. **RTO (Recovery Time Objective)**: 1 hour
2. **RPO (Recovery Point Objective)**: 24 hours
3. **Backup Strategy**: Daily automated backups
4. **Recovery Steps**:
   - Restore database from backup
   - Redeploy services from Git
   - Verify functionality
   - Update DNS if needed

---

## 🚦 Health Checks

### Application Health Endpoints
```yaml
# Backend health check
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

### Smoke Tests
```powershell
# Run after deployment
.\scripts\run-smoke-tests.ps1
```

---

## 📈 Scaling Configuration

### Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-chatbot-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Testing
```powershell
# Install k6
choco install k6

# Run load test
k6 run tests/load-test.js
```

---

## 🎯 Production Checklist

### Pre-Launch
- [ ] All services deployed and healthy
- [ ] Database migrations completed
- [ ] Secrets configured
- [ ] Monitoring dashboards created
- [ ] Alerts configured
- [ ] Backup system tested
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation updated

### Post-Launch
- [ ] Monitor metrics for 24 hours
- [ ] Verify backups working
- [ ] Test disaster recovery
- [ ] Review logs for errors
- [ ] Performance optimization
- [ ] User feedback collection

---

## 🆘 Troubleshooting

### Common Issues

#### 1. Pods Not Starting
```powershell
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

#### 2. Service Unavailable
```powershell
kubectl get svc
kubectl get endpoints
```

#### 3. High Memory Usage
```powershell
kubectl top pods
kubectl describe node
```

#### 4. Kafka Connection Issues
```powershell
kubectl exec -it <kafka-pod> -- rpk cluster info
kubectl logs <service-pod> | findstr kafka
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- **Daily**: Monitor dashboards, check alerts
- **Weekly**: Review logs, update dependencies
- **Monthly**: Security patches, performance review
- **Quarterly**: Disaster recovery drill, capacity planning

### Escalation Path
1. Check monitoring dashboards
2. Review application logs
3. Check Kubernetes events
4. Contact DevOps team
5. Escalate to senior engineer

---

## ✅ Success Criteria

### Performance Targets
- API response time: < 200ms (p95)
- Uptime: 99.9%
- Error rate: < 0.1%
- Event processing: < 1 second

### Business Metrics
- User satisfaction: > 4.5/5
- Task completion rate: > 95%
- System availability: 99.9%

---

**Production deployment complete! Your Phase 5 Todo Chatbot is now live! 🎉**
