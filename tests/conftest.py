"""Shared pytest fixtures for all test files.

This module provides common test fixtures that can be used across
all test files to avoid duplication and ensure consistent test setup.

Author: Worker (Sonnet 4.5 Thinking — Workstream 2.1)
Version: 1.0
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root(tmp_path):
    """Create a minimal project structure for testing.
    
    Creates:
    - .context/ directory
    - PLAN.md file
    - .archive/ with subdirectories
    - src/tools/ directory
    
    Args:
        tmp_path: pytest's temporary directory fixture
    
    Returns:
        Path to the temporary project root
    """
    # Create directory structure
    (tmp_path / ".context").mkdir()
    (tmp_path / ".archive" / "completed").mkdir(parents=True)
    (tmp_path / ".archive" / "deprecated").mkdir(parents=True)
    (tmp_path / ".archive" / "snapshots").mkdir(parents=True)
    (tmp_path / "src" / "tools").mkdir(parents=True)
    
    # Create marker file
    (tmp_path / "PLAN.md").write_text("# Test Plan\n", encoding='utf-8')
    
    return tmp_path


@pytest.fixture
def sample_active_md(project_root):
    """Create a sample ACTIVE.md with valid frontmatter.
    
    Args:
        project_root: The project_root fixture
    
    Returns:
        Path to the created ACTIVE.md file
    """
    active_content = """---
project_name: "Test Project"
mission_summary: "Test mission"
current_phase: "Phase 1: Foundation"
active_workstreams:
  - "Workstream 1.2: Implementation"
blocked_workstreams: []
completed_workstreams:
  - "Workstream 1.1: Protocol Design (COMPLETE)"
last_architect_update: "2026-02-14T00:00:00-03:00"
last_worker_update: "2026-02-14T00:00:00-03:00"
critical_decisions: []
key_files_modified: []
integration_status: "Testing"
next_milestone: "Complete Phase 1"
risk_alerts: []
---

# Active Context

## 🎯 Current Focus
Testing phase

## 📋 Recent Changes
- Recent change 1

## 🚧 Blockers
None

## 💬 Notes for Workers
Test notes
"""
    active_file = project_root / ".context" / "ACTIVE.md"
    active_file.write_text(active_content, encoding='utf-8')
    return active_file


@pytest.fixture
def sample_plan_md(project_root):
    """Create a sample PLAN.md with phases and workstreams.
    
    Args:
        project_root: The project_root fixture
    
    Returns:
        Path to the created PLAN.md file
    """
    plan_content = """# Project Plan

**Architect:** Test Architect
**Start Date:** 2026-02-10
**Target Completion:** 2026-02-20
**Status:** In Progress

---

## Phase 1: Foundation
**Duration:** ~5 hours
**Goal:** Set up project infrastructure

### Workstream 1.1: Protocol Design
- **Worker Role:** Protocol Specialist
- **Model:** Claude Sonnet 4.5
- **Deliverables:**
  - specs/protocol.md
  - .context/ACTIVE.md
- **Dependencies:** None
- **Blocks:** Workstream 1.2

### Workstream 1.2: Implementation
- **Worker Role:** Software Engineer
- **Model:** Claude Sonnet 4.5
- **Deliverables:**
  - src/tools/plan_sync.py
- **Dependencies:** Workstream 1.1
- **Blocks:** None

---

## Phase 2: Enhancement
**Duration:** ~3 hours
**Goal:** Add advanced features

### Workstream 2.1: Testing
- **Worker Role:** QA Engineer
- **Model:** Gemini 3 Flash
- **Deliverables:**
  - tests/test_plan_sync.py
- **Dependencies:** Workstream 1.2
- **Blocks:** None
"""
    plan_file = project_root / "PLAN.md"
    plan_file.write_text(plan_content, encoding='utf-8')
    return plan_file


@pytest.fixture
def archive_structure(project_root):
    """Create a .archive/ directory with subdirectories.
    
    Args:
        project_root: The project_root fixture
    
    Returns:
        Path to the .archive directory
    """
    archive_dir = project_root / ".archive"
    # Already created by project_root, but we can add .keep files
    (archive_dir / "completed" / ".keep").touch()
    (archive_dir / "deprecated" / ".keep").touch()
    (archive_dir / "snapshots" / ".keep").touch()
    return archive_dir
