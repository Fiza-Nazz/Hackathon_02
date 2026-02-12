# Specification: Phase IV Local Kubernetes Deployment

## 1. Goal
Deploy the Cloud-Native Todo Chatbot onto a local Kubernetes cluster (Minikube) using Helm charts and demonstrate AI-assisted DevOps operations.

## 2. Infrastructure Requirements
- **Hypervisor/Driver**: Docker (Docker Desktop)
- **Local Cluster**: Minikube (Profile: `minikube`)
- **Storage**: All data must reside on `E:\minikube` and project files on `E:\Hackathon_02`.
- **Addons**: Ingress controller enabled.

## 3. Application Components
- **Frontend**: Next.js application (todo-frontend)
- **Backend**: Python FastAPI (todo-backend)
- **Chatbot**: Python-based AI agent foundation (todo-chatbot-foundation)
- **Database**: External PostgreSQL (Neon DB, already configured in secrets).

## 4. Deployment Strategy
- **Containerization**: 
  - Build lightweight images using `python:3.11-slim` and `node:18-alpine`.
  - Build images directly into the Minikube Docker daemon (`minikube docker-env`).
- **Orchestration**: 
  - Use Helm charts located in `charts/todo-chatbot/`.
  - Configure Ingress for `todo.local`.
  - Set `imagePullPolicy: Never` for local images.

## 5. AI DevOps Tools
- **kubectl-ai**: For natural language Kubernetes management.
- **Gordon (Docker AI)**: Assist in container operations.
- **k8sgpt**: For cluster health analysis.

## 6. Deliverables
- Fully functional application accessible via `http://todo.local`.
- Helm release `todo-chatbot` successfully deployed.
- Demonstration of scaling and AI-assisted troubleshooting.
