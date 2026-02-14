<!--
SYNC IMPACT REPORT
================================================================================
Version Change: None → 1.0.0
Rationale: Initial constitution ratification for Phase 3 - AI-Powered Todo Chatbot
================================================================================
Modified Principles: None (initial creation)
Added Sections:
  - Vision Statement
  - Core Architectural Principles (5 principles)
  - Technology Stack (Non-Negotiable)
  - Database Schema Requirements
  - MCP Tools Specification (5 tools)
  - Request Flow Architecture
  - User Experience Standards
  - Security Requirements
  - Performance Requirements
  - Testing Standards
  - Spec-Driven Development Workflow
  - Forbidden Practices
  - Deliverables Checklist
  - Success Metrics
  - Version History
  - Support & References
Removed Sections: None (initial creation)
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section aligns with principles
  ✅ spec-template.md - Structure supports constitution requirements
  ✅ tasks-template.md - Task categorization reflects implementation workflow
  ✅ All other templates - No outdated references detected
Follow-up TODOs: None
================================================================================
-->

# Chatbot Phase 3 Constitution

## Core Principles

### I. Stateless Server Architecture
Server maintains NO state in memory. Every request must be independently processable with all conversation state persisted in PostgreSQL database. Enables horizontal scaling, fault tolerance, and resilience.

### II. MCP-First Tool Design
All task operations exposed ONLY through MCP tools (5 total: add, list, complete, delete, update). Direct database calls from chat endpoint are forbidden. Standardized interface for AI agent interaction.

### III. AI Agent Orchestration
OpenAI Agents SDK orchestrates all tool calls. Agent analyzes user intent and selects appropriate tools based on natural language understanding. No manual if-else routing in chat endpoint.

### IV. Conversation Persistence
Every message stored in database with conversation context. Chat history survives server restarts and enables multi-device access. Conversation and Message tables with proper relationships. No in-memory conversation buffers.

### V. Security-First JWT Authentication
Every chat request must include valid JWT token. User isolation and authorization enforcement through Better Auth JWT integration from Phase 2. All MCP tools verify user_id from token.

## Technology Stack (Non-Negotiable)

### Frontend
- **Framework**: OpenAI ChatKit (purpose-built for conversational AI interfaces)
- **Configuration**: Domain allowlist required for production

### Backend
- **Framework**: Python FastAPI (async support, modern Python, excellent OpenAPI integration)

### AI Layer
- **Framework**: OpenAI Agents SDK (official SDK with tool calling support)
- **Model**: GPT-4 or GPT-4-Turbo

### MCP Server
- **Framework**: Official MCP SDK (Python) (standard protocol for AI-tool communication)

### Database
- **Service**: Neon Serverless PostgreSQL (from Phase 2)
- **ORM**: SQLModel (async support, Pydantic integration, type safety)

### Authentication
- **Service**: Better Auth (from Phase 2)
- **Token**: JWT with 7-day expiry

## Database Schema Requirements

### New Tables (Phase 3)

#### Conversation Table
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_conversations (user_id, created_at DESC)
);
```

#### Message Table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_conversation_messages (conversation_id, created_at ASC)
);
```

### Existing Tables (Phase 2)
- **tasks**: Already exists with user_id foreign key
- **users**: Managed by Better Auth

## MCP Tools Specification

### Tool Contract Standards
- **Input Validation**: Pydantic models for all parameters
- **Error Handling**: Return structured error objects, never raise exceptions
- **User Isolation**: Every tool MUST filter by user_id from JWT
- **Idempotency**: Operations should be safe to retry
- **Response Format**: Consistent JSON structure across all tools

### Required Tools (5 Total)

#### 1. add_task
Parameters:
  - user_id: str (from JWT)
  - title: str (1-200 chars, required)
  - description: str (0-1000 chars, optional)

Returns:
  {
    "task_id": int,
    "status": "created",
    "title": str
  }

#### 2. list_tasks
Parameters:
  - user_id: str (from JWT)
  - status: str (optional: "all" | "pending" | "completed")

Returns:
  {
    "tasks": [
      {"id": int, "title": str, "completed": bool, "created_at": str}
    ],
    "total": int
  }

#### 3. complete_task
Parameters:
  - user_id: str (from JWT)
  - task_id: int (required)

Returns:
  {
    "task_id": int,
    "status": "completed",
    "title": str
  }

#### 4. delete_task
Parameters:
  - user_id: str (from JWT)
  - task_id: int (required)

Returns:
  {
    "task_id": int,
    "status": "deleted",
    "title": str
  }

#### 5. update_task
Parameters:
  - user_id: str (from JWT)
  - task_id: int (required)
  - title: str (optional, 1-200 chars)
  - description: str (optional, 0-1000 chars)

Returns:
  {
    "task_id": int,
    "status": "updated",
    "title": str
  }

## Security Requirements

### JWT Token Validation
Every chat request MUST validate:
1. Token present in Authorization header
2. Token signature valid (using BETTER_AUTH_SECRET)
3. Token not expired
4. user_id from token matches {user_id} in URL

### User Data Isolation
Every MCP tool MUST enforce:
1. Filter all queries by user_id from JWT
2. Never expose other users' tasks
3. Validate task ownership before update/delete
4. Return 404 instead of 403 for missing tasks (security by obscurity)

### SQL Injection Prevention
All database queries MUST use:
1. SQLModel ORM (parameterized queries)
2. Never string concatenation
3. Input validation via Pydantic

## Performance Requirements

### Response Time
- **Chat endpoint**: < 3 seconds (95th percentile)
- **MCP tool execution**: < 500ms per tool
- **Database queries**: < 100ms per query

### Scalability
- **Stateless design**: Supports horizontal scaling
- **Database pooling**: Connection reuse for efficiency
- **Async operations**: Non-blocking I/O throughout

## Testing Standards

### Unit Tests Required
- Each MCP tool independently testable
- Mock database for tool tests
- JWT verification logic tested

### Integration Tests Required
- End-to-end chat flow
- Conversation persistence
- Multi-turn conversations

### User Acceptance Tests
- Natural language variations
- Error scenarios
- Conversation history

## Spec-Driven Development Workflow

### Process (NON-NEGOTIABLE)
1. Write Constitution (this file)
2. Write Specification for each component
3. Get Claude Code to generate implementation
4. NO MANUAL CODING ALLOWED
5. Refine spec if output incorrect
6. Iterate until code correct

### Spec Requirements
Every spec MUST include:
- **What**: Clear requirement statement
- **Why**: Rationale and context
- **How**: Technical approach
- **Acceptance Criteria**: Testable success conditions
- **Examples**: Input/output samples

## Forbidden Practices

What NOT to Do:
- Store conversation state in server memory
- Bypass MCP tools with direct database calls from chat endpoint
- Manual if-else routing instead of agent intelligence
- Skip JWT validation for any request
- Write code manually (violates spec-driven approach)
- Use localStorage/sessionStorage (not supported in artifacts)
- Hardcode API keys or secrets
- Return raw database errors to users

## Governance

This constitution is the supreme authority for Phase 3 development. All code, specs, and decisions must align with these principles. Amendments require documentation and version updates per semantic versioning rules.

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
