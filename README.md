---
title: AI Native Todo Backend
emoji: 🚀
colorFrom: blue
colorTo: pink
sdk: docker
pinned: false
app_port: 7860
---

# AI-Native Todo Application

A professional-grade, full-stack task management ecosystem that evolves from a developer-focused CLI to a high-performance, immersive web application. Built with a robust **FastAPI** backend and a modern **Next.js** frontend, this project demonstrates spec-driven development and modern architectural patterns.

---

## 🚀 Key Interfaces

### 1. Full-Stack Web Application (Phase II)
A visually stunning and responsive web interface designed for a premium user experience.
- **Frontend Stack:** Next.js 14, TypeScript, Tailwind CSS, Zustand for state management.
- **Advanced UI/UX:** Features complex 3D models, smooth transitions, and a clean, modern aesthetic.
- **Secure Authentication:** JWT-based user registration and login to ensure personal data isolation.
- **Persistence:** Integrates with PostgreSQL/SQLite via SQLModel for reliable data storage.

### 2. Efficiency-First CLI Tool (Phase I)
A powerful command-line interface for managing tasks directly from your terminal.
- **CLI Stack:** Python, `todo_app.py` logic.
- **Speed:** Quick commands to create, list, update, and delete tasks.
- **Developer-Centric:** Designed for high efficiency without leaving the terminal environment.

---

## 🛠️ Technical Architecture

### Backend (The Core)
Powered by **FastAPI**, the backend handles all business logic, authentication, and data persistence.
- **ORM:** SQLModel (merging the power of SQLAlchemy and Pydantic).
- **Migrations:** Includes automated migration scripts (`migrate_db.py`) to manage schema changes like task priorities and categories.
- **API Documentation:** Automatically generated interactive docs available at `/docs`.

### Frontend (The Experience)
A modular **Next.js** application that prioritizes performance and user engagement.
- **Responsiveness:** Fully optimized for both desktop and mobile devices.
- **Integration:** Seamless communication with the FastAPI backend using Axios.

---

## 📦 Project Structure & Specs

The project follows a **Spec-Driven Development** approach. All technical requirements and phase definitions are documented in the `specs/` directory:
- `specs/001-todo-app/`: Phase I (CLI and core logic) specifications.
- `specs/002-web-app/`: Phase II (Full-stack web app) specifications and API contracts.

---

## ⚙️ Setup & Installation

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- PostgreSQL (or SQLite for local development)

### 1. Backend Setup
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. Configure `.env` with your `DATABASE_URL`.
6. `uvicorn src.main:app --reload`

### 2. Frontend Setup
1. `cd frontend`
2. `npm install`
3. `npm run dev` (Access at `http://localhost:3000`)

### 3. CLI Usage
1. From the root directory:
2. `python -m src.cli.todo_app --help` to see available commands.

---

## 🎨 Design Philosophy
This application is built to bridge the gap between functionality and aesthetics. By combining a reliable API with a high-end web interface and a fast CLI, it provides the ultimate workspace for modern users.