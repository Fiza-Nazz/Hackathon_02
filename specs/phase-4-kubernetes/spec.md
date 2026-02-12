# Specification: Phase 4 - Local Kubernetes Deployment

## 1. Objective
Deploy the Cloud-Native Todo Chatbot application on a local Kubernetes cluster using Minikube and Helm Charts, leveraging AI-assisted DevOps tools (Gordon, kubectl-ai, Kagent).

## 2. Requirements Reference
- **Containerization:** Frontend, Backend, and Chatbot services.
- **Orchestration:** Kubernetes (Minikube).
- **Package Management:** Helm Charts.
- **AI Ops Tools:**
    - `docker ai` (Gordon) for container operations.
    - `kubectl-ai` for K8s manifest generation and deployment.
    - `kagent` for cluster health and optimization.

## 3. Component Architecture
The application consists of three main services:

### 3.1. Frontend Service
- **Source:** `/frontend`
- **Technology:** Next.js
- **Responsibility:** User interface and authentication logic.
- **Port:** 3000

### 3.2. Backend Service
- **Source:** `/backend`
- **Technology:** FastAPI (Python)
- **Responsibility:** Core API, Task management, and Chat integration.
- **Port:** 8000

### 3.3. Chatbot Service
- **Source:** `/Chatbot`
- **Technology:** FastAPI (Python)
- **Responsibility:** MCP Foundation and specialized AI logic.
- **Port:** 8001 (Assumed, as backend uses 8000)

### 3.4. Database
- **Source:** External (Neon PostgreSQL) via `DATABASE_URL`.
- **Note:** In K8s, we will use a Secret to manage the connection string.

## 4. Containerization Strategy
- Each service will have its own `Dockerfile`.
- We will use multi-stage builds for Frontend (Next.js) to reduce image size.
- Backend and Chatbot will use Python 3.11 optimized images.
- Images will be pushed to a local registry or loaded directly into Minikube.

## 5. Kubernetes Resources (Helm Chart)
A unified Helm Chart (`todo-chatbot`) will manage the following resources:
- **Deployments:** Three deployments (frontend, backend, chatbot).
- **Services:** Three ClusterIP services.
- **Ingress:** A single Ingress to expose the Frontend and Backend API.
- **Secrets/ConfigMaps:** For environment variables (`OPENAI_API_KEY`, `DATABASE_URL`, etc.).

## 6. Success Criteria
- [ ] All 3 services containerized successfully.
- [ ] Minikube cluster running locally.
- [ ] Application accessible via a local URL (e.g., `todo.local`).
- [ ] Pods scaled to 2 replicas (using `kubectl-ai` prompt).
- [ ] Cluster health verified by `kagent`.

## 7. Constraints
- Must use Minikube for local development.
- No manual K8s YAML writing where AI tools can be used.
- Adhere to the Spec-Driven Development (SDD) workflow.
