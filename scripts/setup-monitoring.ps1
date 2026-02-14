# Setup Monitoring (Prometheus + Grafana)
Write-Host "📊 Setting up Monitoring Stack..." -ForegroundColor Green

# Step 1: Create monitoring namespace
Write-Host "`n[1/4] Creating monitoring namespace..." -ForegroundColor Cyan
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Step 2: Deploy Prometheus
Write-Host "`n[2/4] Deploying Prometheus..." -ForegroundColor Cyan
kubectl apply -f k8s/monitoring/prometheus.yaml

Write-Host "⏳ Waiting for Prometheus to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=300s

Write-Host "✅ Prometheus deployed!" -ForegroundColor Green

# Step 3: Deploy Grafana
Write-Host "`n[3/4] Deploying Grafana..." -ForegroundColor Cyan
kubectl apply -f k8s/monitoring/grafana.yaml

Write-Host "⏳ Waiting for Grafana to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=300s

Write-Host "✅ Grafana deployed!" -ForegroundColor Green

# Step 4: Get access URLs
Write-Host "`n[4/4] Getting access information..." -ForegroundColor Cyan

$prometheusIP = kubectl get svc prometheus -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
$grafanaIP = kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

Write-Host "`n✅ Monitoring stack deployed successfully!" -ForegroundColor Green
Write-Host "`n📊 Access Information:" -ForegroundColor Cyan
Write-Host "  Prometheus: http://$prometheusIP:9090" -ForegroundColor White
Write-Host "  Grafana: http://$grafanaIP:3000" -ForegroundColor White
Write-Host "    Username: admin" -ForegroundColor White
Write-Host "    Password: admin123" -ForegroundColor White

Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Open Grafana in browser" -ForegroundColor White
Write-Host "  2. Login with admin/admin123" -ForegroundColor White
Write-Host "  3. Import dashboard from grafana-dashboards/" -ForegroundColor White
Write-Host "  4. View metrics and create alerts" -ForegroundColor White
