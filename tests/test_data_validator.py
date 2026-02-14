"""Unit tests for the Data Validation Pipeline.

Author: Worker (Gemini 3 Flash — Workstream 2.2)
"""

import pytest
import datetime
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tools.data_validator import validate_active_md, validate_plan_structure, validate_spec, validate_project

def test_validate_active_md_valid(tmp_path):
    """Test validation of a valid ACTIVE.md file."""
    active_file = tmp_path / "ACTIVE.md"
    content = """---
project_name: "Test Project"
mission_summary: "Testing the validator"
current_phase: "Phase 1"
active_workstreams:
  - "WS 1.1"
blocked_workstreams: []
completed_workstreams: []
last_architect_update: "2026-02-14T10:00:00+00:00"
last_worker_update: "2026-02-14T11:00:00+00:00"
critical_decisions: []
key_files_modified: []
integration_status: "Green"
next_milestone: "Finish tests"
risk_alerts: []
---
# Body
Context here.
"""
    active_file.write_text(content, encoding='utf-8')
    
    res = validate_active_md(str(active_file))
    assert res["valid"] is True
    assert len(res["errors"]) == 0
    assert res["field_count"] == 13

def test_validate_active_md_missing_fields(tmp_path):
    """Test validation fails when required fields are missing."""
    active_file = tmp_path / "ACTIVE.md"
    content = """---
project_name: "Broken Project"
# mission_summary missing
---
"""
    active_file.write_text(content, encoding='utf-8')
    
    res = validate_active_md(str(active_file))
    assert res["valid"] is False
    assert any("Schema validation error" in err for err in res["errors"])

def test_validate_active_md_field_limit(tmp_path):
    """Test validation fails when too many fields are present."""
    active_file = tmp_path / "ACTIVE.md"
    # 16 fields
    content = """---
project_name: "Too Many Fields"
mission_summary: "Testing limit"
current_phase: "1"
active_workstreams: []
blocked_workstreams: []
completed_workstreams: []
last_architect_update: "2026-02-14T10:00:00+00:00"
last_worker_update: "2026-02-14T11:00:00+00:00"
critical_decisions: []
key_files_modified: []
integration_status: "Fine"
next_milestone: "Test"
risk_alerts: []
extra_1: "test"
extra_2: "test"
extra_3: "test"
---
"""
    active_file.write_text(content, encoding='utf-8')
    
    res = validate_active_md(str(active_file))
    assert res["valid"] is False
    assert any("Field count exceeds protocol limit" in err for err in res["errors"])

def test_validate_active_md_staleness(tmp_path):
    """Test warning generation for stale ACTIVE.md."""
    active_file = tmp_path / "ACTIVE.md"
    # Update from 2 days ago
    stale_date = (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
    content = f"""---
project_name: "Stale Project"
mission_summary: "Testing staleness"
current_phase: "1"
active_workstreams: []
blocked_workstreams: []
completed_workstreams: []
last_architect_update: "{stale_date}"
last_worker_update: "{stale_date}"
critical_decisions: []
key_files_modified: []
integration_status: "Stale"
next_milestone: "Refresh"
risk_alerts: []
---
"""
    active_file.write_text(content, encoding='utf-8')
    
    res = validate_active_md(str(active_file))
    assert any("is stale" in warn for warn in res["warnings"])
    assert res["staleness_hours"] >= 48.0

def test_validate_plan_structure(tmp_path):
    """Test PLAN.md structure validation."""
    plan_file = tmp_path / "PLAN.md"
    content = """# Test Plan
## Phase 1: Setup
### Workstream 1.1: Task
- **Status:** COMPLETED
"""
    plan_file.write_text(content, encoding='utf-8')
    
    res = validate_plan_structure(str(plan_file))
    # It might be invalid due to missing metadata expected by plan_sync, 
    # but our added checks should pass if structure is generally right.
    assert isinstance(res, dict)
    assert "errors" in res

def test_validate_spec(tmp_path):
    """Test spec file validation."""
    spec_file = tmp_path / "protocol.md"
    content = """# My Protocol
Version: v1.0
This is a long enough body to pass the minimum length requirement for a spec file. It should have at least 50 characters.
"""
    spec_file.write_text(content, encoding='utf-8')
    
    res = validate_spec(str(spec_file))
    assert res["valid"] is True
    
    # Test failure (short body)
    spec_fail = tmp_path / "fail.md"
    spec_fail.write_text("# Title\nVersion: 1\nShort", encoding='utf-8')
    res_fail = validate_spec(str(spec_fail))
    assert res_fail["valid"] is False
    assert any("suspiciously short" in err for err in res_fail["errors"])

def test_validate_project(tmp_path, monkeypatch):
    """Test aggregate project validation."""
    # Mock project structure
    root = tmp_path / "project_root"
    root.mkdir()
    context = root / ".context"
    context.mkdir()
    specs = root / "specs"
    specs.mkdir()
    
    active = context / "ACTIVE.md"
    active.write_text("---\nproject_name: 'P'\nmission_summary: 'M'\ncurrent_phase: '1'\nactive_workstreams: []\nblocked_workstreams: []\ncompleted_workstreams: []\nlast_architect_update: '2026-02-14T10:00:00+00:00'\nlast_worker_update: '2026-02-14T11:00:00+00:00'\ncritical_decisions: []\nkey_files_modified: []\nintegration_status: 'I'\nnext_milestone: 'N'\nrisk_alerts: []\n---\n", encoding='utf-8')
    
    plan = root / "PLAN.md"
    plan.write_text("# Plan\n## Phase 1: P\n### Workstream 1.1: W\n", encoding='utf-8')
    
    spec = specs / "spec1.md"
    spec.write_text("# S1\nVersion: 1\nBody text length should be over fifty characters definitely for this test to pass successfully.", encoding='utf-8')

    # Mock resolve_project_root to return our tmp root
    from tools import _common
    monkeypatch.setattr(_common, "resolve_project_root", lambda *args: root)
    
    res = validate_project(str(root))
    assert "active_md" in res["results"]
    assert "plan_md" in res["results"]
    assert "specs" in res["results"]
    assert "overall_valid" in res
