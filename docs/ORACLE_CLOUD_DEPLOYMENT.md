# Oracle Cloud Deployment Guide
## Deploy Phase 5 to Oracle Cloud OKE (Oracle Kubernetes Engine)

---

## 🎯 Overview
This guide will deploy your Phase 5 Todo Chatbot to Oracle Cloud Infrastructure (OCI) using OKE.

---

## 📋 Prerequisites

### 1. Oracle Cloud Account
- Sign up: https://www.oracle.com/cloud/free/
- Free tier includes: 2 VMs, 200GB storage, Always Free resources

### 2. Install OCI CLI
```powershell
# Download and install OCI CLI
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.ps1'))"

# Verify installation
oci --version
```

### 3. Configure OCI CLI
```powershell
# Setup OCI configuration
oci setup config

# You'll need:
# - User OCID
# - Tenancy OCID
# - Region (e.g., us-ashburn-1)
# - API Key (will be generated)
```

---

## 🚀 Deployment Steps

### Step 1: Create OKE Cluster

```powershell
# Create VCN (Virtual Cloud Network)
oci network vcn create `
  --compartment-id <YOUR_COMPARTMENT_OCID> `
  --display-name todo-chatbot-vcn `
  --cidr-block 10.0.0.0/16

# Create OKE Cluster (Free Tier Compatible)
oci ce cluster create `
  --compartment-id <YOUR_COMPARTMENT_OCID> `
  --name todo-chatbot-cluster `
  --vcn-id <VCN_OCID> `
  --kubernetes-version v1.28.2 `
  --service-lb-subnet-ids '["<SUBNET_OCID>"]'

# Wait for cluster to be active (5-10 minutes)
oci ce cluster get --cluster-id <CLUSTER_OCID>
```

### Step 2: Configure kubectl for OKE
```powershell
# Get kubeconfig
oci ce cluster create-kubeconfig `
  --cluster-id <CLUSTER_OCID> `
  --file $HOME\.kube\config-oke `
  --region us-ashburn-1

# Set kubectl context
$env:KUBECONFIG="$HOME\.kube\config-oke"
kubectl get nodes
```

### Step 3: Create Container Registry
```powershell
# Create OCIR repository
oci artifacts container repository create `
  --compartment-id <YOUR_COMPARTMENT_OCID> `
  --display-name todo-chatbot/backend

oci artifacts container repository create `
  --compartment-id <YOUR_COMPARTMENT_OCID> `
  --display-name todo-chatbot/frontend

oci artifacts container repository create `
  --compartment-id <YOUR_COMPARTMENT_OCID> `
  --display-name todo-chatbot/chatbot
```
