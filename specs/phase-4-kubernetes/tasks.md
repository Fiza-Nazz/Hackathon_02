# Tasks: Phase 4 - Local Kubernetes Deployment

## Phase 4.1: Preparation & Containerization

- [x] **Task 4.1.1: Create Frontend Dockerfile**
    - **Description:** Write a multi-stage Dockerfile for the Next.js frontend.
    - **Acceptance:** `docker build` succeeds and image runs locally on port 3000.
    - **Tool:** Gordon style logic.
- [x] **Task 4.1.2: Create Backend Dockerfile**
    - **Description:** Write a Dockerfile for the FastAPI backend.
    - **Acceptance:** Image builds and FastAPI server starts on port 8000.
    - **Tool:** Gordon style logic.
- [x] **Task 4.1.3: Create Chatbot Dockerfile**
    - **Description:** Write a Dockerfile for the Chatbot foundation folder.
    - **Acceptance:** Image builds and standalone chatbot logic is accessible.
- [ ] **Task 4.1.4: Push Images to Minikube**
    - **Description:** Use `minikube image load` to make images available to the cluster.

## Phase 4.2: Helm Infrastructure

- [x] **Task 4.2.1: Initialize Helm Chart**
    - **Description:** Create the basic structure of the `todo-chatbot` chart.
- [x] **Task 4.2.2: Generate Deployment YAMLs**
    - **Description:** Use `kubectl-ai` logic to generate deployment manifests for the 3 services.
- [x] **Task 4.2.3: Config & Secrets Setup**
    - **Description:** Create templates for K8s Secrets and ConfigMaps.
- [x] **Task 4.2.4: Ingress Configuration**
    - **Description:** Define Ingress rules to route traffic to frontend and backend.

## Phase 4.3: Deployment & Validation

- [ ] **Task 4.3.1: Deploy to Minikube**
    - **Description:** Run `helm install` and verify pod statuses.
- [ ] **Task 4.3.2: Scaling Verification**
    - **Description:** Use `kubectl-ai` to scale backend to 2 replicas and verify.
- [ ] **Task 4.3.3: Cluster Health Check**
    - **Description:** Use `kagent` to analyze health and optimize resource allocation.
- [ ] **Task 4.3.4: Final End-to-End Test**
    - **Description:** Access the app via browser and confirm Chatbot functionality.
