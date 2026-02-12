# Antigravity Workspace (IDE-Native Edition)

**Starter kit for parallel AI agent development inside the Antigravity IDE.**

![Architecture](https://img.shields.io/badge/Architecture-Parallel_Workers-purple)
![Workflow](https://img.shields.io/badge/Workflow-Head_Architect-blue)

## Philosophy: "The Architect and the Workers"

This template is optimized to run **entirely inside the Antigravity IDE**, removing the need for external Python engines or complex API setup.

The workflow is **100% parallel and delegative**:

1. **You + Main Window** = **Head Architect**.
2. **Other Windows** = **Specialist Workers (Coder, Reviewer, etc.)**.

## Getting Started (Day 1)

No installation required. Your IDE already has everything it needs.
> **Stuck?** Check out the [Troubleshooting Guide](docs/TROUBLESHOOTING.md) or the **[Detailed Guide](docs/DETAILED_GUIDE.md)**.

### 1. Configure the Mission (The Foundation)
Open `mission.md`. This file contains the **System Prompt** that drives the Architect.

> **💡 Pro Tip:** Don't write the mission from scratch. Use a superior model (Sonnet 4.5, GPT-5, Gemini 3 Pro) to generate a robust Objective and Description for you. See the **[Detailed Guide](docs/DETAILED_GUIDE.md)** for the recommended prompt.

*   **Edit**: Replace the default "Objective" with your actual goal.
*   **Save**: Ensure your changes are saved.

### 2. Activate the Architect
1.  **Open Chat**: Go to the **Main Chat Window**.
2.  **Prompt**: Type something like: *"Read mission.md and start the mission"* or *"Act as the Architect defined in mission.md"*.
3.  **Send**: The Agent will read the file and assume the Architect persona.

### 3. Distribute the Work (Parallel Mode)
The Architect will return **Workers' Prompts** (formatted tasks for specific roles).
1.  **Open New Windows**: Open as many new Antigravity windows as needed (e.g., one for Coder, one for Reviewer).
2.  **Paste & Run**: Copy the specific prompt for each role into its own window.
3.  **Monitor**: Your agents are now working in parallel, fully context-aware.

### Architect Preflight
Before delegating any work, the **Architect** must run the preflight workflow to verify available skills and tools:
*   **Workflow**: `.agent/workflows/preflight.md`
*   **Purpose**: Inventory local skills, check `skills.sh` CLI, and validate tool availability.

---

## 🔥 Fast Track: Virtual Swarm (Lite Mode)

For **small tasks** or quick fixes where you don't need multiple windows, use the **Virtual Swarm** workflow.
*   **Workflow**: `.agent/workflows/swarm.md`
*   **How it works**: The agent in a *single window* simulates the roles of **Router -> Coder -> Reviewer** sequentially.
*   **Use Case**: "Refactor this function", "Fix this bug", "Write a quick script".
*   **Benefit**: Zero overhead, but slower than parallel execution for big tasks.

## Project Structure

```
.agent/workflows/   # Role and workflow definitions (Architect, Swarm, Preflight)
.context/           # Automated rules (Coding Style)
src/tools/          # Custom tools (Python, optional)
src/skills/         # Installed skills (planning-with-files, etc.)
openspec/           # Change management system (Specs)
mission.md          # Project objective
artifacts/          # Generated plans and documentation
```

## 🧠 Skills & Tools

The template comes with core skills in `src/skills/`. You can extend capabilities by:

1.  **Creating local skills:** Add new folders with `SKILL.md` and `tools.py` in `src/skills/`.
2.  **Registering external skills:** Add paths to other skill directories in `.agent/skills.json`.
3.  **Discovering community skills:**
    - Use the **Architect Preflight** workflow to search `awesome-agent-skills`.
    - Run `npx skills find <query>` if you have the [Skills CLI](https://skills.sh).

See [Local Skill Registry](docs/skills_registry.md) for configuration details.

## Tools
Any Python script you add to `src/tools/` will be auto-discovered by agents. Use this folder for project-specific utilities.
*   **`src/tools/skills_catalog.py`**: A utility to search for skills on skills.sh and list local skills.

## OpenSpec
For complex changes, use the OpenSpec system in the `openspec/` folder.

## Credits and License
This project is an **IDE-Native fork** of the original [Antigravity Workspace Template](https://github.com/filosofia-codigo/antigravity-workspace-template).
* **License**: MIT (see `LICENSE`).
* **Original Author**: Jingwen Fan.
* **IDE-Native Edition (2026)**: Built by **Catapaz** in collaboration with **Gemini 3**.
* **Modifications**: Adapted for parallel execution without external Python/API dependencies.
