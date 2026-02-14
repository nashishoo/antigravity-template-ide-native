# Contributing to v2.0 Completion

## 🚧 Current Status
*   **Phase 1 & 2:** ✅ Complete (63% of total roadmap)
*   **Phase 3 & 4:** ⏳ Pending (37%)

We are looking for contributors to help us cross the finish line while our lead Architect (Claude Opus) is on a mandatory break (quota limit).

## How to Help

### Option 1: Implement a Workstream (The "Big Help")
Phases 3 and 4 are fully planned. You can pick up a shovel and start digging immediately.

**Available Workstreams (See `PLAN.md` for details):**
*   **[ ] Phase 3.1: Intelligent Preflight Enhancement**
    *   *Goal:* Build `mission_analyzer.py` to recommend skills based on `mission.md`.
*   **[ ] Phase 3.2: Artifact Structure Enforcement**
    *   *Goal:* Build `artifact_manager.py` to enforce the `artifacts/` folder structure.
*   **[ ] Phase 3.3: Smart Prompt Generator**
    *   *Goal:* Build `generate_worker_prompt.py` using Jinja2 templates.
*   **[ ] Phase 4.1: Specification Documentation**
    *   *Goal:* Write formal specs for the Python tooling.

**How to claim a workstream:**
1.  Check the Issues tab (or `PLAN.md`) to ensure it's not claimed.
2.  Read the **Workstream Definition** in `PLAN.md`.
3.  Implement the feature following the coding style in `.context/coding_style.md`.
4.  Write tests (mandatory).
5.  Submit a PR.

### Option 2: Test & Provide Feedback (The "Strategic Help")
We need real-world data. verified
*   Use `ACTIVE.md` in your own project.
*   Does it actually help? Do you often forget to update it?
*   Did `scaffold.py` save you time?
*   Open an Issue with your experience. "I tried Context Sync and here is where it failed" is extremely valuable feedback.

### Option 3: Improve Documentation (The "Friendly Help")
*   Our docstrings are good, but our tutorials are non-existent.
*   Write a "How I used v2.0 to build X" guide.
*   Improve the `MIGRATION_GUIDE` based on your actual migration experience.

## Development Setup

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/nashishoo/antigravity-template-ide-native.git
    cd antigravity-template-ide-native
    ```

2.  **Install Dev Dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install pytest
    ```

3.  **Run Tests:**
    Ensure the baseline is green before you start.
    ```bash
    pytest
    ```

## Coding Standards
*   **Style:** Follow `.context/coding_style.md`.
*   **Types:** Type hints are **mandatory** for all new Python code.
*   **Validation:** Use `pydantic` for data models.
*   **Tests:** No feature is "done" without a test in `tests/`.

## Review Process
*   PRs are reviewed by the core team (currently Human + AI Agents).
*   Automated tests must pass.
*   We value **clarity** over cleverness.

## Questions?
*   Open a GitHub Issue.
*   Join the discussion on the Discord (if applicable).
