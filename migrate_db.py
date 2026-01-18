import sqlite3
import os

db_path = os.path.join("backend", "todo_app.db")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add priority column if not exists
        try:
            cursor.execute("ALTER TABLE task ADD COLUMN priority INTEGER DEFAULT 1")
            print("Added 'priority' column to 'task' table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("'priority' column already exists.")
            else:
                print(f"Error adding priority: {e}")

        # Add category column if not exists
        try:
            cursor.execute("ALTER TABLE task ADD COLUMN category TEXT DEFAULT 'General'")
            print("Added 'category' column to 'task' table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("'category' column already exists.")
            else:
                print(f"Error adding category: {e}")

        conn.commit()
        conn.close()
        print("Migration complete.")
    except Exception as e:
        print(f"Migration failed: {e}")
else:
    print(f"Database not found at {db_path}. No migration needed.")
