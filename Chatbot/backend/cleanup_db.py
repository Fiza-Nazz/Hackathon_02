from backend.db import get_engine
from sqlalchemy import text
from sqlmodel import SQLModel

engine = get_engine()

print("Dropping conversation and message tables to fix FK constraints...")
with engine.connect() as conn:
    # Drop in correct order due to FK
    conn.execute(text("DROP TABLE IF EXISTS messages CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS conversations CASCADE"))
    conn.commit()
print("Tables dropped successfully.")

print("Recreating tables from models...")
# This will recreate conversations and messages with the correct FK to 'user'
from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message

SQLModel.metadata.create_all(engine)
print("Tables recreated successfully with correct constraints.")
