# Data Model: Conversational AI Chatbot Foundation

**Feature**: 004-chatbot-db-mcp
**Date**: 2026-01-09
**Purpose**: Define database entities, relationships, and validation rules

## Overview

The data model consists of 3 core entities (Conversation, Message, Task) plus the existing User entity from Phase 2. Relationships are enforced via foreign keys with cascade deletion for data consistency.

## Entity Relationship Diagram

```
┌─────────────┐
│    users    │
│   (Phase 2) │
└──────┬──────┘
       │ 1
       │
       │ N
       │
┌──────▼──────┐
│conversations│ 1──────N ┌─────────┐
└──────┬──────┘           │ messages│
       │                   └─────────┘
       │
       │ N
       │
┌──────▼──────┐
│   tasks     │
│  (Phase 2)  │
└─────────────┘
```

## Entities

### Conversation

**Purpose**: Represents a chat session between a user and AI assistant

**Table Name**: `conversations`

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique conversation identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | Owner of this conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation was last modified |

**Indexes**:
- `idx_user_conversations`: (user_id, created_at DESC)

**Relationships**:
- **Belongs to**: User (many-to-one)
- **Has many**: Messages (one-to-many)

**Cascading Rules**:
- On User deletion → Delete all conversations (CASCADE)
- On Conversation deletion → Delete all messages (CASCADE)

**State Transitions**: None (conversation is immutable, only timestamps update)

---

### Message

**Purpose**: Represents a single message in a conversation (user or AI assistant)

**Table Name**: `messages`

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique message identifier |
| conversation_id | INTEGER | NOT NULL, FOREIGN KEY → conversations(id) ON DELETE CASCADE | Parent conversation |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | Message author (via conversation owner) |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Who sent the message |
| content | TEXT | NOT NULL | Message text content |
| tool_calls | JSONB | NULLABLE | Array of tool invocations if AI called tools |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When message was created |

**Indexes**:
- `idx_conversation_messages`: (conversation_id, created_at ASC)
- `idx_user_messages`: (user_id, created_at DESC)

**Relationships**:
- **Belongs to**: Conversation (many-to-one)
- **Belongs to**: User (many-to-one, redundant for query optimization)

**Cascading Rules**:
- On Conversation deletion → Delete all messages (CASCADE)
- On User deletion → Delete all messages (CASCADE)

**Validation Rules**:
- `role` must be either 'user' or 'assistant' (enforced by CHECK constraint)
- `content` cannot be empty or NULL
- `tool_calls` must be valid JSONB if present

**State Transitions**: None (messages are immutable once created)

---

### Task (Existing from Phase 2)

**Purpose**: Represents a todo item managed by the user

**Table Name**: `tasks`

**Fields**:

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique task identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users(id) | Task owner |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When task was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When task was last modified |

**Indexes**: (from Phase 2, assumed present)
- `idx_user_tasks`: (user_id, completed, created_at DESC)

**Relationships**:
- **Belongs to**: User (many-to-one)

**Cascading Rules**:
- On User deletion → Delete all tasks (CASCADE)

**Validation Rules**:
- `title` length: 1-200 characters
- `description` length: 0-1000 characters (if provided)

**State Transitions**:
- `completed`: FALSE → TRUE (one-way, cannot be uncompleted)

---

### User (Existing from Phase 2, Managed by Better Auth)

**Purpose**: Application user with authentication

**Table Name**: `users`

**Fields** (from Phase 2):

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| name | VARCHAR(255) | NOT NULL | User display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation date |

**Relationships**:
- **Has many**: Conversations (one-to-many)
- **Has many**: Tasks (one-to-many)

---

## MCP Tool Data Flow

### add_task

**Input**: `{user_id, title, description?}`
**Database Operation**: INSERT INTO tasks (user_id, title, description)
**Returns**: `{task_id, status, title}`

---

### list_tasks

**Input**: `{user_id, status?}` (status = 'all' | 'pending' | 'completed')
**Database Operation**: SELECT * FROM tasks WHERE user_id = ? [AND completed = ?]
**Returns**: `{tasks: [{id, title, completed, created_at}], total}`

---

### complete_task

**Input**: `{user_id, task_id}`
**Database Operation**: UPDATE tasks SET completed = TRUE WHERE id = ? AND user_id = ?
**Returns**: `{task_id, status, title}`

---

### delete_task

**Input**: `{user_id, task_id}`
**Database Operation**: DELETE FROM tasks WHERE id = ? AND user_id = ?
**Returns**: `{task_id, status, title}`

---

### update_task

**Input**: `{user_id, task_id, title?, description?}` (at least one optional field required)
**Database Operation**: UPDATE tasks SET title = ?, description = ? WHERE id = ? AND user_id = ?
**Returns**: `{task_id, status, title}`

---

## Security Considerations

### User Isolation
- All queries MUST filter by `user_id`
- Foreign keys enforce referential integrity
- Cascade deletion prevents orphaned records

### Error Handling
- Missing resources: Return NOT_FOUND (not UNAUTHORIZED) for security by obscurity
- Invalid input: Return INVALID_INPUT with validation error details
- Database errors: Return DATABASE_ERROR without exposing raw exceptions

### SQL Injection Prevention
- All queries use parameterized SQL via SQLModel/SQLAlchemy
- Pydantic validates all input before database operations
- Never concatenate user input into SQL queries

---

## Performance Considerations

### Query Optimization
- Indexes on all foreign key columns
- Composite indexes on common query patterns (user_id + timestamp)
- Redundant user_id in messages table enables direct queries without joins

### Scaling
- Stateless design enables horizontal scaling
- Database connection pooling (handled by asyncpg)
- Async operations enable concurrent tool execution

---

## Migration Path

**Current State (Phase 2)**:
- users table exists
- tasks table exists

**Target State (Phase 3)**:
- Add conversations table
- Add messages table
- Add indexes

**Migration**: `migrations/003_add_conversation_tables.py`
- upgrade(): Create conversations, messages tables and indexes
- downgrade(): Drop messages, conversations tables
