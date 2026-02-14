# 🚀 MISSION: Active Context Protocol Designer

## MODEL RECOMMENDATION FOR USER
**For this specific task, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Sonnet 4.5 (Thinking)** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Thinking mode needed — this is a foundational protocol that all other tools depend on. Edge cases (concurrent updates, stale state) need explicit reasoning.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Claude Opus 4.6 (Thinking) (operating in main window)
**Sync Protocol:** Read PLAN.md if it exists before starting. This is foundational work — there is no ACTIVE.md yet because YOU are designing it.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture, IDE-native agents (Antigravity)
- **Improvement Goal:** Eliminate context drift between Architect and Worker agents
- **Root Cause:** Workers start with zero knowledge of what the Architect decided, what's in progress, and what's blocked
- **Success Metric:** A worker reading ACTIVE.md can understand project state in <60 seconds

## ORIGINAL REVIEW FEEDBACK (Exact Quotes)

**Review 1 (review_adoptme.md):**
> "Workers do not automatically inherit the Architect's `task.md` or latest decisions without manual copy-pasting."
> "Formalize a 'Sync Protocol'. The Architect should update a `PLAN.md` in the root, and every Worker prompt should start with: 'Read `PLAN.md` to understand your current context.'"

**Review 2 (final_review_adoptme.md):**
> "The biggest friction was 'Context Drift'. We shouldn't rely on CLIs for *thinking*, but on files for *memory*."
> "Active Context Protocol (`.context/ACTIVE.md`): A living file that acts as the 'mental state' of the project. Every agent reads it on entry and updates it on exit."

## CURRENT STATE
- `.context/` directory exists with `coding_style.md` and `system_prompt.md`
- No context synchronization protocol exists
- Workers currently receive all context via copy-pasted prompts (fragile, incomplete)
- Architects must manually track what each worker knows

## CODING STANDARDS (from `.context/coding_style.md`)
- Type hints mandatory for all function signatures
- Google-style docstrings with `Args:`, `Returns:`, `Raises:`
- Pydantic for complex data models
- Tools must fail gracefully (return error dicts, not crash)

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

## Constraints
- [ ] ACTIVE.md must be valid YAML frontmatter + Markdown (parseable by standard tools)
- [ ] Max 15 fields in frontmatter (prevent bloat)
- [ ] Must work without Python tools (plain markdown editing)
- [ ] Must gracefully degrade if file doesn't exist
- [ ] Must be human-readable (a developer can understand state by reading it)

## Thinking Mode Guidance
Since you're a Thinking-enabled model, explicitly reason through:
1. "What if two workers update ACTIVE.md at the same time?"
2. "What if ACTIVE.md becomes stale (no one updates it)?"
3. "What's the minimum viable set of fields that provides maximum value?"
4. "How does this interact with PLAN.md (which will be created in Workstream 1.2)?"

## OUTPUTS (Definition of Done)

### Files to Create
- [ ] `.context/ACTIVE.md` — Working template with initial state
- [ ] `specs/active_context_protocol.md` — Formal specification
- [ ] Create `specs/` directory if it doesn't exist

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

---
**Remember:** You are Sonnet 4.5 (Thinking). Your strength is careful reasoning + precise implementation. Trust the Architect's plan. If requirements are unclear, document your assumption and proceed.
