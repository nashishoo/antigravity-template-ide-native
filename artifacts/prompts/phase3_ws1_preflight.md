# 🚀 MISSION: Intelligent Preflight Enhancement

## MODEL RECOMMENDATION FOR USER
**For this specific task, please:**
1. Open a new Antigravity chat window
2. Select: **Claude Sonnet 4.5 (Thinking)** from the dropdown
3. Paste this entire prompt
4. Let the worker execute

**Why this model?** Requires "reasoning" to analyze a mission description and map it to relevant skills/tools largely based on semantic understanding, not just keyword matching.

---

## META-CONTEXT (Read This First)
**Parent Project:** Antigravity Workspace Template Self-Improvement
**Your Architect:** Gemini 2.0 Flash Thinking (Acting as Lead Architect)
**Sync Protocol:** Read `.context/ACTIVE.md` and `PLAN.md` before starting.
**Phase 2 Status:** ✅ COMPLETE. Tools are available in `src/tools/`.

## CONTEXT
- **Project:** Antigravity Workspace Template — an IDE-native template for parallel AI agent workflows
- **Project Root:** `c:\Users\Ignacio\Desktop\Template test\my-project\`
- **Tech Stack:** Python 3.11+, Markdown-first architecture
- **Improvement Goal:** The "Preflight" step should be intelligent, not just a static checklist.
- **Root Cause:** Users start missions without knowing which tools or skills are relevant.
- **Success Metric:** `mission_analyzer.py` reads a 1-paragraph mission and recommends the exact right tools/skills with >80% accuracy.

## PREREQUISITE — READ THESE FILES FIRST
- `.context/ACTIVE.md` — Current project state
- `src/tools/_common.py` — Shared utilities (Import these!)
- `preflight.md` — The current static checkpoint file
- `plan.md` — To understand where this fits (Phase 3)

## YOUR SPECIFIC TASK

### 1. Create `src/tools/mission_analyzer.py`

This tool should analyze the `mission.md` (or a string input) and recommend relevant resources.

```python
"""Mission Analyzer & Intelligent Preflight.

Analyzes mission requirements to recommend:
1. Relevant Skills (from src/skills/)
2. Relevant Tools (from src/tools/)
3. Relevant Workflows (from .agent/workflows/)
"""

from tools._common import resolve_project_root, format_tool_response, safe_read_file
# You may import simple NLP tools or use keyword mapping. 
# SIMPLICITY FIRST: Start with a keyword-based mapping system. 
# "Database" -> recommend "sql_tools", "data_validator"
# "Frontend" -> recommend "react_tools"

def analyze_mission(mission_path: str = "mission.md") -> dict:
    """Read mission.md and return recommendations.
    
    Returns:
        dict: {
            "success": bool,
            "mission_summary": str,
            "recommended_skills": List[str],
            "recommended_tools": List[str],
            "recommended_workflows": List[str],
            "reasoning": str
        }
    """

def update_preflight(analysis: dict, preflight_path: str = "preflight.md") -> dict:
    """Update preflight.md with the specific recommendations for this mission.
    
    Does NOT overwrite the whole file. Injects recommendations into a 
    specific "## 🤖 AI Recommendations" section.
    """
```

### 2. Update `preflight.md`

Modify the root `preflight.md` to include a dynamic section for AI recommendations.
- Keep the existing checklist.
- Add a placeholder section: `## 🤖 AI Recommendations (Run mission_analyzer.py to populate)`

### 3. Write Tests (`tests/test_mission_analyzer.py`)

- Test with a mock `mission.md` containing keywords like "Python", "API", "Database".
- Verify it recommends relevant known tools.
- Verify it handles empty/missing mission files gracefully.

## Constraints
- [ ] Follow `.context/coding_style.md`
- [ ] Import from `_common.py`
- [ ] NO heavy ML libraries (torch/transformers). Use simple keyword/regex matching or lightweight heuristic frequency analysis. *Keep it "IDE-native" and fast.*
- [ ] Use `pathlib.Path`

## OUTPUTS (Definition of Done)
- [ ] `src/tools/mission_analyzer.py`
- [ ] `tests/test_mission_analyzer.py`
- [ ] Updated `preflight.md` template

### Validation Steps
1. [ ] `python -m pytest tests/test_mission_analyzer.py -v`
2. [ ] Manually run `mission_analyzer.py` on the current `mission.md` and check output.

---
**Remember:** You are Sonnet 4.5 (Thinking). Focus on the *logic* of recommendation. How do we map "intent" to "tool"?
