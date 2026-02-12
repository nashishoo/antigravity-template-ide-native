---
description: Head Architect -> Specialized Prompts for Parallel Execution
---
# 🏗️ Parallel Execution Workflow (Architect Mode)

This workflow optimizes for massive parallelism by turning the main window into the "Architect's Desk".

## 1. ARCHITECT PHASE (This Window)
-   **Analyze**: Understand the high-level goal.
-   **Skill Scout**: review `src/skills/` and installed skills to find tools that could solve the problem faster.
-   **Structure**: Break it down into independent components.
-   **Generate Prompts**: Create specialized prompts for each worker.
    -   *CRITICAL*: Each prompt MUST include a "Context Injection" block so the worker agent immediately understands the project structure without manual explanation.
    -   Format:
        ```markdown
        # 🚀 MISSION: [Role Name]
        
        ## CONTEXT
        - Project: Antigravity Workspace
        - Tech Stack: IDE-native agents, optional Python tools
        - Rules: Follow .context/coding_style.md
        - **TOOLING**: Use `planning-with-files` skill for any complex logic. Initialize with `task_plan.md`.
        
        ## SUGGESTED SKILLS
        - [Skill Name] (Install via: `npx -y skills add [skill_name]`) - [Reason]
        
        ## YOUR TASK
        [Specific instructions for this worker]
        
        ## DEFINITION OF DONE
        1. Code is implemented and tested.
        2. `task_plan.md` is updated.
        3. Relevant documentation (e.g. `README.md`, `CONTEXT.md` or inline docs) is updated to reflect changes.
        4. No broken links or "TODO" leftovers.
        
        ## INPUTS
        [File paths, code snippets, or data they need]
        
        ## OUTPUTS
        [What they must generate: Code, File, or Report]
        ```

## 2. DISTRIBUTION PHASE (User Action)
-   User opens multiple Antigravity Agent windows.
-   User pastes the specific prompt into each window.
-   Agents start working immediately, fully context-aware.

## 3. INTEGRATION PHASE (This Window)
-   User reports back when tasks are done.
-   Architect reviews the integration and plans the next parallel batch.
