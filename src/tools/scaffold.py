"""Code Scaffolding Suite.

Generates project files, tool templates, spec documents, and worker prompts
from templates. Reduces boilerplate and ensures consistency across the project.

Author: Worker (Sonnet 4.5 — Workstream 2.3)
Version: 1.0
"""

from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from tools._common import resolve_project_root, format_tool_response, safe_write_file


# ============================================================================
# Templates
# ============================================================================

TOOL_TEMPLATE = '''"""{{description}}

Author: {{worker_model}}
Version: 1.0
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
{{pydantic_import}}
from tools._common import resolve_project_root, format_tool_response, safe_write_file


{{function_stubs}}
'''

TOOL_TEST_TEMPLATE = '''"""Tests for {{tool_name}}.

Author: Worker (Auto-generated)
Version: 1.0
"""

import pytest
from pathlib import Path

from tools.{{tool_name}} import {{function_imports}}


{{test_stubs}}
'''

SPEC_TEMPLATE = '''# {{title}}

**Version:** {{version}}  
**Status:** 🚧 Draft  
**Created:** {{date}}  
**Author:** {{author}}

---

## 1. Overview

### Purpose
[Describe what this specification defines and why it exists]

### Success Metric
[How will we know this spec is successfully implemented?]

### Design Philosophy
[Key principles guiding this specification]

---

## 2. Specification

[Detailed specification content goes here]

---

## 3. Anti-Patterns

❌ **Don't Do This:**

### [Anti-pattern Name]
**Why:** [Explanation]

---

## 4. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| {{version}} | {{date}} | Initial specification | {{author}} |

---

**End of Specification**
'''

WORKSTREAM_TEMPLATE = '''## META-CONTEXT (Read This First)
**Parent Project:** {{project_name}}  
**Your Architect:** {{architect}}  
**Sync Protocol:** Read `.context/ACTIVE.md` and `PLAN.md` before starting.  
**Dependency:** {{dependencies}}

## CONTEXT
- **Project:** {{project_name}}
- **Project Root:** {{project_root}}
- **Tech Stack:** {{tech_stack}}
- **Improvement Goal:** {{goal}}

## PREREQUISITE — READ THESE FILES FIRST
{{prerequisite_files}}

## YOUR SPECIFIC TASK

{{task_description}}

## Constraints
{{constraints}}

## OUTPUTS (Definition of Done)

### Files to Create
{{deliverables}}

### Validation Steps
{{validation_steps}}

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion
- [ ] Report to Architect: {{completion_message}}

---
**Remember:** You are {{role}}. {{reminder}}
'''


# ============================================================================
# Scaffolding Functions
# ============================================================================

def scaffold_tool(
    tool_name: str, 
    description: str, 
    functions: List[str],
    project_root: Path = None
) -> Dict[str, Any]:
    """Generate a new tool in src/tools/ with boilerplate.
    
    Creates:
    - src/tools/{tool_name}.py with function stubs, type hints, docstrings
    - tests/test_{tool_name}.py with test stubs
    
    Args:
        tool_name: Snake_case name (e.g., "data_validator")
        description: Tool description for docstring
        functions: List of function names to stub
        project_root: Optional project root path (for testing)
    
    Returns:
        dict: {"success": bool, "files_created": List[str], "message": str}
    """
    if project_root is None:
        try:
            project_root = resolve_project_root()
        except FileNotFoundError as e:
            return format_tool_response(False, str(e))
    
    tool_file = project_root / "src" / "tools" / f"{tool_name}.py"
    test_file = project_root / "tests" / f"test_{tool_name}.py"
    
    # Check if files already exist
    if tool_file.exists():
        return format_tool_response(
            False, 
            f"Tool file already exists: {tool_file}",
            files_created=[]
        )
    
    if test_file.exists():
        return format_tool_response(
            False, 
            f"Test file already exists: {test_file}",
            files_created=[]
        )
    
    # Generate function stubs
    function_stubs = []
    for func_name in functions:
        stub = f'''def {func_name}() -> Dict[str, Any]:
    """[TODO: Add function description]
    
    Args:
        [TODO: Add arguments]
    
    Returns:
        dict: {{"success": bool, "message": str}}
    """
    # TODO: Implement function
    return format_tool_response(True, "Not implemented yet")
'''
        function_stubs.append(stub)
    
    # Determine if Pydantic import is needed (heuristic: complex data models)
    pydantic_import = "\nfrom pydantic import BaseModel, Field" if len(functions) > 2 else ""
    
    # Generate tool file content
    tool_content = TOOL_TEMPLATE.replace('{{description}}', description)
    tool_content = tool_content.replace('{{worker_model}}', 'Worker (Auto-generated)')
    tool_content = tool_content.replace('{{pydantic_import}}', pydantic_import)
    tool_content = tool_content.replace('{{function_stubs}}', '\n\n'.join(function_stubs))
    
    # Generate test file content
    test_stubs = []
    for func_name in functions:
        test_stub = f'''def test_{func_name}(project_root):
    """Test {func_name} function."""
    # TODO: Implement test
    from tools.{tool_name} import {func_name}
    result = {func_name}()
    assert result["success"] is True
'''
        test_stubs.append(test_stub)
    
    test_content = TOOL_TEST_TEMPLATE.replace('{{tool_name}}', tool_name)
    test_content = test_content.replace('{{function_imports}}', ', '.join(functions))
    test_content = test_content.replace('{{test_stubs}}', '\n\n'.join(test_stubs))
    
    # Validate syntax
    try:
        compile(tool_content, f"{tool_name}.py", 'exec')
        compile(test_content, f"test_{tool_name}.py", 'exec')
    except SyntaxError as e:
        return format_tool_response(
            False,
            f"Generated code has syntax errors: {str(e)}",
            files_created=[]
        )
    
    # Write files
    tool_result = safe_write_file(str(tool_file), tool_content)
    if not tool_result["success"]:
        return format_tool_response(
            False,
            f"Failed to write tool file: {tool_result['errors']}",
            files_created=[]
        )
    
    test_result = safe_write_file(str(test_file), test_content)
    if not test_result["success"]:
        # Clean up tool file if test file fails
        tool_file.unlink()
        return format_tool_response(
            False,
            f"Failed to write test file: {test_result['errors']}",
            files_created=[]
        )
    
    return format_tool_response(
        True,
        f"Successfully scaffolded tool '{tool_name}' with {len(functions)} functions",
        files_created=[str(tool_file), str(test_file)]
    )


def scaffold_spec(
    spec_name: str, 
    title: str, 
    version: str = "v1.0",
    project_root: Path = None
) -> Dict[str, Any]:
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
        project_root: Optional project root path (for testing)
    
    Returns:
        dict: {"success": bool, "file_created": str, "message": str}
    """
    if project_root is None:
        try:
            project_root = resolve_project_root()
        except FileNotFoundError as e:
            return format_tool_response(False, str(e))
    
    spec_file = project_root / "specs" / f"{spec_name}.md"
    
    # Check if file already exists
    if spec_file.exists():
        return format_tool_response(
            False,
            f"Spec file already exists: {spec_file}",
            file_created=""
        )
    
    # Generate spec content
    current_date = datetime.now().strftime("%Y-%m-%d")
    spec_content = SPEC_TEMPLATE.replace('{{title}}', title)
    spec_content = spec_content.replace('{{version}}', version)
    spec_content = spec_content.replace('{{date}}', current_date)
    spec_content = spec_content.replace('{{author}}', 'Worker (Auto-generated)')
    
    # Write file
    result = safe_write_file(str(spec_file), spec_content)
    if not result["success"]:
        return format_tool_response(
            False,
            f"Failed to write spec file: {result['errors']}",
            file_created=""
        )
    
    return format_tool_response(
        True,
        f"Successfully created spec '{spec_name}'",
        file_created=str(spec_file)
    )


def scaffold_workstream(
    workstream_id: str, 
    title: str, 
    role: str, 
    model: str, 
    deliverables: List[str],
    project_root: Path = None
) -> Dict[str, Any]:
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
        project_root: Optional project root path (for testing)
    
    Returns:
        dict: {"success": bool, "file_created": str, "message": str}
    """
    if project_root is None:
        try:
            project_root = resolve_project_root()
        except FileNotFoundError as e:
            return format_tool_response(False, str(e))
    
    # Parse workstream_id (e.g., "3.1" -> phase=3, ws=1)
    try:
        phase, ws = workstream_id.split('.')
        phase = int(phase)
        ws = int(ws)
    except (ValueError, AttributeError):
        return format_tool_response(
            False,
            f"Invalid workstream_id format: {workstream_id}. Expected format: 'P.W' (e.g., '3.1')",
            file_created=""
        )
    
    # Create slug from title
    slug = title.lower().replace(' ', '_').replace('-', '_')
    slug = ''.join(c for c in slug if c.isalnum() or c == '_')
    
    prompt_file = project_root / "artifacts" / "prompts" / f"phase{phase}_ws{ws}_{slug}.md"
    
    # Check if file already exists
    if prompt_file.exists():
        return format_tool_response(
            False,
            f"Workstream prompt already exists: {prompt_file}",
            file_created=""
        )
    
    # Generate workstream content
    deliverables_list = '\n'.join([f"- [ ] `{d}`" for d in deliverables])
    
    workstream_content = WORKSTREAM_TEMPLATE.replace('{{project_name}}', 'Antigravity Workspace Template')
    workstream_content = workstream_content.replace('{{architect}}', 'Claude Opus 4.6 (Thinking)')
    workstream_content = workstream_content.replace('{{dependencies}}', '[TODO: List dependencies]')
    workstream_content = workstream_content.replace('{{project_root}}', str(project_root))
    workstream_content = workstream_content.replace('{{tech_stack}}', 'Python 3.11+, Pydantic 2.0+, Markdown-first architecture')
    workstream_content = workstream_content.replace('{{goal}}', '[TODO: Define improvement goal]')
    workstream_content = workstream_content.replace('{{prerequisite_files}}', '[TODO: List prerequisite files]')
    workstream_content = workstream_content.replace('{{task_description}}', f'[TODO: Describe task for {title}]')
    workstream_content = workstream_content.replace('{{constraints}}', '[TODO: List constraints]')
    workstream_content = workstream_content.replace('{{deliverables}}', deliverables_list)
    workstream_content = workstream_content.replace('{{validation_steps}}', '[TODO: List validation steps]')
    workstream_content = workstream_content.replace('{{completion_message}}', f'{title} completed')
    workstream_content = workstream_content.replace('{{role}}', role)
    workstream_content = workstream_content.replace('{{reminder}}', f'Recommended model: {model}')
    
    # Write file
    result = safe_write_file(str(prompt_file), workstream_content)
    if not result["success"]:
        return format_tool_response(
            False,
            f"Failed to write workstream prompt: {result['errors']}",
            file_created=""
        )
    
    return format_tool_response(
        True,
        f"Successfully created workstream prompt for {workstream_id}: {title}",
        file_created=str(prompt_file)
    )


def scaffold_project_init() -> Dict[str, Any]:
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
    # Use current directory as project root for initialization
    project_root = Path.cwd()
    
    directories_to_create = [
        ".context",
        ".archive/completed",
        ".archive/deprecated",
        ".archive/snapshots",
        "artifacts/prompts",
        "specs",
        "src/tools",
        "tests"
    ]
    
    files_to_create = {
        ".context/ACTIVE.md": '''---
project_name: "New Project"
mission_summary: "Project mission summary"
current_phase: "Phase 1: Foundation"
active_workstreams: []
blocked_workstreams: []
completed_workstreams: []
last_architect_update: ""
last_worker_update: ""
critical_decisions: []
key_files_modified: []
integration_status: "Project initialized"
next_milestone: "Define project goals"
risk_alerts: []
---

# Active Context

## 🎯 Current Focus
Project initialization

## 📋 Recent Changes
- Project structure created

## 🚧 Blockers
None

## 💬 Notes for Workers
Welcome to the Antigravity Workspace Template!
''',
        ".context/coding_style.md": '''# Coding Standards & Best Practices

## Architecture
1. **Tool Isolation**: All external interactions MUST be encapsulated in functions within the `tools/` directory.
2. **Pydantic Everywhere**: Use `pydantic` models for function arguments and return values.

## Python Style
1. **Type Hints**: Mandatory for all function signatures.
2. **Docstrings**: Google-style docstrings are required.

## Agent Design Patterns
1. **Stateless Tools**: Tools should generally be stateless.
2. **Fail Gracefully**: Tools should return error messages rather than crashing.
''',
        ".context/system_prompt.md": '''# System Prompt Template

[TODO: Define your project-specific system prompt]
''',
        "PLAN.md": '''# Project Plan

**Architect:** [Your Name]
**Start Date:** [Date]
**Target Completion:** [Date]
**Status:** Planning

---

## Phase 1: Foundation

[TODO: Define your first phase]
''',
        "mission.md": '''# Project Mission

[TODO: Define your project mission and goals]
'''
    }
    
    created_dirs = []
    created_files = []
    errors = []
    
    # Create directories
    for dir_path in directories_to_create:
        full_path = project_root / dir_path
        try:
            full_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(full_path))
        except Exception as e:
            errors.append(f"Failed to create directory {dir_path}: {str(e)}")
    
    # Create files (only if they don't exist)
    for file_path, content in files_to_create.items():
        full_path = project_root / file_path
        if full_path.exists():
            errors.append(f"File already exists (skipped): {file_path}")
            continue
        
        result = safe_write_file(str(full_path), content)
        if result["success"]:
            created_files.append(str(full_path))
        else:
            errors.append(f"Failed to create {file_path}: {result['errors']}")
    
    if errors:
        return format_tool_response(
            False,
            f"Project initialization completed with {len(errors)} errors",
            files_created=created_files,
            directories_created=created_dirs,
            errors=errors
        )
    
    return format_tool_response(
        True,
        f"Successfully initialized project structure with {len(created_dirs)} directories and {len(created_files)} files",
        files_created=created_files,
        directories_created=created_dirs
    )
