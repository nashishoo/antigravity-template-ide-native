"""Tests for scaffold.

Author: Worker (Sonnet 4.5 — Workstream 2.3)
Version: 1.0
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tools.scaffold import (
    scaffold_tool,
    scaffold_spec,
    scaffold_workstream,
    scaffold_project_init
)


# ============================================================================
# scaffold_tool() Tests
# ============================================================================

def test_scaffold_tool_creates_files(project_root):
    """Test that scaffold_tool creates both tool and test files."""
    result = scaffold_tool(
        tool_name="example_tool",
        description="Example tool for testing",
        functions=["func_a", "func_b"],
        project_root=project_root
    )
    
    assert result["success"] is True
    assert len(result["files_created"]) == 2
    
    tool_file = project_root / "src" / "tools" / "example_tool.py"
    test_file = project_root / "tests" / "test_example_tool.py"
    
    assert tool_file.exists()
    assert test_file.exists()


def test_scaffold_tool_valid_python_syntax(project_root):
    """Test that generated tool file has valid Python syntax."""
    result = scaffold_tool(
        tool_name="syntax_test",
        description="Testing syntax validation",
        functions=["test_func"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    tool_file = project_root / "src" / "tools" / "syntax_test.py"
    content = tool_file.read_text(encoding='utf-8')
    
    # Should compile without errors
    compile(content, "syntax_test.py", 'exec')


def test_scaffold_tool_has_proper_imports(project_root):
    """Test that generated tool has required imports."""
    result = scaffold_tool(
        tool_name="import_test",
        description="Testing imports",
        functions=["func1"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    tool_file = project_root / "src" / "tools" / "import_test.py"
    content = tool_file.read_text(encoding='utf-8')
    
    assert "from tools._common import" in content
    assert "resolve_project_root" in content
    assert "format_tool_response" in content


def test_scaffold_tool_has_type_hints(project_root):
    """Test that generated functions have type hints."""
    result = scaffold_tool(
        tool_name="typehint_test",
        description="Testing type hints",
        functions=["typed_func"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    tool_file = project_root / "src" / "tools" / "typehint_test.py"
    content = tool_file.read_text(encoding='utf-8')
    
    assert "-> Dict[str, Any]:" in content
    assert "from typing import" in content


def test_scaffold_tool_has_docstrings(project_root):
    """Test that generated functions have docstrings."""
    result = scaffold_tool(
        tool_name="docstring_test",
        description="Testing docstrings",
        functions=["documented_func"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    tool_file = project_root / "src" / "tools" / "docstring_test.py"
    content = tool_file.read_text(encoding='utf-8')
    
    assert '"""' in content
    assert "Args:" in content
    assert "Returns:" in content


def test_scaffold_tool_prevents_overwrite(project_root):
    """Test that scaffold_tool won't overwrite existing files."""
    # Create first tool
    result1 = scaffold_tool(
        tool_name="overwrite_test",
        description="First version",
        functions=["func1"],
        project_root=project_root
    )
    assert result1["success"] is True
    
    # Try to create again
    result2 = scaffold_tool(
        tool_name="overwrite_test",
        description="Second version",
        functions=["func2"],
        project_root=project_root
    )
    assert result2["success"] is False
    assert "already exists" in result2["message"]


def test_scaffold_tool_creates_test_stubs(project_root):
    """Test that test file contains test stubs for each function."""
    result = scaffold_tool(
        tool_name="test_stub_check",
        description="Testing test stubs",
        functions=["func_a", "func_b", "func_c"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    test_file = project_root / "tests" / "test_test_stub_check.py"
    content = test_file.read_text(encoding='utf-8')
    
    assert "def test_func_a" in content
    assert "def test_func_b" in content
    assert "def test_func_c" in content


def test_scaffold_tool_multiple_functions(project_root):
    """Test scaffolding a tool with multiple functions."""
    result = scaffold_tool(
        tool_name="multi_func",
        description="Tool with multiple functions",
        functions=["validate", "process", "export"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    tool_file = project_root / "src" / "tools" / "multi_func.py"
    content = tool_file.read_text(encoding='utf-8')
    
    assert "def validate()" in content
    assert "def process()" in content
    assert "def export()" in content


# ============================================================================
# scaffold_spec() Tests
# ============================================================================

def test_scaffold_spec_creates_file(project_root):
    """Test that scaffold_spec creates a spec file."""
    result = scaffold_spec(
        spec_name="test_spec",
        title="Test Specification",
        version="v1.0",
        project_root=project_root
    )
    
    assert result["success"] is True
    assert result["file_created"] != ""
    
    spec_file = project_root / "specs" / "test_spec.md"
    assert spec_file.exists()


def test_scaffold_spec_has_required_sections(project_root):
    """Test that generated spec has all required sections."""
    result = scaffold_spec(
        spec_name="sections_test",
        title="Sections Test Spec",
        project_root=project_root
    )
    
    assert result["success"] is True
    
    spec_file = project_root / "specs" / "sections_test.md"
    content = spec_file.read_text(encoding='utf-8')
    
    assert "# Sections Test Spec" in content
    assert "## 1. Overview" in content
    assert "## 2. Specification" in content
    assert "## 3. Anti-Patterns" in content
    assert "## 4. Revision History" in content


def test_scaffold_spec_has_metadata(project_root):
    """Test that spec has version and status metadata."""
    result = scaffold_spec(
        spec_name="metadata_test",
        title="Metadata Test",
        version="v2.0",
        project_root=project_root
    )
    
    assert result["success"] is True
    
    spec_file = project_root / "specs" / "metadata_test.md"
    content = spec_file.read_text(encoding='utf-8')
    
    assert "**Version:** v2.0" in content
    assert "**Status:** 🚧 Draft" in content
    assert "**Created:**" in content


def test_scaffold_spec_prevents_overwrite(project_root):
    """Test that scaffold_spec won't overwrite existing files."""
    # Create first spec
    result1 = scaffold_spec(
        spec_name="overwrite_spec",
        title="First Version",
        project_root=project_root
    )
    assert result1["success"] is True
    
    # Try to create again
    result2 = scaffold_spec(
        spec_name="overwrite_spec",
        title="Second Version",
        project_root=project_root
    )
    assert result2["success"] is False
    assert "already exists" in result2["message"]


def test_scaffold_spec_default_version(project_root):
    """Test that spec uses default version if not specified."""
    result = scaffold_spec(
        spec_name="default_version",
        title="Default Version Test",
        project_root=project_root
    )
    
    assert result["success"] is True
    
    spec_file = project_root / "specs" / "default_version.md"
    content = spec_file.read_text(encoding='utf-8')
    
    assert "**Version:** v1.0" in content


# ============================================================================
# scaffold_workstream() Tests
# ============================================================================

def test_scaffold_workstream_creates_file(project_root):
    """Test that scaffold_workstream creates a prompt file."""
    result = scaffold_workstream(
        workstream_id="2.1",
        title="Test Workstream",
        role="Test Engineer",
        model="Claude Sonnet 4.5",
        deliverables=["src/test.py", "tests/test_test.py"],
        project_root=project_root
    )
    
    assert result["success"] is True
    assert result["file_created"] != ""
    
    prompt_file = project_root / "artifacts" / "prompts" / "phase2_ws1_test_workstream.md"
    assert prompt_file.exists()


def test_scaffold_workstream_has_required_sections(project_root):
    """Test that workstream prompt has all required sections."""
    result = scaffold_workstream(
        workstream_id="3.2",
        title="Section Test",
        role="Developer",
        model="Gemini Flash",
        deliverables=["output.py"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    prompt_file = project_root / "artifacts" / "prompts" / "phase3_ws2_section_test.md"
    content = prompt_file.read_text(encoding='utf-8')
    
    assert "## META-CONTEXT" in content
    assert "## CONTEXT" in content
    assert "## PREREQUISITE" in content
    assert "## YOUR SPECIFIC TASK" in content
    assert "## Constraints" in content
    assert "## OUTPUTS" in content


def test_scaffold_workstream_includes_deliverables(project_root):
    """Test that workstream prompt includes deliverables list."""
    deliverables = ["src/module.py", "tests/test_module.py", "docs/module.md"]
    
    result = scaffold_workstream(
        workstream_id="1.1",
        title="Deliverables Test",
        role="Engineer",
        model="Sonnet",
        deliverables=deliverables,
        project_root=project_root
    )
    
    assert result["success"] is True
    
    prompt_file = project_root / "artifacts" / "prompts" / "phase1_ws1_deliverables_test.md"
    content = prompt_file.read_text(encoding='utf-8')
    
    for deliverable in deliverables:
        assert deliverable in content


def test_scaffold_workstream_invalid_id_format(project_root):
    """Test that invalid workstream_id format is rejected."""
    result = scaffold_workstream(
        workstream_id="invalid",
        title="Invalid ID Test",
        role="Tester",
        model="Model",
        deliverables=["file.py"],
        project_root=project_root
    )
    
    assert result["success"] is False
    assert "Invalid workstream_id format" in result["message"]


def test_scaffold_workstream_prevents_overwrite(project_root):
    """Test that scaffold_workstream won't overwrite existing files."""
    # Create first workstream
    result1 = scaffold_workstream(
        workstream_id="4.1",
        title="Overwrite Test",
        role="Role1",
        model="Model1",
        deliverables=["file1.py"],
        project_root=project_root
    )
    assert result1["success"] is True
    
    # Try to create again with same ID and title
    result2 = scaffold_workstream(
        workstream_id="4.1",
        title="Overwrite Test",
        role="Role2",
        model="Model2",
        deliverables=["file2.py"],
        project_root=project_root
    )
    assert result2["success"] is False
    assert "already exists" in result2["message"]


def test_scaffold_workstream_slug_generation(project_root):
    """Test that workstream generates proper filename slug."""
    result = scaffold_workstream(
        workstream_id="5.3",
        title="Complex Title-With Special_Chars!",
        role="Engineer",
        model="Model",
        deliverables=["output.py"],
        project_root=project_root
    )
    
    assert result["success"] is True
    
    # Should create file with sanitized slug (hyphens become underscores, special chars removed)
    prompt_file = project_root / "artifacts" / "prompts" / "phase5_ws3_complex_title_with_special_chars.md"
    assert prompt_file.exists()


# ============================================================================
# scaffold_project_init() Tests
# ============================================================================

def test_scaffold_project_init_creates_directories(tmp_path, monkeypatch):
    """Test that project init creates all required directories."""
    # Change to tmp_path for this test
    monkeypatch.chdir(tmp_path)
    
    result = scaffold_project_init()
    
    assert result["success"] is True
    assert len(result["directories_created"]) > 0
    
    # Check key directories
    assert (tmp_path / ".context").exists()
    assert (tmp_path / ".archive" / "completed").exists()
    assert (tmp_path / ".archive" / "deprecated").exists()
    assert (tmp_path / ".archive" / "snapshots").exists()
    assert (tmp_path / "artifacts" / "prompts").exists()
    assert (tmp_path / "specs").exists()
    assert (tmp_path / "src" / "tools").exists()
    assert (tmp_path / "tests").exists()


def test_scaffold_project_init_creates_files(tmp_path, monkeypatch):
    """Test that project init creates all required files."""
    monkeypatch.chdir(tmp_path)
    
    result = scaffold_project_init()
    
    assert result["success"] is True
    assert len(result["files_created"]) > 0
    
    # Check key files
    assert (tmp_path / ".context" / "ACTIVE.md").exists()
    assert (tmp_path / ".context" / "coding_style.md").exists()
    assert (tmp_path / ".context" / "system_prompt.md").exists()
    assert (tmp_path / "PLAN.md").exists()
    assert (tmp_path / "mission.md").exists()


def test_scaffold_project_init_active_md_structure(tmp_path, monkeypatch):
    """Test that generated ACTIVE.md has proper structure."""
    monkeypatch.chdir(tmp_path)
    
    result = scaffold_project_init()
    assert result["success"] is True
    
    active_file = tmp_path / ".context" / "ACTIVE.md"
    content = active_file.read_text(encoding='utf-8')
    
    # Check for YAML frontmatter
    assert content.startswith("---")
    assert "project_name:" in content
    assert "mission_summary:" in content
    
    # Check for markdown sections
    assert "## 🎯 Current Focus" in content
    assert "## 📋 Recent Changes" in content
    assert "## 🚧 Blockers" in content
    assert "## 💬 Notes for Workers" in content


def test_scaffold_project_init_skips_existing_files(tmp_path, monkeypatch):
    """Test that project init doesn't overwrite existing files."""
    monkeypatch.chdir(tmp_path)
    
    # Create a file first
    existing_file = tmp_path / "PLAN.md"
    existing_file.write_text("# Existing Plan\n", encoding='utf-8')
    original_content = existing_file.read_text(encoding='utf-8')
    
    result = scaffold_project_init()
    
    # Should report error for existing file
    assert "already exists" in str(result.get("errors", []))
    
    # Original content should be preserved
    assert existing_file.read_text(encoding='utf-8') == original_content


def test_scaffold_project_init_idempotent(tmp_path, monkeypatch):
    """Test that running project init twice is safe."""
    monkeypatch.chdir(tmp_path)
    
    # First run
    result1 = scaffold_project_init()
    assert result1["success"] is True
    
    # Second run
    result2 = scaffold_project_init()
    
    # Should complete but report existing files
    assert "errors" in result2
    assert len(result2["errors"]) > 0
