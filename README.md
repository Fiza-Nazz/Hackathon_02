# AI-Native Todo Application
### Cloud-Native, Event-Driven Task Management System with AI Chatbot

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue.svg)](https://kubernetes.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Phases](#project-phases)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## 🎯 Overview

A production-grade, cloud-native todo application built with modern technologies and best practices. This project demonstrates the complete journey from a simple CLI application to a fully-featured, event-driven microservices architecture deployed on Kubernetes.

### Key Highlights
- ✅ **Multi-Phase Development**: Evolved from CLI → Web App → AI Chatbot → Kubernetes → Event-Driven
- ✅ **AI-Powered**: Natural language task management with OpenAI integration
- ✅ **Cloud-Native**: Containerized microservices with Kubernetes orchestration
- ✅ **Event-Driven**: Real-time updates using Kafka and WebSocket
- ✅ **Production-Ready**: Complete CI/CD, monitoring, and deployment automation

---

## 🏗 Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│              Responsive UI + Real-time Updates              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                  Backend Services Layer                      │
├──────────────────┬──────────────────┬──────────────────────┤
│  Backend API     │   AI Chatbot     │  WebSocket Service   │
│   (FastAPI)      │   (FastAPI)      │   (Real-time)        │
└────────┬─────────┴────────┬─────────┴──────────┬───────────┘
         │                  │                     │
         └──────────────────┼─────────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Kafka Event Bus     │
                │  (Event Streaming)    │
                └───────────┬───────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
┌────────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│  Notification   │ │  Recurring  │ │   Audit Log     │
│    Service      │ │Task Service │ │    Service      │
└─────────────────┘ └─────────────┘ └─────────────────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                ┌───────────▼───────────┐
                │  PostgreSQL Database  │
                │    (Neon Serverless)  │
                └───────────────────────┘
```

### Technology Layers
- **Presentation**: Next.js 15, React, TailwindCSS
- **API Gateway**: FastAPI with async support
- **Business Logic**: Python microservices
- **Messaging**: Apache Kafka (Redpanda)
- **Data**: PostgreSQL (Neon), Redis cache
- **Orchestration**: Kubernetes + Dapr
- **Monitoring**: Prometheus + Grafana

---

## ✨ Features

### Core Functionality
- 📝 **Task Management**: Create, read, update, delete tasks
- ✅ **Status Tracking**: Mark tasks as complete/incomplete
- 🏷️ **Tags & Categories**: Organize tasks with custom tags
- 🎯 **Priority Levels**: High, Medium, Low priority assignment
- 📅 **Due Dates**: Set deadlines with reminder notifications
- 🔄 **Recurring Tasks**: Automatic task recreation (daily, weekly, monthly)
- 🔍 **Advanced Search**: Full-text search with filters
- 📊 **Sorting & Filtering**: Multiple criteria support

### AI Chatbot Features
- 💬 **Natural Language**: Manage tasks using conversational AI
- 🌐 **Multi-language**: English and Roman Urdu support
- 🤖 **Smart Suggestions**: AI-powered task recommendations
- 📱 **MCP Integration**: 10+ specialized tools for task operations

### Advanced Features
- 🔔 **Real-time Updates**: WebSocket-based live notifications
- 📈 **Event Sourcing**: Complete audit trail of all operations
- 🔐 **Multi-user**: Secure authentication with data isolation
- 📊 **Analytics**: Task completion metrics and insights
- 🌍 **Cloud-Native**: Scalable microservices architecture

---

## 🛠 Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19
- **Styling**: TailwindCSS
- **State Management**: React Context + Hooks
- **Authentication**: Better Auth with JWT
- **Real-time**: WebSocket client

### Backend
- **API Framework**: FastAPI 0.115+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Caching**: Redis
- **Task Queue**: Celery (optional)
- **AI Integration**: OpenAI GPT-4

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (Minikube/OKE)
- **Service Mesh**: Dapr
- **Message Broker**: Apache Kafka (Redpanda)
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions

### Development Tools
- **Package Manager**: uv (Python), pnpm (Node.js)
- **Code Quality**: Ruff, ESLint, Prettier
- **Testing**: Pytest, Jest
- **Documentation**: Markdown, OpenAPI

---

## 📚 Project Phases

### Phase I: CLI Application ✅
**Status**: Complete | **Duration**: Week 1

Simple in-memory todo application with console interface.

**Features**:
- Basic CRUD operations
- In-memory storage
- Menu-driven interface
- Python 3.13+ with uv

**Tech Stack**: Python, uv, SQLModel

📁 **Code**: `src/cli/`
📄 **Spec**: `specs/001-todo-app/spec.md`

---

### Phase II: Web Application ✅
**Status**: Complete | **Duration**: Week 2

Full-stack web application with authentication and database.

**Features**:
- User registration & authentication
- Multi-user support with data isolation
- Responsive web interface
- PostgreSQL database
- RESTful API

**Tech Stack**: Next.js, FastAPI, PostgreSQL, Better Auth

📁 **Code**: `frontend/`, `backend/`
📄 **Spec**: `specs/002-web-app/spec.md`

---

### Phase III: AI Chatbot ✅
**Status**: Complete | **Duration**: Week 3

AI-powered chatbot for natural language task management.

**Features**:
- OpenAI GPT-4 integration
- MCP (Model Context Protocol) tools
- Conversation history
- Roman Urdu support
- 10+ specialized task operations

**Tech Stack**: FastAPI, OpenAI API, MCP, LangChain

📁 **Code**: `Chatbot/`
📄 **Docs**: `Chatbot/README.md`

---

### Phase IV: Kubernetes Deployment ✅
**Status**: Complete | **Duration**: Week 4

Cloud-native deployment with container orchestration.

**Features**:
- Docker containerization
- Kubernetes deployment (Minikube)
- Helm charts
- Ingress configuration
- Multi-replica scaling
- Health checks & monitoring

**Tech Stack**: Docker, Kubernetes, Helm, Minikube

📁 **Code**: `charts/`, `k8s/`
📄 **Spec**: `specs/phase4_deployment_spec.md`

---

### Phase V: Event-Driven Architecture 🚧
**Status**: In Progress | **Duration**: Week 5

Production-grade event-driven microservices architecture.

**Implemented Features** ✅:
- Advanced task features (priorities, tags, due dates, recurring)
- Event schemas and publishers
- Kafka integration
- Microservices (Notification, Recurring Tasks)
- WebSocket real-time updates
- Dapr runtime integration
- Complete deployment automation

**In Progress** 🚧:
- Oracle Cloud OKE deployment
- Production monitoring setup
- CI/CD pipeline testing

**Tech Stack**: Kafka, Dapr, Prometheus, Grafana, Oracle Cloud

📁 **Code**: `services/`, `k8s/monitoring/`
📄 **Spec**: `specs/phase5_specification.md`
📄 **Guide**: `PHASE5_DEPLOYMENT_GUIDE.md`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js 20+
- Docker Desktop
- uv (Python package manager)
- pnpm (Node.js package manager)

### Quick Start

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/todo-chatbot.git
cd todo-chatbot
```

#### 2. Setup Backend
```bash
cd backend
uv sync
cp .env.example .env
# Edit .env with your database URL
uv run python -m src.main
```

#### 3. Setup Frontend
```bash
cd frontend
pnpm install
cp .env.example .env.local
# Edit .env.local with API URL
pnpm dev
```

#### 4. Setup Chatbot
```bash
cd Chatbot
uv sync
cp .env.example .env
# Add OpenAI API key
uv run python backend/main.py
```

### Access Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Chatbot**: http://localhost:8001

---

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services
```bash
# Backend
docker build -t todo-backend ./backend
docker run -p 8000:8000 todo-backend

# Frontend
docker build -t todo-frontend ./frontend
docker run -p 3000:3000 todo-frontend

# Chatbot
docker build -t todo-chatbot ./Chatbot
docker run -p 8001:8001 todo-chatbot
```

---

## ☸️ Kubernetes Deployment

### Local Deployment (Minikube)

#### Phase 4: Basic Kubernetes
```bash
# Start Minikube
minikube start --memory=4096 --cpus=2

# Deploy using Helm
helm install todo-chatbot ./charts/todo-chatbot

# Access application
minikube tunnel
# Visit: http://todo.local
```

#### Phase 5: Event-Driven Architecture
```bash
# Quick deployment
.\scripts\deploy-phase5-simple.ps1

# Or step-by-step
.\scripts\install-dapr.ps1
.\scripts\deploy-phase5.ps1
.\scripts\setup-monitoring.ps1
```

### Production Deployment (Oracle Cloud)
```bash
# Configure OCI CLI
oci setup config

# Deploy to OKE
.\scripts\deploy-oracle-simple.ps1 `
  -CompartmentId "ocid1.compartment..." `
  -ClusterId "ocid1.cluster..." `
  -Region "us-ashburn-1"
```

📄 **Full Guide**: `docs/PRODUCTION_DEPLOYMENT_GUIDE.md`

---

## 📊 Monitoring

### Access Monitoring Tools
```bash
# Prometheus
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Visit: http://localhost:9090

# Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000
# Visit: http://localhost:3000
# Login: admin / admin123
```

### Key Metrics
- API response time (p95)
- Request rate
- Error rate
- Kafka event throughput
- Active WebSocket connections
- Pod CPU/Memory usage

---

## 📖 Documentation

### Project Documentation
- [Phase 1 Spec](specs/001-todo-app/spec.md) - CLI Application
- [Phase 2 Spec](specs/002-web-app/spec.md) - Web Application
- [Phase 3 README](Chatbot/README.md) - AI Chatbot
- [Phase 4 Spec](specs/phase4_deployment_spec.md) - Kubernetes
- [Phase 5 Spec](specs/phase5_specification.md) - Event-Driven

### Deployment Guides
- [Phase 5 Deployment](PHASE5_DEPLOYMENT_GUIDE.md)
- [Oracle Cloud Deployment](docs/ORACLE_CLOUD_DEPLOYMENT.md)
- [Production Guide](docs/PRODUCTION_DEPLOYMENT_GUIDE.md)

### API Documentation
- Backend API: http://localhost:8000/docs
- Chatbot API: http://localhost:8001/docs

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
pnpm test
```

### Integration Tests
```bash
# Run smoke tests
.\scripts\run-smoke-tests.ps1
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/TypeScript
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - Initial work and architecture

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Neon for serverless PostgreSQL
- Vercel for Next.js framework
- FastAPI team for the amazing framework
- Kubernetes and CNCF community

---

## 📞 Support

For support, email your-email@example.com or open an issue in the repository.

---

## 🗺 Roadmap

### Completed ✅
- [x] Phase I: CLI Application
- [x] Phase II: Web Application
- [x] Phase III: AI Chatbot
- [x] Phase IV: Kubernetes Deployment
- [x] Phase V: Event-Driven Architecture (Core)

### In Progress 🚧
- [ ] Phase V: Production Deployment
- [ ] Phase V: Complete Monitoring Setup

### Planned 📋
- [ ] Mobile application (React Native)
- [ ] Desktop application (Electron)
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Third-party integrations (Slack, Teams)

---

**Built with ❤️ using modern cloud-native technologies**
