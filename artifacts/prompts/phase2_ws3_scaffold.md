# 🚀 MISSION: Code Scaffolding Suite

## ⚠️ BLOCKED — Wait for Workstream 2.1
**This workstream depends on WS 2.1 (Shared Utilities).** Wait until `src/tools/_common.py` and `tests/conftest.py` exist.

## MODEL RECOMMENDATION FOR USER
**When ready, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Sonnet 4.5** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Template generation requires good code generation capabilities. Sonnet handles Jinja2-style templating and code output well.

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
- **Improvement Goal:** Auto-generate boilerplate from spec files, reducing manual typing and syntax errors
- **Root Cause:** Creating interfaces, schemas, and project structures requires careful manual typing that agents can automate

## ORIGINAL REVIEW FEEDBACK (Exact Quote)
> "Creating the `TradeItem` interface and the initial `items.json` structure required careful manual typing. A script that reads `specs/data_model.md` and *generates* the TypeScript interfaces and JSON schemas automatically would have eliminated syntax errors."

## PREREQUISITE — READ THESE FILES FIRST
- `.context/ACTIVE.md` — Current project state
- `src/tools/_common.py` — Import shared utilities
- `.context/coding_style.md` — Coding standards
- `specs/active_context_protocol.md` — Example of a good spec to scaffold from

## YOUR SPECIFIC TASK

### 1. Create `src/tools/scaffold.py`

```python
"""Code Scaffolding Suite.

Generates project files, tool templates, spec documents, and worker prompts
from templates. Reduces boilerplate and ensures consistency across the project.
"""

from tools._common import resolve_project_root, format_tool_response, safe_write_file

def scaffold_tool(tool_name: str, description: str, functions: List[str]) -> dict:
    """Generate a new tool in src/tools/ with boilerplate.
    
    Creates:
    - src/tools/{tool_name}.py with function stubs, type hints, docstrings
    - tests/test_{tool_name}.py with test stubs
    
    Args:
        tool_name: Snake_case name (e.g., "data_validator")
        description: Tool description for docstring
        functions: List of function names to stub
    
    Returns:
        dict: {"success": bool, "files_created": List[str], "message": str}
    """

def scaffold_spec(spec_name: str, title: str, version: str = "v1.0") -> dict:
    """Generate a spec document in specs/ with standard structure.
    
    Creates specs/{spec_name}.md with:
    - Title, version, status header
    - Overview section
    - Specification section
    - Anti-patterns section
    - Revision history
    
    Args:
        spec_name: Filename (without .md)
        title: Document title
        version: Initial version
    
    Returns:
        dict: {"success": bool, "file_created": str, "message": str}
    """

def scaffold_workstream(workstream_id: str, title: str, role: str, model: str, deliverables: List[str]) -> dict:
    """Generate a worker prompt file in artifacts/prompts/.
    
    Creates artifacts/prompts/phase{P}_ws{W}_{slug}.md with:
    - Model recommendation
    - Meta-context
    - Task description
    - Constraints and outputs sections
    
    Args:
        workstream_id: e.g., "3.1"
        title: Workstream title
        role: Worker role description
        model: Recommended AI model
        deliverables: List of expected output files
    
    Returns:
        dict: {"success": bool, "file_created": str, "message": str}
    """

def scaffold_project_init() -> dict:
    """Initialize a new project with full Antigravity template structure.
    
    Creates:
    - .context/ACTIVE.md (template)
    - .context/coding_style.md (template)
    - .context/system_prompt.md (template)
    - .archive/ with subdirectories
    - artifacts/prompts/ directory
    - specs/ directory
    - src/tools/ directory  
    - tests/ directory
    - PLAN.md (template)
    - mission.md (template)
    
    Returns:
        dict: {"success": bool, "files_created": List[str], "directories_created": List[str]}
    """
```

### 2. Templates

Use Python string templates (not Jinja2 — keep stdlib-only for this workstream). Create templates as module-level constants or a `_templates.py` file:

```python
TOOL_TEMPLATE = '''"""{description}

Author: {{worker_model}}
Version: 1.0
"""

from pathlib import Path
from typing import Dict, List, Optional
{pydantic_import}
from tools._common import resolve_project_root, format_tool_response

{function_stubs}
'''
```

### 3. Write Tests

Create `tests/test_scaffold.py`:
- `scaffold_tool()` creates both .py and test file
- Generated tool file has proper imports, type hints, docstrings
- `scaffold_spec()` creates valid markdown with required sections
- `scaffold_project_init()` creates full directory structure
- All scaffolded files are syntactically valid Python (use `compile()` to check)

## Constraints
- [ ] Follow `.context/coding_style.md`
- [ ] Import from `_common.py`
- [ ] Use stdlib string formatting (no Jinja2 dependency for THIS workstream)
- [ ] Generated files must be syntactically valid (test with `compile()`)
- [ ] Must not overwrite existing files (check before writing)
- [ ] Use `pathlib.Path` for all paths

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `src/tools/scaffold.py` — Scaffolding tool
- [ ] `tests/test_scaffold.py` — Unit tests

### Validation Steps
1. [ ] `python -m pytest tests/test_scaffold.py -v` — All pass
2. [ ] `python -m pytest tests/ -v` — No regressions
3. [ ] `scaffold_tool("example", "Test", ["func_a"])` creates valid Python
4. [ ] `scaffold_project_init()` creates complete project structure

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion
- [ ] Report to Architect: templates created, test coverage

---
**Remember:** You are Sonnet 4.5. Generate clean, well-structured boilerplate. Import from `_common.py`. Trust the Architect's plan.
