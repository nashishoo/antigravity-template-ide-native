# Archive Hygiene Conventions

This directory serves as the long-term storage for the project, ensuring the active workspace remains lean and focused.

## Archive Structure

- `completed/`: Finished workstreams, phases, and mission logs.
- `deprecated/`: Old tools, specifications, and components no longer in active use.
- `snapshots/`: Periodic point-in-time backups of critical system state (e.g., `ACTIVE.md`).

## Archival Rules

### When to Archive
- A workstream is marked as 100% complete.
- A tool or specification has been fully replaced by a newer version.
- Before major refactors (snapshot).

### When NOT to Archive
- Active task files or plans.
- Core project configuration (`.agent/`, `.context/`).
- Git history.

## How to Restore
Archives include a `.meta.json` sidecar. To restore:
1. Locate the item in `.archive/`.
2. check `.meta.json` for the `original_path`.
3. Use the `Archive Manager` tool:
   ```python
   restore_from_archive(".archive/completed/my_item")
   ```

## Naming Conventions
- Archived items retain their original names when possible.
- If a name conflict exists, a timestamp suffix is appended.
