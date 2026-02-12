# Plan: Preflight Skills Workflow + Tools

## Goals
- Add a dedicated preflight workflow for the Architect before delegating work.
- Provide tools to inspect local skills and consult the skills.sh ecosystem.
- Update Architect prompt to require preflight before delegation.

## Tasks
1. Create `.agent/workflows/preflight.md` describing the Architect-only pre-inspection sequence.
2. Add `src/tools/skills_catalog.py` with:
   - `list_local_skills()` for local SKILL.md discovery.
   - `search_skills_catalog()` to fetch skills.sh query results (best-effort HTML parse).
   - `check_npx_skills_available()` to detect Node/npx availability.
3. Update `.context/system_prompt.md` and `.agent/workflows/parallel_architect.md` to mandate preflight and reference tools.
4. Update `CONTEXT.md` to explain the preflight requirement and skills.sh integration.

## Verification
- Run `pytest` (no tests yet for tools; ensure no syntax errors).
- Optionally run `python -m py_compile src/tools/skills_catalog.py`.
