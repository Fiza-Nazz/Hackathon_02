# Zenith-Flow: The AI-Native Hybrid Workspace

Zenith-Flow is a professional-grade, full-stack task management ecosystem that bridges the gap between high-end web aesthetics and developer-centric CLI efficiency. Built with a robust **FastAPI** backend, it offers two powerful interfaces to manage your productivity.

---

## 🚀 Dual Interface Architecture

### 1. Modern Web Application (The "Experience" Layer)
A stunning, responsive web interface designed for users who value visual excellence and interactivity.
- **3D Immersive UI:** Featuring interactive 3D models and smooth CSS/Framer Motion animations.
- **Glassmorphism Design:** A premium, modern aesthetic with vibrant gradients and blur effects.
- **Real-time Updates:** Reactive state management using Zustand and Axios.
- **Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, Three.js.

### 2. Powerful CLI Companion (The "Efficiency" Layer)
A developer-first command-line tool for lightning-fast task management directly from the terminal.
- **Terminal Efficiency:** Quick commands to add, list, and complete tasks without leaving your workflow.
- **Secure Integration:** Connects seamlessly to the same FastAPI backend using secure tokens.
- **Clean Output:** Formatted terminal logs and intuitive command structures.
- **Tech Stack:** Python, Typer/Click, Rich (for beautiful terminal formatting).

---

## 🛠️ Tech Stack & Features
- **Backend:** FastAPI (Python), SQLModel (PostgreSQL/SQLite), JWT Authentication.
- **Security:** Bcrypt password hashing and secure token-based access.
- **Data Integrity:** Fully validated API schemas and relational database design.
- **Cross-Platform:** Access your tasks via browser or terminal, perfectly synced.

---

## 📦 Setup & Installation

### Backend & API
1. `cd backend`
2. `pip install -r requirements.txt`
3. Configure `.env` with your `DATABASE_URL`
4. `uvicorn src.main:app --reload`

### Web Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev` (Access at `http://localhost:3000`)

### CLI Tool
1. Navigate to the root directory.
2. Ensure Python environment is active.
3. Run `python -m src.cli.todo_app --help` to explore commands.

---

## 🛡️ Security & Best Practices
- **JWT Authentication:** Secure user sessions across both interfaces.
- **Environment Safety:** Strictly enforced `.gitignore` to prevent leaking secrets.
- **Input Validation:** Pydantic-powered schemas ensure data consistency.

---

## 🎨 Design Philosophy
Zenith-Flow isn't just a todo app; it's a statement. We believe that professional tools should not only work perfectly but also look extraordinary. Every transition, 3D model, and command is crafted to provide a premium user experience.