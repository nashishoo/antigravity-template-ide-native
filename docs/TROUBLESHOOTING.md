# 🔧 Troubleshooting Guide

## The "Parallel Architect" Workflow

### 1. "My workers are lost / hallucinating."
**Cause:** Poor Context Injection.
**Fix:** Ensure every worker prompt starts with the **Context Block**:
```markdown
## CONTEXT
- Project: [Name]
- Stack: IDE-Native
- Tooling: `src/skills/` (planning-with-files)
```
Without this, the agent doesn't know it's part of a larger system.

### 2. "I don't know what to do next."
**Cause:** Missing `task_plan.md`.
**Fix:** Ask your Architect (Main Window) to:
> "Initialize the `task_plan.md` file using the `planning-with-files` skill."
This file becomes your project's GPS.

### 3. "The agent keeps trying to run Python code and failing."
**Cause:** Ghost of the old engine.
**Fix:** Remind the agent:
> "You are an IDE-Native agent. Do not try to execute python scripts directly unless they are in `src/tools/`. Use your internal tools (edit_file, run_terminal) instead."

### 4. "How do I install new skills?"
**Cause:** Confusion about `skills.sh`.
**Fix:** Use the terminal in any window:
```bash
npx skills search [query]
npx -y skills add [skill-name]
```
Then tell the agent: "I installed [skill]. Check `src/skills/`."

## Common Errors

### `Element type is invalid...` (React)
- **Check:** Are you importing a default export as a named export?
- **Fix:** check `import X from './X'` vs `import { X } from './X'`.

### `Git push failed`
- **Check:** Did you configure your identity?
- **Fix:**
  ```bash
  git config user.name "Your Name"
  git config user.email "you@example.com"
  ```
