# Quickstart Guide: AI-Native Todo Application Phase II

## Phase II: Full-Stack Web Application

### Prerequisites
- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL (or Neon PostgreSQL account)
- npm or yarn package manager

### Setup

#### Backend Setup
1. Navigate to the backend directory
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi sqlmodel uvicorn python-multipart
   ```
4. Set up environment variables:
   ```bash
   # Create .env file with database connection details
   DATABASE_URL="postgresql://user:password@localhost/dbname"
   SECRET_KEY="your-secret-key"
   ```
5. Initialize the database:
   ```bash
   python -m backend.database.init_db
   ```
6. Run the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

#### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```
3. Set up environment variables:
   ```bash
   # Create .env.local file
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   ```
4. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Running the Application
1. Start the backend server first (typically on port 8000)
2. Start the frontend server (typically on port 3000)
3. Open your browser to http://localhost:3000

### Basic Usage
1. Register a new account using the registration form
2. Verify your email if required
3. Log in to access your personal dashboard
4. Create tasks using the "Add Task" button
5. View, update, delete, or mark tasks complete from the dashboard
6. Log out when finished

### Data Storage
- All data is stored in Neon PostgreSQL database
- Data persists across application restarts
- Multi-user data isolation ensures users only see their own tasks

### API Endpoints
- Authentication: `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
- Users: `/api/users/me` (get current user)
- Tasks: `/api/tasks/` (CRUD operations for user's tasks)