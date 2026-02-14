# Architectural Reasoning — 2026-02-13
**Architect:** Claude Opus 4.6 (Thinking)
**Mission:** Antigravity Template Self-Improvement ("Native Agentic" Evolution)

---

## Root Cause Analysis (Not Symptoms — Causes)

### The 3 True Root Causes

After absorbing both review summaries encoded in `mission.md`, I identify **3 root causes** that explain all 8 reported symptoms:

#### Root Cause 1: **No Shared State Protocol**
**Symptoms it explains:**
- Context Synchronization Gap (Review 1, #1)
- Active Context Maintenance (Review 2, #3)
- Workers lack automatic access to Architect's decisions

**Why it exists:** The template treats each agent window as fully independent. There's no file-based "handshake" protocol — workers start cold, the Architect talks into a void, and context drifts as work progresses.

**If I fix this, what improves automatically?**
- Worker onboarding drops from ~5 min (reading + understanding context) to ~1 min (read ACTIVE.md)
- Context drift reduces by ~60% (automatic sync points)
- Integration conflicts decrease (shared state prevents divergent assumptions)

#### Root Cause 2: **Markdown-Only Execution (No Automation Layer)**
**Symptoms it explains:**
- Data Post-Processing gap (Review 2, #1)
- Scaffolding Automation missing (Review 2, #2)
- Manual Prompt Generation (Review 1, #3)
- Blind Skill Discovery (Review 1, #4)

**Why it exists:** The template was designed as "zero-config markdown" — brilliant for thinking, terrible for doing. There's `skills_catalog.py` for discovery, but zero tools for validation, generation, or monitoring.

**If I fix this, what improves automatically?**
- Prompt generation goes from ~10min manual to ~30sec automated
- Data validation goes from "hope it's right" to schema-verified
- Skill recommendations become proactive instead of reactive

#### Root Cause 3: **No Lifecycle Management**
**Symptoms it explains:**
- Artifact Sprawl (Review 1, #2)
- No auto-sync between file changes and task tracking (Review 2, #3)
- Hybrid Vision unfulfilled (Review 2, #4)

**Why it exists:** Projects grow organically. Without archival, cleanup, or structure enforcement, the workspace degrades over time. Old artifacts pollute context windows.

**If I fix this, what improves automatically?**
- Context windows stay clean (auto-archive old artifacts)
- File organization is deterministic (enforced structure)
- Task tracking stays accurate (watchdog updates on changes)

---

## Dependency Chain Analysis

```
RC1: Shared State Protocol
   └─> ACTIVE.md spec          ─┐
   └─> PLAN.md sync system     ─┤─> Enables RC2 tools to know *what* to automate
   └─> Archive hygiene          ─┘

RC2: Automation Layer
   └─> data_validator.py       ─┐
   └─> scaffold.py             ─┤─> Requires RC1 to know project context
   └─> generate_worker_prompt.py─┤
   └─> watchdog_sync.py        ─┘─> Feeds back into RC1 (auto-updates state)

RC3: Lifecycle Management
   └─> Artifact structure      ─┐
   └─> Auto-archival           ─┤─> Requires RC1 for state awareness
   └─> Intelligent preflight   ─┘─> Requires RC2 for tooling
```

**Critical Insight:** RC1 → RC2 → RC3 is the correct sequence. You cannot automate without shared state, and you cannot manage lifecycle without automation.

**What if I resequence?**
- RC2 first → Tools don't know what state the project is in; generate prompts blindly
- RC3 first → Structure enforcement without content; organizing emptiness
- RC1 first → ✅ Everything else gets context-aware capabilities

---

## Strategic Reframes (Surface → Architectural)

| Review Complaint | Surface Solution | Architectural Solution |
|---|---|---|
| "Manual prompt generation is slow" | `generate_prompt.py` script | **Prompt DSL** with templates, context injection from ACTIVE.md, and validation |
| "Workers don't know what happened" | Copy-paste context | **ACTIVE.md protocol** — read-on-entry, update-on-exit contract |
| "No data validation" | Simple validation script | **Pipeline toolkit** with schema registry and Pydantic models |
| "Artifacts everywhere" | Naming conventions doc | **Enforced directory structure** with auto-scaffolding and placement validation |
| "Skills are hard to find" | Better docs | **Mission-aware preflight** that analyzes mission.md and recommends skills |
| "Context drifts mid-project" | More frequent check-ins | **Watchdog** that detects file changes and auto-updates task tracking |

---

## Risk Assessment

### High Risk
- **Over-engineering ACTIVE.md**: If the protocol is too complex, agents won't follow it → Keep it under 30 fields
- **Python dependency bloat**: Adding pandas/watchdog/jinja2 breaks "zero-config" → Make all deps optional with graceful fallback

### Medium Risk
- **Backward compatibility**: Existing projects using v1.0 structure could break → Must test migration path
- **Tool-Agent interface**: Current `skills_catalog.py` is the only tool; pattern may not scale → Design tool registration system early

### Low Risk
- **Documentation overhead**: More docs to maintain → But automation handles this (self-documenting tools)
- **Naming conflicts**: Multiple tools in same directory → Python package conventions handle this

---

## Phase Sequencing Rationale

| Phase | Focus | Duration | Why This Order |
|---|---|---|---|
| **Phase 1** | Context Sync (RC1) | ~2h design + ~3h implement | Foundation — everything else depends on this |
| **Phase 2** | Python Tooling (RC2) | ~4h parallel workstreams | Now tools know *what* to do (context-aware) |
| **Phase 3** | Discovery & Guidance (RC3) | ~3h parallel workstreams | Requires Phases 1+2 for intelligent behavior |
| **Phase 4** | Documentation & Migration | ~2h | Codifies everything, can only happen after building |

**Total estimated:** 14-16 working hours across multiple sessions

---

## Decision: What I'm Building First

**Phase 1, Workstream 1: ACTIVE.md Protocol** — This is the keystone. Everything else collapses without it.

**Design principles for ACTIVE.md:**
1. Simple YAML frontmatter + Markdown body (not JSON — agents read markdown better)
2. Max 15 fields in frontmatter (constraint prevents bloat)
3. Read-on-entry, update-on-exit contract (not continuous polling)
4. Graceful degradation: if ACTIVE.md doesn't exist, fallback to manual context
5. Human-readable: A developer should be able to understand project state by reading ACTIVE.md
