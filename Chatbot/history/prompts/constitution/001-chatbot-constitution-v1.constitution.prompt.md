---
id: 001
title: Chatbot Constitution v1
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: TBD
command: /sp.constitution
labels: ["constitution","phase3","chatbot"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None (constitution update)
---

## Prompt

# Phase 3 Constitution - AI-Powered Todo Chatbot

**Project**: Evolution of Todo - Phase 3
**Due Date**: December 21, 2025
**Points**: 200

---

## 🎯 Vision Statement

Transform the Todo web application into an intelligent conversational interface where users manage tasks through natural language, powered by AI agents and MCP (Model Context Protocol) architecture.

---

## 🏗️ Core Architectural Principles

### 1. **Stateless Server Architecture**
- **Principle**: Server maintains NO state in memory
- **Rationale**: Enables horizontal scaling, fault tolerance, and resilience
- **Implementation**: All conversation state persists in PostgreSQL database
- **Enforcement**: Every request must be independently processable

### 2. **MCP-First Tool Design**
- **Principle**: All task operations exposed ONLY through MCP tools
- **Rationale**: Standardized interface for AI agent interaction
- **Implementation**: 5 MCP tools (add, list, complete, delete, update)
- **Enforcement**: Direct database calls from chat endpoint are forbidden

### 3. **AI Agent Orchestration**
- **Principle**: OpenAI Agents SDK orchestrates all tool calls
- **Rationale**: Intelligent routing based on natural language understanding
- **Implementation**: Agent analyzes user intent and selects appropriate tools
- **Enforcement**: No manual if-else routing in chat endpoint

### 4. **Conversation Persistence**
- **Principle**: Every message stored in database with conversation context
- **Rationale**: Chat history survives server restarts and enables multi-device access
- **Implementation**: Conversation and Message tables with proper relationships
- **Enforcement**: No in-memory conversation buffers

### 5. **Security-First JWT Authentication**
- **Principle**: Every chat request must include valid JWT token
- **Rationale**: User isolation and authorization enforcement
- **Implementation**: Better Auth JWT integration from Phase 2
- **Enforcement**: All MCP tools verify user_id from token

---

## 🔧 Technology Stack (Non-Negotiable)

### Frontend
- **Framework**: OpenAI ChatKit
- **Reasoning**: Purpose-built for conversational AI interfaces
- **Configuration**: Domain allowlist required for production

### Backend
- **Framework**: Python FastAPI
- **Reasoning**: Async support, modern Python, excellent OpenAPI integration

### AI Layer
- **Framework**: OpenAI Agents SDK
- **Reasoning**: Official SDK with tool calling support
- **Model**: GPT-4 or GPT-4-Turbo

### MCP Server
- **Framework**: Official MCP SDK (Python)
- **Reasoning**: Standard protocol for AI-tool communication

### Database
- **Service**: Neon Serverless PostgreSQL (from Phase 2)
- **ORM**: SQLModel
- **Reasoning**: Async support, Pydantic integration, type safety

### Authentication
- **Service**: Better Auth (from Phase 2)
- **Token**: JWT with 7-day expiry
- **Reasoning**: Already integrated, proven in Phase 2

---

## 📊 Database Schema Requirements

### New Tables (Phase 3)

#### **Conversation Table**
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

#### **Message Table**
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

---

## 🛠️ MCP Tools Specification

### Tool Contract Standards
- **Input Validation**: Pydantic models for all parameters
- **Error Handling**: Return structured error objects, never raise exceptions
- **User Isolation**: Every tool MUST filter by user_id from JWT
- **Idempotency**: Operations should be safe to retry
- **Response Format**: Consistent JSON structure across all tools

### Required Tools (5 Total)

#### 1. **add_task**
```python
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
```

#### 2. **list_tasks**
```python
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
```

#### 3. **complete_task**
```python
Parameters:
  - user_id: str (from JWT)
  - task_id: int (required)

Returns:
  {
    "task_id": int,
    "status": "completed",
    "title": str
  }
```

#### 4. **delete_task**
```python
Parameters:
  - user_id: str (from JWT)
  - task_id: int (required)

Returns:
  {
    "task_id": int,
    "status": "deleted",
    "title": str
  }
```

#### 5. **update_task**
```python
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
```

---

## 🔄 Request Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     STATELESS REQUEST CYCLE                      │
└──────────────────────────────────────────────────────────────────┘

1. User sends message via ChatKit UI
   ↓
2. POST /api/{user_id}/chat (JWT in Authorization header)
   ↓
3. Verify JWT → Extract user_id
   ↓
4. Fetch conversation history from database (if conversation_id exists)
   ↓
5. Save user message to messages table
   ↓
6. Build message array: [history] + [new_message]
   ↓
7. Call OpenAI Agents SDK with message array + MCP tools
   ↓
8. Agent analyzes intent → Selects appropriate MCP tool(s)
   ↓
9. MCP tool executes (e.g., add_task, list_tasks)
   ↓
10. Tool returns result to agent
    ↓
11. Agent generates natural language response
    ↓
12. Save assistant message to messages table
    ↓
13. Return response to client
    ↓
14. Server forgets everything (stateless) ✅
```

---

## 🎨 User Experience Standards

### Natural Language Understanding
The agent MUST understand variations:
- **Add Task**: "add groceries", "remind me to buy milk", "create task for meeting"
- **List Tasks**: "show tasks", "what's pending?", "my todo list"
- **Complete Task**: "done with task 3", "mark #5 complete", "finished meeting"
- **Delete Task**: "remove task 2", "delete the old task", "cancel meeting task"
- **Update Task**: "change task 1 to X", "update description", "rename task"

### Response Quality
- **Confirmation**: Always confirm actions ("✅ Added 'Buy groceries' to your list")
- **Context**: Reference task details in responses
- **Errors**: User-friendly error messages ("Task #99 doesn't exist in your list")
- **Suggestions**: Proactive help ("You have 3 pending tasks. Want to see them?")

---

## 🔐 Security Requirements

### JWT Token Validation
```python
# Every chat request MUST validate:
1. Token present in Authorization header
2. Token signature valid (using BETTER_AUTH_SECRET)
3. Token not expired
4. user_id from token matches {user_id} in URL
```

### User Data Isolation
```python
# Every MCP tool MUST enforce:
1. Filter all queries by user_id from JWT
2. Never expose other users' tasks
3. Validate task ownership before update/delete
4. Return 404 instead of 403 for missing tasks (security by obscurity)
```

### SQL Injection Prevention
```python
# All database queries MUST use:
1. SQLModel ORM (parameterized queries)
2. Never string concatenation
3. Input validation via Pydantic
```

---

## 📈 Performance Requirements

### Response Time
- **Chat endpoint**: < 3 seconds (95th percentile)
- **MCP tool execution**: < 500ms per tool
- **Database queries**: < 100ms per query

### Scalability
- **Stateless design**: Supports horizontal scaling
- **Database pooling**: Connection reuse for efficiency
- **Async operations**: Non-blocking I/O throughout

---

## 🧪 Testing Standards

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

---

## 📝 Spec-Driven Development Workflow

### Process (Non-Negotiable)
```
1. Write Constitution (this file) ✅
2. Write Specification for each component
3. Get Claude Code to generate implementation
4. NO MANUAL CODING ALLOWED
5. Refine spec if output incorrect
6. Iterate until code correct
```

### Spec Requirements
Every spec MUST include:
- **What**: Clear requirement statement
- **Why**: Rationale and context
- **How**: Technical approach
- **Acceptance Criteria**: Testable success conditions
- **Examples**: Input/output samples

---

## 🚫 Forbidden Practices

### What NOT to Do
- ❌ Store conversation state in server memory
- ❌ Bypass MCP tools with direct database calls from chat endpoint
- ❌ Manual if-else routing instead of agent intelligence
- ❌ Skip JWT validation for any request
- ❌ Write code manually (violates spec-driven approach)
- ❌ Use localStorage/sessionStorage (not supported in artifacts)
- ❌ Hardcode API keys or secrets
- ❌ Return raw database errors to users

---

## 📦 Deliverables Checklist

### Code
- [ ] 5 MCP tools fully implemented
- [ ] Chat endpoint with OpenAI Agents SDK
- [ ] Conversation + Message database models
- [ ] Database migrations for new tables
- [ ] ChatKit frontend integrated
- [ ] JWT authentication working

### Documentation
- [ ] Constitution file (this document)
- [ ] Specs for all components (in /specs/003-chatbot/)
- [ ] README with setup instructions
- [ ] CLAUDE.md updated for Phase 3
- [ ] API documentation (OpenAPI spec)

### Deployment
- [ ] Frontend deployed on Vercel
- [ ] Backend deployed (Railway/Render/etc.)
- [ ] OpenAI domain allowlist configured
- [ ] Environment variables documented
- [ ] Demo video < 90 seconds

### Testing
- [ ] All natural language commands working
- [ ] Conversation persistence verified
- [ ] Multi-user isolation tested
- [ ] Server restart doesn't lose conversations

---

## 🎯 Success Metrics

### Functional Completeness
- All 5 basic features accessible via natural language
- Conversation history persists across sessions
- Multi-user support with proper isolation

### Code Quality
- 100% spec-driven (no manual code)
- Stateless architecture verified
- MCP tools properly abstracted
- JWT authentication enforced

### User Experience
- Natural language understanding works
- Response time < 3 seconds
- Error messages user-friendly
- Conversation feels natural

---

## 🔄 Version History

- **v1.0** (2026-01-08): Initial constitution for Phase 3
- Architecture finalized: Stateless + MCP + OpenAI Agents SDK
- Technology stack locked
- Security requirements defined

---

## 📞 Support & References

### Key Documentation
- OpenAI Agents SDK: https://platform.openai.com/docs/guides/agents
- MCP Protocol: https://github.com/modelcontextprotocol/python-sdk
- ChatKit: https://platform.openai.com/docs/guides/chatkit
- Better Auth JWT: https://www.better-auth.com/docs/concepts/jwt

### Project Context
- Phase 1: Console app (completed)
- Phase 2: Web app with auth (completed)
- **Phase 3: AI chatbot (current)**
- Phase 4: Kubernetes deployment (upcoming)
- Phase 5: Advanced cloud features (upcoming)

---

**This constitution is the supreme authority for Phase 3 development. All code, specs, and decisions must align with these principles.**

**Last Updated**: January 8, 2026
**Status**: Active
**Compliance**: Mandatory

## Response snapshot

Constitution successfully created at version 1.0.0. Document includes:

- 5 Core Architectural Principles (Stateless, MCP-First, AI Agent Orchestration, Conversation Persistence, Security-First JWT)
- Complete Technology Stack (FastAPI, OpenAI Agents SDK, MCP SDK, ChatKit, SQLModel, Better Auth)
- Database Schema Requirements (Conversation and Message tables)
- 5 MCP Tools Specification (add_task, list_tasks, complete_task, delete_task, update_task)
- Security Requirements (JWT validation, user isolation, SQL injection prevention)
- Performance Requirements (<3s chat endpoint, <500ms tool execution)
- Testing Standards (unit, integration, user acceptance)
- Spec-Driven Development Workflow (constitution → spec → implementation)
- Forbidden Practices (8 explicit prohibitions)
- Governance section with semantic versioning

All templates validated and aligned with constitution. No manual follow-up required.

## Outcome

- ✅ Impact: Initial constitution ratified for Phase 3 AI-Powered Todo Chatbot project
- 🧪 Tests: None (governance document)
- 📁 Files: Created .specify/memory/constitution.md (v1.0.0)
- 🔁 Next prompts: Write specs for chat components using /sp.specify
- 🧠 Reflection: Constitution establishes non-negotiable architectural principles. All subsequent work MUST follow spec-driven workflow. MCP tool abstraction and stateless design are critical for success.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution)
- Prompt variant (if applicable): Initial
- Next experiment (smallest change to try): Monitor adherence during implementation phase
