---
description: Simulate multi-agent swarm (Router -> Coder -> Reviewer)
---
# 🪐 Virtual Swarm Protocol (No-API Mode)

This workflow enables the IDE Agent (Antigravity) to simulate the multi-agent swarm behavior without requiring external API keys.

1.  **ROUTER PHASE**
    -   Analyze the user request: "{{user_input}}"
    -   Identify necessary functional roles:
        -   **Coder**: For implementation.
        -   **Researcher**: For checking docs/files.
        -   **Reviewer**: For quality/security checks.
    -   Output a **Delegation Plan** (list of subtasks).

2.  **EXECUTION PHASE (Sequential)**
    -   Execute the subtasks in order.
    -   *Constraint*: Do not ask for user permission between subtasks unless critical (e.g., deleting files). Assume the persona of the specialized agent (e.g., "🤖 [CODER] Implementing feature...").

3.  **REVIEW PHASE**
    -   After execution, switch to **Reviewer** persona.
    -   Verify changes against `.antigravity/rules.md`.
    -   Run tests if applicable (`pytest`).

4.  **SYNTHESIS**
    -   Present a final report summarizing the work of all agents.
