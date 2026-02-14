# Strategic Preflight — 2026-02-13
**Architect:** Claude Opus 4.6 (Thinking)

---

## 1. Current Capabilities Inventory

### Python Tools (`src/tools/`)
| Tool | Purpose | Status |
|------|---------|--------|
| `skills_catalog.py` | Skill discovery (local + remote) | ✅ Functional (4 functions) |
| `loader.py` | Skill loading from filesystem | ✅ Functional |

### Skills (`src/skills/`)
| Skill | Purpose | Status |
|-------|---------|--------|
| `research/` | Web research capability | ✅ Has SKILL.md + tools.py |

### Workflows (`.agent/workflows/`)
| Workflow | Purpose | Status |
|----------|---------|--------|
| `preflight.md` | Skill inventory before delegation | ✅ Functional |
| `parallel_architect.md` | Architect → Worker prompt generation | ✅ Functional |
| `swarm.md` | Router → Coder → Reviewer simulation | ✅ Functional |
| `openspec-proposal.md` | Scaffold OpenSpec changes | ✅ Functional |
| `openspec-apply.md` | Implement approved OpenSpec changes | ✅ Functional |
| `openspec-archive.md` | Archive deployed OpenSpec changes | ✅ Functional |

### Context Files (`.context/`)
| File | Purpose | Status |
|------|---------|--------|
| `coding_style.md` | Python coding standards (type hints, Pydantic, docstrings) | ✅ |
| `system_prompt.md` | Core persona definition | ✅ |

### Infrastructure
| Component | Status |
|-----------|--------|
| `venv/` | ✅ Python virtual environment exists |
| `tests/` | ❌ **Empty** — no test infrastructure |
| `openspec/` | ✅ Has AGENTS.md, project.md, specs/, changes/ |
| `artifacts/` | ⚠️ Created (had only `.keep` before today) |

---

## 2. Critical Gaps Analysis

### Gap 1: No Context Synchronization Files
- **Missing:** `.context/ACTIVE.md` — No shared state protocol
- **Missing:** `PLAN.md` — No centralized project roadmap file
- **Impact:** Workers start with zero knowledge of Architect's decisions
- **Priority:** 🔴 CRITICAL (Phase 1)

### Gap 2: No Python Automation Tools
- **Missing:** `data_validator.py` — No data validation capability
- **Missing:** `data_cleaner.py` — No data cleaning
- **Missing:** `scaffold.py` — No code generation from specs
- **Missing:** `watchdog_sync.py` — No file change monitoring
- **Missing:** `generate_worker_prompt.py` — No automated prompt generation
- **Impact:** All "grunt work" is manual; prone to errors and slow
- **Priority:** 🟡 HIGH (Phase 2)

### Gap 3: No Test Infrastructure
- **Missing:** `tests/` is completely empty
- **Missing:** No `pytest.ini` or `pyproject.toml` for test config
- **Missing:** No CI/CD pipeline (`.github/workflows/` may exist but untested)
- **Impact:** Cannot verify tool correctness; no regression protection
- **Priority:** 🟡 HIGH (Phase 2 — parallel with tool development)

### Gap 4: No Structured Artifact Management
- **Missing:** No `artifacts/logs/`, `artifacts/data/`, `artifacts/reports/` subdirectories
- **Missing:** No auto-archival mechanism
- **Impact:** Artifacts accumulate in flat directory; hard to find things
- **Priority:** 🟢 MEDIUM (Phase 3)

---

## 3. Dependency Recommendations

### Required Python Packages (Add to `requirements.txt`)

| Package | Purpose | Phase | Optional? |
|---------|---------|-------|-----------|
| `pydantic >= 2.0` | Data models for tools | Phase 2 | No (in coding_style.md) |
| `pyyaml` | ACTIVE.md YAML frontmatter parsing | Phase 1 | No |
| `jinja2` | Prompt template generation | Phase 2 | Yes (graceful fallback) |
| `watchdog` | File system monitoring | Phase 2 | Yes (core works without it) |
| `pytest` | Test framework | Phase 2 | No (must verify tools) |

### NOT Recommended (Keep Optional)
| Package | Why Not Required |
|---------|-----------------|
| `pandas` | Overkill for template; Pydantic handles data validation |
| `rich` | Nice-to-have but adds dep; plain print is fine |

---

## 4. Shared Tooling Opportunities

Several workstreams can share infrastructure:

```
ACTIVE.md parser     → Used by: watchdog_sync, generate_worker_prompt, preflight
Pydantic models     → Used by: data_validator, scaffold, ACTIVE.md protocol
Template engine      → Used by: generate_worker_prompt, scaffold
File system utils   → Used by: watchdog_sync, archive hygiene, artifact structure
```

**Recommendation:** Create `src/tools/_common.py` with shared utilities:
- `parse_active_md()` — Read/write ACTIVE.md
- `parse_plan_md()` — Read/write PLAN.md
- `resolve_project_root()` — Find project root from any tool location

---

## 5. Preflight Verdict

| Category | Ready? | Action Needed |
|----------|--------|---------------|
| **Skills infrastructure** | ✅ Yes | Discovery tools work |
| **Workflow definitions** | ✅ Yes | 6 workflows operational |
| **Context protocol** | ❌ No | Must create ACTIVE.md + PLAN.md specs |
| **Python tooling** | ❌ No | 0/5 required tools exist |
| **Test infrastructure** | ❌ No | Must create test framework |
| **Artifact structure** | ⚠️ Partial | Directory exists but unstructured |

**Delegation Gate: OPEN** — Enough infrastructure exists to begin Phase 1 (documentation/spec work). Phase 2 workers will need the `venv` with additional packages.
