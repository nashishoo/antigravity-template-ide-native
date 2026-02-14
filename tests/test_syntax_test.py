"""Tests for syntax_test.

Author: Worker (Auto-generated)
Version: 1.0
"""

import pytest
from pathlib import Path

from tools.syntax_test import test_func


def test_test_func(project_root):
    """Test test_func function."""
    # TODO: Implement test
    from tools.syntax_test import test_func
    result = test_func()
    assert result["success"] is True

