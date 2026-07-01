# Engineering Constitution for AI Agents

> This repository is an AI Agent Platform.
> Stability, consistency, and extensibility are more important than introducing new ideas.
> Every change should integrate into the existing architecture instead of reshaping it.

These principles override implementation preferences unless explicitly instructed otherwise.

---

# 1. Understand Before You Modify

Before writing code:

- Understand the actual goal.
- Read the relevant implementation.
- Understand how the module fits into the system.
- Identify the root cause.
- Consider the impact on related modules.

Never implement immediately after reading a request.

If requirements are unclear, ask instead of assuming.

---

# 2. Search Before You Create

Before implementing:

- Search existing implementations.
- Search shared utilities.
- Search reusable components.
- Search existing services.
- Search plugin interfaces.
- Search workflow mechanisms.

Do not assume functionality does not already exist.

Reuse before creating.

---

# 3. Integrate, Don't Reinvent

Extend the existing architecture.

Prefer reusing:

- Services
- APIs
- Components
- Plugin interfaces
- Workflow mechanisms

Consistency is preferred over novelty.

---

# 4. Minimal, Targeted Changes

Every change should be as small as possible.

- Modify only what is required.
- Do not refactor unrelated modules.
- Do not reorganize project structure.
- Do not rename existing APIs.
- Do not perform unrelated cleanup.

If ten lines solve the problem, do not rewrite one hundred.

---

# 5. Respect System Boundaries

Treat each subsystem independently:

- Frontend
- Backend
- Plugin Runtime
- Workflow Engine
- Docker Sandbox
- Database
- Agent Runtime

Avoid crossing subsystem boundaries unless required.

---

# 6. Platform Stability First

This repository is a platform.

Preserve whenever possible:

- Public APIs
- Plugin contracts
- Workflow behavior
- Data models
- Backward compatibility

A stable platform is more valuable than a "better" implementation.

---

# 7. Large Changes Require Approval

Before performing:

- Architecture redesign
- Database schema changes
- Plugin interface changes
- Workflow engine changes
- Docker runtime changes
- Public API changes
- New dependencies
- Large-scale refactoring

Explain:

- Why
- Affected files
- Risks
- Alternatives

Wait for approval before proceeding.

---

# 8. Default Assumptions

Unless instructed otherwise:

- Preserve public APIs.
- Preserve plugin contracts.
- Preserve workflow behavior.
- Preserve file structure.
- Preserve naming conventions.
- Preserve backward compatibility.

Assume existing behavior should remain unchanged.

---

# 9. Verification

Before completing work, verify:

- Existing behavior remains unchanged.
- Requested functionality works.
- No unrelated files were modified.
- No duplicate implementation was introduced.
- Architecture remains consistent.

---

# Engineering Decision Priority

1. Correctness
2. Platform Stability
3. Architectural Consistency
4. Simplicity
5. Maintainability
6. Performance

Never sacrifice maintainability for optimization.

---

# When in Doubt

If uncertain:

- Do not guess.
- Do not invent missing information.
- Read more code.
- Ask for clarification.
- Preserve existing behavior.

---

# Default Working Style

Unless instructed otherwise:

- Think before coding.
- Read before modifying.
- Search before creating.
- Reuse before implementing.
- Modify before rewriting.
- Extend before replacing.
- Verify before finishing.

Your goal is not to build a new project.

Your goal is to evolve the existing project safely, predictably, and consistently.