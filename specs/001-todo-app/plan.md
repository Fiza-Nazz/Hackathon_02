# Implementation Plan: Phase I — In-Memory Python Todo CLI (Strict Compliance)

**Date**: 2026-01-10
**Spec**: `specs/001-todo-app/spec.md`

## Summary

Implement a terminal-based Todo application (single-user) that supports create/list/update/delete/toggle-complete, storing tasks in **memory only**.

This plan also upgrades Phase I tooling to strict hackathon compliance: Python 3.13+ and uv (`pyproject.toml` + `uv.lock`).

## Technical Context

- **Language/Version**: Python **3.13+**
- **Dependency management**: **uv**
- **Storage**: In-memory only
- **Architecture**: Clean separation between CLI (UI), services (business logic), and storage (in-memory repository)

## Project Structure

```text
src/
├── cli/todo_app.py        # UI/menu + user input
├── services/task_service.py # business operations
├── lib/storage.py         # in-memory storage
└── models/task.py         # Task entity

specs/001-todo-app/        # spec/plan/tasks/quickstart
pyproject.toml             # uv project config
uv.lock                    # uv lockfile
.python-version            # pinned Python version
```

## Key Decisions

1. **In-memory storage** (dict) is the single source of truth in Phase I.
2. **No DB/files** are used for Phase I behavior.
3. **uv** is used for reproducible setup and strict Python 3.13+ targeting.

## Acceptance Checks

- [ ] `uv run --python 3.13.3 todo-app` starts the CLI
- [ ] Create/list/update/delete/toggle work in a single run
- [ ] Restarting the app shows an empty list (no persistence)
