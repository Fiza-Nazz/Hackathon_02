# Implementation Plan: Conversational AI Chatbot Foundation

**Branch**: `004-chatbot-db-mcp` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-chatbot-db-mcp/spec.md`

## Summary

Implement the foundational infrastructure for an AI-powered conversational chatbot that manages tasks through natural language. This includes database schema extensions for persistent conversation history (conversations and messages tables) and a Model Context Protocol (MCP) server exposing 5 standardized task management tools (add, list, complete, delete, update). The architecture enforces stateless server operation with all state persisted in PostgreSQL, complete user data isolation via JWT authentication, and AI agent orchestration through OpenAI Agents SDK for natural language understanding.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.14+, Pydantic 2.0+, mcp python-sdk, OpenAI Agents SDK, asyncpg 0.29+
**Storage**: Neon Serverless PostgreSQL (existing from Phase 2)
**Testing**: pytest 7.4+, pytest-asyncio 0.21+, pytest-mock
**Target Platform**: Linux server (deployed on Railway/Render)
**Project Type**: Web application (backend MCP server + database)
**Performance Goals**: <500ms per MCP tool execution, <100ms per database query, <3s chat endpoint p95
**Constraints**: Stateless server (no in-memory state), JWT-based auth, <3s chat response time p95, support 10k messages per conversation
**Scale/Scope**: Multiple users, 5 MCP tools, 2 new database tables, concurrent chat sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Stateless Server Architecture
- **Requirement**: All conversation state persisted in database, no in-memory buffers
- **Design Compliance**: Conversations and Messages tables store all chat history
- **Verification Point**: Conversation persistence tests (Phase 3 testing)
- **Status**: ✅ PASS

### Principle II: MCP-First Tool Design
- **Requirement**: All task operations exposed ONLY through MCP tools (5 tools)
- **Design Compliance**: 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Verification Point**: MCP tool contract tests
- **Status**: ✅ PASS

### Principle III: AI Agent Orchestration
- **Requirement**: OpenAI Agents SDK orchestrates tool calls, no manual if-else routing
- **Design Compliance**: Chat endpoint delegates all tool selection to AI agent
- **Verification Point**: Agent integration tests (future phase)
- **Status**: ✅ PASS (out of scope for this feature, foundation only)

### Principle IV: Conversation Persistence
- **Requirement**: Every message stored in database with conversation context
- **Design Compliance**: Message table with conversation_id, user_id, role, content, timestamp
- **Verification Point**: Message persistence and retrieval tests
- **Status**: ✅ PASS

### Principle V: Security-First JWT Authentication
- **Requirement**: Every chat request includes valid JWT, all MCP tools verify user_id
- **Design Compliance**: MCP tools accept user_id parameter injected by JWT verification
- **Verification Point**: User isolation security tests
- **Status**: ✅ PASS

### Overall Status: ✅ PASS - No violations detected

## Project Structure

### Documentation (this feature)

```text
specs/004-chatbot-db-mcp/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── mcp-tools.yaml   # MCP tool contracts
│   └── database-schema.sql
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── models/
│   ├── __init__.py
│   ├── conversation.py     # New: Conversation model
│   ├── message.py          # New: Message model
│   └── task.py             # Existing: Task model from Phase 2
├── mcp_server/
│   ├── __init__.py
│   ├── server.py           # MCP server entry point
│   ├── schemas.py          # Pydantic models for tool inputs/outputs
│   └── tools/
│       ├── __init__.py
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
├── db.py                   # Database connection (existing)
└── migrations/
    ├── 002_add_tasks.py    # Existing (Phase 2)
    └── 003_add_conversation_tables.py  # New: Conversation and Message tables

tests/
├── unit/
│   ├── test_conversation_model.py
│   ├── test_message_model.py
│   ├── test_add_task_tool.py
│   ├── test_list_tasks_tool.py
│   ├── test_complete_task_tool.py
│   ├── test_delete_task_tool.py
│   └── test_update_task_tool.py
├── integration/
│   ├── test_conversation_persistence.py
│   ├── test_message_persistence.py
│   └── test_mcp_tool_integration.py
└── security/
    ├── test_user_isolation.py
    └── test_cross_user_access_prevention.py
```

**Structure Decision**: Web application architecture with backend MCP server. Backend contains models (database entities), MCP server (tool implementations), and migrations. Tests are organized by unit, integration, and security categories. The frontend chat interface is out of scope for this feature (future phase).

## Complexity Tracking

> No violations detected, no complexity tracking required

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
