# Plan Synchronization Protocol Specification

**Version:** v1.0  
**Status:** ✅ Approved  
**Created:** 2026-02-14  
**Author:** Worker (Claude Sonnet 4.5 Thinking — Workstream 1.2)

---

## 1. Overview

### Purpose
The Plan Synchronization Protocol enables workers to extract context from PLAN.md (strategic roadmap) and maintain consistency with ACTIVE.md (tactical state). This eliminates manual context transfer and provides a verifiable single source of truth for project planning.

### Success Metrics
- Any worker can validate their task alignment against PLAN.md
- Workers can extract their specific workstream context programmatically
- Architect can update workstream status without manual file editing
- PLAN.md and ACTIVE.md remain synchronized (detectable via sync_check)

### Design Philosophy
- **Backward Compatible**: Parse existing PLAN.md format without modifications
- **Regex-Based Parsing**: No external markdown parser dependencies
- **Graceful Degradation**: Missing or malformed PLAN.md doesn't crash tools
- **Read-Heavy, Write-Light**: Workers read PLAN.md; Architect updates it
- **Validation, Not Enforcement**: Sync check warns, doesn't auto-fix

---

## 2. PLAN.md Structure

### Location
`PLAN.md` (project root)

### Required Sections

#### Header Metadata (Optional but Recommended)
```markdown
# [Project Title]

**Architect:** [Name/Model]
**Start Date:** YYYY-MM-DD
**Target Completion:** YYYY-MM-DD (duration)
**Status:** [Status description]
```

#### Phase Sections (Required for Parsing)
```markdown
## Phase N: [Phase Title]
**Duration:** [Estimate]
**Goal:** [Phase objective]

### Workstream N.N: [Workstream Title]
- **Worker Role:** [Role description]
- **Model:** [AI model name]
- **Deliverables:**
  - [File/Artifact 1]
  - [File/Artifact 2]
- **Dependencies:** [Workstream IDs or "None"]
- **Blocks:** [Workstream IDs or "None"]
```

### Format Conventions

| Element | Pattern | Example |
|---------|---------|---------|
| **Phase Header** | `## Phase N: Title` | `## Phase 1: Context Synchronization (Foundation)` |
| **Workstream Header** | `### Workstream N.N: Title` | `### Workstream 1.2: Plan Synchronization System` |
| **Metadata Field** | `- **FieldName:** Value` | `- **Model:** Claude Sonnet 4.5 (Thinking)` |
| **List Item** | `  - Item text` | `  - .context/ACTIVE.md` |
| **Dependency/Blocks** | `Workstream N.N` or `None` | `Workstream 1.1` |

### Regex Patterns (Implementation Reference)

```python
PHASE_PATTERN = r"^## Phase (\d+): (.+)$"
# Captures: (phase_id, title)

WORKSTREAM_PATTERN = r"^### Workstream ([\d\.]+): (.+)$"
# Captures: (workstream_id, title)

METADATA_PATTERN = r"^\s*-\s+\*\*([^:]+):\*\*\s+(.+)$"
# Captures: (field_name, value)

LIST_ITEM_PATTERN = r"^\s+-\s+(.+)$"
# Captures: (item_text)
```

---

## 3. Status Vocabulary

### Status States

| Status | Meaning | PLAN.md Indicator | ACTIVE.md Field |
|--------|---------|-------------------|-----------------|
| **PLANNED** | Not started, scheduled for future | `[ ]` in checklist | Not in any workstream arrays |
| **IN_PROGRESS** | Currently being worked on | `[/]` in checklist or explicit text | `active_workstreams` array |
| **BLOCKED** | Stuck, waiting for dependency or resolution | Explicit "BLOCKED" text | `blocked_workstreams` array |
| **COMPLETED** | Finished and validated | `[x]` in checklist | `completed_workstreams` array |
| **CANCELLED** | Abandoned, no longer planned | Struck through or removed | Not in any arrays (or noted in ACTIVE.md body) |

### Status Transitions

```
PLANNED → IN_PROGRESS → COMPLETED
PLANNED → IN_PROGRESS → BLOCKED → IN_PROGRESS → COMPLETED
PLANNED → CANCELLED
IN_PROGRESS → CANCELLED
```

### Determining Status (Parsing Logic)

1. **Check for explicit checklist marker**:
   - `[x]` → `COMPLETED`
   - `[/]` → `IN_PROGRESS`
   - `[ ]` → `PLANNED`

2. **Check for explicit text**:
   - Contains "BLOCKED" or "blocked" → `BLOCKED`
   - Contains "CANCELLED" or struck through → `CANCELLED`

3. **Default**: If no indicator found → `PLANNED`

---

## 4. Relationship to ACTIVE.md

### Division of Responsibilities

| Aspect | PLAN.md | ACTIVE.md |
|--------|---------|-----------|
| **Owner** | Architect creates/updates | Workers update, Architect reviews |
| **Scope** | Strategic roadmap (all phases, all workstreams) | Tactical state (active work, recent changes) |
| **Timeframe** | Long-term (project lifecycle) | Short-term (current session, hours/days) |
| **Update Frequency** | When plan changes (phases added, workstreams reordered) | On every worker entry/exit |
| **Read Priority** | Read FIRST | Read SECOND |
| **Granularity** | High-level (workstream level) | Detailed (file-level changes, blockers) |

### Sync Rules

#### Rule 1: Workstream Status Alignment
- **PLAN.md shows `COMPLETED`** → ACTIVE.md should have workstream in `completed_workstreams`
- **PLAN.md shows `IN_PROGRESS`** → ACTIVE.md should have workstream in `active_workstreams`
- **PLAN.md shows `BLOCKED`** → ACTIVE.md should have workstream in `blocked_workstreams`

#### Rule 2: Dependency Consistency
- If Workstream A depends on Workstream B, and PLAN.md shows A as `IN_PROGRESS`, then B should be `COMPLETED`
- Violation = Warning in `sync_check()`

#### Rule 3: Phase Alignment
- `current_phase` in ACTIVE.md should match an active phase in PLAN.md
- If all workstreams in Phase N are `COMPLETED`, ACTIVE.md should move to Phase N+1

### Sync Enforcement

**v1.0 Strategy:** Validation only (no auto-correction)

- `sync_check()` function detects discrepancies
- Returns warnings for Architect to resolve manually
- Workers should call `sync_check()` before starting work (optional)

**Future (Phase 2):** Auto-sync via file watchdog
- Architect updates PLAN.md → Watchdog updates ACTIVE.md
- Worker updates ACTIVE.md → Watchdog validates against PLAN.md

---

## 5. Pydantic Models

### WorkstreamMetadata

```python
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class WorkstreamMetadata(BaseModel):
    """Metadata for a single workstream.
    
    Attributes:
        workstream_id: Unique ID (e.g., "1.2")
        title: Human-readable title
        worker_role: Role description (e.g., "Workflow Engineer")
        model: AI model name (e.g., "Claude Sonnet 4.5 (Thinking)")
        deliverables: List of files/artifacts to create
        dependencies: List of workstream IDs this depends on
        blocks: List of workstream IDs this blocks
        status: Current status (PLANNED, IN_PROGRESS, etc.)
    """
    workstream_id: str
    title: str
    worker_role: Optional[str] = None
    model: Optional[str] = None
    deliverables: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    blocks: List[str] = Field(default_factory=list)
    status: Literal["PLANNED", "IN_PROGRESS", "BLOCKED", "COMPLETED", "CANCELLED"] = "PLANNED"
```

### PhaseMetadata

```python
class PhaseMetadata(BaseModel):
    """Metadata for a single phase.
    
    Attributes:
        phase_id: Phase number (1, 2, 3, ...)
        title: Human-readable title
        duration: Estimated duration (e.g., "~5 hours")
        goal: Phase objective
        workstreams: List of workstreams in this phase
    """
    phase_id: int
    title: str
    duration: Optional[str] = None
    goal: Optional[str] = None
    workstreams: List[WorkstreamMetadata] = Field(default_factory=list)
```

### PlanMetadata

```python
class PlanMetadata(BaseModel):
    """Parsed PLAN.md metadata.
    
    Attributes:
        architect: Name/model of Architect
        start_date: Project start date
        target_completion: Target completion date
        status: Current project status
        phases: List of all phases
    """
    architect: Optional[str] = None
    start_date: Optional[str] = None
    target_completion: Optional[str] = None
    status: Optional[str] = None
    phases: List[PhaseMetadata] = Field(default_factory=list)
    
    def get_workstream(self, workstream_id: str) -> Optional[WorkstreamMetadata]:
        """Find workstream by ID across all phases."""
        for phase in self.phases:
            for ws in phase.workstreams:
                if ws.workstream_id == workstream_id:
                    return ws
        return None
    
    def get_phase(self, phase_id: int) -> Optional[PhaseMetadata]:
        """Find phase by ID."""
        for phase in self.phases:
            if phase.phase_id == phase_id:
                return phase
        return None
```

---

## 6. Tool Functions

### parse_plan()

**Purpose:** Parse PLAN.md into structured data

**Signature:**
```python
def parse_plan(plan_path: str = "PLAN.md") -> dict:
    """Parse PLAN.md into structured data.
    
    Args:
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "success": bool,
            "metadata": PlanMetadata | None,
            "errors": List[str],
            "raw_content": str
        }
    """
```

**Behavior:**
- **Missing file**: Returns `{"success": False, "metadata": None, "errors": ["File not found: PLAN.md"]}`
- **Parse error**: Logs error, continues parsing remaining sections
- **Unknown fields**: Ignored (forward compatibility)

---

### validate_plan()

**Purpose:** Check PLAN.md for consistency

**Signature:**
```python
def validate_plan(plan_path: str = "PLAN.md") -> dict:
    """Check PLAN.md for consistency.
    
    Args:
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str]
        }
    """
```

**Validation Checks:**
1. **Orphan Dependencies**: Workstream claims dependency on non-existent workstream
2. **Circular Dependencies**: A depends on B, B depends on A
3. **Invalid Status**: Status value not in vocabulary
4. **Missing Required Fields**: Workstream has no title

**Example Output:**
```json
{
  "valid": false,
  "errors": [
    "Workstream 1.2 depends on non-existent Workstream 1.5",
    "Circular dependency detected: 2.1 → 2.2 → 2.1"
  ],
  "warnings": [
    "Workstream 1.3 has no deliverables"
  ]
}
```

---

### generate_worker_context()

**Purpose:** Extract context for a specific workstream

**Signature:**
```python
def generate_worker_context(workstream_id: str, plan_path: str = "PLAN.md") -> dict:
    """Extract context for a specific workstream.
    
    Args:
        workstream_id: Workstream ID (e.g., "1.2")
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "success": bool,
            "workstream": WorkstreamMetadata | None,
            "phase_context": PhaseMetadata | None,
            "dependency_details": List[WorkstreamMetadata],
            "blocks_details": List[WorkstreamMetadata],
            "errors": List[str]
        }
    """
```

**Use Case:** Worker can call this at the start of their session to understand:
- What they need to deliver
- What dependencies are already completed
- What they're blocking (so they know the urgency)
- What phase context they're operating in

**Example Output:**
```json
{
  "success": true,
  "workstream": {
    "workstream_id": "1.2",
    "title": "Plan Synchronization System",
    "worker_role": "Workflow Engineer",
    "model": "Claude Sonnet 4.5 (Thinking)",
    "deliverables": ["specs/plan_sync_protocol.md", "src/tools/plan_sync.py", ...],
    "dependencies": ["1.1"],
    "blocks": ["2.4"],
    "status": "IN_PROGRESS"
  },
  "phase_context": {
    "phase_id": 1,
    "title": "Context Synchronization (Foundation)",
    "duration": "~5 hours",
    "goal": "Eliminate manual context transfer between Architect and Workers"
  },
  "dependency_details": [
    {
      "workstream_id": "1.1",
      "title": "Active Context Protocol",
      "status": "COMPLETED",
      ...
    }
  ],
  "blocks_details": [
    {
      "workstream_id": "2.4",
      "title": "File Watchdog & Task Sync",
      "status": "PLANNED",
      ...
    }
  ],
  "errors": []
}
```

---

### update_workstream_status()

**Purpose:** Update workstream status in PLAN.md

**Signature:**
```python
def update_workstream_status(
    workstream_id: str, 
    new_status: Literal["PLANNED", "IN_PROGRESS", "BLOCKED", "COMPLETED", "CANCELLED"],
    plan_path: str = "PLAN.md"
) -> dict:
    """Update workstream status in PLAN.md.
    
    Args:
        workstream_id: Workstream ID (e.g., "1.2")
        new_status: New status value
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "success": bool,
            "old_status": str,
            "new_status": str,
            "updated_lines": int,
            "errors": List[str]
        }
    """
```

**Strategy:**
- Find workstream section in PLAN.md
- Update checklist marker if present (e.g., `[ ]` → `[x]`)
- If no checklist, add status indicator text
- Preserve all other content

**Example:** Workstream 1.1 transitions from `IN_PROGRESS` to `COMPLETED`
```diff
- [/] Workstream 1.1 — ACTIVE.md Protocol → **Prompt ready** (see below)
+ [x] Workstream 1.1 — ACTIVE.md Protocol → **COMPLETE**
```

---

### sync_check()

**Purpose:** Check consistency between PLAN.md and ACTIVE.md

**Signature:**
```python
def sync_check(plan_path: str = "PLAN.md", active_path: str = ".context/ACTIVE.md") -> dict:
    """Check consistency between PLAN.md and ACTIVE.md.
    
    Args:
        plan_path: Path to PLAN.md
        active_path: Path to ACTIVE.md
        
    Returns:
        dict: {
            "in_sync": bool,
            "discrepancies": List[dict],
            "warnings": List[str]
        }
    """
```

**Checks:**
1. Workstreams marked `COMPLETED` in PLAN.md are in `completed_workstreams` in ACTIVE.md
2. Workstreams marked `IN_PROGRESS` in PLAN.md are in `active_workstreams` in ACTIVE.md
3. Workstreams marked `BLOCKED` in PLAN.md are in `blocked_workstreams` in ACTIVE.md
4. `current_phase` in ACTIVE.md matches an active phase in PLAN.md

**Example Output:**
```json
{
  "in_sync": false,
  "discrepancies": [
    {
      "type": "workstream_mismatch",
      "workstream_id": "1.1",
      "plan_status": "COMPLETED",
      "active_status": "not found in completed_workstreams",
      "recommendation": "Add 'Workstream 1.1' to completed_workstreams in ACTIVE.md"
    }
  ],
  "warnings": [
    "current_phase in ACTIVE.md is 'Phase 1' but PLAN.md shows Phase 2 has started"
  ]
}
```

---

## 7. Graceful Degradation

### Missing PLAN.md
**Behavior:** All functions return error dict  
**Example:**
```json
{
  "success": false,
  "metadata": null,
  "errors": ["File not found: PLAN.md"]
}
```
**Action:** Worker proceeds with prompt-provided context

### Malformed Section
**Behavior:** Skip section, log warning, continue parsing  
**Example Warning:** `"Could not parse Phase 3 header (malformed format)"`

### Unknown Status Value
**Behavior:** Treat as "PLANNED", log warning  
**Example Warning:** `"Unknown status 'PAUSED' for Workstream 2.1, defaulting to PLANNED"`

### Orphan Dependency
**Behavior:** `validate_plan()` returns error  
**Example:** `"Workstream 1.2 depends on non-existent Workstream 1.5"`  
**Action:** Architect fixes dependency or creates missing workstream

### Missing ACTIVE.md (for sync_check)
**Behavior:** Return error dict  
**Example:**
```json
{
  "in_sync": false,
  "discrepancies": [],
  "warnings": ["ACTIVE.md not found, cannot verify sync"]
}
```

---

## 8. Anti-Patterns

❌ **Don't Do This:**

### Don't Require External Markdown Parsers
**Why:** Adds dependency; regex is sufficient for our use case

### Don't Modify PLAN.md Structure in Parser
**Why:** Backward compatibility; parse what exists, don't enforce structure

### Don't Auto-Fix PLAN.md/ACTIVE.md Discrepancies (v1.0)
**Why:** Manual review prevents accidental data loss; auto-fix comes in Phase 2

### Don't Crash on Missing Fields
**Why:** Graceful degradation; use defaults (e.g., `model = None`)

### Don't Store State in Parser
**Why:** Stateless tools; context is passed as arguments

### Don't Hardcode File Paths
**Why:** Testability; paths should be function arguments with defaults

---

## 9. Example PLAN.md (Sample Project)

```markdown
# AI Recipe Generator — Master Plan

**Architect:** Claude Opus 4  
**Start Date:** 2026-02-10  
**Target Completion:** 2026-02-20  
**Status:** 🟢 Phase 1 Complete, Phase 2 In Progress

---

## Phase 1: Foundation
**Duration:** ~3 days  
**Goal:** Set up project infrastructure and database schema

### Workstream 1.1: Project Setup
- **Worker Role:** DevOps Engineer
- **Model:** Claude Sonnet 4
- **Deliverables:**
  - `pyproject.toml`
  - `requirements.txt`
  - `README.md`
- **Dependencies:** None
- **Blocks:** Workstream 1.2

### Workstream 1.2: Database Schema
- **Worker Role:** Database Architect
- **Model:** Claude Sonnet 4.5
- **Deliverables:**
  - `schema.sql`
  - `migrations/001_initial.sql`
- **Dependencies:** Workstream 1.1
- **Blocks:** Workstream 2.1

---

## Phase 2: Core Features
**Duration:** ~5 days  
**Goal:** Implement recipe generation algorithm

### Workstream 2.1: Recipe Algorithm
- **Worker Role:** ML Engineer
- **Model:** Claude Opus 4
- **Deliverables:**
  - `src/recipe_generator.py`
  - `tests/test_recipe_generator.py`
- **Dependencies:** Workstream 1.2
- **Blocks:** None

---

## Integration Checkpoint 1
- [x] Database schema migrated successfully
- [x] Tests pass locally
- [/] Recipe algorithm MVP complete
```

**Parsed Output (truncated):**
```json
{
  "success": true,
  "metadata": {
    "architect": "Claude Opus 4",
    "start_date": "2026-02-10",
    "target_completion": "2026-02-20",
    "status": "🟢 Phase 1 Complete, Phase 2 In Progress",
    "phases": [
      {
        "phase_id": 1,
        "title": "Foundation",
        "duration": "~3 days",
        "goal": "Set up project infrastructure and database schema",
        "workstreams": [
          {
            "workstream_id": "1.1",
            "title": "Project Setup",
            "worker_role": "DevOps Engineer",
            "model": "Claude Sonnet 4",
            "deliverables": ["pyproject.toml", "requirements.txt", "README.md"],
            "dependencies": [],
            "blocks": ["1.2"],
            "status": "COMPLETED"
          },
          ...
        ]
      },
      ...
    ]
  },
  "errors": []
}
```

---

## 10. Validation Checklist

Use this checklist when implementing the protocol:

- [ ] PLAN.md parsing handles missing file gracefully
- [ ] Regex patterns correctly extract phases and workstreams
- [ ] Pydantic models validate all required fields
- [ ] `parse_plan()` returns structured PlanMetadata
- [ ] `validate_plan()` detects orphan dependencies
- [ ] `validate_plan()` detects circular dependencies
- [ ] `generate_worker_context()` resolves dependencies and blocks
- [ ] `update_workstream_status()` modifies PLAN.md correctly
- [ ] `sync_check()` detects PLAN.md/ACTIVE.md discrepancies
- [ ] All functions return status dicts (no exceptions)
- [ ] Tests cover happy path and error cases
- [ ] Manual testing with existing PLAN.md succeeds

---

## 11. Python Implementation Guidance

### Dependencies
- `re` (stdlib) — Regex parsing
- `pathlib` (stdlib) — Path handling
- `typing` (stdlib) — Type hints
- `pydantic` (required) — Data validation

### Code Organization
```
src/tools/plan_sync.py
├── Pydantic Models (WorkstreamMetadata, PhaseMetadata, PlanMetadata)
├── parse_plan()
├── validate_plan()
├── generate_worker_context()
├── update_workstream_status()
└── sync_check()
```

### Error Handling Pattern
```python
def some_function(arg: str) -> dict:
    """Function that can fail gracefully."""
    try:
        # Attempt operation
        result = do_something(arg)
        return {
            "success": True,
            "data": result,
            "errors": []
        }
    except FileNotFoundError as e:
        return {
            "success": False,
            "data": None,
            "errors": [f"File not found: {arg}"]
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "errors": [f"Unexpected error: {str(e)}"]
        }
```

---

## 12. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | 2026-02-14 | Initial protocol specification | Worker (Sonnet 4.5) |

---

## 13. Future Enhancements (Post-v1.0)

**For Phase 2+:**
- Auto-sync via file watchdog (Workstream 2.4)
- Real-time sync check on file modification
- Visual dashboard for PLAN.md status
- Dependency graph visualization
- AI-powered plan validation (detect logical inconsistencies)

**For v2.0:**
- TOML/YAML frontmatter in PLAN.md for cleaner parsing
- Bidirectional sync (ACTIVE.md updates → PLAN.md reflects)
- Version tracking for PLAN.md changes

---

**End of Specification**
