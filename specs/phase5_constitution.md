# PHASE V CONSTITUTION
## Advanced Cloud Deployment - Core Principles

### 🎯 PROJECT MISSION
Transform Phase IV Todo Chatbot into production-grade, event-driven, cloud-native system using Kafka + Dapr on Oracle Cloud.

---

## 📋 CORE PRINCIPLES

### 1. **Event-Driven Architecture First**
- All inter-service communication via Kafka events
- No direct service-to-service API calls
- Async processing for all non-critical operations
- Event sourcing for audit trails

### 2. **Cloud-Native Patterns**
- Dapr for all infrastructure abstractions
- Kubernetes-native deployments
- 12-factor app compliance
- Stateless services with external state stores

### 3. **Production Quality Standards**
- Zero downtime deployments
- Health checks for all services
- Proper error handling and retries
- Comprehensive logging and monitoring

### 4. **Security First**
- All secrets via Dapr secret stores
- mTLS between services via Dapr
- No hardcoded credentials
- Principle of least privilege

---

## 🛠️ TECHNICAL CONSTRAINTS

### **Technology Stack (Non-Negotiable)**
- **Messaging**: Kafka (Redpanda Cloud)
- **Runtime**: Dapr sidecars
- **Orchestration**: Kubernetes (Minikube → Oracle OKE)
- **Frontend**: Next.js (existing)
- **Backend**: FastAPI (existing)
- **Chatbot**: FastAPI + Groq AI (existing)
- **Database**: Neon PostgreSQL (existing)

### **Development Approach**
- **Agentic Dev Stack**: Specify → Plan → Tasks → Implement
- **No Manual Coding**: All code via Claude Code
- **E: Drive Only**: No C: drive operations
- **Step-by-Step**: Complete verification at each stage

### **Architecture Patterns**
- **Microservices**: Each service has single responsibility
- **Event Sourcing**: All state changes as events
- **CQRS**: Separate read/write models where beneficial
- **Saga Pattern**: Distributed transactions via events

---

## 🏗️ SERVICE BOUNDARIES

### **Core Services (Existing)**
1. **Frontend Service** - User interface (Next.js)
2. **Backend Service** - Task CRUD operations (FastAPI)
3. **Chatbot Service** - AI interactions (FastAPI + Groq)

### **New Services (Phase V)**
4. **Notification Service** - Handles reminders and alerts
5. **Recurring Task Service** - Manages recurring task creation
6. **WebSocket Service** - Real-time client updates
7. **Audit Service** - Activity logging and compliance

### **Infrastructure Services**
- **Kafka Cluster** - Event streaming platform
- **Dapr Runtime** - Service mesh and abstractions
- **PostgreSQL** - Primary data store (Neon)
- **Redis** - Caching and session store (via Dapr)

---

## 📊 EVENT SCHEMA STANDARDS

### **Event Structure (Required)**
```json
{
  "event_id": "uuid",
  "event_type": "task.created|task.updated|task.completed|task.deleted",
  "aggregate_id": "task_id",
  "user_id": "string",
  "timestamp": "ISO8601",
  "version": "integer",
  "data": {
    // Event-specific payload
  },
  "metadata": {
    "source": "service_name",
    "correlation_id": "uuid"
  }
}
```

### **Kafka Topics**
- `task-events` - All task lifecycle events
- `reminders` - Due date and notification events
- `task-updates` - Real-time UI sync events
- `audit-log` - Compliance and activity tracking

---

## 🔧 DAPR COMPONENT STANDARDS

### **Required Components**
1. **Pub/Sub** - Kafka abstraction for messaging
2. **State Store** - PostgreSQL for conversation state
3. **Secret Store** - Kubernetes secrets for credentials
4. **Jobs API** - Scheduled reminders and recurring tasks
5. **Service Invocation** - Inter-service communication

### **Configuration Principles**
- All components defined as Kubernetes CRDs
- Environment-specific configurations (dev/prod)
- No hardcoded connection strings
- Graceful degradation when components unavailable

---

## 🚀 DEPLOYMENT STANDARDS

### **Local Development (Minikube)**
- Full stack deployment with Dapr
- Local Kafka cluster (Redpanda)
- Hot reload for development
- Complete feature parity with production

### **Production (Oracle Cloud OKE)**
- Multi-zone deployment for HA
- Managed Kafka (Redpanda Cloud)
- Horizontal pod autoscaling
- Blue-green deployment strategy

### **CI/CD Requirements**
- Automated testing on every commit
- Security scanning for all images
- Automated deployment to staging
- Manual approval for production

---

## 📈 PERFORMANCE REQUIREMENTS

### **Response Times**
- API responses: < 200ms (95th percentile)
- Event processing: < 1 second
- Real-time updates: < 100ms
- Search operations: < 500ms

### **Scalability**
- Support 1000+ concurrent users
- Handle 10,000+ events per minute
- Auto-scale based on CPU/memory
- Graceful degradation under load

---

## 🔍 MONITORING & OBSERVABILITY

### **Required Metrics**
- Request latency and throughput
- Event processing lag
- Error rates and types
- Resource utilization

### **Logging Standards**
- Structured JSON logs
- Correlation IDs for tracing
- Appropriate log levels
- No sensitive data in logs

---

## ✅ QUALITY GATES

### **Before Each Step**
- All tests passing
- No security vulnerabilities
- Performance benchmarks met
- Documentation updated

### **Before Production**
- Load testing completed
- Disaster recovery tested
- Monitoring alerts configured
- Runbook documentation complete

---

**This constitution governs all Phase V development decisions and implementations.**