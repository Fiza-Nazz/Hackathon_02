# Tasks: Conversational AI Chatbot Foundation

**Input**: Design documents from `/specs/004-chatbot-db-mcp/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, research.md, contracts/

**Tests**: Unit and integration tests included for model and tool verification

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `tests/` at repository root
- Paths below match plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend/models/__init__.py to export all models
- [x] T002 Create backend/mcp_server/__init__.py to export server and tools
- [x] T003 [P] Create backend/mcp_server/tools/__init__.py to export all tool functions
- [x] T004 [P] Install required Python packages: sqlmodel, mcp, pydantic, pytest, pytest-asyncio, pytest-mock, asyncpg

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create database migration script in backend/migrations/003_add_conversation_tables.py with upgrade() and downgrade() functions
- [x] T006 [P] Create Pydantic schemas in backend/mcp_server/schemas.py for all tool inputs/outputs (AddTaskInput, ListTasksInput, CompleteTaskInput, DeleteTaskInput, UpdateTaskInput, SuccessResponse, ErrorResponse)
- [x] T007 [P] Create MCP server skeleton in backend/mcp_server/server.py with list_tools() and call_tool() decorators
- [x] T008 [P] Create Conversation model in backend/models/conversation.py with SQLModel base class, all fields, and relationships
- [x] T009 [P] Create Message model in backend/models/message.py with SQLModel base class, all fields, and relationships
- [ ] T010 Run migration 003_add_conversation_tables.py upgrade to create conversations and messages tables in database (requires DATABASE_URL)
- [x] T011 Create base error response helper function in backend/mcp_server/schemas.py for standardizing error returns (INVALID_INPUT, NOT_FOUND, UNAUTHORIZED, DATABASE_ERROR)
- [ ] T012 Verify database tables created by checking indexes and constraints in PostgreSQL (requires DATABASE_URL)

**Checkpoint**: Foundation ready - database schema, models, MCP server structure, and error handling complete. User story implementation can now begin.

---

## Phase 3: User Story 1 - Persistent Chat History (Priority: P1) 🎯 MVP

**Goal**: Enable users to have persistent conversations that survive sessions and device switches.

**Independent Test**: Create conversation, add messages, simulate logout/login, verify all messages still accessible in chronological order.

### Tests for User Story 1

- [x] T013 [P] [US1] Unit test for Conversation model in tests/unit/test_conversation_model.py (test creation, relationships, cascade behavior)
- [x] T014 [P] [US1] Unit test for Message model in tests/unit/test_message_model.py (test creation, role validation, tool_calls storage)
- [x] T015 [US1] Integration test for conversation persistence in tests/integration/test_conversation_persistence.py (test multi-message scenario, retrieval order)
- [x] T016 [US1] Integration test for message persistence in tests/integration/test_message_persistence.py (test cross-session retrieval, chronological order)

### Implementation for User Story 1

- [x] T017 [US1] Update backend/models/__init__.py to export Conversation and Message models
- [x] T018 [US1] Update backend/mcp_server/server.py to import and expose all 5 MCP tools
- [x] T019 [US1] Create conversation creation utility in backend/mcp_server/server.py helper functions for use by chat endpoint (future)
- [ ] T020 [US1] Verify cascade deletion works by running test scenarios from T013 and T015 (requires DATABASE_URL)

**Checkpoint**: User Story 1 complete - conversations and messages persist, relationships work, cascade deletion verified (tests written, running requires DATABASE_URL).

---

## Phase 4: User Story 2 - Create Tasks via Natural Language (Priority: P2)

**Goal**: Users can add tasks through natural language commands via AI assistant.

**Independent Test**: Send natural language phrases (add groceries, remind me to call mom, create task for meeting), verify tasks created with correct titles and descriptions.

### Tests for User Story 2

- [x] T021 [P] [US2] Unit test for add_task tool in tests/unit/test_add_task_tool.py (test valid input, title validation, description validation, user isolation)
- [x] T022 [US2] Unit test for error handling in add_task in tests/unit/test_add_task_tool.py (test empty title, title too long, description too long, database error)

### Implementation for User Story 2

- [x] T023 [P] [US2] Implement add_task tool in backend/mcp_server/tools/add_task.py with user_id parameter, title validation, description validation
- [x] T024 [US2] Add structured error handling in backend/mcp_server/tools/add_task.py (INVALID_INPUT for validation failures, DATABASE_ERROR for db failures)
- [x] T025 [US2] Verify add_task returns correct format in backend/mcp_server/tools/add_task.py (task_id, status, title)
- [x] T026 [US2] Import and register add_task in backend/mcp_server/server.py for MCP tool discovery
- [ ] T027 [US2] Run integration test to verify task created with correct user association and data isolation (requires DATABASE_URL)

**Checkpoint**: User Story 2 complete - add_task tool works, validates input, enforces user isolation (testing requires DATABASE_URL).

---

## Phase 5: User Story 3 - View and Manage Tasks via Chat (Priority: P3)

**Goal**: Users can list, complete, update, and delete tasks through natural language commands.

**Independent Test**: Create multiple tasks, then use natural language to list (with filters), complete, update, and delete them, verifying each operation succeeds and user isolation maintained.

### Tests for User Story 3

- [ ] T028 [P] [US3] Unit test for list_tasks tool in tests/unit/test_list_tasks_tool.py (test all tasks, pending only, completed only, invalid status)
- [ ] T029 [P] [US3] Unit test for complete_task tool in tests/unit/test_complete_task_tool.py (test success, task not found, idempotent when already complete)
- [ ] T030 [P] [US3] Unit test for delete_task tool in tests/unit/test_delete_task_tool.py (test success, task not found, ownership verification)
- [ ] T031 [P] [US3] Unit test for update_task tool in tests/unit/test_update_task_tool.py (test update title only, description only, both, neither, not found)
- [ ] T032 [US3] Security test for user isolation in tests/security/test_user_isolation.py (test cross-user access prevention for all 4 read/write tools)
- [ ] T033 [US3] Integration test for MCP tool coordination in tests/integration/test_mcp_tool_integration.py (test full workflow: add, list, complete, update, delete)

### Implementation for User Story 3

#### list_tasks
- [ ] T034 [P] [US3] Implement list_tasks tool in backend/mcp_server/tools/list_tasks.py with user_id and optional status parameter
- [ ] T035 [US3] Add status filtering logic in backend/mcp_server/tools/list_tasks.py (all, pending, completed with default to all)
- [ ] T036 [US3] Verify list_tasks returns correct format in backend/mcp_server/tools/list_tasks.py (tasks array with id, title, completed, created_at, total count)
- [ ] T037 [US3] Import and register list_tasks in backend/mcp_server/server.py

#### complete_task
- [ ] T038 [P] [US3] Implement complete_task tool in backend/mcp_server/tools/complete_task.py with user_id and task_id parameters
- [ ] T039 [US3] Add idempotency check in backend/mcp_server/tools/complete_task.py (no error if task already complete)
- [ ] T040 [US3] Verify complete_task returns NOT_FOUND for non-existent tasks in backend/mcp_server/tools/complete_task.py
- [ ] T041 [US3] Import and register complete_task in backend/mcp_server/server.py

#### delete_task
- [ ] T042 [P] [US3] Implement delete_task tool in backend/mcp_server/tools/delete_task.py with user_id and task_id parameters
- [ ] T043 [US3] Add title retrieval before deletion in backend/mcp_server/tools/delete_task.py to return task title in response
- [ ] T044 [US3] Verify delete_task returns NOT_FOUND for non-existent tasks in backend/mcp_server/tools/delete_task.py
- [ ] T045 [US3] Import and register delete_task in backend/mcp_server/server.py

#### update_task
- [ ] T046 [P] [US3] Implement update_task tool in backend/mcp_server/tools/update_task.py with user_id, task_id, optional title and description
- [ ] T047 [US3] Add validation for at least one field provided in backend/mcp_server/tools/update_task.py
- [ ] T048 [US3] Verify update_task returns NOT_FOUND for non-existent tasks in backend/mcp_server/tools/update_task.py
- [ ] T049 [US3] Import and register update_task in backend/mcp_server/server.py

**Checkpoint**: User Story 3 complete - All 4 tools (list, complete, delete, update) implemented and tested. User isolation verified across all tools.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T050 Run full test suite to verify all unit, integration, and security tests pass
- [ ] T051 [P] Update README.md with MCP server setup instructions and usage examples
- [ ] T052 [P] Update CLAUDE.md if needed with new implementation details or patterns used
- [ ] T053 Verify database migration can be rolled back by running downgrade and confirming tables removed
- [ ] T054 [P] Verify all MCP tools are registered and discoverable by starting server and listing tools
- [ ] T055 [P] Verify performance requirements by measuring tool execution times (target <500ms per tool)
- [ ] T056 Run quickstart.md validation to ensure setup instructions work end-to-end
- [ ] T057 Final code review for consistency with constitution principles (stateless, MCP-first, security-first)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on other stories
  - User Story 3 (P3): Can start after Foundational - No dependencies on other stories
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before tools
- Tools before server integration
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- All 4 MCP tools in User Story 3 marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Conversation model in tests/unit/test_conversation_model.py"
Task: "Unit test for Message model in tests/unit/test_message_model.py"
Task: "Integration test for conversation persistence in tests/integration/test_conversation_persistence.py"
Task: "Integration test for message persistence in tests/integration/test_message_persistence.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch all tests and implementations for add_task together:
Task: "Unit test for add_task tool in tests/unit/test_add_task_tool.py"
Task: "Unit test for error handling in add_task in tests/unit/test_add_task_tool.py"
Task: "Implement add_task tool in backend/mcp_server/tools/add_task.py"
Task: "Add structured error handling in backend/mcp_server/tools/add_task.py"
```

---

## Parallel Example: User Story 3

```bash
# Launch all 4 tools in parallel:
Task: "Implement list_tasks tool in backend/mcp_server/tools/list_tasks.py"
Task: "Implement complete_task tool in backend/mcp_server/tools/complete_task.py"
Task: "Implement delete_task tool in backend/mcp_server/tools/delete_task.py"
Task: "Implement update_task tool in backend/mcp_server/tools/update_task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Persistent Chat History)
4. **STOP and VALIDATE**: Test conversation and message persistence independently
5. Verify database schema, relationships, and cascade deletion work
6. **MVP DELIVERABLE**: Users can have persistent conversations that survive restarts

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Database persistence verified (MVP!)
3. Add User Story 2 → Test independently → Task creation via MCP tool works
4. Add User Story 3 → Test independently → All 5 MCP tools functional
5. Complete Polish phase → Full feature ready
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (models and persistence)
   - Developer B: User Story 2 (add_task tool)
   - Developer C: User Story 3 (4 remaining tools)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing where applicable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All MCP tools enforce user isolation via user_id filtering
- All tools return structured success/error responses
- Constitution principles enforced throughout (stateless, MCP-first, security-first)
- Total tasks: 57
- Tasks per user story: US1 (8), US2 (7), US3 (26), Shared (16)
