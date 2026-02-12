# Project Context

## Purpose
**Antigravity Workspace Template (IDE-Native Edition)** is a production-grade starter kit for building parallel AI agent workflows directly inside the Antigravity IDE.
Its primary goals are to provide a minimal, transparent workspace where:
- **No external runtime is required** beyond the IDE.
- **Parallel coordination** happens through human-directed worker prompts.
- **Artifact-first workflows** keep plans, findings, and evidence in files.
- **Skills are filesystem-native** and can be discovered locally.

## Tech Stack
- **Runtime:** Antigravity IDE (IDE-native agents)
- **Language:** Optional Python utilities in `src/tools/`
- **Testing:** `pytest` when you add Python utilities

## Project Conventions

### Code Style
- **Python (optional tools):**
  - **Type Hints:** Mandatory for all function signatures (e.g., `def func(a: int) -> bool:`).
  - **Docstrings:** Google-style docstrings are required for all tools (include `Args:`, `Returns:`, `Raises:`).
  - **Pydantic:** Use Pydantic models for complex data structures.

### Architecture Patterns
- **Tool Isolation:** External I/O is encapsulated as functions in `src/tools/`.
- **Statelessness:** Tools should generally be stateless; context is passed via arguments.
- **Parallel Workflow:** The Head Architect coordinates specialized worker agents.
- **Zero-Config:** The repository is ready to use immediately after cloning.

### Testing Strategy
- **Framework:** `pytest` is the standard testing framework.
- **Scope:** Tests should cover tool behavior and integrations.
- **Safety:** Tools must fail gracefully with clear error messages.

### Git Workflow
- Standard feature-branch workflow.
- Commits should be atomic and descriptive.
- Documentation (in `docs/`) should be updated alongside code changes.

## Domain Context
- **Artifact-first:** Plans, decisions, and findings are written to files in `artifacts/`.
- **Skills-as-files:** Skills live in `src/skills/` and are referenced by agents in prompts.

## Important Constraints
- **No External Engine:** Do not reintroduce legacy Python agent runners.
- **No Hidden Config:** Avoid `.env` requirements for default usage.
