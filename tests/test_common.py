"""Tests for _common.py shared utilities.

This module contains comprehensive tests for the shared utility functions
to ensure robustness and consistency across all tools.

Author: Worker (Sonnet 4.5 Thinking — Workstream 2.1)
Version: 1.0
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tools._common import (
    resolve_project_root,
    parse_yaml_frontmatter,
    format_tool_response,
    safe_read_file,
    safe_write_file
)


# ============================================================================
# Tests for resolve_project_root()
# ============================================================================

def test_resolve_project_root_from_root(project_root):
    """Test finding project root from the root directory itself."""
    result = resolve_project_root(str(project_root))
    assert result == project_root


def test_resolve_project_root_from_nested_dir(project_root):
    """Test finding project root from a nested subdirectory."""
    nested_dir = project_root / "src" / "tools"
    result = resolve_project_root(str(nested_dir))
    assert result == project_root


def test_resolve_project_root_from_cwd(project_root, monkeypatch):
    """Test finding project root using cwd when no path specified."""
    monkeypatch.chdir(project_root / "src")
    result = resolve_project_root()
    assert result == project_root


def test_resolve_project_root_fails_from_temp_dir(tmp_path):
    """Test that resolve_project_root raises error from non-project directory."""
    # Create a temp dir without project markers
    temp_dir = tmp_path / "not_a_project"
    temp_dir.mkdir()
    
    with pytest.raises(FileNotFoundError) as exc_info:
        resolve_project_root(str(temp_dir))
    
    assert "Could not find project root" in str(exc_info.value)


# ============================================================================
# Tests for parse_yaml_frontmatter()
# ============================================================================

def test_parse_yaml_frontmatter_valid(tmp_path):
    """Test parsing a file with valid YAML frontmatter."""
    test_file = tmp_path / "test.md"
    content = """---
title: "Test Document"
version: 1.0
tags:
  - test
  - example
---

# Test Body

This is the body content.
"""
    test_file.write_text(content, encoding='utf-8')
    
    result = parse_yaml_frontmatter(str(test_file))
    
    assert result["success"] is True
    assert result["frontmatter"]["title"] == "Test Document"
    assert result["frontmatter"]["version"] in [1.0, "1.0"]  # Could be parsed as number or string
    assert "test" in result["frontmatter"]["tags"]
    assert "# Test Body" in result["body"]
    assert len(result["errors"]) == 0


def test_parse_yaml_frontmatter_no_frontmatter(tmp_path):
    """Test parsing a file without frontmatter."""
    test_file = tmp_path / "no_frontmatter.md"
    content = "# Just a heading\n\nSome content."
    test_file.write_text(content, encoding='utf-8')
    
    result = parse_yaml_frontmatter(str(test_file))
    
    assert result["success"] is True
    assert result["frontmatter"] == {}
    assert result["body"] == content
    assert len(result["errors"]) == 0


def test_parse_yaml_frontmatter_empty_frontmatter(tmp_path):
    """Test parsing a file with empty frontmatter."""
    test_file = tmp_path / "empty.md"
    content = """---
---

Content after empty frontmatter.
"""
    test_file.write_text(content, encoding='utf-8')
    
    result = parse_yaml_frontmatter(str(test_file))
    
    assert result["success"] is True
    assert result["frontmatter"] == {}
    assert "Content after empty frontmatter" in result["body"]


def test_parse_yaml_frontmatter_with_arrays(tmp_path):
    """Test parsing frontmatter with array fields."""
    test_file = tmp_path / "arrays.md"
    content = """---
project_name: "Test"
active_workstreams:
  - "Workstream 1.1: Design"
  - "Workstream 1.2: Implementation"
completed_workstreams: []
---

Body content.
"""
    test_file.write_text(content, encoding='utf-8')
    
    result = parse_yaml_frontmatter(str(test_file))
    
    assert result["success"] is True
    assert "Workstream 1.1: Design" in result["frontmatter"]["active_workstreams"]
    assert len(result["frontmatter"]["active_workstreams"]) == 2
    assert result["frontmatter"]["completed_workstreams"] == []


def test_parse_yaml_frontmatter_missing_file():
    """Test parsing a non-existent file."""
    result = parse_yaml_frontmatter("nonexistent.md")
    
    assert result["success"] is False
    assert len(result["errors"]) > 0
    assert "not found" in result["errors"][0].lower()


def test_parse_yaml_frontmatter_windows_line_endings(tmp_path):
    """Test parsing with Windows CRLF line endings."""
    test_file = tmp_path / "windows.md"
    content = "---\r\ntitle: \"Windows\"\r\n---\r\n\r\nBody\r\n"
    test_file.write_text(content, encoding='utf-8')
    
    result = parse_yaml_frontmatter(str(test_file))
    
    assert result["success"] is True
    assert result["frontmatter"]["title"] == "Windows"


# ============================================================================
# Tests for format_tool_response()
# ============================================================================

def test_format_tool_response_basic():
    """Test creating a basic tool response."""
    result = format_tool_response(True, "Operation completed")
    
    assert result["success"] is True
    assert result["message"] == "Operation completed"
    assert len(result) == 2


def test_format_tool_response_with_kwargs():
    """Test creating a tool response with additional fields."""
    result = format_tool_response(
        False, 
        "Operation failed",
        error_code=404,
        details={"reason": "Not found"}
    )
    
    assert result["success"] is False
    assert result["message"] == "Operation failed"
    assert result["error_code"] == 404
    assert result["details"]["reason"] == "Not found"


def test_format_tool_response_empty_message():
    """Test creating a response with empty message."""
    result = format_tool_response(True, "")
    
    assert result["success"] is True
    assert result["message"] == ""


# ============================================================================
# Tests for safe_read_file()
# ============================================================================

def test_safe_read_file_success(tmp_path):
    """Test reading a file successfully."""
    test_file = tmp_path / "test.txt"
    content = "Test content\nLine 2"
    test_file.write_text(content, encoding='utf-8')
    
    result = safe_read_file(str(test_file))
    
    assert result["success"] is True
    assert result["content"] == content
    assert len(result["errors"]) == 0


def test_safe_read_file_missing():
    """Test reading a non-existent file."""
    result = safe_read_file("nonexistent.txt")
    
    assert result["success"] is False
    assert result["content"] == ""
    assert len(result["errors"]) > 0
    assert "not found" in result["errors"][0].lower()


def test_safe_read_file_directory(tmp_path):
    """Test reading a directory instead of a file."""
    test_dir = tmp_path / "testdir"
    test_dir.mkdir()
    
    result = safe_read_file(str(test_dir))
    
    assert result["success"] is False
    assert "not a file" in result["errors"][0].lower()


def test_safe_read_file_encoding(tmp_path):
    """Test reading a file with specified encoding."""
    test_file = tmp_path / "encoded.txt"
    test_file.write_text("Test content", encoding='utf-8')
    
    result = safe_read_file(str(test_file), encoding='utf-8')
    
    assert result["success"] is True
    assert result["content"] == "Test content"


# ============================================================================
# Tests for safe_write_file()
# ============================================================================

def test_safe_write_file_success(tmp_path):
    """Test writing a file successfully."""
    test_file = tmp_path / "write_test.txt"
    content = "Test content to write"
    
    result = safe_write_file(str(test_file), content)
    
    assert result["success"] is True
    assert "Successfully wrote" in result["message"]
    assert len(result["errors"]) == 0
    
    # Verify file was actually written
    assert test_file.read_text(encoding='utf-8') == content


def test_safe_write_file_creates_parents(tmp_path):
    """Test that safe_write_file creates parent directories."""
    test_file = tmp_path / "nested" / "dir" / "file.txt"
    content = "Nested content"
    
    result = safe_write_file(str(test_file), content, create_parents=True)
    
    assert result["success"] is True
    assert test_file.exists()
    assert test_file.read_text(encoding='utf-8') == content


def test_safe_write_file_no_create_parents(tmp_path):
    """Test that safe_write_file fails when parent doesn't exist and create_parents=False."""
    test_file = tmp_path / "nonexistent" / "file.txt"
    
    result = safe_write_file(str(test_file), "content", create_parents=False)
    
    assert result["success"] is False
    assert len(result["errors"]) > 0


def test_safe_write_file_overwrites(tmp_path):
    """Test that safe_write_file overwrites existing files."""
    test_file = tmp_path / "overwrite.txt"
    test_file.write_text("Original content", encoding='utf-8')
    
    new_content = "New content"
    result = safe_write_file(str(test_file), new_content)
    
    assert result["success"] is True
    assert test_file.read_text(encoding='utf-8') == new_content


def test_safe_write_file_encoding(tmp_path):
    """Test writing a file with specified encoding."""
    test_file = tmp_path / "encoded.txt"
    content = "Test content with encoding"
    
    result = safe_write_file(str(test_file), content, encoding='utf-8')
    
    assert result["success"] is True
    assert test_file.read_text(encoding='utf-8') == content
