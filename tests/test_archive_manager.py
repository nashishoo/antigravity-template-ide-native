import os
import json
from pathlib import Path
import pytest
import sys

# Add src to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.archive_manager import ArchiveManager

@pytest.fixture
def manager(tmp_path):
    """Setup a mock project structure in tmp_path."""
    (tmp_path / ".context").mkdir(parents=True, exist_ok=True)
    (tmp_path / "PLAN.md").write_text("Plan content")
    (tmp_path / ".context" / "ACTIVE.md").write_text("Active content")
    return ArchiveManager(project_root=str(tmp_path))

def test_archive_completed(manager, tmp_path):
    """Test archiving a completed file."""
    dummy_file = tmp_path / "completed_work.txt"
    dummy_file.write_text("Some work")
    
    result = manager.archive_completed("completed_work.txt", "Work finished")
    
    assert result["status"] == "success"
    assert not dummy_file.exists()
    
    archive_path = tmp_path / result["archive_path"]
    assert archive_path.exists()
    
    # Check meta file
    meta_file = archive_path.with_suffix(".txt.meta.json")
    assert meta_file.exists()
    
    with open(meta_file, "r") as f:
        meta = json.load(f)
        assert meta["original_path"] == "completed_work.txt"
        assert meta["reason"] == "Work finished"

def test_archive_deprecated(manager, tmp_path):
    """Test archiving a deprecated item."""
    dummy_file = tmp_path / "old_tool.py"
    dummy_file.write_text("old code")
    
    result = manager.archive_deprecated("old_tool.py", "new_tool.py")
    
    assert result["status"] == "success"
    assert not dummy_file.exists()
    
    archive_path = tmp_path / result["archive_path"]
    assert archive_path.exists()
    
    # Check meta file
    meta_file = archive_path.with_suffix(".py.meta.json")
    assert meta_file.exists()
    
    with open(meta_file, "r") as f:
        meta = json.load(f)
        assert meta["replacement"] == "new_tool.py"

def test_create_snapshot(manager, tmp_path):
    """Test creating a snapshot of context files."""
    result = manager.create_snapshot("test_label")
    assert result["status"] == "success"
    
    snapshot_path = tmp_path / result["snapshot_path"]
    assert snapshot_path.exists()
    assert (snapshot_path / "ACTIVE.md").exists()
    assert (snapshot_path / "PLAN.md").exists()

def test_restore_from_archive(manager, tmp_path):
    """Test restoring an item from archive."""
    # 1. Archive a file
    dummy_file = tmp_path / "to_restore.txt"
    dummy_file.write_text("content")
    res_arch = manager.archive_completed("to_restore.txt", "Testing restore")
    
    # 2. Restore it
    res_rest = manager.restore_from_archive(res_arch["archive_path"])
    
    assert res_rest["status"] == "success"
    assert dummy_file.exists()
    assert dummy_file.read_text() == "content"
    
    # Meta file should be gone
    archive_path = tmp_path / res_arch["archive_path"]
    meta_file = archive_path.with_suffix(".txt.meta.json")
    assert not meta_file.exists()

def test_restore_conflict(manager, tmp_path):
    """Test restoration conflict detection."""
    # Archive a file
    dummy_file = tmp_path / "conflict.txt"
    dummy_file.write_text("old content")
    res_arch = manager.archive_completed("conflict.txt", "Testing conflict")
    
    # Create a NEW file with same name
    dummy_file.write_text("new content")
    
    # Try to restore
    res_rest = manager.restore_from_archive(res_arch["archive_path"])
    
    assert res_rest["status"] == "error"
    assert "Conflict" in res_rest["message"]
    assert dummy_file.read_text() == "new content" # New file preserved

def test_list_archive(manager, tmp_path):
    """Test listing archive contents."""
    # Archive two things
    (tmp_path / "file1.txt").write_text("1")
    (tmp_path / "file2.txt").write_text("2")
    manager.archive_completed("file1.txt", "R1")
    manager.archive_deprecated("file2.txt", "None")
    
    result = manager.list_archive("all")
    assert result["status"] == "success"
    assert len(result["items"]) >= 2
    
    names = [item["name"] for item in result["items"]]
    assert "file1.txt" in names
    assert "file2.txt" in names

def test_archive_directory(manager, tmp_path):
    """Test archiving an entire directory."""
    dummy_dir = tmp_path / "my_dir"
    dummy_dir.mkdir()
    (dummy_dir / "subfile.txt").write_text("subcontent")
    
    result = manager.archive_completed("my_dir", "Dir finished")
    
    assert result["status"] == "success"
    assert not dummy_dir.exists()
    
    archive_path = tmp_path / result["archive_path"]
    assert archive_path.is_dir()
    assert (archive_path / "subfile.txt").exists()
    
    # Check meta file
    meta_file = archive_path.parent / "my_dir.meta.json"
    assert meta_file.exists()
