from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager

from dotenv import load_dotenv

from dotenv import load_dotenv
from pathlib import Path

# File is at: E:\Hackathon_02\backend\src\database\database.py
# We want: E:\Hackathon_02\backend\.env
# Solution: Go up 3 levels to reach 'backend'
# Professional Database Connection for TODOAI Engine
# Ensure both Frontend (Next.js/Better-Auth) and Backend (FastAPI) use the same NEON cloud instance
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Create the database engine
# Use connect_args={"check_same_thread": False} for SQLite to allow multiple threads
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    # For PostgreSQL, use pooling options to handle connection timeouts from serverless dbs like Neon
    engine = create_engine(
        DATABASE_URL, 
        echo=True,
        pool_pre_ping=True,
        pool_recycle=300
    )


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()