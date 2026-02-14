"""
Database connection and engine configuration.

This module provides the database engine for SQLModel.
"""

from sqlmodel import create_engine, SQLModel
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Database URL from environment variable
# Professional Fallback to ensure same NEON DB as Backend/Frontend
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Create database engine with pooling options for stability
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300
)


def get_engine():
    """Get the database engine."""
    return engine


def init_db():
    """Initialize database tables and seed default data."""
    from backend.models.user import User, Account
    from backend.models.task import Task
    from backend.models.conversation import Conversation
    from backend.models.message import Message
    from sqlmodel import Session, select

    # Create tables
    SQLModel.metadata.create_all(engine)

    # Seed default user if none exists (for development/demo)
    with Session(engine) as session:
        # Check for user '1' as a string
        statement = select(User).where(User.id == "1")
        results = session.exec(statement)
        user = results.first()

        if not user:
            print("Seeding default demo user...")
            demo_user = User(
                id="1",
                email="demo@example.com",
                emailVerified=True,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )
            session.add(demo_user)
            session.commit()
            print("Default user created (ID: '1')")
