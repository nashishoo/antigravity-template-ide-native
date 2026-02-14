# 🚀 MISSION: Artifact Structure Enforcement

## MODEL RECOMMENDATION FOR USER
**For this specific task, please:**
1. Open a new Antigravity chat window
2. Select: **Gemini 3 Flash** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** This is structured filesystem organization. Gemini Flash is fast and effective at following structural rules.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Gemini 2.0 Flash Thinking
**Sync Protocol:** Read `.context/ACTIVE.md` before starting.
**Phase 2 Status:** ✅ COMPLETE.

## CONTEXT
- **Project:** Antigravity Workspace Template
- **Improvement Goal:** Organize the `artifacts/` folder so it doesn't become a dumping ground.
- **Current State:** `artifacts/` is a flat list. `.archive/` exists (created in Phase 1) for *old* stuff, but *active* artifacts need structure too.

## YOUR SPECIFIC TASK

### 1. Design `artifacts/` Structure

Enforce this structure:
```
artifacts/
├── architecture/      # High-level design docs (e.g., architectural_reasoning.md)
├── prompts/           # Generated worker prompts
├── reports/           # Analysis reports, validation outputs
├── data/              # Temporary data files (scraped jsons, etc.)
└── logs/              # Execution logs
```
*Note: Do NOT delete existing files. Move them into the appropriate subfolder.*

### 2. Create `src/tools/artifact_manager.py`

This tool manages the creation and placement of artifacts.

```python
"""Artifact Manager.

Enforces folder structure for new artifacts and helps organize existing ones.
"""
from tools._common import resolve_project_root, safe_write_file, format_tool_response

def create_artifact(category: str, filename: str, content: str) -> dict:
    """Create a new artifact in the correct subdirectory.
    
    Args:
        category: "architecture", "prompts", "reports", "data", "logs"
        filename: e.g., "my_report.md"
        content: The file content
        
    Returns:
        dict: Success status with full path.
    """

def organize_artifacts() -> dict:
    """Scan root artifacts/ folder and suggest moves for loose files.
    
    Does NOT auto-move potentially sensitive files, but returns a 
    plan of action or auto-moves obvious matches (e.g., *.log -> logs/).
    """
```

### 3. Write Tests (`tests/test_artifact_manager.py`)

- Test creating an artifact in "reports" puts it in `artifacts/reports/`.
- Test handling invalid categories (should default to root or error? Decide and document).

## Constraints
- [ ] Follow `.context/coding_style.md`
- [ ] Import from `_common.py`
- [ ] Existing files in `artifacts/` must be preserved (moved, not deleted).

## OUTPUTS
- [ ] `src/tools/artifact_manager.py`
- [ ] `tests/test_artifact_manager.py`
- [ ] The physical directory structure in `artifacts/` (create the folders).

---
**Remember:** Keep it clean. A tidy workspace is a productive workspace.
