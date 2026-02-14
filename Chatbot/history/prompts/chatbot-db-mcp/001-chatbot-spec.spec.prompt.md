---
id: 001
title: Chatbot spec creation
stage: spec
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: chatbot-db-mcp
branch: 004-chatbot-db-mcp
user: FIZA
command: /sp.specify
labels: ["spec","chatbot","mcp","database"]
links:
  spec: specs/004-chatbot-db-mcp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-chatbot-db-mcp/spec.md
  - specs/004-chatbot-db-mcp/checklists/requirements.md
tests:
  - None (spec creation)
---

## Prompt

Specification: Phase 3 — Conversational AI Chatbot with Task Management (Database Schema + MCP Tools)
Component: Database Schema Extension & MCP Tool Server
Version: 1.0
Date: January 9, 2026
Status: Ready for Implementation
Author: FIZA (using SpecKit+ format)

1. Context & Purpose
What
Implement the full foundation for a persistent, multi-device conversational AI chatbot that can intelligently manage user tasks via natural language. This phase combines:

Database schema extension with conversations and messages tables
An MCP (Model Context Protocol) server exposing 5 secure task-management tools

Why

Enable persistent chat history across sessions and devices
Keep server completely stateless (all state in DB)
Provide a standardized, secure, reusable tool interface for AI agents
Ensure complete user data isolation and audit trail
Allow AI to perform CRUD operations on tasks via natural language

Alignment with Project Constitution

✅ Stateless Server Architecture (Principle #1)
✅ MCP-First Tool Design (Principle #2)
✅ Conversation Persistence (Principle #4)
✅ Security-First JWT Authentication & User Isolation (Principle #5)

2. Current State (Phase 2 Complete)
Existing Tables
SQL-- Users table (managed by Better Auth)
users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    created_at TIMESTAMP
)

-- Tasks table
tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
)

3. Phase 3 Deliverables
Part A: Database Schema Extension
New Tables
1. conversations
SQLCREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_conversation_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_user_conversations
    ON conversations(user_id, created_at DESC);
2. messages
SQLCREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_message_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_message_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_conversation_messages
    ON messages(conversation_id, created_at ASC);

CREATE INDEX idx_user_messages
    ON messages(user_id, created_at DESC);
SQLModel Definitions
Python# backend/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")
Python# backend/models/message.py
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: str = Field(max_length=20)
    content: str = Field(sa_column=Column("content", sa.Text))
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
Relationships & Cascading
textusers
  ├── tasks (existing)
  └── conversations (NEW)
        └── messages (NEW)
              ├── conversation_id → conversations.id
              └── user_id → users.id (redundant, indexed for queries)

On user delete → all tasks, conversations, messages deleted (CASCADE)
On conversation delete → all messages deleted (CASCADE)

Migration Script
Python# backend/migrations/003_add_conversation_tables.py
from sqlmodel import SQLModel
from backend.models import Conversation, Message
from backend.db import engine

def upgrade():
    SQLModel.metadata.create_all(
        engine,
        tables=[Conversation.__table__, Message.__table__]
    )
    print("✅ Created conversations and messages tables")

def downgrade():
    Message.__table__.drop(engine)
    Conversation.__table__.drop(engine)
    print("⚠️ Dropped conversations and messages tables")

if __name__ == "__main__":
    import sys
    command = sys.argv[1] if len(sys.argv) >= 2 else "upgrade"
    {"upgrade": upgrade, "downgrade": downgrade}[command]()
Run with: python migrations/003_add_conversation_tables.py upgrade

Part B: MCP Tool Server (5 Task Management Tools)
Server Structure
textbackend/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   ├── schemas.py
│   └── tools/
│       ├── __init__.py
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
Tool Standards (Applied to All Tools)

Input: Pydantic-validated
User Context: user_id from JWT (injected by chat endpoint)
Output Format:JSON{ "success": true, "data": { ... } }orJSON{ "success": false, "error": { "code": "...", "message": "..." } }
Error Codes: INVALID_INPUT, NOT_FOUND, UNAUTHORIZED, DATABASE_ERROR
Security: All queries filter by user_id; ownership checked on modify/delete; return NOT_FOUND (not UNAUTHORIZED) for security by obscurity

Tool Details
ToolPurposeKey ParametersNatural Language Triggersadd_taskCreate new tasktitle (req), description (opt)"Add task...", "Create a reminder...", "Remind me to..."list_tasksList tasks with status filterstatus: all/pending/completed (default: all)"Show my tasks", "What's pending?", "List completed"complete_taskMark task as donetask_id"Mark task 3 complete", "I finished groceries"delete_taskPermanently delete tasktask_id"Delete task 5", "Remove old task"update_taskUpdate title and/or descriptiontask_id, title (opt), description (opt) – at least one"Rename task 1", "Update description of meeting"
MCP Server Implementation (server.py)
Python# backend/mcp_server/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent
from .tools import (
    add_task, list_tasks, complete_task,
    delete_task, update_task
)

server = Server("task-management-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="add_task", description="Create a new task", inputSchema={...}),
        Tool(name="list_tasks", description="List user's tasks", inputSchema={...}),
        Tool(name="complete_task", description="Mark task as completed", inputSchema={...}),
        Tool(name="delete_task", description="Delete a task", inputSchema={...}),
        Tool(name="update_task", description="Update task title/description", inputSchema={...}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    tool_map = {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task,
    }
    func = tool_map.get(name)
    if not func:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    result = await func(**arguments)
    return [TextContent(type="text", text=str(result))]

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())

4. Acceptance Criteria
Database

conversations and messages tables created with correct schema, FKs, indexes
 SQLModel models defined and imported
 Migration script runs successfully (upgrade/downgrade)
 Cascade deletes work correctly
 Can create/fetch/update conversations and messages

MCP Tools

 All 5 tools implemented with full validation and security
 Standardized success/error response format
 User isolation enforced on all operations
 MCP server starts and exposes tools correctly

Testing

 Unit tests for models and each tool
 Integration tests for DB relationships and tool flows
 Security tests confirming cross-user access blocked

5. Implementation Checklist

 Create backend/models/conversation.py and message.py
 Update __init__.py to export new models
 Create migration 003_add_conversation_tables.py
 Run migration on Neon DB
 Implement MCP server structure and all 5 tools
 Write Pydantic schemas and tool logic
 Write unit + integration tests
 Test MCP server startup and tool registration
 Update README with new schema and MCP usage

6. Next Steps After This Phase

Implement chat endpoint using conversation history + MCP tools
Integrate OpenAI Agents SDK with tool calling
Build frontend chat interface (ChatKit)
End-to-end testing of natural language task management

## Response snapshot

Specification created successfully at `specs/004-chatbot-db-mcp/spec.md`.

**Branch**: 004-chatbot-db-mcp (created and checked out)
**Spec File**: `specs/004-chatbot-db-mcp/spec.md`
**Checklist**: `specs/004-chatbot-db-mcp/checklists/requirements.md`

### Summary
- 3 User Stories defined (P1: Persistent Chat History, P2: Create Tasks via Natural Language, P3: View and Manage Tasks via Chat)
- 25 Functional Requirements covering database persistence, task management tools, security, and error handling
- 4 Key Entities (Conversation, Message, Task, Tool Call)
- 10 Measurable Success Criteria
- 7 Edge Cases documented
- Assumptions and Out of Scope sections clearly defined

### Quality Validation
All checklist items passed:
- No implementation details in spec
- Focused on user value and business needs
- All requirements testable and unambiguous
- Success criteria are technology-agnostic and measurable
- No [NEEDS CLARIFICATION] markers

## Outcome

- ✅ Impact: Complete specification for Phase 3 chatbot foundation ready for planning
- 🧪 Tests: None (spec creation phase)
- 📁 Files: Created spec.md, requirements.md checklist, branch 004-chatbot-db-mcp
- 🔁 Next prompts: Run `/sp.plan` to generate implementation plan
- 🧠 Reflection: Specification aligns perfectly with constitution principles. Made informed assumptions about JWT auth and existing task table. No clarifications needed as spec uses reasonable defaults.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All quality checks PASS
- Prompt variant (if applicable): Initial spec creation
- Next experiment (smallest change to try): Monitor during planning phase for any technical assumptions that need validation
