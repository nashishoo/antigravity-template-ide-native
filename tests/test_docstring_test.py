"""Tests for docstring_test.

Author: Worker (Auto-generated)
Version: 1.0
"""

import pytest
from pathlib import Path

from tools.docstring_test import documented_func


def test_documented_func(project_root):
    """Test documented_func function."""
    # TODO: Implement test
    from tools.docstring_test import documented_func
    result = documented_func()
    assert result["success"] is True

