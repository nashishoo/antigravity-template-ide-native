# Migration Guide: v1.0 → v2.0-alpha

## Should You Upgrade Now?

v2.0-alpha is **additive**, meaning it adds new capabilities without breaking existing v1.0 workflows. However, it introduces more structure.

### ✅ Upgrade if:
*   **You experience "Context Drift":** Agents constantly forget what was decided in previous turns.
*   **You lose track of status:** You manually edit a `status.txt` or just keep it in your head.
*   **You validate manually:** You find yourself fixing broken YAML frontmatter or JSON files by hand.
*   **You hate boilerplate:** You want to generate tool scaffolding automatically.

### ⏳ Wait for v2.0 Final if:
*   **You want magic:** You are waiting for the "Smart Prompt Generator" and "Intelligent Preflight" (Phase 3).
*   **You need perfect docs:** Documentation is currently sparse (alpha).
*   **You are mid-sprint:** If you are in the middle of a critical feature, finish it first.

## What Changed (High-Level)

### New Files (Safe to Add)
*   `.context/ACTIVE.md`: **Highly Recommended.** The new brain of your project.
*   `src/tools/*`: A suite of 5 new Python tools for automation.
*   `.archive/`: A folder structure for cleanup.
*   `tests/`: Unit tests for the new tools.

### Modified Files
*   **None.** We have not modified any core v1.0 files in a breaking way.
*   *Note:* `PLAN.md` has a stricter schema if you want to use `plan_sync.py`, but your old `PLAN.md` will essentially just be ignored by the tool until you update it.

### New Dependencies
*   `pyyaml`: Required for parsing `ACTIVE.md`.
*   `pydantic`: Required for `data_validator.py` (schema validation).
*   `pytest`: Required to run the test suite.
*   `watchdog` (Optional): For the file watcher tool.

## Step-by-Step Migration

### 1. Backup Your Project
Always be safe.
```bash
git checkout -b backup-before-v2
# or just zip your project folder
```

### 2. Add v2.0 Files (Non-Destructive)
Copy the following directories from the v2.0 template to your project root:
*   `.context/`
*   `.archive/`
*   `src/tools/`
*   `tests/`
*   `specs/` (specifically `active_context_protocol.md`)

*Tip: Do NOT overwrite your existing `PLAN.md` or `mission.md` yet.*

### 3. Initialize ACTIVE.md
Create `.context/ACTIVE.md` if you didn't copy it. You can use the template in `specs/active_context_protocol.md`. This file will immediately start serving as the "Source of Truth" for any agent that knows to look for it.

### 4. Install Dependencies
Create or update your `requirements.txt` / `pyproject.toml`:
```text
pyyaml>=6.0
pydantic>=2.0
pytest>=7.0
watchdog>=3.0  # Optional
```
Install them:
```bash
pip install -r requirements.txt
```

### 5. Validate Installation
Run the validator to ensure everything is set up correctly:
```bash
python src/tools/data_validator.py
```
It should report "Validation Successful" (or tell you if `ACTIVE.md` is missing fields).

## Rollback Plan
If you decide v2.0 isn't for you yet:
1.  Delete `.context/ACTIVE.md`
2.  Delete `src/tools/` (or strictly the new files)
3.  Delete `.archive/`
4.  Your project is back to v1.0 standard.

## FAQ

**Q: Will my existing workers still work?**
A: **Yes.** v2.0 protocols are "opt-in". If a worker doesn't look for `ACTIVE.md`, they just work like they did before (with the same context limitations).

**Q: Do I HAVE to use ACTIVE.md?**
A: **No**, but we highly recommend it. It's the mechanism that stops agents from hallucinating project state.

**Q: Can I use the tools without the protocols?**
A: Mostly yes. `scaffold.py` works standalone. `archive_manager.py` works standalone. `plan_sync.py` requires `PLAN.md` to follow the new schema.
