from sqlmodel import SQLModel
from .database import engine
from ..models import User, Task


def create_db_and_tables():
    """
    Create database tables for User and Task models.
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_db_and_tables()