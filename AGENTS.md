<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Repository Agent Guide (Antigravity IDE Edition)

This repo is the **Antigravity Workspace Template**.
It follows the **Parallel Architect Workflow**.

## Core Rules (`.antigravity/rules.md`)
1.  **Read Context First**: Before coding, read `mission.md` and `CONTEXT.md`.
2.  **Preflight Check (Architect Only)**: Use `.agent/workflows/preflight.md` to verify skills before delegation.
3.  **Use Skills**: Use `src/skills/planning-with-files` for complex tasks.
4.  **Artifact-First**: Create plans in `artifacts/` before executing.

## Workflow: Parallel Architect
- **Role**: You are likely a "Worker" (Coder, Reviewer, Researcher) delegated by the Head Architect.
- **Input**: You will receive a specific Prompt with injected context.
- **Output**:
    - Code changes.
    - `task_plan.md` updates.
    - Final report to the user.

## Must-Read Files
- `mission.md`: The current project objective.
- `CONTEXT.md`: The architectural source of truth.
- `.agent/workflows/parallel_architect.md`: The workflow definition.
- `src/skills/planning-with-files/SKILL.md`: Instructions for using persistent memory.

## Code Style
- **Python**: Follow Google Style Guide. Type hints and docstrings are mandatory.
- **Tools**: Place new scripts in `src/tools/`.
- **Testing**: Use `pytest`. Store logs in `artifacts/logs/`.

## Do Not Use
- Do not look for `src/agent.py` (Legacy engine removed).
- Do not run `python src/agent.py`.
