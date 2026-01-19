from sqlalchemy import text
from backend.db import get_engine
from sqlmodel import Session

def reset_database():
    engine = get_engine()
    print("🚀 Starting Database Reset...")
    
    with Session(engine) as session:
        try:
            # 1. Delete all tasks
            print("Cleaning up 'task' table...")
            session.execute(text("DELETE FROM \"task\""))
            
            # 2. Delete all messages and conversations
            print("Cleaning up Chat history...")
            session.execute(text("DELETE FROM messages"))
            session.execute(text("DELETE FROM conversations"))
            
            # 3. Reset ID sequences (if Postgres, truncate with RESTART IDENTITY is better)
            # For this setup, we'll try to restart sequences if possible, 
            # or just rely on the deletion for the demo.
            try:
                session.execute(text("ALTER SEQUENCE task_id_seq RESTART WITH 1"))
                session.execute(text("ALTER SEQUENCE conversations_id_seq RESTART WITH 1"))
                session.execute(text("ALTER SEQUENCE messages_id_seq RESTART WITH 1"))
            except Exception:
                # If sequence names are different or using SQLite, this might fail silently
                pass
                
            session.commit()
            print("✨ Database reset successful! all tasks and chats cleared.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error during reset: {e}")

if __name__ == "__main__":
    reset_database()
