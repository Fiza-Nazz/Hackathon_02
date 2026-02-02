from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
loaded = load_dotenv(env_path)
print(f"DEBUG: Environment loading from {env_path}: {'SUCCESS' if loaded else 'FAILED'}")
if not loaded:
    print(f"DEBUG: Attempting fallback to project root .env")
    load_dotenv(BASE_DIR.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .api.auth import router as auth_router
# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
from .api.users import router as users_router
from .api.tasks import router as tasks_router
from .api.chatbot import router as chatbot_router
from .database.init_db import create_db_and_tables


app = FastAPI(
    title="Todo Web Application API",
    description="API for the Todo Web Application (Phase II)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-eight-gilt-98.vercel.app",
        "https://frontend-fiza-qureshis-projects.vercel.app",
        "https://todo-ai-professional-fiza.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chatbot_router, prefix="/api/chat", tags=["chatbot"])


@app.on_event("startup")
def on_startup():
    """
    Create database tables on startup.
    """
    create_db_and_tables()


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Todo Web Application API"}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}