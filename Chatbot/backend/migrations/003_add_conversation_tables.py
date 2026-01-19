"""
Database migration for Phase 3: Add conversations and messages tables.

Migration: 003_add_conversation_tables
Usage: python backend/migrations/003_add_conversation_tables.py upgrade|downgrade
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

try:
    from sqlmodel import SQLModel, create_engine, Session
    from backend.models.conversation import Conversation
    from backend.models.message import Message
    from backend.db import engine
except ImportError:
    # If db.py doesn't exist, create a temporary engine
    from sqlmodel import create_engine
    engine = None
    print("Warning: backend.db not found, migration may not work without proper engine")


def upgrade():
    """Create conversations and messages tables."""
    if engine is None:
        print("❌ Error: Database engine not configured")
        return False

    try:
        SQLModel.metadata.create_all(
            engine,
            tables=[Conversation.__table__, Message.__table__]
        )
        print("✅ Created conversations and messages tables")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def downgrade():
    """Drop conversations and messages tables."""
    if engine is None:
        print("❌ Error: Database engine not configured")
        return False

    try:
        Message.__table__.drop(engine)
        Conversation.__table__.drop(engine)
        print("⚠️ Dropped conversations and messages tables")
        return True
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return False


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) >= 2 else "upgrade"

    if command == "upgrade":
        success = upgrade()
        sys.exit(0 if success else 1)
    elif command == "downgrade":
        success = downgrade()
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python 003_add_conversation_tables.py upgrade|downgrade")
        sys.exit(1)
