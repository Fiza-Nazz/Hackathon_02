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
from .api.tags import router as tags_router
from .api.reminders import router as reminders_router
from .api.websocket import router as websocket_router
from .database.init_db import create_db_and_tables
from .events.publisher import get_publisher, shutdown_publisher
from .events.event_bus import init_event_handlers, publish_task_event, TaskEvents


app = FastAPI(
    title="Todo Web Application API",
    description="API for the Todo Web Application (Phase II)",
    version="2.1.0-ULTRA"
)

print("SYSTEM BOOT: Neural Backend Version 2.1.0-ULTRA starting...")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-eight-gilt-98.vercel.app",
        "https://frontend-fiza-qureshis-projects.vercel.app",
        "https://todo-ai-professional-fiza.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://todo.local",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .api.auth import router as auth_router
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chatbot_router, prefix="/api/chat", tags=["chatbot"])
app.include_router(tags_router, prefix="/api/tags", tags=["tags"])
app.include_router(reminders_router, prefix="/api/reminders", tags=["reminders"])
app.include_router(websocket_router, tags=["websocket"])


@app.on_event("startup")
async def on_startup():
    """
    Create database tables and initialize event publisher on startup.
    """
    create_db_and_tables()
    
    # Initialize event publisher (will start when first used)
    try:
        await get_publisher()
        print("✅ Event publisher initialized")
    except Exception as e:
        print(f"⚠️ Event publisher initialization failed: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    """
    Cleanup resources on shutdown.
    """
    await shutdown_publisher()
    print("✅ Event publisher shutdown complete")


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