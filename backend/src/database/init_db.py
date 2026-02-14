from sqlmodel import SQLModel
from .database import engine
from ..models import User, Task


def create_db_and_tables():
    """
    Create database tables for User and Task models.
    """
    print("RE-INITIALIZING TABLES: Starting metadata sync...")
    try:
        SQLModel.metadata.create_all(engine)
        print("RE-INITIALIZING TABLES: Success. Neural link is active.")
    except Exception as e:
        print(f"RE-INITIALIZING TABLES: CRITICAL FAILURE: {e}")


if __name__ == "__main__":
    create_db_and_tables()