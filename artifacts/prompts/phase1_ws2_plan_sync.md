# 🚀 MISSION: Plan Synchronization System Engineer

## ⚠️ BLOCKED — DO NOT DELEGATE YET
**This workstream depends on Workstream 1.1 (ACTIVE.md Protocol).** Wait until the Active Context Protocol worker reports back and `.context/ACTIVE.md` + `specs/active_context_protocol.md` exist.

## MODEL RECOMMENDATION FOR USER
**When ready, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Sonnet 4.5 (Thinking)** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Thinking mode needed — this tool must parse markdown reliably and interact with the ACTIVE.md protocol correctly.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)
**Dependency:** Workstream 1.1 (ACTIVE.md Protocol) must be COMPLETE. Read `.context/ACTIVE.md` and `specs/active_context_protocol.md` before starting.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture
- **Improvement Goal:** Centralized project planning with auto-sync between PLAN.md and worker context
- **Root Cause:** Workers diverge from plan because there's no single source of truth they can reference
- **Success Metric:** Any worker can validate their task alignment against PLAN.md

## ORIGINAL REVIEW FEEDBACK (Exact Quotes)

**Review 1 (review_adoptme.md):**
> "Formalize a 'Sync Protocol'. The Architect should update a `PLAN.md` in the root, and every Worker prompt should start with: 'Read `PLAN.md` to understand your current context.'"

**Review 2 (final_review_adoptme.md):**
> "Spec-Driven Development (`specs/*.md`): Replacing chatty prompts with rigorous technical specifications."
> "I had to manually update `task.md` after every file edit."

## PREREQUISITE — READ THESE FILES FIRST
- `.context/ACTIVE.md` — Understand the state protocol designed by Workstream 1.1
- `specs/active_context_protocol.md` — Understand the formal spec
- `PLAN.md` — The existing master plan created by the Architect (you'll systematize this format)

## CODING STANDARDS (from `.context/coding_style.md`)
- Type hints mandatory for all function signatures
- Google-style docstrings with `Args:`, `Returns:`, `Raises:`
- Pydantic for complex data models
- Tools must fail gracefully (return error dicts, not crash)

## YOUR SPECIFIC TASK

### 1. Formalize the PLAN.md Template

Create `specs/plan_sync_protocol.md` defining:
- Required sections in PLAN.md (phases, workstreams, status markers, dependencies)
- Update rules (who updates what, when)
- Relationship to ACTIVE.md: `PLAN.md = strategy (Architect writes, Workers reference)` vs `ACTIVE.md = tactics (Workers update, Architect reviews)`
- Status vocabulary: `PLANNED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`, `CANCELLED`

### 2. Create the Plan Sync Tool

Create `src/tools/plan_sync.py` with these functions:

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

**Requirements:**
- Parse markdown with regex (don't require external markdown parsers)
- Use Pydantic models for structured output (Phase, Workstream, PlanStatus)
- Handle edge cases: missing PLAN.md, malformed sections, unknown status values
- All functions return status dictionaries

### 3. Define the Sync Protocol

Document how PLAN.md and ACTIVE.md work together:
- PLAN.md = Long-term roadmap (Architect creates, Workers reference)
- ACTIVE.md = Short-term state (Workers update, Architect reviews)
- Sync rule: When a workstream in PLAN.md changes status, ACTIVE.md should reflect it
- The tool should provide a `sync_check()` function that verifies PLAN.md and ACTIVE.md are consistent

### 4. Write Tests

Create `tests/test_plan_sync.py` with tests for:
- Parsing a sample PLAN.md into structured data
- Validating a plan with orphan dependencies
- Generating worker context for a specific workstream
- Updating workstream status

## Constraints
- [ ] Follow `.context/coding_style.md` (type hints, Google docstrings, Pydantic)
- [ ] Parse markdown with regex — no external markdown parser dependencies
- [ ] Maintain backward compatibility with existing PLAN.md format
- [ ] Must handle the case where PLAN.md doesn't exist (graceful error)
- [ ] Pydantic models for all structured data

## Thinking Mode Guidance
Since you're a Thinking-enabled model, explicitly reason through:
1. "What markdown patterns reliably identify phases vs workstreams vs status?"
2. "How do I detect orphan dependencies (workstream claims dependency that doesn't exist)?"
3. "What if PLAN.md format evolves — how do I make the parser future-proof?"
4. "How should PLAN.md <-> ACTIVE.md sync actually work in practice?"

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `specs/plan_sync_protocol.md` — Formal specification
- [ ] `src/tools/plan_sync.py` — Plan sync tool
- [ ] `tests/test_plan_sync.py` — Unit tests

### Validation Steps
1. [ ] `parse_plan()` correctly extracts phases and workstreams from PLAN.md
2. [ ] `validate_plan()` detects orphan dependencies
3. [ ] `generate_worker_context()` returns relevant context for a given workstream
4. [ ] `update_workstream_status()` modifies PLAN.md correctly
5. [ ] Tests pass: `python -m pytest tests/test_plan_sync.py -v`

### State Synchronization
- [ ] Update `.context/ACTIVE.md` on completion (following the protocol from WS 1.1)
- [ ] Report to Architect: design decisions, any incompatibilities found with ACTIVE.md

## ANTI-PATTERNS (Don't Do This)
- ❌ Don't require external markdown parsing libraries
- ❌ Don't modify PLAN.md structure (parse what exists)
- ❌ Don't skip Pydantic models (other tools will consume your output)
- ❌ Don't ignore ACTIVE.md protocol (read and follow it)

---
**Remember:** You are Sonnet 4.5 (Thinking). Your strength is careful reasoning + precise implementation. Read ACTIVE.md and the spec BEFORE you start coding. Trust the Architect's plan.
