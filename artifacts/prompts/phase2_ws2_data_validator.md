# 🚀 MISSION: Data Validation Pipeline

## ⚠️ BLOCKED — Wait for Workstream 2.1
**This workstream depends on WS 2.1 (Shared Utilities).** Wait until `src/tools/_common.py` and `tests/conftest.py` exist.

## MODEL RECOMMENDATION FOR USER
**When ready, please:**
1. Open a new Antigravity chat window
2. Select: **Gemini 3 Flash** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Straightforward Pydantic schema work — Flash handles well-defined data modeling efficiently.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement  
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)  
**Sync Protocol:** Read `.context/ACTIVE.md` and `PLAN.md` before starting.  
**Dependency:** WS 2.1 must be COMPLETE. Import from `src/tools/_common.py`.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Pydantic 2.0+, Markdown-first architecture
- **Improvement Goal:** Automated validation of project data files (ACTIVE.md, PLAN.md, specs/*.md)
- **Root Cause:** Manual inspection of 4,000+ items was slow; no automated way to flag missing fields or malformed data

## ORIGINAL REVIEW FEEDBACK (Exact Quote)
> "The scraper dumped 4,000+ items. Inspecting and validating them manually (or via LLM context) was slow. A simple Python script with `pandas` could have instantly flagged missing images, outliers in value, or duplicate names."

## PREREQUISITE — READ THESE FILES FIRST
- `.context/ACTIVE.md` — Current project state
- `src/tools/_common.py` — Import `parse_yaml_frontmatter`, `format_tool_response`, `resolve_project_root`
- `specs/active_context_protocol.md` — ACTIVE.md field definitions (your Pydantic model should match)
- `.context/coding_style.md` — Coding standards

## YOUR SPECIFIC TASK

### 1. Create `src/tools/data_validator.py`

```python
"""Data Validation Pipeline.

Validates project data files against expected schemas using Pydantic models.
Supports ACTIVE.md frontmatter, PLAN.md structure, and custom schema definitions.
"""

from tools._common import parse_yaml_frontmatter, format_tool_response, resolve_project_root

class ActiveMdSchema(BaseModel):
    """Pydantic model matching the ACTIVE.md frontmatter specification."""
    project_name: str
    mission_summary: str
    current_phase: str
    active_workstreams: List[str] = Field(default_factory=list)
    blocked_workstreams: List[str] = Field(default_factory=list)
    completed_workstreams: List[str] = Field(default_factory=list)
    last_architect_update: str
    last_worker_update: str
    critical_decisions: List[str] = Field(default_factory=list)
    key_files_modified: List[str] = Field(default_factory=list)
    integration_status: str
    next_milestone: str
    risk_alerts: List[str] = Field(default_factory=list)

def validate_active_md(active_path: str = ".context/ACTIVE.md") -> dict:
    """Validate ACTIVE.md against the protocol schema.
    
    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],       # Schema violations
            "warnings": List[str],     # Non-fatal issues (stale timestamps, etc.)
            "field_count": int,
            "staleness_hours": float   # Hours since last update
        }
    """

def validate_plan_structure(plan_path: str = "PLAN.md") -> dict:
    """Validate PLAN.md has required sections and consistent structure.
    
    Checks:
    - Phase headers exist
    - Workstream format is consistent
    - Status values are valid vocabulary (PLANNED, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED)
    - Dependencies reference existing workstreams
    """

def validate_spec(spec_path: str) -> dict:
    """Validate a spec file has required structure.
    
    Checks:
    - Has a title (# heading)
    - Has version info
    - Has a non-empty body
    """

def validate_project(project_root: Optional[str] = None) -> dict:
    """Run all validations across the project.
    
    Returns:
        dict: {
            "overall_valid": bool,
            "results": {
                "active_md": {...},
                "plan_md": {...},
                "specs": [{...}],
            },
            "summary": str  # Human-readable summary
        }
    """
```

### 2. Key Behaviors

**Staleness Detection:**
- Parse `last_architect_update` and `last_worker_update` timestamps
- Warn if >24 hours old (per protocol spec)
- Report staleness in hours

**Field Count Enforcement:**
- Count frontmatter fields in ACTIVE.md
- Error if >15 (protocol limit)
- Warn if >13 (approaching limit)

**Cross-Validation:**
- If both ACTIVE.md and PLAN.md exist, check that workstream statuses are consistent
- Reuse logic from `plan_sync.sync_check()` where possible (import it)

### 3. Write Tests

Create `tests/test_data_validator.py`:
- Valid ACTIVE.md passes validation
- Missing required fields detected
- Stale timestamps generate warnings
- Field count >15 generates error
- `validate_project()` aggregates all results
- Integration with `plan_sync.sync_check()` works

## Constraints
- [ ] Follow `.context/coding_style.md` (type hints, Google docstrings, Pydantic)
- [ ] Import from `_common.py` (don't reimplement shared utilities)
- [ ] Pydantic v2 models for all schemas
- [ ] Must handle missing files gracefully
- [ ] ISO 8601 timestamp parsing (for staleness detection)

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `src/tools/data_validator.py` — Validation pipeline
- [ ] `tests/test_data_validator.py` — Unit tests

### Validation Steps
1. [ ] `python -m pytest tests/test_data_validator.py -v` — All pass
2. [ ] `python -m pytest tests/ -v` — No regressions
3. [ ] Validates current real ACTIVE.md successfully
4. [ ] Detects missing fields in malformed ACTIVE.md

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion
- [ ] Report to Architect: schemas defined, validation coverage

---
**Remember:** You are Gemini 3 Flash. Efficient, focused implementation. Import from `_common.py`. Trust the Architect's plan.
