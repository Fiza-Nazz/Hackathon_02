---
id: 1
title: Update Constitution AI-Native Todo App
stage: constitution
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,spec-driven,ai-native]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: AI-Native Todo Application (Spec-Driven Evolution Project)

Purpose:
This constitution defines the non-negotiable principles, quality standards,
and constraints governing the development of this project.
All AI agents and contributors MUST comply with this document
before proposing specifications, plans, or implementations.

────────────────────────────────────────
CORE PRINCIPLES
────────────────────────────────────────

1. Spec-Driven First
- No code may be written without an approved specification.
- All implementation must trace back to an explicit spec requirement.
- If behavior is unclear, the specification must be refined — not the code.

2. AI-Native Development
- The system is designed assuming AI agents as first-class developers.
- Claude Code is the primary implementation agent.
- Humans act as architects, not syntax writers.

3. Determinism over Creativity
- Predictable, reproducible behavior is preferred over creative output.
- AI agents must never invent features, endpoints, or behaviors.
- Ambiguity must halt execution until clarified in specs.

4. Progressive Evolution
- Each phase must cleanly build upon the previous phase.
- No skipping phases, shortcuts, or premature optimizations.
- Phase I simplicity must be preserved in later phases conceptually.

5. Clean Architecture
- Separation of concerns is mandatory.
- Business logic must remain independent of UI and infrastructure.
- Stateless services are preferred unless explicitly specified.

────────────────────────────────────────
QUALITY STANDARDS
────────────────────────────────────────

1. Traceability
- Every feature must map to:
  - A specification section
  - An implementation task
- Every code artifact must reference its originating task.

2. Reproducibility
- The project must be reproducible from specs alone.
- A new agent should be able to regenerate the system
  using only the specification files.

3. Consistency
- Naming, structure, and patterns must remain consistent
  across all phases and services.
- No ad-hoc styles or deviations are allowed.

4. Simplicity First
- Prefer the simplest solution that satisfies the spec.
- Avoid overengineering unless explicitly required by the phase.

────────────────────────────────────────
TECHNOLOGY CONSTRAINTS
────────────────────────────────────────

- Phase I: Python console application (in-memory only)
- Phase II: Next.js + FastAPI + SQLModel + Neon PostgreSQL
- Authentication: Better Auth with JWT
- Spec Management: Spec-Kit Plus
- Implementation Agent: Claude Code

Changing the technology stack is NOT allowed
unless the specification is formally updated and approved.

──────────────
```

## Response snapshot

The project constitution has been successfully updated with the following changes:

- New version: 1.1.0 (incremented from 1.0.0)
- Added 5 core principles: "Spec-Driven First", "AI-Native Development", "Determinism over Creativity", "Progressive Evolution", and "Clean Architecture"
- Added Quality Standards section with 4 standards: Traceability, Reproducibility, Consistency, and Simplicity First
- Added Technology Constraints section defining the technology stack for Phase I and Phase II
- Updated Governance section with the project's non-negotiable principles
- Included a Sync Impact Report at the top of the file documenting the changes made

## Outcome

- ✅ Impact: Constitution file updated with comprehensive principles for AI-native development
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new principles and constraints
- 🔁 Next prompts: Plan development based on new constitution
- 🧠 Reflection: The constitution now properly defines the non-negotiable principles for the AI-Native Todo Application project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution properly filled with all required principles
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create initial specification based on constitution