# 🚀 MISSION: Archive Hygiene Automation Specialist

## MODEL RECOMMENDATION FOR USER
**For this specific task, please:**
1. Open a new Antigravity chat window
2. Select: **Gemini 3 Flash** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Straightforward implementation — no complex architecture decisions. Flash handles file operations and simple logic efficiently.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)
**Note:** This is a parallel workstream. Workstream 1.1 (ACTIVE.md) is being worked on simultaneously by another agent. You do NOT depend on it.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture
- **Improvement Goal:** Prevent artifact sprawl and context window pollution
- **Root Cause:** Old artifacts and completed task files accumulate, clogging agent context windows
- **Success Metric:** Completed work auto-archives, keeping active workspace clean

## ORIGINAL REVIEW FEEDBACK (Exact Quotes)

**Review 1 (review_adoptme.md):**
> "Large outputs (like JSON dumps) or temporary files can clutter the workspace if not strictly directed."
> "Enforce an `artifacts/outputs/` directory structure in the template. Pre-create folders for `logs`, `data`, and `reports`."

**Review 2 (final_review_adoptme.md):**
> "Archive Hygiene: Moving old tasks to `.archive/` to keep the context window clean."

## CURRENT STATE
- `artifacts/` directory exists (currently has `architectural_reasoning_20260213.md`, `strategic_preflight_20260213.md`, and `prompts/` folder)
- No `.archive/` directory exists
- No archival conventions or scripts
- `tests/` directory is empty

## CODING STANDARDS (from `.context/coding_style.md`)
- Type hints mandatory for all function signatures
- Google-style docstrings with `Args:`, `Returns:`, `Raises:`
- Pydantic for complex data models
- Tools must fail gracefully (return error dicts, not crash)
- All tools in `src/tools/` directory

## YOUR SPECIFIC TASK

### 1. Design the `.archive/` Directory Structure

Create:
```
.archive/
├── README.md          ← Conventions doc
├── completed/         ← Finished workstreams/phases
├── deprecated/        ← Old tools/specs that were replaced
└── snapshots/         ← Point-in-time state snapshots
```

### 2. Create the Archive Manager Tool

Create `src/tools/archive_manager.py` with these functions:

```python
def archive_completed(source_path: str, reason: str) -> dict:
    """Move a file/directory to .archive/completed/ with metadata."""

def archive_deprecated(source_path: str, replacement: str) -> dict:
    """Move to .archive/deprecated/ noting what replaced it."""

def create_snapshot(label: str) -> dict:
    """Create a timestamped snapshot of current ACTIVE.md + PLAN.md state."""

def list_archive(category: str = "all") -> dict:
    """List archived items with metadata."""

def restore_from_archive(archive_path: str) -> dict:
    """Restore an archived item to its original location."""
```

**Requirements:**
- Each archived item gets a `.meta.json` sidecar with: `original_path`, `archive_date`, `reason`, `archived_by`
- Restore function checks for conflicts before overwriting
- All functions return status dictionaries (not exceptions)
- Use `pathlib.Path` for all path operations (Windows compatible)

### 3. Create the Archive README

Create `.archive/README.md` with:
- When to archive (completed phases, deprecated tools)
- When NOT to archive (active working files)
- How to restore items
- Naming conventions

### 4. Write Tests

Create `tests/test_archive_manager.py` with tests using `pytest` and `tmp_path` fixture for:
- Archive a file, verify it moved + .meta.json created
- Restore a file, verify it returned to original location
- List archive contents
- Attempt to restore over existing file (conflict detection)

## Constraints
- [ ] Follow `.context/coding_style.md` (type hints, Google docstrings, Pydantic)
- [ ] Tool must work without external dependencies (stdlib only — pathlib, shutil, json, datetime)
- [ ] Archive operations must be reversible (restore function)
- [ ] Metadata must be JSON (machine-readable)
- [ ] Must handle Windows paths correctly (use `pathlib.Path`)
- [ ] Never delete source files — always move + create metadata

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `.archive/README.md` — Archive conventions
- [ ] `.archive/completed/.keep` — Empty dir placeholder
- [ ] `.archive/deprecated/.keep` — Empty dir placeholder
- [ ] `.archive/snapshots/.keep` — Empty dir placeholder
- [ ] `src/tools/archive_manager.py` — Archive management tool
- [ ] `tests/test_archive_manager.py` — Unit tests

### Validation Steps
1. [ ] `archive_completed()` moves file and creates `.meta.json`
2. [ ] `restore_from_archive()` restores file to original location
3. [ ] `list_archive()` returns correct inventory
4. [ ] All functions have type hints and docstrings
5. [ ] Tests pass: `python -m pytest tests/test_archive_manager.py -v`

### State Synchronization
- [ ] Report back to Architect with: summary of archive structure + any design decisions

## ANTI-PATTERNS (Don't Do This)
- ❌ Don't delete files (always move + metadata)
- ❌ Don't use external packages (stdlib + pathlib only)
- ❌ Don't create deeply nested archive structures (max 2 levels)
- ❌ Don't archive `.git/`, `.agent/`, or `.context/` directories
- ❌ Don't use hardcoded paths (everything relative to project root)

---
**Remember:** You are Gemini 3 Flash. Your strength is fast, efficient implementation of well-defined tasks. Trust the Architect's plan. If requirements are unclear, make a reasonable assumption and document it.
