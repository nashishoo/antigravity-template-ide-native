# Antigravity Template Evolution — Master Plan

**Architect:** Claude Opus 4.6 (Thinking)  
**Start Date:** 2026-02-13  
**Target Completion:** 2026-02-16 (3 working sessions)  
**Status:** 🟡 Phase 1 — Planning Complete, Ready for Delegation

---

## Phase Sequencing & Rationale

```
Phase 1: Context Sync (FOUNDATION)     ──> Phase 2: Python Tooling (AUTOMATION)
    │                                            │
    └── Everything reads/writes state ───────────┘
                                                 │
                                        Phase 3: Discovery & Guidance (INTELLIGENCE)
                                                 │
                                        Phase 4: Documentation & Migration (CONSOLIDATION)
```

**Why this order:**
1. **Phase 1 first** because Phases 2-4 all need shared state to function
2. **Phase 2 before 3** because intelligent discovery requires tools that exist
3. **Phase 3 before 4** because documentation should describe the final system
4. **Phase 4 last** because it codifies everything (can only document what's built)

**What breaks if resequenced:** Building tools (Phase 2) without ACTIVE.md (Phase 1) means tools can't know project context → they generate blind prompts → rework.

---

## Phase 1: Context Synchronization (Foundation)
**Duration:** ~5 hours (2h design + 3h implementation)  
**Goal:** Eliminate manual context transfer between Architect and Workers

### Workstream 1.1: Active Context Protocol
- **Worker Role:** Documentation/Protocol Specialist
- **Model:** Claude Sonnet 4.5 (Thinking)
- **Deliverables:**
  - `.context/ACTIVE.md` — Protocol specification + template
  - `specs/active_context_protocol.md` — Formal spec
- **Dependencies:** None (foundational)
- **Blocks:** Workstream 1.2, all Phase 2 tools

### Workstream 1.2: Plan Synchronization System
- **Worker Role:** Workflow Engineer
- **Model:** Claude Sonnet 4.5 (Thinking)
- **Deliverables:**
  - `PLAN.md` template with auto-generation guidelines
  - `src/tools/plan_sync.py` — Parse/validate/update PLAN.md
- **Dependencies:** Workstream 1.1 (needs ACTIVE.md format)
- **Blocks:** Phase 2 watchdog

### Workstream 1.3: Archive Hygiene Automation
- **Worker Role:** Maintenance Specialist
- **Model:** Gemini 3 Flash
- **Deliverables:**
  - `.archive/` directory structure + conventions
  - `src/tools/archive_manager.py` — Auto-archival script
- **Dependencies:** None (can run parallel with 1.1)
- **Blocks:** Phase 3 artifact structure

### Integration Checkpoint 1
- **Validate:** Workers can read ACTIVE.md on entry
- **Validate:** PLAN.md stays synced after multiple worker sessions
- **Validate:** Archive script correctly moves completed work
- **Gemini Validation:** "Does ACTIVE.md solve the context drift complaint?"

---

## Phase 2: Python Tooling Infrastructure (Automation)
**Duration:** ~6 hours (parallel workstreams)  
**Goal:** Add "grunt work" automation while preserving markdown-first thinking

### Workstream 2.1: Shared Utilities + Test Infrastructure
- **Worker Role:** Platform Engineer
- **Model:** Claude Sonnet 4.5 (Thinking)
- **Deliverables:**
  - `src/tools/_common.py` — Shared utilities (parse_active_md, resolve_root)
  - `tests/conftest.py` — Test fixtures
  - `pyproject.toml` — Project config with pytest settings
  - `requirements.txt` — Updated dependencies
- **Dependencies:** Phase 1 (needs ACTIVE.md format)
- **Blocks:** All other Phase 2 workstreams

### Workstream 2.2: Data Validation Pipeline
- **Worker Role:** Data Engineer
- **Model:** Gemini 3 Flash
- **Deliverables:**
  - `src/tools/data_validator.py` — Schema validation with Pydantic
  - `tests/test_data_validator.py`
- **Dependencies:** Workstream 2.1
- **Blocks:** None

### Workstream 2.3: Code Scaffolding Suite
- **Worker Role:** Automation Specialist
- **Model:** Claude Sonnet 4.5
- **Deliverables:**
  - `src/tools/scaffold.py` — Spec-to-code generator
  - `tests/test_scaffold.py`
- **Dependencies:** Workstream 2.1
- **Blocks:** Phase 3 artifact structure

### Workstream 2.4: File Watchdog & Task Sync
- **Worker Role:** DevOps Specialist
- **Model:** Claude Sonnet 4.5 (Thinking)
- **Deliverables:**
  - `src/tools/watchdog_sync.py` — File change monitoring + task update
  - `tests/test_watchdog_sync.py`
- **Dependencies:** Workstream 2.1 + Phase 1 PLAN.md sync
- **Blocks:** Phase 3 intelligent preflight

### Integration Checkpoint 2
- **Validate:** `pytest tests/` passes with all tools
- **Validate:** Tools respect ACTIVE.md protocol
- **Validate:** No mandatory external deps (optional imports handled gracefully)
- **Gemini Validation:** "Does the Python tooling solve the automation gap?"

---

## Phase 3: Enhanced Discovery & Guidance (Intelligence)
**Duration:** ~4 hours (parallel workstreams)  
**Goal:** Proactive skill recommendation and artifact management

### Workstream 3.1: Intelligent Preflight Enhancement
- **Worker Role:** ML Integration Specialist
- **Model:** Claude Sonnet 4.5 (Thinking)
- **Deliverables:**
  - Updated `preflight.md` with mission analysis
  - `src/tools/mission_analyzer.py` — Parse mission.md → recommend skills
- **Dependencies:** Phase 2 shared utils
- **Blocks:** None

### Workstream 3.2: Artifact Structure Enforcement
- **Worker Role:** Standards Specialist
- **Model:** Gemini 3 Flash
- **Deliverables:**
  - `artifacts/` subdir structure (logs/, data/, reports/)
  - `src/tools/artifact_manager.py` — Placement validation + auto-scaffold
- **Dependencies:** Phase 1 archive hygiene
- **Blocks:** None

### Workstream 3.3: Smart Prompt Generator
- **Worker Role:** Prompt Engineering Specialist
- **Model:** Claude Opus 4.5 (Thinking)
- **Deliverables:**
  - `src/tools/generate_worker_prompt.py` — Context-aware prompt generation
  - Jinja2 templates in `src/tools/templates/`
- **Dependencies:** Phase 1 ACTIVE.md + Phase 2 shared utils
- **Blocks:** Phase 4 workflow updates

### Integration Checkpoint 3
- **Validate:** Preflight recommends relevant skills for sample missions
- **Validate:** Artifacts auto-scaffold on project init
- **Validate:** Generated prompts are self-contained and executable
- **Gemini Validation:** "Does intelligent preflight solve the blind discovery complaint?"

---

## Phase 4: Documentation & Integration (Consolidation)
**Duration:** ~3 hours  
**Goal:** Codify new patterns and ensure adoption

### Workstream 4.1: Specification Documentation
- **Worker Role:** Technical Writer
- **Model:** Claude Sonnet 4.5
- **Deliverables:**
  - `specs/workflow_evolution.md`
  - `specs/active_context_protocol.md` (formalized)
  - `specs/python_tooling_guide.md`

### Workstream 4.2: Updated Workflows
- **Worker Role:** Workflow Designer
- **Model:** Claude Sonnet 4.5
- **Deliverables:**
  - Updated `.agent/workflows/parallel_architect.md`
  - New `.agent/workflows/self_maintenance.md`
  - Updated `preflight.md`

### Workstream 4.3: Migration Guide
- **Worker Role:** Developer Advocate
- **Model:** Gemini 3 Flash
- **Deliverables:**
  - `README_UPGRADE.md` — v1.0 → v2.0 migration path
  - Updated `README.md` + `README_ES.md`
  - `specs/compatibility_matrix.md`

### Integration Checkpoint 4 (Final)
- **Validate:** All docs accurate and cross-referenced
- **Validate:** Migration guide tested on clean v1.0 clone
- **Validate:** No broken links or TODOs
- **Gemini Validation:** "Would you onboard faster with this documentation?"

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| ACTIVE.md too complex for agents | Medium | High | Cap at 15 frontmatter fields; user test with Haiku |
| Python deps break "zero-config" | High | Medium | All imports wrapped in try/except; graceful fallback |
| Workers edit same files | Low | High | PLAN.md assigns file ownership per workstream |
| Phase 1 takes longer than estimated | Medium | Medium | Phase 2 specs can be drafted in parallel |
| Backward compatibility breaks | Low | High | Test migration on clean v1.0 clone before release |

---

## Worker Prompt Queue (Phase 1 — Ready for Delegation)

### 📋 Status
- [/] Workstream 1.1 — ACTIVE.md Protocol → **Prompt ready** (see below)
- [/] Workstream 1.3 — Archive Hygiene → **Prompt ready** (can run in parallel)
- [ ] Workstream 1.2 — PLAN.md Sync → **Blocked** by Workstream 1.1 completion

---

## PHASE 1 WORKER PROMPTS

---

### 🚀 PROMPT 1: Active Context Protocol Specialist

**FOR USER:** Open a new Antigravity chat window → Select **Claude Sonnet 4.5 (Thinking)** → Paste the entire block below:

---

```markdown
# 🚀 MISSION: Active Context Protocol Designer

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)
**Your Model:** Claude Sonnet 4.5 (Thinking)
**Sync Protocol:** Read PLAN.md if it exists before starting. This is foundational work — there is no ACTIVE.md yet because YOU are designing it.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture, IDE-native agents (Antigravity)
- **Improvement Goal:** Eliminate context drift between Architect and Worker agents
- **Root Cause:** Workers start with zero knowledge of what the Architect decided, what's in progress, and what's blocked
- **Success Metric:** A worker reading ACTIVE.md can understand project state in <60 seconds

## CURRENT STATE
- `.context/` directory exists with `coding_style.md` and `system_prompt.md`
- No context synchronization protocol exists
- Workers currently receive all context via copy-pasted prompts (fragile, incomplete)
- Architects must manually track what each worker knows

## YOUR SPECIFIC TASK

### 1. Design the `.context/ACTIVE.md` Protocol

Create a file `.context/ACTIVE.md` with this structure:

**YAML Frontmatter** (machine-readable, max 15 fields):
```yaml
---
project_name: ""
mission_summary: ""
current_phase: ""
active_workstreams: []
blocked_workstreams: []
completed_workstreams: []
last_architect_update: ""
last_worker_update: ""
critical_decisions: []
key_files_modified: []
integration_status: ""
next_milestone: ""
risk_alerts: []
---
```

**Markdown Body** (human-readable):
- Current Focus: What's being worked on right now
- Recent Changes: What happened since last update
- Blockers: What's stuck and why
- Notes for Workers: Architect's instructions for anyone picking up work

### 2. Define the Read/Update Contract

Document these rules:
- **On Entry (Worker starts):** Read ACTIVE.md. If it doesn't exist, proceed without it (graceful degradation). Report back to Architect that ACTIVE.md was not found.
- **On Exit (Worker finishes):** Update relevant frontmatter fields + add entry to "Recent Changes" in body. Timestamp the update.
- **On Block (Worker stuck):** Update `blocked_workstreams` and `risk_alerts`. Add blocker description to body.
- **Conflict Resolution:** If two workers update ACTIVE.md simultaneously, last-write-wins. Workers should timestamp their updates so the Architect can reconcile.

### 3. Create the Formal Specification

Create `specs/active_context_protocol.md` with:
- Protocol version (start at v1.0)
- Field definitions with types and examples
- Contract rules (entry/exit/block)
- Graceful degradation behavior
- Example ACTIVE.md for a sample project
- Anti-patterns (what NOT to put in ACTIVE.md)

### Constraints
- [ ] ACTIVE.md must be valid YAML frontmatter + Markdown (parseable by standard tools)
- [ ] Max 15 fields in frontmatter (prevent bloat)
- [ ] Must work without Python tools (plain markdown editing)
- [ ] Must gracefully degrade if file doesn't exist
- [ ] Must be human-readable (a developer can understand state by reading it)

### Thinking Mode Guidance
Since you're a Thinking-enabled model, explicitly reason through:
1. "What if two workers update ACTIVE.md at the same time?"
2. "What if ACTIVE.md becomes stale (no one updates it)?"
3. "What's the minimum viable set of fields that provides maximum value?"
4. "How does this interact with PLAN.md (which will be created in Workstream 1.2)?"

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `.context/ACTIVE.md` — Working template with initial state
- [ ] `specs/active_context_protocol.md` — Formal specification

### Validation Steps
1. [ ] ACTIVE.md has valid YAML frontmatter (test with any YAML parser)
2. [ ] Frontmatter has ≤15 fields
3. [ ] A human can understand project state in <60 seconds by reading it
4. [ ] Protocol handles missing ACTIVE.md gracefully (documented)
5. [ ] No external dependencies required to use the protocol

### State Synchronization
- [ ] Report back to Architect with: Summary of design decisions + any open questions

## ANTI-PATTERNS (Don't Do This)
- ❌ Don't make ACTIVE.md a JSON file (agents read markdown better)
- ❌ Don't add execution logic (it's a state file, not a script)
- ❌ Don't exceed 15 frontmatter fields (every field is a maintenance burden)
- ❌ Don't require Python tools to update it (manual editing must work)

## COMMUNICATION PROTOCOL
**When complete:** Report these items to the Architect:
1. Final field list with rationale for each field
2. Any design decisions you made that weren't specified
3. Edge cases you identified and how you handled them
4. Estimated complexity for a Python parser (Workstream 2.1 will build one)
```

---

### 🚀 PROMPT 2: Archive Hygiene Specialist

**FOR USER:** Open a new Antigravity chat window → Select **Gemini 3 Flash** → Paste the entire block below:

---

```markdown
# 🚀 MISSION: Archive Hygiene Automation Specialist

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)
**Your Model:** Gemini 3 Flash
**Note:** This is a parallel workstream. Workstream 1.1 (ACTIVE.md) is being worked on simultaneously by another agent. You do NOT depend on it.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture
- **Improvement Goal:** Prevent artifact sprawl and context window pollution
- **Root Cause:** Old artifacts and completed task files accumulate, clogging agent context windows
- **Success Metric:** Completed work auto-archives, keeping active workspace clean

## CURRENT STATE
- `artifacts/` directory exists (currently has architectural reasoning and preflight files)
- No `.archive/` directory exists
- No archival conventions or scripts
- `tests/` directory is empty

## YOUR SPECIFIC TASK

### 1. Design the `.archive/` Directory Structure

Create:
```
.archive/
├── README.md          ← Conventions doc
├── completed/         ← Finished workstreams/phases
├── deprecated/        ← Old tools/specs that were replaced
└── snapshots/         ← Point-in-time state snapshots
```

### 2. Create the Archive Manager Tool

Create `src/tools/archive_manager.py` with these functions:

```python
def archive_completed(source_path: str, reason: str) -> dict:
    """Move a file/directory to .archive/completed/ with metadata."""

def archive_deprecated(source_path: str, replacement: str) -> dict:
    """Move to .archive/deprecated/ noting what replaced it."""

def create_snapshot(label: str) -> dict:
    """Create a timestamped snapshot of current ACTIVE.md + PLAN.md state."""

def list_archive(category: str = "all") -> dict:
    """List archived items with metadata."""

def restore_from_archive(archive_path: str) -> dict:
    """Restore an archived item to its original location."""
```

**Requirements:**
- Each archived item gets a `.meta.json` sidecar with: original_path, archive_date, reason, archived_by
- Restore function checks for conflicts before overwriting
- All functions return status dictionaries (not exceptions)

### 3. Create the Archive README

Create `.archive/README.md` with:
- When to archive (completed phases, deprecated tools)
- When NOT to archive (active working files)
- How to restore items
- Naming conventions

### Constraints
- [ ] Follow `.context/coding_style.md` (type hints, Google docstrings, Pydantic)
- [ ] Tool must work without external dependencies (stdlib only)
- [ ] Archive operations must be reversible (restore function)
- [ ] Metadata must be JSON (machine-readable)
- [ ] Must handle Windows paths correctly (os.path or pathlib)

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `.archive/README.md` — Archive conventions
- [ ] `.archive/completed/.keep` — Empty dir placeholder
- [ ] `.archive/deprecated/.keep` — Empty dir placeholder
- [ ] `.archive/snapshots/.keep` — Empty dir placeholder
- [ ] `src/tools/archive_manager.py` — Archive management tool
- [ ] `tests/test_archive_manager.py` — Unit tests

### Validation Steps
1. [ ] `archive_completed()` moves file and creates `.meta.json`
2. [ ] `restore_from_archive()` restores file to original location
3. [ ] `list_archive()` returns correct inventory
4. [ ] All functions have type hints and docstrings
5. [ ] Tests pass: `python -m pytest tests/test_archive_manager.py -v`

### State Synchronization
- [ ] Report back to Architect with: summary of archive structure + any design decisions

## ANTI-PATTERNS (Don't Do This)
- ❌ Don't delete files (always move + metadata)
- ❌ Don't use external packages (stdlib + pathlib only)
- ❌ Don't create deeply nested archive structures (max 2 levels)
- ❌ Don't archive `.git/`, `.agent/`, or `.context/` directories
```

---

### 📋 PROMPT 3: PLAN.md Sync Specialist (BLOCKED — Queue for After Workstream 1.1)

**⚠️ DO NOT DELEGATE YET.** This workstream depends on the ACTIVE.md protocol design from Workstream 1.1. Queue this prompt for after Workstream 1.1 reports back.

**When ready — FOR USER:** Open a new Antigravity chat window → Select **Claude Sonnet 4.5 (Thinking)** → Paste the prompt below.

---

```markdown
# 🚀 MISSION: Plan Synchronization System Engineer

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)
**Your Model:** Claude Sonnet 4.5 (Thinking)
**Dependency:** Workstream 1.1 (ACTIVE.md Protocol) is COMPLETE. Read `.context/ACTIVE.md` and `specs/active_context_protocol.md` before starting.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture
- **Improvement Goal:** Centralized project planning with auto-sync between PLAN.md and worker context
- **Root Cause:** Workers diverge from plan because there's no single source of truth they can reference
- **Success Metric:** Any worker can validate their task alignment against PLAN.md

## PREREQUISITE
**READ FIRST:**
- `.context/ACTIVE.md` — Understand the state protocol
- `specs/active_context_protocol.md` — Understand the formal spec
- `PLAN.md` (this file — the existing one created by the Architect) — The plan you'll systematize

## YOUR SPECIFIC TASK

### 1. Formalize the PLAN.md Template

Create `specs/plan_sync_protocol.md` defining:
- Required sections in PLAN.md (phases, workstreams, status, dependencies)
- Update rules (who updates what, when)
- Relationship to ACTIVE.md (PLAN.md = strategy, ACTIVE.md = tactics)

### 2. Create the Plan Sync Tool

Create `src/tools/plan_sync.py` with:

```python
def parse_plan(plan_path: str = "PLAN.md") -> dict:
    """Parse PLAN.md into structured data (phases, workstreams, status)."""

def validate_plan(plan_path: str = "PLAN.md") -> dict:
    """Check PLAN.md for consistency (no orphan dependencies, valid status values)."""

def generate_worker_context(workstream_id: str, plan_path: str = "PLAN.md") -> dict:
    """Extract the context a specific worker needs from PLAN.md."""

def update_workstream_status(workstream_id: str, new_status: str, plan_path: str = "PLAN.md") -> dict:
    """Update the status of a workstream in PLAN.md."""
```

### 3. Define the Sync Protocol

Document how PLAN.md and ACTIVE.md work together:
- PLAN.md = Long-term roadmap (Architect creates, Workers reference)
- ACTIVE.md = Short-term state (Workers update, Architect reviews)
- Sync rule: When a workstream in PLAN.md changes status, ACTIVE.md should reflect it

### Constraints
- [ ] Follow `.context/coding_style.md`
- [ ] Parse markdown with regex (don't require external markdown parsers)
- [ ] Maintain backward compatibility (existing PLAN.md format should work)
- [ ] Type hints + Pydantic models for structured data

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `specs/plan_sync_protocol.md` — Formal specification
- [ ] `src/tools/plan_sync.py` — Sync tool
- [ ] `tests/test_plan_sync.py` — Unit tests

### Validation Steps
1. [ ] `parse_plan()` correctly extracts phases and workstreams from PLAN.md
2. [ ] `validate_plan()` detects orphan dependencies
3. [ ] `generate_worker_context()` returns relevant context for a given workstream
4. [ ] Tests pass: `python -m pytest tests/test_plan_sync.py -v`

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion
- [ ] Report to Architect: design decisions, any incompatibilities found
```

---

## Gemini Validation Prompt (For After Phase 1 Completion)

**FOR USER:** After all Phase 1 workstreams complete, open a new window → Select **Gemini 3 Pro (High)** → Paste:

```markdown
# VALIDATION REQUEST: Phase 1 Review

**FOR USER:** Open a new window, select Gemini 3 Pro (High), and paste this prompt.

---

You are Gemini 3 Pro (High). You wrote the original reviews of the Antigravity Template that identified critical friction points.

## YOUR ORIGINAL COMPLAINTS:
> "Context Synchronization Gap: Workers lack automatic access to Architect's decisions"
> "Active Context Maintenance: No auto-sync between file changes and task tracking"

## IMPLEMENTED SOLUTION:
Phase 1 introduced 3 components:
- **ACTIVE.md Protocol** (`.context/ACTIVE.md`): Read-on-entry, update-on-exit state file
- **PLAN.md Sync System** (`src/tools/plan_sync.py`): Centralized roadmap with auto-extraction
- **Archive Hygiene** (`.archive/`, `src/tools/archive_manager.py`): Auto-archival of completed work

### Files created:
- `.context/ACTIVE.md` — State protocol template
- `specs/active_context_protocol.md` — Formal specification
- `specs/plan_sync_protocol.md` — Plan sync rules
- `src/tools/plan_sync.py` — Plan parsing and sync
- `src/tools/archive_manager.py` — Archive management
- `.archive/` — Archive directory structure

## YOUR VALIDATION TASK:
Answer honestly:
1. Does ACTIVE.md actually solve the "context drift" complaint you raised?
2. Is the read/update contract enforceable, or will agents skip it?
3. Are there edge cases (2 agents updating simultaneously, stale state) not addressed?
4. Would PLAN.md sync have prevented the friction you experienced in the Adopt Me Bot project?
5. Is the archive system useful, or is it overhead?
6. What's still missing (if anything)?

Be critical. If it misses the mark, explain why. The Architect needs your honest perspective to refine.
```
