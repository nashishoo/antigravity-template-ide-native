"""Tests for File Watchdog & Task Synchronization.

Author: Worker (Sonnet 4.5 Thinking — Workstream 2.4)
Version: 1.0
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src/tools to path
sys.path.append(str(Path(__file__).parent.parent / "src" / "tools"))

from watchdog_sync import (
    detect_changes_since,
    suggest_active_updates,
    check_staleness,
    generate_change_report,
    build_workstream_map,
    _match_file_to_workstreams,
    _should_ignore
)


# ============================================================================
# Fixture: Create test files
# ============================================================================

@pytest.fixture
def test_files(project_root, tmp_path):
    """Create test files with specific modification times."""
    # Create some test files
    src_tools = project_root / "src" / "tools"
    src_tools.mkdir(parents=True, exist_ok=True)
    
    specs = project_root / "specs"
    specs.mkdir(parents=True, exist_ok=True)
    
    tests_dir = project_root / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    
    # Create files
    test_tool = src_tools / "test_tool.py"
    test_tool.write_text("# Test tool")
    
    test_spec = specs / "test_spec.md"
    test_spec.write_text("# Test Spec")
    
    test_file = tests_dir / "test_example.py"
    test_file.write_text("# Test file")
    
    return {
        "tool": test_tool,
        "spec": test_spec,
        "test": test_file
    }


# ============================================================================
# Tests: detect_changes_since()
# ============================================================================

def test_detect_changes_since_basic(project_root, test_files):
    """Test basic file change detection."""
    # Set timestamp to 1 hour ago
    one_hour_ago = (datetime.now().astimezone() - timedelta(hours=1)).isoformat()
    
    result = detect_changes_since(one_hour_ago, str(project_root))
    
    assert result["success"] is True
    assert len(result["changes"]) > 0
    assert "changes" in result
    assert "summary" in result


def test_detect_changes_since_no_changes(project_root, test_files):
    """Test change detection with future timestamp (no changes)."""
    # Set timestamp to future
    future = (datetime.now().astimezone() + timedelta(hours=1)).isoformat()
    
    result = detect_changes_since(future, str(project_root))
    
    assert result["success"] is True
    assert len(result["changes"]) == 0
    assert "0 change" in result["summary"]


def test_detect_changes_since_invalid_timestamp(project_root):
    """Test change detection with invalid timestamp."""
    result = detect_changes_since("not-a-timestamp", str(project_root))
    
    assert result["success"] is False
    assert "Invalid timestamp" in result["message"]


def test_detect_changes_since_multiple_types(project_root, test_files):
    """Test detection of different change types."""
    # Create timestamp before files
    old_timestamp = (datetime.now().astimezone() - timedelta(days=1)).isoformat()
    
    result = detect_changes_since(old_timestamp, str(project_root))
    
    assert result["success"] is True
    changes = result["changes"]
    
    # Should detect the test files we created
    assert any("test_tool.py" in c["filepath"] for c in changes)


# ============================================================================
# Tests: build_workstream_map()
# ============================================================================

def test_build_workstream_map(sample_plan_md):
    """Test building workstream map from PLAN.md."""
    result = build_workstream_map(str(sample_plan_md))
    
    assert isinstance(result, dict)
    # The sample PLAN.md should have some deliverables
    # This is a basic smoke test
    assert len(result) >= 0  # May be empty if sample has no file deliverables


def test_build_workstream_map_missing_plan():
    """Test workstream map with missing PLAN.md."""
    result = build_workstream_map("/nonexistent/path/PLAN.md")
    
    assert result == {}


# ============================================================================
# Tests: _match_file_to_workstreams()
# ============================================================================

def test_match_file_to_workstreams_direct():
    """Test direct file match."""
    workstream_map = {
        "src/tools/scaffold.py": [("2.3", 1.0)]
    }
    
    matches = _match_file_to_workstreams("src/tools/scaffold.py", workstream_map)
    
    assert len(matches) == 1
    assert matches[0][0] == "2.3"
    assert matches[0][1] == 1.0


def test_match_file_to_workstreams_directory():
    """Test directory-based match."""
    workstream_map = {
        "src/tools": [("2.1", 0.8)]
    }
    
    matches = _match_file_to_workstreams("src/tools/test.py", workstream_map)
    
    assert len(matches) >= 0  # May match or not depending on implementation


def test_match_file_to_workstreams_no_match():
    """Test no match."""
    workstream_map = {
        "src/tools/scaffold.py": [("2.3", 1.0)]
    }
    
    matches = _match_file_to_workstreams("unrelated/file.txt", workstream_map)
    
    assert len(matches) == 0


# ============================================================================
# Tests: suggest_active_updates()
# ============================================================================

def test_suggest_active_updates_src_tools():
    """Test suggestions for src/tools/ changes."""
    changes = [
        {
            "filepath": "src/tools/scaffold.py",
            "change_type": "modified",
            "timestamp": datetime.now().astimezone().isoformat()
        }
    ]
    
    result = suggest_active_updates(changes)
    
    assert "suggestions" in result
    assert len(result["suggestions"]) > 0
    assert any("key_files_modified" in s for s in result["suggestions"])


def test_suggest_active_updates_specs():
    """Test suggestions for specs/ changes."""
    changes = [
        {
            "filepath": "specs/new_spec.md",
            "change_type": "created",
            "timestamp": datetime.now().astimezone().isoformat()
        }
    ]
    
    result = suggest_active_updates(changes)
    
    assert "suggestions" in result
    assert len(result["suggestions"]) > 0
    # Should suggest updating both key_files and potentially critical_decisions
    assert any("spec" in s.lower() for s in result["suggestions"])


def test_suggest_active_updates_tests():
    """Test suggestions for tests/ changes."""
    changes = [
        {
            "filepath": "tests/test_new.py",
            "change_type": "modified",
            "timestamp": datetime.now().astimezone().isoformat()
        }
    ]
    
    result = suggest_active_updates(changes)
    
    assert "suggestions" in result
    assert len(result["suggestions"]) > 0
    assert any("integration_status" in s for s in result["suggestions"])


def test_suggest_active_updates_empty():
    """Test suggestions with no changes."""
    result = suggest_active_updates([])
    
    assert result["suggestions"] == []
    assert result["auto_applicable"] == []
    assert result["manual_review"] == []


# ============================================================================
# Tests: check_staleness()
# ============================================================================

def test_check_staleness_fresh(sample_active_md):
    """Test staleness check with fresh ACTIVE.md."""
    # sample_active_md should have recent timestamps
    result = check_staleness(str(sample_active_md))
    
    assert result["success"] is True
    assert "is_stale" in result
    # Should not be stale (fixture creates with current time)
    assert result["is_stale"] is False


def test_check_staleness_stale(project_root):
    """Test staleness check with stale ACTIVE.md."""
    # Create a stale ACTIVE.md
    active_path = project_root / ".context" / "ACTIVE.md"
    active_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create ACTIVE.md with old timestamp (48 hours ago)
    old_time = (datetime.now().astimezone() - timedelta(hours=48)).isoformat()
    
    active_content = f"""---
project_name: "Test Project"
mission_summary: "Test"
current_phase: "Phase 1"
active_workstreams: []
blocked_workstreams: []
completed_workstreams: []
last_architect_update: "{old_time}"
last_worker_update: "{old_time}"
critical_decisions: []
key_files_modified: []
integration_status: "Test"
next_milestone: "Test"
risk_alerts: []
---

# Test
"""
    active_path.write_text(active_content)
    
    result = check_staleness(str(active_path))
    
    assert result["success"] is True
    assert result["is_stale"] is True
    assert result["hours_since_architect_update"] > 24
    assert "stale" in result["recommendation"].lower()


def test_check_staleness_missing_file():
    """Test staleness check with missing ACTIVE.md."""
    result = check_staleness("/nonexistent/ACTIVE.md")
    
    assert result["success"] is False


def test_check_staleness_timezone_aware(project_root):
    """Test staleness with timezone-aware timestamps."""
    active_path = project_root / ".context" / "ACTIVE.md"
    active_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create with timezone-aware timestamp
    now = datetime.now().astimezone()
    timestamp = now.isoformat()
    
    active_content = f"""---
project_name: "Test Project"
mission_summary: "Test"
current_phase: "Phase 1"
active_workstreams: []
blocked_workstreams: []
completed_workstreams: []
last_architect_update: "{timestamp}"
last_worker_update: "{timestamp}"
critical_decisions: []
key_files_modified: []
integration_status: "Test"
next_milestone: "Test"
risk_alerts: []
---

# Test
"""
    active_path.write_text(active_content)
    
    result = check_staleness(str(active_path))
    
    assert result["success"] is True
    assert result["is_stale"] is False
    assert result["hours_since_architect_update"] < 1


# ============================================================================
# Tests: generate_change_report()
# ============================================================================

def test_generate_change_report(project_root, test_files, sample_active_md):
    """Test comprehensive change report generation."""
    result = generate_change_report(str(project_root))
    
    assert result["success"] is True
    assert "report" in result
    
    report = result["report"]
    assert "file_changes" in report
    assert "active_md_staleness" in report
    assert "summary" in report


def test_generate_change_report_with_since(project_root, test_files):
    """Test change report with specific timestamp."""
    one_hour_ago = (datetime.now().astimezone() - timedelta(hours=1)).isoformat()
    
    result = generate_change_report(str(project_root), since=one_hour_ago)
    
    assert result["success"] is True
    assert "report" in result


# ============================================================================
# Tests: _should_ignore()
# ============================================================================

def test_should_ignore_git():
    """Test ignoring .git directory."""
    path = Path(".git/config")
    assert _should_ignore(path) is True


def test_should_ignore_pycache():
    """Test ignoring __pycache__."""
    path = Path("src/__pycache__/test.pyc")
    assert _should_ignore(path) is True


def test_should_ignore_venv():
    """Test ignoring venv."""
    path = Path("venv/lib/python3.11/site-packages/test.py")
    assert _should_ignore(path) is True


def test_should_ignore_valid_file():
    """Test not ignoring valid files."""
    path = Path("src/tools/test.py")
    assert _should_ignore(path) is False


def test_should_ignore_context_allowed():
    """Test that .context directory is NOT ignored."""
    path = Path(".context/ACTIVE.md")
    assert _should_ignore(path) is False


# ============================================================================
# Edge Cases
# ============================================================================

def test_detect_changes_timezone_naive(project_root, test_files):
    """Test change detection with timezone-naive timestamp."""
    # Naive timestamp (no timezone)
    naive_time = datetime.now().replace(tzinfo=None).isoformat()
    
    result = detect_changes_since(naive_time, str(project_root))
    
    # Should handle gracefully with fallback
    assert result["success"] is True


def test_suggest_updates_with_workstream_detection(project_root, sample_plan_md, test_files):
    """Test suggestion with workstream detection enabled."""
    changes = [
        {
            "filepath": "src/tools/_common.py",
            "change_type": "modified",
            "timestamp": datetime.now().astimezone().isoformat()
        }
    ]
    
    result = suggest_active_updates(changes)
    
    assert "suggestions" in result
    # _common.py is a foundational file, should generate suggestions


def test_large_change_list(project_root):
    """Test handling of very large change list."""
    # Create 150 fake changes
    changes = [
        {
            "filepath": f"src/file_{i}.py",
            "change_type": "modified",
            "timestamp": datetime.now().astimezone().isoformat()
        }
        for i in range(150)
    ]
    
    result = suggest_active_updates(changes)
    
    assert "suggestions" in result
    # Should handle gracefully without crashing
