---
description: Head Architect -> Specialized Prompts for Parallel Execution
---
# 🏗️ Parallel Execution Workflow (Architect Mode) and Project Specifics

This workflow optimizes for massive parallelism by turning the main window into the "Architect's Desk".

## 🚀 Project Specific Workflow: Adopt Me PWA

This project has pre-defined phases in `task.md`.

1.  **Check Status:** Look at `task.md` to see which Phase is active (e.g., Phase 2: Frontend).
2.  **Get Prompts:** Open `worker_prompts.md`. This file contains pre-written, high-context prompts for the current phase.
3.  **Delegate:**
    -   Open a new window.
    -   Paste the prompt for the required role (e.g., "Worker 1: Frontend Architect").
4.  **Integrate:**
    -   When the worker finishes, copy their code/files into the main repo.
    -   Mark the task as done in `task.md`.

---

## 1. ARCHITECT PHASE (General)
-   **Analyze**: Understand the high-level goal.
-   **Structure**: Break it down into independent components.
-   **Generate Prompts**: Create specialized prompts for each worker.
    -   *CRITICAL*: Each prompt MUST include a "Context Injection" block.

## 2. DISTRIBUTION PHASE (User Action)
-   User opens multiple Antigravity Agent windows.
-   User pastes the specific prompt into each window.
-   Agents start working immediately, fully context-aware.

## 3. INTEGRATION PHASE (This Window)
-   User reports back when tasks are done.
-   Architect reviews the integration and plans the next parallel batch.
