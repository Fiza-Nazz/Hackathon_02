# Smoke Tests for Production Deployment
Write-Host "🧪 Running Smoke Tests..." -ForegroundColor Green

$testsPassed = 0
$testsFailed = 0

# Test 1: Backend Health Check
Write-Host "`n[Test 1/6] Backend Health Check..." -ForegroundColor Cyan
try {
    $backendUrl = kubectl get svc backend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
    $response = Invoke-WebRequest -Uri "http://${backendUrl}:8000/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend health check passed" -ForegroundColor Green
        $testsPassed++
    }
} catch {
    Write-Host "❌ Backend health check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 2: Frontend Accessibility
Write-Host "`n[Test 2/6] Frontend Accessibility..." -ForegroundColor Cyan
try {
    $frontendUrl = kubectl get svc frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
    $response = Invoke-WebRequest -Uri "http://${frontendUrl}:3000" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend accessible" -ForegroundColor Green
        $testsPassed++
    }
} catch {
    Write-Host "❌ Frontend accessibility failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 3: Kafka Connectivity
Write-Host "`n[Test 3/6] Kafka Connectivity..." -ForegroundColor Cyan
try {
    $kafkaPod = kubectl get pod -l app=kafka -o jsonpath='{.items[0].metadata.name}'
    $result = kubectl exec $kafkaPod -- rpk cluster info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Kafka connectivity passed" -ForegroundColor Green
        $testsPassed++
    }
} catch {
    Write-Host "❌ Kafka connectivity failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 4: Database Connection
Write-Host "`n[Test 4/6] Database Connection..." -ForegroundColor Cyan
try {
    $backendPod = kubectl get pod -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}'
    $result = kubectl exec $backendPod -- python -c "from sqlmodel import create_engine; engine = create_engine('$env:DATABASE_URL'); engine.connect()" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database connection passed" -ForegroundColor Green
        $testsPassed++
    }
} catch {
    Write-Host "❌ Database connection failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 5: Dapr Status
Write-Host "`n[Test 5/6] Dapr Status..." -ForegroundColor Cyan
try {
    $daprStatus = C:\dapr\dapr.exe status -k 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dapr status check passed" -ForegroundColor Green
        $testsPassed++
    }
} catch {
    Write-Host "❌ Dapr status check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Test 6: All Pods Running
Write-Host "`n[Test 6/6] All Pods Running..." -ForegroundColor Cyan
try {
    $pods = kubectl get pods -o json | ConvertFrom-Json
    $runningPods = ($pods.items | Where-Object { $_.status.phase -eq "Running" }).Count
    $totalPods = $pods.items.Count
    
    if ($runningPods -eq $totalPods) {
        Write-Host "✅ All $totalPods pods running" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Only $runningPods/$totalPods pods running" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "❌ Pod status check failed: $_" -ForegroundColor Red
    $testsFailed++
}

# Summary
Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "📊 Smoke Test Results" -ForegroundColor Cyan
Write-Host "="*50 -ForegroundColor Cyan
Write-Host "✅ Passed: $testsPassed" -ForegroundColor Green
Write-Host "❌ Failed: $testsFailed" -ForegroundColor Red
Write-Host "Total: $($testsPassed + $testsFailed)" -ForegroundColor White

if ($testsFailed -eq 0) {
    Write-Host "`n🎉 All smoke tests passed! Production deployment successful!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n⚠️  Some tests failed. Please investigate before proceeding." -ForegroundColor Yellow
    exit 1
}
