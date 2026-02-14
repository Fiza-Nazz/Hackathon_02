# Research: Conversational AI Chatbot Foundation

**Feature**: 004-chatbot-db-mcp
**Date**: 2026-01-09
**Purpose**: Resolve technology choices and architectural decisions for implementation

## Research Summary

This document captures research decisions for implementing the Phase 3 chatbot foundation, focusing on database schema design for conversation persistence and MCP (Model Context Protocol) server architecture for task management tools.

---

## Topic 1: Database Schema Design for Conversation Persistence

### Decision: Two-table relational model with cascade deletion

**Chosen Approach**:
- `conversations` table: Stores chat session metadata (id, user_id, created_at, updated_at)
- `messages` table: Stores individual message records with conversation foreign key
- Cascade deletion: Deleting a conversation automatically removes all messages
- Redundant user_id in messages table for query optimization

**Rationale**:
1. **Separation of concerns**: Conversation metadata (timestamps, user ownership) separated from message content
2. **Query efficiency**: Indexing on conversation_id allows fast message retrieval per conversation
3. **Data integrity**: Foreign key constraints ensure referential integrity
4. **Cascade deletion**: Automatically cleans up messages when conversation deleted
5. **Multi-device access**: Centralized conversation state enables cross-device synchronization
6. **Performance optimization**: Redundant user_id index enables direct user message queries without joins

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Single table with JSONB column for messages | Simple schema, no joins | Difficult to query individual messages, no foreign key constraints, poor performance at scale | Messages table enables fine-grained queries and foreign key integrity |
| Document database (MongoDB) | Flexible schema, native JSON support | Additional technology stack, migration complexity from PostgreSQL | Project already uses PostgreSQL (Neon) from Phase 2 |
| Messages-only table (no conversations table) | Simpler structure | No way to track conversation metadata (timestamps, session grouping), difficult to implement multi-device sync | Conversations table enables session-level operations and metadata tracking |

**Best Practices Applied**:
- Foreign key constraints for referential integrity
- Cascade deletion for automatic cleanup
- Composite indexes on (user_id, created_at) for efficient user queries
- CHECK constraint on role field to enforce enum-like behavior
- JSONB for flexible tool call metadata storage

---

## Topic 2: MCP Server Architecture for Task Management

### Decision: Async Python MCP server with Pydantic validation

**Chosen Approach**:
- Official MCP Python SDK for server implementation
- Async/await pattern with FastAPI-style coroutines
- Pydantic models for all tool input/output validation
- Separate module per tool for maintainability
- Centralized server.py for tool registration and dispatch

**Rationale**:
1. **Standard compliance**: Official SDK ensures MCP protocol compatibility
2. **Type safety**: Pydantic provides runtime validation and automatic error messages
3. **Performance**: Async/await enables non-blocking I/O for concurrent tool calls
4. **Maintainability**: Separate tool modules make code organization clear
5. **Error handling**: Standardized error response format across all tools
6. **Testing**: Modular structure enables isolated unit testing per tool

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| REST API instead of MCP | Standard web pattern, easier testing | Breaks constitution principle #2 (MCP-First), requires custom tool registry | MCP is constitutionally required for AI agent integration |
| Synchronous MCP server | Simpler implementation | Blocks on database calls, poor performance under load | Async enables concurrent tool execution for multi-user scenarios |
| Single monolithic tool file | Fewer files to manage | Hard to maintain, difficult to test, poor code organization | Modular structure scales better as tools grow |

**Best Practices Applied**:
- Pydantic BaseModel for all input validation
- Consistent error response format: `{success, data/error}`
- Error codes: INVALID_INPUT, NOT_FOUND, UNAUTHORIZED, DATABASE_ERROR
- User isolation enforced via user_id filtering in all queries
- Idempotent operations where possible (task updates)
- Never raise exceptions - return structured error objects

---

## Topic 3: SQLModel vs SQLAlchemy for ORM

### Decision: SQLModel (Pydantic + SQLAlchemy)

**Chosen Approach**:
- SQLModel for database models
- Leverages Pydantic v2 for validation
- SQLAlchemy core for database operations
- Automatic migration via Alembic

**Rationale**:
1. **Type safety**: Full IDE support with auto-completion
2. **Validation**: Pydantic automatically validates on input and output
3. **Documentation**: Models serve as both database schema and API contract documentation
4. **Async support**: Compatible with asyncpg for high performance
5. **Project consistency**: Already used in Phase 2 for Task model

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Pure SQLAlchemy | More control, established | No automatic validation, more boilerplate | SQLModel provides same power with less code |
| SQLAlchemy + Pydantic separate layers | Maximum flexibility | Duplicate model definitions (one for DB, one for API) | SQLModel eliminates duplication |

---

## Topic 4: Error Handling Strategy

### Decision: Never raise exceptions - return structured errors

**Chosen Approach**:
- All tools return dict: `{success: bool, data: Any | None, error: dict | None}`
- Error dict: `{code: str, message: str}`
- Error codes limited to 4 types: INVALID_INPUT, NOT_FOUND, UNAUTHORIZED, DATABASE_ERROR
- Database exceptions caught and converted to DATABASE_ERROR
- Validation errors converted to INVALID_INPUT

**Rationale**:
1. **MCP protocol compatibility**: MCP tools return results, not exceptions
2. **User experience**: Clear error messages for end users
3. **Security**: Never expose raw database errors
4. **Consistency**: Standard format across all 5 tools
5. **Debugging**: Error codes enable programmatic handling

**Best Practices Applied**:
- Security by obscurity: Return NOT_FOUND instead of UNAUTHORIZED for missing resources
- Never include stack traces in error messages
- Log full errors server-side while returning safe messages to users
- Validate inputs before database operations (fail fast)

---

## Topic 5: Database Indexing Strategy

### Decision: Strategic indexes for query performance

**Chosen Approach**:
- `idx_user_conversations`: (user_id, created_at DESC) - Fast retrieval of user's conversation list
- `idx_conversation_messages`: (conversation_id, created_at ASC) - Fast chronological message retrieval
- `idx_user_messages`: (user_id, created_at DESC) - Direct user message queries without joins

**Rationale**:
1. **Query optimization**: All common queries supported by indexes
2. **Performance**: Meet 100ms query requirement from constitution
3. **Multi-column indexes**: Optimize for specific access patterns
4. **ASC/DESC sorting**: Match typical query patterns

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Single index on all columns | Simpler | Larger index size, slower writes, less effective for specific queries | Multi-column indexes optimize for actual query patterns |
| No indexes | Simpler schema | Performance degrades with message count | 10k messages per conversation requires indexed access |

---

## Topic 6: Tool Call Metadata Storage

### Decision: JSONB field in messages table

**Chosen Approach**:
- `tool_calls` column as JSONB type in messages table
- Stores array of tool invocations: `[{name, parameters, result}]`
- Only populated for assistant messages when tools were called

**Rationale**:
1. **Flexibility**: JSONB accommodates any tool structure
2. **Queryability**: JSONB indexing possible for future analysis
3. **Audit trail**: Tracks exactly which tools AI invoked
4. **Conversation context**: Enables replay or analysis of AI decision-making

**Best Practices Applied**:
- PostgreSQL JSONB for efficient storage and querying
- Optional field (nullable) - not all messages have tool calls
- Type checking at application layer, not database level

---

## Topic 7: Migration Strategy

### Decision: Versioned migration scripts with upgrade/downgrade

**Chosen Approach**:
- Migration 003_add_conversation_tables.py
- `upgrade()` function creates tables
- `downgrade()` function drops tables
- Run via `python migrations/003_add_conversation_tables.py upgrade/downgrade`

**Rationale**:
1. **Reversibility**: Downgrade enables rollback if needed
2. **Reproducibility**: Versioned migrations track database state
3. **Simplicity**: No dependency on complex migration frameworks
4. **Phase alignment**: Extends existing migration pattern from Phase 2

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Alembic migrations | Industry standard, automatic versioning | Additional dependency, complex setup | Simple script sufficient for this scope |
| Manual SQL execution | Maximum control | No version tracking, manual rollback risk | Versioned scripts provide safety net |

---

## Conclusion

All research topics resolved with clear decisions aligned to:
- Project constitution principles
- Phase 2 existing architecture
- Performance requirements (<500ms tools, <100ms queries)
- Security requirements (user isolation, no raw errors)
- Maintainability and testability goals

**Next Steps**: Proceed to Phase 1 (data model, contracts, quickstart) and Phase 2 (tasks generation).
