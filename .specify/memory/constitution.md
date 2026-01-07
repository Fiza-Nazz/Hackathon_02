<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → "Spec-Driven First", [PRINCIPLE_2_NAME] → "AI-Native Development", [PRINCIPLE_3_NAME] → "Determinism over Creativity", [PRINCIPLE_4_NAME] → "Progressive Evolution", [PRINCIPLE_5_NAME] → "Clean Architecture"
Added sections: Quality Standards section, Technology Constraints section
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# AI-Native Todo Application (Spec-Driven Evolution Project) Constitution

## Core Principles

### Spec-Driven First
No code may be written without an approved specification. All implementation must trace back to an explicit spec requirement. If behavior is unclear, the specification must be refined — not the code.

### AI-Native Development
The system is designed assuming AI agents as first-class developers. Claude Code is the primary implementation agent. Humans act as architects, not syntax writers.

### Determinism over Creativity
Predictable, reproducible behavior is preferred over creative output. AI agents must never invent features, endpoints, or behaviors. Ambiguity must halt execution until clarified in specs.

### Progressive Evolution
Each phase must cleanly build upon the previous phase. No skipping phases, shortcuts, or premature optimizations. Phase I simplicity must be preserved in later phases conceptually.

### Clean Architecture
Separation of concerns is mandatory. Business logic must remain independent of UI and infrastructure. Stateless services are preferred unless explicitly specified.

## Quality Standards

### Traceability
Every feature must map to:
  - A specification section
  - An implementation task
Every code artifact must reference its originating task.

### Reproducibility
The project must be reproducible from specs alone.
A new agent should be able to regenerate the system
using only the specification files.

### Consistency
Naming, structure, and patterns must remain consistent
across all phases and services.
No ad-hoc styles or deviations are allowed.

### Simplicity First
Prefer the simplest solution that satisfies the spec.
Avoid overengineering unless explicitly required by the phase.

## Technology Constraints

- Phase I: Python console application (in-memory only)
- Phase II: Next.js + FastAPI + SQLModel + Neon PostgreSQL
- Authentication: Better Auth with JWT
- Spec Management: Spec-Kit Plus
- Implementation Agent: Claude Code

Changing the technology stack is NOT allowed
unless the specification is formally updated and approved.

## Governance

The constitution defines the non-negotiable principles, quality standards,
and constraints governing the development of this project.
All AI agents and contributors MUST comply with this document
before proposing specifications, plans, or implementations.

**Version**: 1.1.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-03