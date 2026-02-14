# Deploy Phase 5 Event-Driven Architecture to Minikube
Write-Host "🚀 Deploying Phase 5 to Minikube..." -ForegroundColor Green

# Step 1: Deploy Kafka
Write-Host "`n📦 Step 1: Deploying Kafka..." -ForegroundColor Cyan
kubectl apply -f k8s/kafka-deployment.yaml

Write-Host "⏳ Waiting for Kafka to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s

Write-Host "✅ Kafka deployed successfully!" -ForegroundColor Green

# Step 2: Apply Dapr Components
Write-Host "`n📦 Step 2: Applying Dapr Components..." -ForegroundColor Cyan
kubectl apply -f dapr-components/

Write-Host "✅ Dapr components applied!" -ForegroundColor Green

# Step 3: Deploy Notification Service
Write-Host "`n📦 Step 3: Deploying Notification Service..." -ForegroundColor Cyan
kubectl apply -f k8s/notification-service.yaml

Write-Host "⏳ Waiting for Notification Service to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=notification-service --timeout=300s

Write-Host "✅ Notification Service deployed!" -ForegroundColor Green

# Step 4: Deploy Recurring Task Service
Write-Host "`n📦 Step 4: Deploying Recurring Task Service..." -ForegroundColor Cyan
kubectl apply -f k8s/recurring-task-service.yaml

Write-Host "⏳ Waiting for Recurring Task Service to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=recurring-task-service --timeout=300s

Write-Host "✅ Recurring Task Service deployed!" -ForegroundColor Green

# Step 5: Verify all services
Write-Host "`n🔍 Verifying all Phase 5 services..." -ForegroundColor Cyan
kubectl get pods
kubectl get services

Write-Host "`n✅ Phase 5 deployed successfully!" -ForegroundColor Green
Write-Host "`n📊 Service Status:" -ForegroundColor Cyan
Write-Host "  - Kafka: Running on kafka:9092" -ForegroundColor White
Write-Host "  - Notification Service: Running on port 8765" -ForegroundColor White
Write-Host "  - Recurring Task Service: Running" -ForegroundColor White
Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Test event publishing: Create/update/delete tasks" -ForegroundColor White
Write-Host "  2. Check Kafka topics: kubectl exec -it kafka-xxx -- rpk topic list" -ForegroundColor White
Write-Host "  3. View service logs: kubectl logs -f <pod-name>" -ForegroundColor White
