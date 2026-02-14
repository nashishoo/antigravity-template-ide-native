"""Shared utilities for all Antigravity tools.

This module provides common functions used across all tools to avoid
code duplication and ensure consistent behavior.

Author: Worker (Sonnet 4.5 Thinking — Workstream 2.1)
Version: 1.0
"""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any

# Optional YAML import with fallback
try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False


# ============================================================================
# Project Root Resolution
# ============================================================================

def resolve_project_root(start_path: Optional[str] = None) -> Path:
    """Find the project root by looking for marker files.
    
    Searches upward from start_path for project markers:
    - .context/ directory
    - PLAN.md file
    - .git/ directory
    
    Args:
        start_path: Starting directory. If None, uses cwd.
    
    Returns:
        Path to the project root.
    
    Raises:
        FileNotFoundError: If no project root markers are found.
    """
    current = Path(start_path) if start_path else Path.cwd()
    current = current.resolve()
    
    # Search upward for markers
    markers = [".context", "PLAN.md", ".git"]
    
    for parent in [current] + list(current.parents):
        for marker in markers:
            marker_path = parent / marker
            if marker_path.exists():
                return parent
    
    raise FileNotFoundError(
        f"Could not find project root from {current}. "
        f"Looking for markers: {', '.join(markers)}"
    )


# ============================================================================
# YAML Frontmatter Parsing
# ============================================================================

def parse_yaml_frontmatter(filepath: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from a markdown file.
    
    Handles:
    - Standard --- delimited YAML
    - Files without frontmatter (returns empty dict)
    - Malformed YAML (best-effort parsing with errors)
    - Array fields (active_workstreams, etc.)
    
    Uses pyyaml if available, falls back to regex parsing.
    
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
    path = Path(filepath)
    
    if not path.exists():
        return {
            "success": False,
            "frontmatter": {},
            "body": "",
            "errors": [f"File not found: {filepath}"]
        }
    
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "success": False,
            "frontmatter": {},
            "body": "",
            "errors": [f"Error reading file: {str(e)}"]
        }
    
    # Extract frontmatter section
    # Match: --- at start, content, --- (allowing \r\n on Windows)
    frontmatter_match = re.search(r'^---\r?\n(.*?)\r?\n---', content, re.DOTALL)
    
    if not frontmatter_match:
        # No frontmatter found
        return {
            "success": True,
            "frontmatter": {},
            "body": content,
            "errors": []
        }
    
    yaml_content = frontmatter_match.group(1)
    body = content[frontmatter_match.end():].lstrip('\r\n')
    errors = []
    
    # Try pyyaml first if available
    if _HAS_YAML:
        try:
            frontmatter = yaml.safe_load(yaml_content)
            if frontmatter is None:
                frontmatter = {}
            return {
                "success": True,
                "frontmatter": frontmatter,
                "body": body,
                "errors": []
            }
        except yaml.YAMLError as e:
            errors.append(f"YAML parsing error: {str(e)}")
            # Fall through to regex parsing
    
    # Fallback: regex-based parsing
    frontmatter = {}
    
    # Parse simple key-value pairs
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Match: key: value
        simple_match = re.match(r'^(\w+):\s*(.*)$', line)
        if simple_match:
            key = simple_match.group(1)
            value = simple_match.group(2).strip()
            
            # Remove quotes from strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            # Handle empty arrays
            if value == '[]':
                frontmatter[key] = []
            else:
                frontmatter[key] = value
    
    # Parse arrays (multi-line lists)
    array_pattern = re.compile(r'^(\w+):\s*\r?\n((?:  - .+\r?\n)*)', re.MULTILINE)
    for match in array_pattern.finditer(yaml_content):
        key = match.group(1)
        array_content = match.group(2)
        
        # Extract list items, removing quotes
        items = re.findall(r'  - "?(.+?)"?\s*$', array_content, re.MULTILINE)
        frontmatter[key] = items
    
    return {
        "success": len(errors) == 0,
        "frontmatter": frontmatter,
        "body": body,
        "errors": errors
    }


# ============================================================================
# Standardized Response Format
# ============================================================================

def format_tool_response(success: bool, message: str, **kwargs) -> Dict[str, Any]:
    """Create a standardized tool response dictionary.
    
    Every tool in the project should use this for consistent return format.
    
    Args:
        success: Whether the operation succeeded.
        message: Human-readable message.
        **kwargs: Additional key-value pairs to include.
    
    Returns:
        dict with "success", "message", and any additional fields.
    
    Examples:
        >>> format_tool_response(True, "Operation completed")
        {'success': True, 'message': 'Operation completed'}
        
        >>> format_tool_response(False, "Failed", error_code=404)
        {'success': False, 'message': 'Failed', 'error_code': 404}
    """
    response = {
        "success": success,
        "message": message
    }
    response.update(kwargs)
    return response


# ============================================================================
# Safe File I/O
# ============================================================================

def safe_read_file(filepath: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Read a file with comprehensive error handling.
    
    Args:
        filepath: Path to read.
        encoding: File encoding.
    
    Returns:
        dict: {"success": bool, "content": str, "errors": List[str]}
    """
    path = Path(filepath)
    
    if not path.exists():
        return {
            "success": False,
            "content": "",
            "errors": [f"File not found: {filepath}"]
        }
    
    if not path.is_file():
        return {
            "success": False,
            "content": "",
            "errors": [f"Path is not a file: {filepath}"]
        }
    
    try:
        content = path.read_text(encoding=encoding)
        return {
            "success": True,
            "content": content,
            "errors": []
        }
    except UnicodeDecodeError as e:
        return {
            "success": False,
            "content": "",
            "errors": [f"Encoding error: {str(e)}"]
        }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "errors": [f"Error reading file: {str(e)}"]
        }


def safe_write_file(
    filepath: str, 
    content: str, 
    encoding: str = "utf-8", 
    create_parents: bool = True
) -> Dict[str, Any]:
    """Write a file with comprehensive error handling.
    
    Args:
        filepath: Path to write.
        content: Content to write.
        encoding: File encoding.
        create_parents: Whether to create parent directories.
    
    Returns:
        dict: {"success": bool, "message": str, "errors": List[str]}
    """
    path = Path(filepath)
    
    try:
        # Create parent directories if requested
        if create_parents and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        path.write_text(content, encoding=encoding)
        
        return {
            "success": True,
            "message": f"Successfully wrote {len(content)} characters to {filepath}",
            "errors": []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to write file: {filepath}",
            "errors": [str(e)]
        }
