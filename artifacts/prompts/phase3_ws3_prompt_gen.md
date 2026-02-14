# 🚀 MISSION: Smart Prompt Generator

## MODEL RECOMMENDATION FOR USER
**For this specific task, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Opus 4.5 (Thinking)** (or 3.5 Sonnet if Opus unavailable)
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Prompt engineering requires high nuancing and understanding of "Meta-Context".

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Gemini 2.0 Flash Thinking
**Phase 2 Status:** ✅ COMPLETE.

## CONTEXT
- **Improvement Goal:** Automate the creation of these "Worker Prompts" we've been writing manually.
- **Root Cause:** Writing high-quality, context-aware prompts (with "Meta-Context", "Checklists", "Constraints") is tedious and error-prone.
- **Solution:** A Jinja2-based generator that pulls state from `ACTIVE.md`, `PLAN.md`, and creates a prompt file.

## PREREQUISITE
- `src/tools/_common.py`
- `PLAN.md` (Source of workstream definitions)
- `.context/ACTIVE.md` (Source of project status)

## YOUR SPECIFIC TASK

### 1. Create `src/tools/templates/worker_prompt.j2`

Create a Jinja2 template for the standard Agent Prompt format. It should include:
- Header: `# 🚀 MISSION: {{ title }}`
- Meta-Context Section (Parent Project, Architect, Dependencies)
- Context Section (Project Root, Tech Stack — read from `ACTIVE.md`?)
- Task Section (Dynamic based on specific workstream)
- Definition of Done

### 2. Create `src/tools/generate_worker_prompt.py`

```python
"""Smart Prompt Generator.

Generates tailored worker prompts using project context.
"""
import jinja2
from tools._common import resolve_project_root, parse_yaml_frontmatter, safe_write_file

def generate_prompt(workstream_id: str, plan_path: str = "PLAN.md") -> dict:
    """Generate a prompt for a specific workstream defined in PLAN.md.
    
    1. Read PLAN.md, find the workstream (title, role, model, deliverables).
    2. Read ACTIVE.md (project name, current phase).
    3. Render the jinja2 template.
    4. Save to artifacts/prompts/.
    """
```

*Note: You will need to parse PLAN.md to extract workstream details. You can import `src.tools.plan_sync` (created in Phase 1) to help with this! It has `parse_plan()`.*

### 3. Write Tests (`tests/test_prompt_gen.py`)

- Mock `PLAN.md` and `ACTIVE.md`.
- Verify generated markdown contains expected sections.

## Constraints
- [ ] Use `jinja2` (Add to requirements.txt if missing, but it was likely added in Phase 2 or is standard). If not present, use standard python string formatting as fallback, but ideally use Jinja2 for complexity.
- [ ] Import from `tools.plan_sync` to avoid re-parsing PLAN.md.
- [ ] Follow coding style.

## OUTPUTS
- [ ] `src/tools/templates/worker_prompt.j2`
- [ ] `src/tools/generate_worker_prompt.py`
- [ ] `tests/test_prompt_gen.py`

---
**Remember:** You are building the "Agent duplicator". The prompts you generate must be high quality.
