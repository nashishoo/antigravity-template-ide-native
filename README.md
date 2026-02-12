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
> **Stuck?** Check out the [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

### 1. Define Your Mission
Edit `mission.md` with the goal of your project.
> Example: "Create a REST API for inventory management."

### 2. Activate the Architect
In the main chat window, say:
> "I updated the mission. Act as Architect and give me prompts for my workers."

### 3. Distribute the Work (Parallel Mode)
The Architect will analyze your mission, **scan available skills**, and return copy-paste prompts.
* **Open a new chat window** -> Paste the **Coder** prompt.
* **Open another window** -> Paste the **Reviewer** prompt.

Your agents will work in parallel with built-in tooling.

## Native Features

### Persistent Memory (`planning-with-files`)
The template ships with a native skill for long-term memory.
* Your agents automatically create `task_plan.md` and `findings.md`.
* This makes complex decisions persistent between sessions.

### Skill Scouting
The Architect can review installed skills in `src/skills/` and suggest them in worker prompts.

## Project Structure

```
.agent/workflows/   # Role and workflow definitions (Architect, Swarm)
.context/           # Automated rules (Coding Style)
src/tools/          # Custom tools (Python, optional)
src/skills/         # Installed skills (planning-with-files, etc.)
openspec/           # Change management system (Specs)
mission.md          # Project objective
artifacts/          # Generated plans and documentation
```

## Tools
Any Python script you add to `src/tools/` will be auto-discovered by agents. Use this folder for project-specific utilities.

## OpenSpec
For complex changes, use the OpenSpec system in the `openspec/` folder.

## Credits and License
This project is an **IDE-Native fork** of the original [Antigravity Workspace Template](https://github.com/filosofia-codigo/antigravity-workspace-template).
* **License**: MIT (see `LICENSE`).
* **Original Author**: Jingwen Fan.
* **IDE-Native Edition (2026)**: Built by **Catapaz** in collaboration with **Gemini 3**.
* **Modifications**: Adapted for parallel execution without external Python/API dependencies.
