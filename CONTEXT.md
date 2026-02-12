# 🧠 AI-Optimized Project Context: Antigravity Workspace Template (IDE-Native)

## 1. Executive Summary & Core Mission
**Project Name:** Antigravity Workspace Template (IDE Edition)
**Mission:** To provide a "Zero-Config," enterprise-grade starter kit for building autonomous AI agents directly within the Antigravity IDE.

**Core Philosophy: "Parallel Architect Workflow"**
1.  **Architect (You + Main Window):** Defines strategy, **scouts for skills**, and generates prompts for specialized workers.
2.  **Workers (New Windows):** Execute specific tasks in parallel using the provided prompts and installed skills.

**Architect Preflight Requirement**
Before delegating any work, the Architect MUST run the preflight workflow at `.agent/workflows/preflight.md` to:
- Inventory local skills under `src/skills/`.
- Check skills.sh / `npx skills` availability.
- Provide evidence of any skills suggested to workers.

## 2. Cognitive Architecture (`.context/`)
*   **`coding_style.md`**: Strict coding standards that all agents automatically follow.
*   **`system_prompt.md`**: Core persona definition.
*   **`src/skills/planning-with-files/`**: Native skill for persistent memory. Use it to create `task_plan.md` for complex tasks.

## 3. Skill System
- **Location**: `src/skills/` (default) and paths in `.agent/skills.json`.
- **Structure**: Each skill is a folder with `SKILL.md` (docs) and `tools.py` (code).
- **Discovery**:
    - Local: Recursively scans `src/skills` and registered directories.
    - Remote: Can search [awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) and [skills.sh](https://skills.sh).

## 4. Key Directories
*   **`.agent/workflows/`**: Defines the role of the Architect and the Swarm protocol.
*   **`src/tools/`**: Place any Python utility script here, and the agents will automatically be able to use it.
*   **`openspec/`**: Use this for proposing and validating complex changes.
*   **`artifacts/`**: All plans, logs, and evidence must be saved here.

## 5. How to Interact
1.  **Day 1:** Edit `mission.md` to define your goal.
2.  **Act:** Tell the Main Agent (Architect) to break down the work.
3.  **Distribute:** Copy-paste the generated prompts into new agent windows.

## 6. Artifact-First Workflow
- For complex code changes, create a plan file in `artifacts/plan_[task_id].md`.
- Store test/log output in `artifacts/logs/`.
- If UI is modified, include a screenshot artifact.

## 7. Coding Standards
- **Type hints are required** for all function signatures.
- **Docstrings are required** for functions/classes; use Google-style format.
- **Use Pydantic** for data models and settings.
- **External API calls** must be wrapped in tools under `src/tools/`.
