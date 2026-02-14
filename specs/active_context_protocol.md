# Active Context Protocol Specification

**Version:** v1.0  
**Status:** ✅ Approved  
**Created:** 2026-02-14  
**Author:** Worker (Claude Sonnet 4.5 Thinking — Workstream 1.1)

---

## 1. Overview

### Purpose
The Active Context Protocol eliminates **context drift** between Architect and Worker agents by providing a canonical, machine-readable state file that answers:
- What is the project?
- What's being worked on right now?
- What's stuck and why?
- What's already done?
- When was this last accurate?

### Success Metric
A worker reading `.context/ACTIVE.md` can understand project state in **<60 seconds**.

### Design Philosophy
- **Hybrid Format**: YAML frontmatter (machine-parseable) + Markdown body (human-readable)
- **Zero Dependencies**: Works with plain text editors; Python parser optional
- **Graceful Degradation**: Workers proceed if ACTIVE.md is missing (report absence to Architect)
- **Minimal Overhead**: Capped at 15 frontmatter fields to prevent bloat

---

## 2. File Structure

### Location
`.context/ACTIVE.md` (project root)

### Format
```markdown
---
# YAML Frontmatter (13 fields, 2 reserved for future expansion)
project_name: "string"
mission_summary: "string"
current_phase: "string"
active_workstreams: ["array", "of", "strings"]
blocked_workstreams: ["array", "of", "strings"]
completed_workstreams: ["array", "of", "strings"]
last_architect_update: "ISO 8601 timestamp"
last_worker_update: "ISO 8601 timestamp"
critical_decisions: ["array", "of", "strings"]
key_files_modified: ["array", "of", "strings"]
integration_status: "string"
next_milestone: "string"
risk_alerts: ["array", "of", "strings"]
---

# Markdown Body (Human-Readable Narrative)
## 🎯 Current Focus
...

## 📋 Recent Changes
...

## 🚧 Blockers
...

## 💬 Notes for Workers
...
```

---

## 3. Field Definitions

### Required Fields

#### `project_name` (string)
- **Type:** String (max 100 chars)
- **Purpose:** Human-readable project identifier
- **Example:** `"Antigravity Workspace Template"`

#### `mission_summary` (string)
- **Type:** String (max 200 chars)
- **Purpose:** One-line project purpose
- **Example:** `"IDE-native template for parallel AI agent workflows"`

#### `current_phase` (string)
- **Type:** String
- **Purpose:** High-level phase identifier
- **Example:** `"Phase 1: Context Synchronization (Foundation)"`
- **Valid Values:** Any phase naming convention (suggest "Phase N: Description")

#### `active_workstreams` (array)
- **Type:** Array of strings
- **Purpose:** What's being worked on RIGHT NOW
- **Example:** `["Workstream 1.1: Active Context Protocol", "Workstream 1.3: Archive Hygiene"]`
- **Constraint:** Should not exceed 5 items (focus limit)

#### `blocked_workstreams` (array)
- **Type:** Array of strings
- **Purpose:** What's stuck and waiting for resolution
- **Example:** `["Workstream 1.2: Blocked on Workstream 1.1 completion"]`
- **Update Trigger:** Worker encounters a blocker

#### `completed_workstreams` (array)
- **Type:** Array of strings
- **Purpose:** What's finished (recent history for context)
- **Example:** `["Workstream 1.1: Active Context Protocol"]`
- **Pruning:** Archive when list exceeds 10 items

#### `last_architect_update` (string)
- **Type:** ISO 8601 timestamp with timezone
- **Purpose:** When Architect last modified this file
- **Example:** `"2026-02-14T00:13:00-03:00"`
- **Format:** `YYYY-MM-DDTHH:MM:SS±HH:MM`

#### `last_worker_update` (string)
- **Type:** ISO 8601 timestamp with timezone
- **Purpose:** When a Worker last modified this file
- **Example:** `"2026-02-14T00:45:22-03:00"`
- **Format:** `YYYY-MM-DDTHH:MM:SS±HH:MM`

#### `critical_decisions` (array)
- **Type:** Array of strings (max 100 chars each)
- **Purpose:** Key architectural choices that workers MUST know
- **Example:** `["Use Pydantic for all data models", "Archive hygiene runs weekly, not on-commit"]`
- **Constraint:** Max 10 items (only truly critical decisions)

#### `key_files_modified` (array)
- **Type:** Array of relative file paths
- **Purpose:** Recently changed files (helps workers understand what's active)
- **Example:** `[".context/ACTIVE.md", "src/tools/archive_manager.py"]`
- **Pruning:** Keep last 15 files only

#### `integration_status` (string)
- **Type:** String
- **Purpose:** How multiple workstreams are fitting together
- **Example:** `"Protocol established; Python parser pending Phase 2"`
- **Valid Values:** Freeform (suggest <150 chars)

#### `next_milestone` (string)
- **Type:** String
- **Purpose:** Immediate goal that drives current work
- **Example:** `"Complete Phase 1 (all 3 workstreams) by 2026-02-15"`
- **Constraint:** Should be achievable within current phase

#### `risk_alerts` (array)
- **Type:** Array of strings
- **Purpose:** Active warnings/concerns needing attention
- **Example:** `["ACTIVE.md schema may be too complex for Haiku agents"]`
- **Update Trigger:** Worker identifies a risk; Architect on strategic concern
- **Resolution:** Remove item when risk is mitigated

---

## 4. Contract Rules

### On Entry (Worker Starts)

**MUST DO:**
1. Read `.context/ACTIVE.md` (if it exists)
2. Parse YAML frontmatter to extract:
   - `current_phase`
   - `active_workstreams` (confirm your task is listed)
   - `blocked_workstreams` (check if you're blocked)
   - `critical_decisions` (constraints you must respect)
3. Read markdown body for context narrative

**IF MISSING:**
- Proceed without it (graceful degradation)
- Report to Architect: "ACTIVE.md not found at entry"

**VALIDATION:**
- If `last_architect_update` or `last_worker_update` is >24 hours old, warn: "ACTIVE.md may be stale"

---

### On Exit (Worker Finishes)

**MUST DO:**
1. Update `last_worker_update` with current timestamp
2. Move your workstream from `active_workstreams` to `completed_workstreams`
3. Add entry to "📋 Recent Changes" section:
   ```markdown
   - **YYYY-MM-DDTHH:MM:SS±HH:MM** — [Workstream Name] completed by Worker ([Model])
     - Key files: `file1.py`, `file2.md`
     - Notes: [Brief summary]
   ```
4. Update `key_files_modified` with files you created/edited
5. If you made a critical decision, add to `critical_decisions`

---

### On Block (Worker Encounters Blocker)

**MUST DO:**
1. Move your workstream from `active_workstreams` to `blocked_workstreams`
2. Add item to `risk_alerts`: `"[Workstream Name] blocked: [reason]"`
3. Add to "🚧 Blockers" section in markdown body:
   ```markdown
   ### [Workstream Name] — BLOCKED
   - **Reason:** [Describe what's stuck]
   - **Needs:** [What's required to unblock]
   - **Reported:** YYYY-MM-DDTHH:MM:SS±HH:MM
   ```
4. Update `last_worker_update`
5. Notify Architect immediately

---

### Conflict Resolution

**Scenario:** Two workers update ACTIVE.md simultaneously

**Strategy:** Last-write-wins (file system default)

**Mitigation:**
1. Workers MUST timestamp all updates
2. Architect reviews `last_worker_update` and "Recent Changes" to reconcile
3. If conflict detected, Architect manually merges changes

**Future Enhancement (Phase 2):**  
Python watchdog tool can detect conflicts and queue for Architect review.

---

## 5. Relationship to PLAN.md

| Aspect | PLAN.md | ACTIVE.md |
|--------|---------|-----------|
| **Owner** | Architect creates/maintains | Workers update, Architect reviews |
| **Scope** | Strategic roadmap (phases, dependencies) | Tactical state (what's happening now) |
| **Timeframe** | Long-term (weeks) | Short-term (hours/days) |
| **Update Frequency** | When plan changes | On every worker entry/exit |
| **Read Priority** | Read FIRST (if exists) | Read SECOND |

**Sync Rule:**  
When a workstream in PLAN.md changes status, ACTIVE.md should reflect it. Phase 2 tools will automate this sync.

---

## 6. Graceful Degradation

### Missing ACTIVE.md
**Behavior:** Worker proceeds with prompt-provided context  
**Action:** Report to Architect: "ACTIVE.md not found"

### Stale ACTIVE.md
**Detection:** `last_architect_update` or `last_worker_update` >24 hours old  
**Behavior:** Worker warns Architect but proceeds  
**Action:** Architect updates or confirms accuracy

### Malformed YAML
**Detection:** YAML frontmatter parsing fails  
**Behavior:** Worker reads markdown body only (human-readable fallback)  
**Action:** Report to Architect: "ACTIVE.md YAML parse error"

### Exceeds Field Limits
**Detection:** >15 frontmatter fields  
**Behavior:** Parser ignores unknown fields  
**Action:** Architect prunes to 15 fields

---

## 7. Anti-Patterns

❌ **Don't Do This:**

### Don't Make ACTIVE.md a JSON File
**Why:** Agents and humans read markdown better; JSON is machine-only

### Don't Add Execution Logic
**Why:** ACTIVE.md is a STATE file, not a script

### Don't Exceed 15 Frontmatter Fields
**Why:** Every field is a maintenance burden; forces discipline

### Don't Require Python Tools to Update
**Why:** Manual editing must work (agents use text editors)

### Don't Put Code in ACTIVE.md
**Why:** Code belongs in `src/`; ACTIVE.md is metadata

### Don't Archive ACTIVE.md
**Why:** It's the living state file; archive snapshots instead

### Don't Update ACTIVE.md Without Timestamps
**Why:** Architect can't reconcile conflicts without timestamps

---

## 8. Example ACTIVE.md (Sample Project)

```markdown
---
project_name: "AI-Powered Recipe Generator"
mission_summary: "Generate personalized recipes using dietary preferences and available ingredients"
current_phase: "Phase 2: Core Algorithm Development"
active_workstreams:
  - "Workstream 2.1: Ingredient Database Schema"
  - "Workstream 2.2: Recipe Generation API"
blocked_workstreams:
  - "Workstream 2.3: Nutrition Calculator (blocked on external API keys)"
completed_workstreams:
  - "Workstream 1.1: Project Setup"
  - "Workstream 1.2: User Stories Documentation"
last_architect_update: "2026-02-13T14:30:00-05:00"
last_worker_update: "2026-02-14T09:15:00-05:00"
critical_decisions:
  - "Use PostgreSQL for ingredient database (not SQLite)"
  - "Recipe algorithm must support vegan/vegetarian/keto filters"
key_files_modified:
  - "src/database/schema.sql"
  - "src/api/recipe_generator.py"
  - "tests/test_recipe_api.py"
integration_status: "Database schema complete; API in progress (70%)"
next_milestone: "Release v0.1 MVP with 100 recipes by 2026-02-20"
risk_alerts:
  - "External nutrition API has rate limits (500 req/day)"
---

# Active Context — AI Recipe Generator

## 🎯 Current Focus
**Workstream 2.2** — Building the Recipe Generation API with dietary filter support.

## 📋 Recent Changes
- **2026-02-14T09:15:00-05:00** — Worker (Sonnet 4.5) completed `recipe_generator.py` core logic
  - Implemented vegan/vegetarian/keto filters
  - Added unit tests (12/12 passing)
- **2026-02-13T16:45:00-05:00** — Worker (Gemini Flash) completed database schema migration
  - Migrated 500 ingredients from CSV to PostgreSQL

## 🚧 Blockers
### Workstream 2.3: Nutrition Calculator — BLOCKED
- **Reason:** Waiting for external API keys from nutritionix.com
- **Needs:** Architect to provide API credentials
- **Reported:** 2026-02-13T18:00:00-05:00

## 💬 Notes for Workers
- All recipe algorithms must return results in <2 seconds (performance requirement)
- Use `src/utils/filter.py` for dietary filters (don't reimplement)
- Nutrition data cache expires after 7 days (update logic if consuming API)
```

---

## 9. Validation Checklist

Use this checklist when creating or updating ACTIVE.md:

- [ ] YAML frontmatter is valid (test with `python -c "import yaml; yaml.safe_load(open('.context/ACTIVE.md').read())"`)
- [ ] Frontmatter has ≤15 fields
- [ ] All timestamps use ISO 8601 format with timezone
- [ ] `active_workstreams` has ≤5 items
- [ ] `critical_decisions` has ≤10 items
- [ ] `key_files_modified` has ≤15 items
- [ ] Markdown body has all 4 sections (Current Focus, Recent Changes, Blockers, Notes for Workers)
- [ ] A human can understand state in <60 seconds
- [ ] No code snippets in the file (only metadata)

---

## 10. Python Parser Guidance (For Workstream 2.1)

**Estimated Complexity:** 🟢 Low (2-3 hours)

### Recommended Implementation

```python
from typing import Dict, List, Optional
from datetime import datetime
import yaml
from pydantic import BaseModel, Field

class ActiveContext(BaseModel):
    """Pydantic model for ACTIVE.md frontmatter."""
    project_name: str = Field(..., max_length=100)
    mission_summary: str = Field(..., max_length=200)
    current_phase: str
    active_workstreams: List[str] = Field(default_factory=list, max_items=5)
    blocked_workstreams: List[str] = Field(default_factory=list)
    completed_workstreams: List[str] = Field(default_factory=list, max_items=10)
    last_architect_update: datetime
    last_worker_update: datetime
    critical_decisions: List[str] = Field(default_factory=list, max_items=10)
    key_files_modified: List[str] = Field(default_factory=list, max_items=15)
    integration_status: str = Field(..., max_length=150)
    next_milestone: str
    risk_alerts: List[str] = Field(default_factory=list)

def parse_active_md(path: str = ".context/ACTIVE.md") -> Dict:
    """Parse ACTIVE.md into structured data.
    
    Args:
        path: Path to ACTIVE.md file
        
    Returns:
        dict: {
            "frontmatter": ActiveContext instance,
            "body": str (markdown content),
            "valid": bool,
            "errors": List[str]
        }
    """
    # Implementation left to Workstream 2.1
    pass
```

### Dependencies
- `pyyaml` (YAML parsing)
- `pydantic` (data validation)

Both are already in `.context/coding_style.md` requirements.

---

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | 2026-02-14 | Initial protocol specification | Worker (Sonnet 4.5) |

---

## 12. Future Enhancements (Post-v1.0)

**For Phase 2+:**
- Auto-sync with PLAN.md (Workstream 2.4)
- Conflict detection via file watchdog (Workstream 2.4)
- Auto-archival of stale entries (Workstream 1.3)
- Gemini-powered staleness detection
- Snapshot diffing (show what changed between updates)

**Field Expansion (if needed):**
- `dependencies_status` — Track external service health
- `test_coverage` — Current test coverage percentage

**Constraint:** Total fields must remain ≤15 (prune low-value fields if adding new ones)

---

**End of Specification**
