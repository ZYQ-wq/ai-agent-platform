# Engineering Constitution

> This repository is an AI Agent Platform. Stability, consistency, and extensibility are more important than introducing new ideas. Every change should integrate into the existing architecture instead of reshaping it.

These principles override all implementation details unless explicitly instructed otherwise.

---

# 1. Understand Before You Modify

Before writing code:

* Understand the user's actual goal.
* Read the relevant implementation first.
* Understand how the affected module fits into the overall architecture.
* Identify the root cause instead of treating symptoms.
* Think through the impact on related modules before making changes.

Never begin implementation immediately after reading a request.

If requirements are unclear, ask questions instead of making assumptions.

---

# 2. Integrate, Don't Reinvent

This project already has its own architecture.

When implementing new functionality:

* Reuse existing services.
* Reuse existing APIs.
* Reuse existing UI components.
* Reuse existing plugin interfaces.
* Reuse existing workflow mechanisms.

Avoid introducing new patterns when existing ones already solve the problem.

Consistency is always preferred over novelty.

---

# 3. Minimal, Targeted Changes

Every modification should be as small as possible.

Rules:

* Only modify code directly related to the requested task.
* Do not refactor unrelated modules.
* Do not reorganize folders.
* Do not rename existing APIs.
* Do not change project structure.
* Do not perform "cleanup" outside the task scope.

If ten lines solve the problem, do not rewrite one hundred.

---

# 4. Respect System Boundaries

This project consists of multiple independent domains:

* Frontend
* Backend
* Plugin Runtime
* Workflow Engine
* Docker Sandbox
* Database
* Agent Runtime

Treat each domain as an independent subsystem.

Never modify another subsystem simply because it is technically possible.

Changes should remain within the intended boundary whenever possible.

---

# 5. Platform Stability Comes First

This is a platform rather than a single application.

Therefore:

* Preserve backward compatibility whenever possible.
* Avoid breaking existing APIs.
* Avoid changing plugin contracts.
* Avoid changing workflow behavior.
* Avoid changing data models without necessity.

A stable platform is more valuable than a "better" implementation.

---

# 6. Large Changes Require Approval

Before performing any of the following:

* Architecture redesign
* Database schema changes
* Plugin interface changes
* Workflow engine changes
* Docker runtime changes
* Public API changes
* Introducing new dependencies
* Large-scale refactoring

First explain:

* Why the change is necessary.
* Which files will be affected.
* Potential risks.
* Alternative approaches.

Wait for confirmation before implementation.

Never perform large structural changes silently.

---

# Engineering Decision Priority

Whenever multiple implementations are possible, follow this priority:

1. Correctness
2. Platform Stability
3. Architectural Consistency
4. Simplicity
5. Maintainability
6. Performance Optimization

Never sacrifice long-term maintainability for short-term optimization.

---

# Default Working Style

Unless explicitly instructed otherwise:

* Think before coding.
* Reuse before creating.
* Modify before rewriting.
* Extend before replacing.
* Explain before restructuring.

Your goal is not to build a new project.

Your goal is to evolve the existing project safely and predictably.
