# 🚀 MISSION: File Watchdog & Task Sync

## ⚠️ BLOCKED — Wait for Workstream 2.1
**This workstream depends on WS 2.1 (Shared Utilities) + Phase 1 plan_sync.** Wait until `src/tools/_common.py` exists.

## MODEL RECOMMENDATION FOR USER
**When ready, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Sonnet 4.5 (Thinking)** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Thinking mode needed — file watching has concurrency edge cases (race conditions, rapid successive changes) that need careful reasoning.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement  
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)  
**Sync Protocol:** Read `.context/ACTIVE.md` and `PLAN.md` before starting.  
**Dependency:** WS 2.1 must be COMPLETE. Also depends on Phase 1 (`plan_sync.py`).

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Pydantic 2.0+, Markdown-first architecture
- **Improvement Goal:** Automatically detect file changes and suggest ACTIVE.md/PLAN.md updates
- **Root Cause:** Manual task tracking is tedious — agents forget to update ACTIVE.md after completing work

## ORIGINAL REVIEW FEEDBACK (Exact Quote)
> "I had to manually update `task.md` after every file edit. A background Python script using `watchdog` could listen for file changes (e.g., `modified: AIAdvisor.tsx`) and automatically suggest checking off the corresponding task in `task.md`, keeping the Architect focused on high-level decisions."

## GEMINI VALIDATOR FEEDBACK
> "The main risks are now behavioral (enforcing agents to read the files)... These should be the focus of Phase 2 automation."

## PREREQUISITE — READ THESE FILES FIRST
- `.context/ACTIVE.md` — Current project state
- `src/tools/_common.py` — Import shared utilities
- `src/tools/plan_sync.py` — Import `parse_plan`, `update_workstream_status`
- `specs/active_context_protocol.md` — The protocol this tool helps enforce
- `.context/coding_style.md` — Coding standards

## YOUR SPECIFIC TASK

### 1. Create `src/tools/watchdog_sync.py`

**Important:** `watchdog` is an OPTIONAL dependency. The tool must work in two modes:
- **Full mode** (with `watchdog`): Real-time file watching
- **Poll mode** (stdlib only): Periodic directory scanning with `os.scandir()`

```python
"""File Watchdog & Task Synchronization.

Monitors file changes in the project and suggests updates to ACTIVE.md
and PLAN.md. Works in two modes:
- Full mode: Uses watchdog library for real-time monitoring
- Poll mode: Uses os.scandir() for periodic checks (no external deps)
"""

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    _HAS_WATCHDOG = True
except ImportError:
    _HAS_WATCHDOG = False

from tools._common import resolve_project_root, parse_yaml_frontmatter, format_tool_response
from tools.plan_sync import parse_plan

class FileChangeRecord(BaseModel):
    """Record of a single file change."""
    filepath: str
    change_type: Literal["created", "modified", "deleted", "moved"]
    timestamp: str  # ISO 8601
    size_bytes: Optional[int] = None
    relates_to_workstream: Optional[str] = None  # Auto-detected

def detect_changes_since(last_check: str, project_root: Optional[str] = None) -> dict:
    """Detect file changes since a given timestamp (poll mode).
    
    Scans key directories (src/, specs/, .context/, tests/) and compares
    modification times against the given timestamp.
    
    Args:
        last_check: ISO 8601 timestamp of last check
        project_root: Project root path
    
    Returns:
        dict: {
            "changes": List[FileChangeRecord],
            "summary": str,
            "suggested_updates": List[str]  # Suggestions for ACTIVE.md
        }
    """

def suggest_active_updates(changes: List[dict]) -> dict:
    """Given a list of file changes, suggest updates to ACTIVE.md.
    
    Mapping logic:
    - Changes in src/tools/ → update key_files_modified
    - Changes in specs/ → update key_files_modified  
    - Changes in tests/ → update integration_status
    - New files in .archive/ → update completed_workstreams
    
    Returns:
        dict: {
            "suggestions": List[str],
            "auto_applicable": List[dict],  # Can be applied automatically
            "manual_review": List[dict]      # Need architect review
        }
    """

def check_staleness(active_path: str = ".context/ACTIVE.md") -> dict:
    """Check if ACTIVE.md is stale (>24h since last update).
    
    Returns:
        dict: {
            "is_stale": bool,
            "hours_since_architect_update": float,
            "hours_since_worker_update": float,
            "recommendation": str
        }
    """

def generate_change_report(project_root: Optional[str] = None) -> dict:
    """Generate a comprehensive report of project state for the Architect.
    
    Combines:
    - File change detection
    - ACTIVE.md staleness
    - PLAN.md validation
    - Suggested actions
    
    Returns:
        dict: Full status report
    """
```

### 2. Key Design Decisions

**Workstream Detection:**
- Parse `PLAN.md` deliverables to map files → workstreams
- When `src/tools/scaffold.py` is modified, suggest: "This may relate to Workstream 2.3"
- This is a SUGGESTION system, not automatic — the Architect decides

**Staleness Protocol:**
- Read `last_architect_update` and `last_worker_update` from ACTIVE.md frontmatter
- Parse ISO 8601 timestamps
- Warn at >24h, alert at >48h

**Watchdog Mode (Optional):**
- Only implement if `watchdog` is available
- Create a `start_monitoring()` function that watches project root
- Ignores: `.git/`, `__pycache__/`, `venv/`, `.archive/`, `node_modules/`
- On change: adds to an in-memory queue, summarizes on request

### 3. Write Tests

Create `tests/test_watchdog_sync.py`:
- `detect_changes_since()` — finds new/modified files after timestamp
- `suggest_active_updates()` — maps file changes to ACTIVE.md fields correctly
- `check_staleness()` — detects stale and fresh ACTIVE.md
- Poll mode works without watchdog installed
- Edge case: rapid successive changes to same file

## Constraints
- [ ] Follow `.context/coding_style.md`
- [ ] Import from `_common.py` and `plan_sync.py`
- [ ] `watchdog` is OPTIONAL (must work without it using poll mode)
- [ ] ISO 8601 timestamp parsing (use `datetime.fromisoformat()`)
- [ ] Suggestions only — never auto-modify ACTIVE.md without Architect approval
- [ ] Ignore standard noise directories (.git, __pycache__, venv, node_modules)

## Thinking Mode Guidance
Since you're a Thinking-enabled model, explicitly reason through:
1. "What if a file is modified 10 times in 5 seconds? How do I debounce?"
2. "How do I map an arbitrary file path to a workstream? What if it matches multiple?"
3. "What's the minimal useful output for `generate_change_report()`?"
4. "How do I handle timezone-naive vs timezone-aware timestamps?"

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `src/tools/watchdog_sync.py` — File monitoring tool
- [ ] `tests/test_watchdog_sync.py` — Unit tests

### Validation Steps
1. [ ] `python -m pytest tests/test_watchdog_sync.py -v` — All pass
2. [ ] `python -m pytest tests/ -v` — No regressions
3. [ ] `detect_changes_since()` correctly identifies modified files
4. [ ] `check_staleness()` reports correct staleness for current ACTIVE.md
5. [ ] Tool works without watchdog installed (poll mode)

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion
- [ ] Report to Architect: mode capabilities, test coverage, watchdog availability

---
**Remember:** You are Sonnet 4.5 (Thinking). This tool enforces the behavioral protocol that Gemini flagged as the main Phase 2 risk. Be thorough with edge cases.
