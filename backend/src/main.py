from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .api.users import router as users_router
from .api.tasks import router as tasks_router
from .database.init_db import create_db_and_tables


app = FastAPI(
    title="Todo Web Application API",
    description="API for the Todo Web Application (Phase II)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])


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