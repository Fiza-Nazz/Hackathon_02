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
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

# Get database URL from environment variable, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

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