---
description: Architect preflight inspection before delegation.
---
# Preflight Workflow (Architect Only)

Run this workflow in the main window before delegating tasks or claiming the
existence of skills/tools. Record findings in your summary to keep the
parallel workflow grounded in reality.

## 1. Local Skills Inventory
- Use `list_local_skills()` to enumerate all `SKILL.md` files under `src/skills/`.
- Note any nested skill packs (e.g. `.agents/skills/*`).
- If required skills are missing, call it out explicitly.

## 2. skills.sh / Skills CLI Check
- Use `check_npx_skills_available()` to confirm whether `node`/`npx` exist.
- If available, recommend `npx skills find <query>` for detailed catalog searches.
- If not available, explicitly report the missing dependency and suggest install.

## 3. External Skill Discovery
- Use `search_skills_catalog("<query>")` to scan `skills.sh` for relevant skills.
- Provide top 3-5 matches with install commands (`npx skills add owner/repo@skill`).
- If results are empty, suggest refining keywords or using `npx skills find`.

## 4. Delegation Gate
- Only after the above checks, generate worker prompts and tasks.
- Include a "Skills Evidence" section in prompts with the skills you verified.
