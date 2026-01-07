# AI-Native Todo Application (Phase II - Full-Stack Web Application)

## Overview
This is a full-stack web application built with Next.js (frontend) and FastAPI (backend) that allows users to manage their tasks with secure authentication.

## Features
- User registration and authentication
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Responsive web interface
- JWT-based authentication
- PostgreSQL database

## Tech Stack
- **Frontend**: Next.js, TypeScript, Tailwind CSS, Zustand
- **Backend**: FastAPI, SQLModel, PostgreSQL, JWT
- **Authentication**: JWT tokens with bcrypt password hashing
- **State Management**: Zustand
- **HTTP Client**: Axios

## Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- PostgreSQL database
- pip (Python package manager)

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend/
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-super-secret-key-change-in-production
```

6. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend/
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the frontend development server:
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user
- `POST /api/auth/logout` - Logout a user

### Users
- `GET /api/users/me` - Get current user info

### Tasks
- `GET /api/tasks/` - Get all tasks for current user
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion status

## Running the Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Open your browser and navigate to `http://localhost:3000`
4. Register a new account or login with an existing account
5. Start managing your tasks!

## Development
- Backend: FastAPI with automatic API documentation at `/docs`
- Frontend: Next.js with hot reloading
- Database: SQLModel with PostgreSQL

## Security
- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Input validation on both frontend and backend
- SQL injection protection via SQLModel

## Database Models
- User: id, email, password_hash, created_at, updated_at
- Task: id, title, description, completed, user_id, created_at, updated_at