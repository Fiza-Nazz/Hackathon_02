# Quickstart: Conversational AI Chatbot Foundation

**Feature**: 004-chatbot-db-mcp
**Purpose**: Get the MCP server and database schema running locally

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon Serverless from Phase 2)
- Existing Better Auth setup (Phase 2)
- Existing Task model (Phase 2)

## Installation

### 1. Install Dependencies

```bash
# From project root
pip install sqlmodel mcp pydantic pytest pytest-asyncio pytest-mock asyncpg
```

### 2. Run Database Migration

```bash
# From project root
python backend/migrations/003_add_conversation_tables.py upgrade
```

Expected output:
```
✅ Created conversations and messages tables
```

To rollback:
```bash
python backend/migrations/003_add_conversation_tables.py downgrade
```

## Verify Setup

### Check Database Tables

Connect to your PostgreSQL database and run:

```sql
-- Check if tables exist
SELECT table_name FROM information_schema.tables
WHERE table_name IN ('conversations', 'messages');

-- Should return:
-- conversations
-- messages
```

### Test MCP Server

```bash
# From project root
python backend/mcp_server/server.py
```

Expected output:
```
MCP server running on stdio
Tools available:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task
```

## Basic Usage

### Creating a Conversation

```python
from backend.models import Conversation
from backend.db import engine
from sqlmodel import Session

def create_conversation(user_id: str):
    with Session(engine) as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

# Usage
conv = create_conversation("user_abc123")
print(f"Created conversation {conv.id}")
```

### Adding a Message

```python
from backend.models import Message
from datetime import datetime

def add_message(conversation_id: int, user_id: str, role: str, content: str):
    with Session(engine) as session:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,  # "user" or "assistant"
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

# Usage
msg = add_message(
    conversation_id=123,
    user_id="user_abc123",
    role="user",
    content="Add a task to buy groceries"
)
print(f"Created message {msg.id}")
```

### Using MCP Tools

```python
from backend.mcp_server.tools import add_task, list_tasks

# Add a task
result = add_task(
    user_id="user_abc123",
    title="Buy groceries",
    description="Milk, eggs, bread"
)
# Returns: {"success": True, "data": {"task_id": 456, "status": "created", "title": "Buy groceries"}}

# List tasks
result = list_tasks(user_id="user_abc123", status="pending")
# Returns: {"success": True, "data": {"tasks": [...], "total": 1}}
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run security tests
pytest tests/security/ -v
```

## Troubleshooting

### Migration Fails

**Error**: `relation "conversations" already exists`

**Solution**: Run downgrade first, then upgrade:
```bash
python backend/migrations/003_add_conversation_tables.py downgrade
python backend/migrations/003_add_conversation_tables.py upgrade
```

### Database Connection Error

**Error**: `could not connect to server`

**Solution**: Check your `DATABASE_URL` environment variable:
```bash
echo $DATABASE_URL
```

### MCP Server Won't Start

**Error**: `ModuleNotFoundError: No module named 'mcp'`

**Solution**: Install dependencies:
```bash
pip install mcp
```

## Project Structure

```
backend/
├── models/
│   ├── conversation.py     # Conversation model
│   ├── message.py          # Message model
│   └── task.py             # Existing Task model
├── mcp_server/
│   ├── server.py           # MCP server entry point
│   ├── schemas.py          # Pydantic models
│   └── tools/
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
└── migrations/
    └── 003_add_conversation_tables.py

tests/
├── unit/                   # Unit tests
├── integration/            # Integration tests
└── security/               # Security tests
```

## Next Steps

1. Implement all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
2. Write unit tests for each tool
3. Write integration tests for conversation/message persistence
4. Write security tests for user isolation
5. Run `/sp.tasks` to generate implementation tasks

## Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:password@host:port/database

# Optional
BETTER_AUTH_SECRET=your-secret-key-here
```

## Documentation

- [Data Model](./data-model.md)
- [MCP Tool Contracts](./contracts/mcp-tools.yaml)
- [Database Schema](./contracts/database-schema.sql)
- [Research](./research.md)
