from sqlmodel import Session, text
from backend.src.database.database import engine
from backend.src.database.init_db import create_db_and_tables

def fix_schema():
    print("WARNING: Attempting to fix Tasks table schema...")
    with Session(engine) as session:
        try:
            # 1. Drop the incompatible tasks table
            print("Dropping 'tasks' table to resolve Integer/UUID mismatch...")
            session.exec(text("DROP TABLE IF EXISTS tasks CASCADE;"))
            session.commit()
            print("Tasks table dropped successfully.")
            
            # 2. Re-create tables with new schema
            print("Re-creating tables...")
            create_db_and_tables()
            print("Schema fix complete.")
            
        except Exception as e:
            print(f"Error fixing schema: {e}")
            session.rollback()

if __name__ == "__main__":
    fix_schema()
