# 🚀 MISSION: Shared Utilities & Test Infrastructure

## MODEL RECOMMENDATION FOR USER
**For this specific task, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Sonnet 4.5 (Thinking)** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** This is foundational platform work — all other Phase 2 workstreams depend on it. Thinking mode ensures edge cases in YAML parsing and project root resolution are handled correctly.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement  
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)  
**Sync Protocol:** Read `.context/ACTIVE.md` and `PLAN.md` before starting.  
**Phase 1 Status:** ✅ COMPLETE and validated by Gemini.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture, IDE-native agents (Antigravity)
- **Phase 1 Delivered:** `.context/ACTIVE.md` protocol, `src/tools/plan_sync.py`, `src/tools/archive_manager.py`
- **Improvement Goal:** Create shared utilities that all Phase 2+ tools can import, plus proper test infrastructure
- **Root Cause:** Each Phase 1 tool reimplements common functions (path resolution, YAML parsing, error formatting)

## GEMINI VALIDATOR FEEDBACK (Phase 1)
> "The main risks are now behavioral (enforcing agents to read the files) and syntactic (regex fragility in parsing). These should be the focus of Phase 2 automation."

**Architect's note:** We already hit a regex bug in Phase 1 (`(.+)` vs `(.*)` in `plan_sync.py`). This workstream should create robust shared parsers to prevent similar issues.

## EXISTING TOOLS TO STUDY (Read These First)
- `src/tools/plan_sync.py` (686 lines) — PLAN.md parser with Pydantic models. Note the YAML frontmatter regex parsing in `sync_check()` (lines 600-635) — this should be extracted into `_common.py`.
- `src/tools/archive_manager.py` (298 lines) — Archive tool using TypedDicts. Note the path resolution logic in `__init__` — this should be extracted.
- `src/tools/skills_catalog.py` — Existing skill discovery tool.
- `.context/coding_style.md` — Coding standards (type hints, Google docstrings, Pydantic).

## YOUR SPECIFIC TASK

### 1. Create `src/tools/_common.py` — Shared Utilities

```python
"""Shared utilities for all Antigravity tools.

This module provides common functions used across all tools to avoid
code duplication and ensure consistent behavior.
"""

def resolve_project_root(start_path: Optional[str] = None) -> Path:
    """Find the project root by looking for marker files (.context/, PLAN.md, .git/).
    
    Args:
        start_path: Starting directory. If None, uses cwd.
    
    Returns:
        Path to the project root.
    
    Raises:
        FileNotFoundError: If no project root markers are found.
    """

def parse_yaml_frontmatter(filepath: str) -> dict:
    """Parse YAML frontmatter from a markdown file.
    
    Handles:
    - Standard --- delimited YAML
    - Files without frontmatter (returns empty dict)
    - Malformed YAML (returns partial dict + errors)
    - Array fields (active_workstreams, etc.)
    
    Args:
        filepath: Path to the markdown file.
    
    Returns:
        dict: {
            "success": bool,
            "frontmatter": dict,  # parsed YAML fields
            "body": str,  # markdown content after frontmatter
            "errors": List[str]
        }
    """

def format_tool_response(success: bool, message: str, **kwargs) -> dict:
    """Create a standardized tool response dictionary.
    
    Every tool in the project should use this for consistent return format.
    
    Args:
        success: Whether the operation succeeded.
        message: Human-readable message.
        **kwargs: Additional key-value pairs to include.
    
    Returns:
        dict with "success", "message", and any additional fields.
    """

def safe_read_file(filepath: str, encoding: str = "utf-8") -> dict:
    """Read a file with comprehensive error handling.
    
    Args:
        filepath: Path to read.
        encoding: File encoding.
    
    Returns:
        dict: {"success": bool, "content": str, "errors": List[str]}
    """

def safe_write_file(filepath: str, content: str, encoding: str = "utf-8", create_parents: bool = True) -> dict:
    """Write a file with comprehensive error handling and optional parent directory creation.
    
    Args:
        filepath: Path to write.
        content: Content to write.
        encoding: File encoding.
        create_parents: Whether to create parent directories.
    
    Returns:
        dict: {"success": bool, "message": str, "errors": List[str]}
    """
```

**Critical:** The `parse_yaml_frontmatter()` function must be more robust than the regex-based parser currently in `plan_sync.py`. Use `yaml.safe_load()` if pyyaml is available, with regex fallback if not:

```python
try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False
```

### 2. Create `tests/conftest.py` — Test Fixtures

Shared fixtures that all test files can use:

```python
@pytest.fixture
def project_root(tmp_path):
    """Create a minimal project structure for testing."""
    # Creates: .context/, PLAN.md, .archive/, src/tools/

@pytest.fixture
def sample_active_md(project_root):
    """Create a sample ACTIVE.md with valid frontmatter."""

@pytest.fixture
def sample_plan_md(project_root):
    """Create a sample PLAN.md with phases and workstreams."""

@pytest.fixture
def archive_structure(project_root):
    """Create a .archive/ directory with subdirectories."""
```

### 3. Create `pyproject.toml`

```toml
[project]
name = "antigravity-template"
version = "2.0.0"
description = "IDE-native template for parallel AI agent workflows"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest>=7.0", "pydantic>=2.0"]
full = ["pyyaml>=6.0", "jinja2>=3.0", "watchdog>=3.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

### 4. Create/Update `requirements.txt`

```
# Core (required)
pydantic>=2.0

# Optional (enhanced functionality)
pyyaml>=6.0
jinja2>=3.0
watchdog>=3.0

# Development
pytest>=7.0
```

### 5. Write Tests

Create `tests/test_common.py` with tests for:
- `resolve_project_root()` — finds root from nested directory, fails gracefully from temp dir
- `parse_yaml_frontmatter()` — valid YAML, empty file, no frontmatter, malformed YAML
- `format_tool_response()` — standard format, extra kwargs
- `safe_read_file()` / `safe_write_file()` — success, missing file, encoding errors

### 6. Refactor Existing Tools (Optional but Recommended)

If time permits, update `plan_sync.py` and `archive_manager.py` to import from `_common.py`:
- Replace inline YAML frontmatter parsing in `sync_check()` with `parse_yaml_frontmatter()`
- Replace inline path resolution with `resolve_project_root()`

**This is optional.** Only do it if you have confidence no regressions will occur. Run existing tests after refactoring:
```
python -m pytest tests/ -v
```

## Constraints
- [ ] Follow `.context/coding_style.md` (type hints, Google docstrings, Pydantic where appropriate)
- [ ] `_common.py` must work with stdlib only (pyyaml optional with try/except)
- [ ] All functions must return dicts (consistent with project convention)
- [ ] Must not break existing `test_plan_sync.py` (20 tests) or `test_archive_manager.py`
- [ ] Path operations must use `pathlib.Path` (Windows compatibility)

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `src/tools/_common.py` — Shared utilities
- [ ] `tests/conftest.py` — Shared test fixtures
- [ ] `tests/test_common.py` — Tests for shared utilities
- [ ] `pyproject.toml` — Project configuration
- [ ] `requirements.txt` — Updated dependencies

### Validation Steps
1. [ ] `python -m pytest tests/test_common.py -v` — All pass
2. [ ] `python -m pytest tests/ -v` — All existing tests still pass (no regressions)
3. [ ] `parse_yaml_frontmatter()` handles: valid YAML, no frontmatter, malformed YAML
4. [ ] `resolve_project_root()` finds root from `src/tools/` subdirectory
5. [ ] Report total tests count across all test files

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion
- [ ] Report to Architect: summary of utilities created, any refactoring done, test counts

## ANTI-PATTERNS (Don't Do This)
- ❌ Don't require pyyaml (optional import with fallback)
- ❌ Don't break existing tests (run `pytest tests/` before reporting done)
- ❌ Don't duplicate logic already in `_common.py` in new tools
- ❌ Don't use `os.path` — use `pathlib.Path` everywhere

---
**Remember:** You are Sonnet 4.5 (Thinking). This is FOUNDATIONAL work — all Phase 2 tools will import `_common.py`. Be thorough.
