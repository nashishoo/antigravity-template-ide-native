"""Tests for example_tool.

Author: Worker (Auto-generated)
Version: 1.0
"""

import pytest
from pathlib import Path

from tools.example_tool import func_a, func_b


def test_func_a(project_root):
    """Test func_a function."""
    # TODO: Implement test
    from tools.example_tool import func_a
    result = func_a()
    assert result["success"] is True


def test_func_b(project_root):
    """Test func_b function."""
    # TODO: Implement test
    from tools.example_tool import func_b
    result = func_b()
    assert result["success"] is True

