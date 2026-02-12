# Architectural Plan: Phase 4 - Local Kubernetes Deployment

## 1. Component Strategy

### 1.1. Frontend (Next.js)
- **Dockerfile:** Multi-stage build (build stage + runner stage).
- **Base Image:** `node:18-alpine`.
- **Port:** 3000.
- **Environment:** `NEXT_PUBLIC_API_URL` (points to Backend Service in K8s).

### 1.2. Backend (FastAPI)
- **Dockerfile:** Lean Python image with requirements installed.
- **Base Image:** `python:3.11-slim`.
- **Port:** 8000.
- **Environment:** `DATABASE_URL`, `OPENAI_API_KEY`.

### 1.3. Chatbot (FastAPI/Standalone)
- **Dockerfile:** Similar to Backend.
- **Base Image:** `python:3.11-slim`.
- **Port:** 8001.
- **Environment:** Dedicated tools or config if separate from main backend.

## 2. Infrastructure (Local K8s)

### 2.1. Minikube
- **Driver:** Docker Desktop (standard).
- **Ingress Controller:** Enabled via `minikube addons enable ingress`.
- **Local IP:** Mapping `todo.local` to Minikube IP in `/etc/hosts` (manually or via helper).

### 2.2. Helm Chart Structure
- `charts/todo-chatbot/`
    - `templates/`
        - `frontend-deploy.yaml`
        - `backend-deploy.yaml`
        - `chatbot-deploy.yaml`
        - `service-frontend.yaml`
        - `service-backend.yaml`
        - `service-chatbot.yaml`
        - `ingress.yaml`
        - `secrets.yaml`
    - `values.yaml`
    - `Chart.yaml`

## 3. Data & Secrets
- **Secrets:** We will create a `K8s Secret` to store sensitive data like `DATABASE_URL` and `OPENAI_API_KEY`.
- **ConfigMaps:** For non-sensitive configs like `LOG_LEVEL` or service URLs.

## 4. AI-Assisted Tasks
- **Gordon (Docker AI):** We will prompt Gordon style logic to generate the Dockerfiles.
- **kubectl-ai:** We will use it to generate the initial YAML templates for the Helm charts.
- **kagent:** After deployment, we will run analysis to ensure memory limits and CPU requests are optimized.

## 5. Deployment Workflow
1. Build images for Frontend, Backend, and Chatbot.
2. Push/Load images to Minikube.
3. Initialize Helm Chart.
4. Deploy using `helm upgrade --install`.
5. Verify with `kubectl get pods`.
6. Test UI accessibility.

## 6. Risks & Mitigations
- **Image Size:** Use alpine/slim images.
- **Connectivity:** Ensure Ingress paths correctly route to `/api` for backend and `/` for frontend.
- **Resource Constraints:** Minikube might run out of memory; we will set reasonable resource limits.

## 7. ADR Suggestions
📋 Architectural decision detected: Local Helm Chart vs Standard YAML.
Rationale: Helm allows better parameterization and multi-service management.
Document? Run `/sp.adr "Unified Helm Deployment Strategy"`.
