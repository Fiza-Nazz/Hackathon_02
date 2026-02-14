#!/usr/bin/env python3
"""
Phase V Database Migration Script
Applies schema updates for advanced features
"""

import os
import sys
import asyncio
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add backend src to path
backend_path = Path(__file__).parent / "src"
sys.path.append(str(backend_path))

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

def run_migration():
    """Run Phase V database migration"""
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    print("🔄 Starting Phase V database migration...")
    print(f"📊 Database: {database_url.split('@')[1] if '@' in database_url else 'local'}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Execute migration in steps
        with engine.connect() as conn:
            
            # Step 1: Add columns to tasks table
            print("📝 Step 1: Adding columns to tasks table...")
            columns_sql = [
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'",
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP NULL",
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurring_pattern VARCHAR(20) NULL",
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurring_interval INTEGER DEFAULT 1",
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS parent_task_id INTEGER NULL",
                "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE"
            ]
            
            for sql in columns_sql:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                except Exception as e:
                    if "already exists" in str(e).lower():
                        print(f"⚠️  Column already exists, skipping...")
                    else:
                        print(f"❌ Error: {e}")
                        return False
            
            # Step 2: Create new tables
            print("📝 Step 2: Creating new tables...")
            tables_sql = [
                """CREATE TABLE IF NOT EXISTS task_tags (
                    id SERIAL PRIMARY KEY,
                    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                    tag_name VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(task_id, tag_name)
                )""",
                """CREATE TABLE IF NOT EXISTS tags (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL,
                    color VARCHAR(7) DEFAULT '#3B82F6',
                    user_id VARCHAR(255) NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )""",
                """CREATE TABLE IF NOT EXISTS reminders (
                    id SERIAL PRIMARY KEY,
                    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                    user_id VARCHAR(255) NOT NULL,
                    remind_at TIMESTAMP NOT NULL,
                    reminder_type VARCHAR(20) DEFAULT 'due_date',
                    status VARCHAR(20) DEFAULT 'pending',
                    message TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )""",
                """CREATE TABLE IF NOT EXISTS audit_log (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    aggregate_id VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    event_data JSONB NOT NULL,
                    correlation_id UUID,
                    timestamp TIMESTAMP DEFAULT NOW()
                )"""
            ]
            
            for sql in tables_sql:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"✅ Table created successfully")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        print(f"⚠️  Table already exists, skipping...")
                    else:
                        print(f"❌ Error: {e}")
                        return False
            
            # Step 3: Create indexes
            print("📝 Step 3: Creating indexes...")
            indexes_sql = [
                "CREATE INDEX IF NOT EXISTS idx_task_tags_task_id ON task_tags(task_id)",
                "CREATE INDEX IF NOT EXISTS idx_task_tags_name ON task_tags(tag_name)",
                "CREATE INDEX IF NOT EXISTS idx_reminders_task_id ON reminders(task_id)",
                "CREATE INDEX IF NOT EXISTS idx_reminders_user_id ON reminders(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_reminders_remind_at ON reminders(remind_at)",
                "CREATE INDEX IF NOT EXISTS idx_reminders_status ON reminders(status)",
                "CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type)",
                "CREATE INDEX IF NOT EXISTS idx_audit_log_aggregate_id ON audit_log(aggregate_id)",
                "CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_tags_user_id ON tags(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name)",
                "CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)",
                "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)",
                "CREATE INDEX IF NOT EXISTS idx_tasks_user_id_status ON tasks(user_id, completed)",
                "CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at)"
            ]
            
            for sql in indexes_sql:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                except Exception as e:
                    if "already exists" in str(e).lower():
                        print(f"⚠️  Index already exists, skipping...")
                    else:
                        print(f"❌ Error creating index: {e}")
            
            # Step 4: Insert default data
            print("📝 Step 4: Inserting default data...")
            try:
                conn.execute(text("""
                    INSERT INTO tags (name, color, user_id, usage_count) VALUES
                        ('work', '#EF4444', 'system', 0),
                        ('personal', '#10B981', 'system', 0),
                        ('urgent', '#F59E0B', 'system', 0),
                        ('important', '#8B5CF6', 'system', 0)
                    ON CONFLICT (name) DO NOTHING
                """))
                conn.commit()
                print("✅ Default tags inserted")
            except Exception as e:
                print(f"⚠️  Default data insertion: {e}")
            
            # Step 5: Update existing data
            print("📝 Step 5: Updating existing data...")
            try:
                conn.execute(text("UPDATE tasks SET priority = 'medium' WHERE priority IS NULL"))
                conn.commit()
                print("✅ Existing tasks updated")
            except Exception as e:
                print(f"⚠️  Data update: {e}")
        
        print("✅ Phase V database migration completed successfully!")
        
        # Verify new tables exist
        with engine.connect() as conn:
            tables_to_check = ['task_tags', 'reminders', 'audit_log', 'tags']
            for table in tables_to_check:
                result = conn.execute(text(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table}'"))
                count = result.scalar()
                if count > 0:
                    print(f"✅ Table '{table}' verified")
                else:
                    print(f"❌ Table '{table}' not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)