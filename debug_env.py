import os
from pathlib import Path
from dotenv import load_dotenv

# Replicate the logic from database.py
BASE_DIR = Path('backend/src/database/database.py').resolve().parent.parent.parent
env_path = BASE_DIR / "backend/.env"  # Explicitly pointing to backend/.env

print(f"Checking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

load_dotenv(env_path)

url = os.getenv("DATABASE_URL")
print(f"Loaded DATABASE_URL: {url}")

if url and url.startswith("postgresql"):
    print("✅ SUCCESS: PostgreSQL URL detected!")
else:
    print("❌ FAILURE: SQLite or None detected.")
