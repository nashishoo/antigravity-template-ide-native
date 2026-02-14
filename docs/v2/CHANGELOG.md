# Changelog - v2.0.0-alpha.1

All notable changes to the **Antigravity Workspace Template** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-alpha.1] - 2026-02-14

### Added (Phase 1: Context Synchronization)
*   `.context/ACTIVE.md` - **The cornerstone of v2.0.** A dedicated state file for tracking current focus, active workstreams, and blockers. Solves the "Context Drift" problem where agents lose track of project status.
*   `specs/active_context_protocol.md` - Formal specification for the Context Sync protocol, defining the "Read-on-Entry / Update-on-Exit" contract.
*   `.archive/` directory structure - Standardized folders for `completed`, `deprecated`, and `snapshots` to keep the workspace clean.
*   `src/tools/archive_manager.py` - Tool to programmatically move files to the archive with metadata (who archived it, when, and why).
*   `src/tools/plan_sync.py` - Tool to parse `PLAN.md` and sync its status with `ACTIVE.md`.

### Added (Phase 2: Python Tooling)
*   `src/tools/_common.py` - Shared utilities for path resolution, ACTIVE.md parsing, and standardized logging.
*   `src/tools/data_validator.py` - **Critical Integrity Layer.** Pydantic-based validation engine that ensures `ACTIVE.md`, `PLAN.md`, and other data files adhere to their schemas.
*   `src/tools/scaffold.py` - Automation tool to generate new tools, spec files, and test files from templates, reducing boilerplate fatigue.
*   `src/tools/watchdog_sync.py` - A daemon that monitors file system events and prompts the user/agent to update `ACTIVE.md` when files are modified.
*   `tests/` hierarchy - A complete pytest suite for all new tools.
*   `pyproject.toml` - Standardized Python project configuration.

### Changed
*   `PLAN.md` - Enhanced structure to support programmatic parsing. Now serves as the "Long Term Memory" while `ACTIVE.md` is "Short Term Memory".
*   `artifacts/` - Structure is now strictly enforced (though not yet fully automated until Phase 3).

### Architecture Changes
*   **Shared State Protocol**: Moved from "implicit knowledge" (in the chat window) to "explicit knowledge" (in `.context/ACTIVE.md`).
*   **Hybrid Model (Markdown + Python)**: We now explicitly distinguish between *Thinking* (Markdown files) and *Doing* (Python tools). v1.0 tried to do everything in Markdown or ad-hoc scripts.
*   **Validation-First**: All core protocols now have corresponding validation tools. You can't break `ACTIVE.md` structure without the validator yelling at you.

### Tests
*   Added **49** unit tests covering all Phase 2 tools.
*   Test coverage estimated at >90% for `src/tools/`.
*   Run tests with: `pytest`

### Breaking Changes
*   **None.** v2.0 is designed to be **additive**. Existing v1.0 projects can adopt these tools incrementally.
*   *Note:* If you choose to use `ACTIVE.md`, you must follow the schema, otherwise `data_validator.py` will report errors.

### Known Issues
*   **Phase 3 & 4 Incomplete**: The "Intelligent" layer (Smart Preflight, Prompt Generator) is missing.
*   **Watchdog Polling**: The `watchdog_sync.py` tool currently relies on polling in some environments if the `watchdog` library isn't fully supported.
*   **Manual Spec Writing**: You still have to write `specs/` manually; the AI generator for specs is coming in Phase 3.
