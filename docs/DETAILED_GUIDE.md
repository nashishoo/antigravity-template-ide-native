# Antigravity Workspace: Detailed Guide

**A comprehensive guide to the Parallel Architect Workflow and IDE-Native features.**

## 1. Overview
**Mission:** Provide a zero-config, parallel-execution environment for AI agents within the Antigravity IDE.
**Core Philosophy:** "The Architect and the Workers" - A human-in-the-loop parallel processing model.

---

## 2. Step 0: Context Configuration (The Foundation)
Before the Architect can start, the "Brain" of the operation must be configured in `mission.md`. This file contains the System Prompt that defines the Architect's current goal.

### How to Configure `mission.md`
The file has two distinct parts:
1.  **Editable Core (Lines 1-6):** This is where you define WHAT you want to build.
2.  **Static Framework (Lines 7+):** This defines HOW the agent works (the Parallel Architect persona). **Do not touch this part** unless you want to change the agent's fundamental behavior.

### Recommended Workflow: "Prompt Engineering via Superior Models"
Do not write the mission from scratch. Use a superior reasoning model (like Sonnet 4.5, Opus 4.6, GPT-5, or Gemini 3 Pro) to generate a high-quality mission statement.

**Prompt for the External Model:**
> "I need to configure an AI Architect agent to build [YOUR PROJECT IDEA]. Please generate a concise but detailed 'Objective' and 'Description' for a `mission.md` file. The goal should be specific, measurable, and broken down into high-level phases. Output ONLY the Objective and Description text."

**What to Paste into `mission.md`:**
```markdown
# Agent Mission: Parallel Execution Architect

# [EDIT THIS PART]
**Objective:** [Paste the AI-generated objective here]

## Description
[Paste the AI-generated description here]
# [END EDIT]

# [DO NOT TOUCH]
Your primary role is NOT to write all the code yourself...
(Keep the rest of the file as is)
```

---

## 3. The Architect's Role
The "Main Window" agent acts as the **Head Architect**.

### Key Responsibilities:
1.  **Strategy & Planning:** Break down high-level user missions into independent parallel tasks.
2.  **Skill Scouting (Preflight):**
    -   The Architect **MUST** run the `.agent/workflows/preflight.md` workflow before delegation.
    -   **Discovery Sources:**
        1.  **Local Core:** `src/skills/` (e.g., `research`, `planning-with-files`).
        2.  **Local Registry:** Custom paths defined in `.agent/skills.json`.
        3.  **Remote:** `skills.sh` catalog and `awesome-agent-skills` repository.
3.  **Prompt Generation:**
    -   Creates specialized prompts for "Workers" (Coders, Reviewers, etc.).
    -   **Context Injection:** Each prompt includes a `## CONTEXT` block with project rules and `## SUGGESTED SKILLS`.

---

## 4. Worker Capabilities
Workers are specialized agents running in separate IDE windows. They receive a high-context prompt from the Architect and execute locally.

### Capabilities:
-   **Autonomous Execution:** Workers have full file system access and terminal control.
-   **Persistent Memory:** They rely on the **Planning with Files** skill.
    -   **Mechanism:** Instead of keeping everything in context, workers maintain `task_plan.md`, `findings.md`, and `progress.md` on disk.
    -   **Benefit:** Allows for long-running, complex tasks without context window exhaustion.

---

## 5. Skill System Architecture
The project uses a hybrid skill system (Native + External).

### Skill Loading
-   **Dynamic Discovery:** Recursively scans `src/skills/` and any paths in `.agent/skills.json` at startup.
-   **Hybrid Loading:**
    -   **Code:** If `tools.py` exists, its functions are registered as executable tools.
    -   **Knowledge:** If `SKILL.md` exists, its content is injected into the agent's system prompt.

### IDE-Native Skill Discovery
Your workspace is equipped with an expanded "Skill Scout" capability:
-   **Local Flexibility:** Bring your own private skill libraries via `.agent/skills.json`.
-   **Community Access:** The Architect scrapes `awesome-agent-skills` for community tools.

---

## 6. Governance
-   **Parallel Execution:** Verified via `parallel_architect.md`.
    - Flow: `User -> Architect -> [Context + Prompt] -> Worker(s) -> [Code + Artifacts] -> User`.
-   **Change Management:** `openspec/` directory contains the governance model for proposing complex changes.
