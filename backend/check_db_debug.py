
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, select, SQLModel
from src.models.task import Task
from src.models.user import User

# Load Env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# 1. Check Postgres
pg_url = os.getenv("DATABASE_URL")
print(f"--- CHECKING POSTGRES ({pg_url}) ---")
if pg_url:
    try:
        engine_pg = create_engine(pg_url)
        with Session(engine_pg) as session:
            tasks = session.exec(select(Task)).all()
            print(f"Total Tasks in Postgres: {len(tasks)}")
            for t in tasks:
                print(f"ID: {t.id} | Title: {t.title} | Completed: {t.completed}")
    except Exception as e:
        print(f"Postgres Connection Failed: {e}")
else:
    print("No DATABASE_URL found.")

# 2. Check SQLite
print("\n--- CHECKING LOCAL SQLITE (todo_app.db) ---")
sqlite_path = "sqlite:///./todo_app.db"
try:
    if os.path.exists("todo_app.db"):
        engine_lite = create_engine(sqlite_path)
        with Session(engine_lite) as session:
            tasks = session.exec(select(Task)).all()
            print(f"Total Tasks in SQLite: {len(tasks)}")
            for t in tasks:
                print(f"ID: {t.id} | Title: {t.title} | Completed: {t.completed}")
    else:
        print("todo_app.db does not exist.")
except Exception as e:
    print(f"SQLite Check Failed: {e}")
