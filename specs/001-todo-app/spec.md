# Feature Specification: Phase I — In-Memory Python Todo CLI (Strict Compliance)

**Feature**: Phase I Console Todo App
**Created**: 2026-01-03
**Updated (Strict Compliance)**: 2026-01-10

## Overview

Build a simple, single-user Todo application that runs in the terminal and stores all data **in memory only** (no database, no file persistence). The user manages tasks via a menu-driven console interface.

This phase must be delivered using **Spec-Driven Development** artifacts (spec → plan → tasks → implementation) and a clean Python project structure.

## In Scope

### Core task features (Basic Level — all required)
1. **Add Task**: title (required) + description (optional)
2. **View Task List**: show ID + title + completion status
3. **Update Task**: update title and/or description by ID
4. **Delete Task**: delete by ID
5. **Mark as Complete**: toggle completed/incomplete by ID

### Tooling / structure requirements (Hackathon Phase I)
- Python **3.13+**
- **uv**-managed project with `pyproject.toml` and `uv.lock`
- Code organized under `/src` (separation of concerns)
- `README.md` includes setup/run instructions
- `CLAUDE.md` exists (project rules)

## Out of Scope
- Authentication
- Multi-user support
- Web UI
- Database storage (SQLite/Postgres/etc.)
- AI chatbot

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Create a task (P1)
A user wants to add a new task with a required title and an optional description.

**Acceptance Scenarios**:
1. Given the user chooses “create task”, when they provide a non-empty title, then the task is created with a unique ID and `completed = false`.
2. Given the user provides an empty title, when they submit, then the system rejects it with an immediate error message.

### User Story 2 — View tasks (P1)
A user wants to see all tasks with their status.

**Acceptance Scenarios**:
1. Given tasks exist, when the user views tasks, then the list shows each task’s ID, title, and completion status.
2. Given no tasks exist, when the user views tasks, then the system shows “no tasks” message.

### User Story 3 — Update a task (P2)
A user wants to update an existing task’s title and/or description.

**Acceptance Scenarios**:
1. Given a task exists, when the user provides a valid ID and new values, then the task updates.
2. Given an invalid/non-existent ID, when the user updates, then the system reports “task not found”.

### User Story 4 — Delete a task (P2)
A user wants to delete a task by ID.

**Acceptance Scenarios**:
1. Given a task exists, when the user deletes by ID, then the task is removed.
2. Given an invalid/non-existent ID, when the user deletes, then the system reports “task not found”.

### User Story 5 — Toggle completion (P2)
A user wants to mark a task complete/incomplete.

**Acceptance Scenarios**:
1. Given a task is incomplete, when the user toggles completion, then it becomes complete.
2. Given a task is complete, when the user toggles completion, then it becomes incomplete.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST allow creating tasks with required `title` and optional `description`.
- **FR-002**: System MUST assign a unique task ID.
- **FR-003**: System MUST list all tasks with `id`, `title`, and `completed`.
- **FR-004**: System MUST update `title` and/or `description` for an existing task by ID.
- **FR-005**: System MUST delete a task by ID.
- **FR-006**: System MUST toggle completion status by ID.
- **FR-007**: System MUST provide immediate feedback for invalid actions.

### Non-Functional Requirements
- **NFR-001**: Data MUST remain in memory only and be lost on process exit.
- **NFR-002**: Project MUST be runnable via uv with Python 3.13+.
- **NFR-003**: Console output MUST be readable and consistent.

### Key Entities
- **Task**: `{ id, title, description?, completed }`

## Success Criteria *(mandatory)*
- **SC-001**: A user can complete all 5 core operations in one session without errors.
- **SC-002**: Invalid inputs (empty title, bad ID) are rejected with clear feedback.
- **SC-003**: No task data persists after the program exits.
- **SC-004**: Project runs with Python 3.13+ via uv (`pyproject.toml` + `uv.lock`).
