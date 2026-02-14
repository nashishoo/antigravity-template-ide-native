"""File Watchdog & Task Synchronization.

Monitors file changes in the project and suggests updates to ACTIVE.md
and PLAN.md. Works in two modes:
- Full mode: Uses watchdog library for real-time monitoring
- Poll mode: Uses os.scandir() for periodic checks (no external deps)

Author: Worker (Sonnet 4.5 Thinking — Workstream 2.4)
Version: 1.0
"""

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    _HAS_WATCHDOG = True
except ImportError:
    _HAS_WATCHDOG = False

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Literal, Tuple
from pydantic import BaseModel

# Add src/tools to path for relative imports if run as script
sys.path.append(str(Path(__file__).parent))

from _common import (
    resolve_project_root,
    parse_yaml_frontmatter,
    format_tool_response
)
from plan_sync import parse_plan


# ============================================================================
# Constants
# ============================================================================

MONITORED_DIRS = ["src", "specs", ".context", "tests", "artifacts"]
IGNORE_PATTERNS = [
    ".git", "__pycache__", "venv", ".archive", "node_modules",
    ".pytest_cache", ".venv", "build", "dist", ".egg-info"
]


# ============================================================================
# Models
# ============================================================================

class FileChangeRecord(BaseModel):
    """Record of a single file change."""
    filepath: str
    change_type: Literal["created", "modified", "deleted", "moved"]
    timestamp: str  # ISO 8601
    size_bytes: Optional[int] = None
    relates_to_workstream: Optional[List[str]] = None  # Auto-detected


# ============================================================================
# Core Functions
# ============================================================================

def _should_ignore(path: Path) -> bool:
    """Check if a path should be ignored based on IGNORE_PATTERNS.
    
    Args:
        path: Path to check
    
    Returns:
        bool: True if should be ignored
    """
    parts = path.parts
    for pattern in IGNORE_PATTERNS:
        if pattern in parts:
            return True
        if path.name.startswith('.') and path.name != '.context':
            return True
    return False


def detect_changes_since(
    last_check: str, 
    project_root: Optional[str] = None
) -> Dict[str, Any]:
    """Detect file changes since a given timestamp (poll mode).
    
    Scans key directories (src/, specs/, .context/, tests/) and compares
    modification times against the given timestamp.
    
    Args:
        last_check: ISO 8601 timestamp of last check
        project_root: Project root path
    
    Returns:
        dict: {
            "success": bool,
            "changes": List[FileChangeRecord],
            "summary": str,
            "suggested_updates": List[str]
        }
    """
    try:
        root = resolve_project_root(project_root)
    except FileNotFoundError:
        return format_tool_response(
            False, 
            "Could not resolve project root",
            changes=[],
            summary="",
            suggested_updates=[]
        )
    
    # Parse timestamp
    try:
        check_time = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
        if check_time.tzinfo is None:
            # Fallback: treat as local timezone
            check_time = check_time.astimezone()
    except ValueError as e:
        return format_tool_response(
            False,
            f"Invalid timestamp format: {e}",
            changes=[],
            summary="",
            suggested_updates=[]
        )
    
    changes = []
    
    # Scan monitored directories
    for dir_name in MONITORED_DIRS:
        dir_path = root / dir_name
        if not dir_path.exists():
            continue
        
        # Walk directory
        for entry in dir_path.rglob("*"):
            if _should_ignore(entry):
                continue
            
            if entry.is_file():
                try:
                    mtime = datetime.fromtimestamp(entry.stat().st_mtime).astimezone()
                    
                    if mtime > check_time:
                        # Determine change type (simplified: all are "modified")
                        change_type = "modified"
                        if mtime - check_time < datetime.now().astimezone() - check_time:
                            # Very recent → likely created
                            change_type = "created"
                        
                        relative_path = str(entry.relative_to(root))
                        
                        changes.append(FileChangeRecord(
                            filepath=relative_path,
                            change_type=change_type,
                            timestamp=mtime.isoformat(),
                            size_bytes=entry.stat().st_size
                        ))
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
    
    # Sort by timestamp (most recent first)
    changes.sort(key=lambda c: c.timestamp, reverse=True)
    
    # Limit to 100 most recent
    if len(changes) > 100:
        summary = f"{len(changes)} changes detected (showing most recent 100)"
        changes = changes[:100]
    else:
        summary = f"{len(changes)} change{'s' if len(changes) != 1 else ''} detected"
    
    # Convert to dicts
    change_dicts = [c.model_dump() for c in changes]
    
    # Generate suggestions
    suggestions_result = suggest_active_updates(change_dicts)
    
    return format_tool_response(
        True,
        summary,
        changes=change_dicts,
        summary=summary,
        suggested_updates=suggestions_result["suggestions"]
    )


def build_workstream_map(plan_path: Optional[str] = None) -> Dict[str, List[Tuple[str, float]]]:
    """Build a mapping of file paths to workstream IDs from PLAN.md.
    
    Args:
        plan_path: Path to PLAN.md
    
    Returns:
        dict: {filepath: [(workstream_id, confidence_score)]}
    """
    if plan_path is None:
        try:
            root = resolve_project_root()
            plan_path = str(root / "PLAN.md")
        except FileNotFoundError:
            return {}
    
    # Parse PLAN.md
    parse_result = parse_plan(plan_path)
    if not parse_result.get("success"):
        return {}
    
    plan_data = parse_result.get("plan")
    if not plan_data:
        return {}
    
    workstream_map = {}
    
    # Extract deliverables from each workstream
    for phase in plan_data.phases:
        for workstream in phase.workstreams:
            ws_id = workstream.id
            
            for deliverable in workstream.deliverables:
                # Deliverable is a string, might be a file path or description
                # Try to extract file-like patterns
                
                # Direct file mention (e.g., "src/tools/scaffold.py")
                if "/" in deliverable or "\\" in deliverable:
                    filepath = deliverable.strip("`").strip()
                    if filepath not in workstream_map:
                        workstream_map[filepath] = []
                    workstream_map[filepath].append((ws_id, 1.0))  # Direct match
                
                # Directory mention (e.g., "tools in src/tools/")
                if "src/" in deliverable or "tests/" in deliverable or "specs/" in deliverable:
                    # Extract directory pattern
                    parts = deliverable.split()
                    for part in parts:
                        if "/" in part and not part.startswith("http"):
                            dirpath = part.strip("`").strip().rstrip("/")
                            if dirpath not in workstream_map:
                                workstream_map[dirpath] = []
                            workstream_map[dirpath].append((ws_id, 0.8))  # Directory match
    
    return workstream_map


def _match_file_to_workstreams(filepath: str, workstream_map: Dict[str, List[Tuple[str, float]]]) -> List[Tuple[str, float]]:
    """Match a file to workstreams using the workstream map.
    
    Args:
        filepath: Relative file path
        workstream_map: Map from build_workstream_map()
    
    Returns:
        List of (workstream_id, confidence) tuples
    """
    matches = []
    
    # Direct match
    if filepath in workstream_map:
        matches.extend(workstream_map[filepath])
    
    # Directory match
    file_path = Path(filepath)
    for map_path, ws_list in workstream_map.items():
        map_path_obj = Path(map_path)
        
        # Check if file is in this directory
        try:
            if file_path.is_relative_to(map_path_obj):
                for ws_id, conf in ws_list:
                    # Reduce confidence for directory matches
                    matches.append((ws_id, conf * 0.9))
        except (ValueError, AttributeError):
            # is_relative_to might fail on some paths
            if str(file_path).startswith(str(map_path_obj)):
                for ws_id, conf in ws_list:
                    matches.append((ws_id, conf * 0.9))
    
    # Deduplicate and sort by confidence
    unique_matches = {}
    for ws_id, conf in matches:
        if ws_id not in unique_matches or conf > unique_matches[ws_id]:
            unique_matches[ws_id] = conf
    
    result = [(ws_id, conf) for ws_id, conf in unique_matches.items()]
    result.sort(key=lambda x: x[1], reverse=True)
    
    return result


def suggest_active_updates(changes: List[Dict]) -> Dict[str, Any]:
    """Given a list of file changes, suggest updates to ACTIVE.md.
    
    Mapping logic:
    - Changes in src/tools/ → update key_files_modified
    - Changes in specs/ → update key_files_modified  
    - Changes in tests/ → update integration_status
    - New files in .archive/ → update completed_workstreams
    
    Returns:
        dict: {
            "suggestions": List[str],
            "auto_applicable": List[dict],  # Can be applied automatically
            "manual_review": List[dict]      # Need architect review
        }
    """
    if not changes:
        return {
            "suggestions": [],
            "auto_applicable": [],
            "manual_review": []
        }
    
    suggestions = []
    auto_applicable = []
    manual_review = []
    
    # Build workstream map for detection
    workstream_map = build_workstream_map()
    
    # Categorize changes
    key_files = []
    test_files = []
    spec_files = []
    context_files = []
    
    for change in changes:
        filepath = change["filepath"]
        path_obj = Path(filepath)
        
        # Detect workstream relationships
        ws_matches = _match_file_to_workstreams(filepath, workstream_map)
        if ws_matches:
            change["relates_to_workstream"] = [ws[0] for ws in ws_matches[:3]]  # Top 3
        
        # Categorize by directory
        if filepath.startswith("src/tools/") or filepath.startswith("src\\tools\\"):
            key_files.append(filepath)
        elif filepath.startswith("specs/") or filepath.startswith("specs\\"):
            spec_files.append(filepath)
            key_files.append(filepath)
        elif filepath.startswith("tests/") or filepath.startswith("tests\\"):
            test_files.append(filepath)
        elif filepath.startswith(".context/") or filepath.startswith(".context\\"):
            context_files.append(filepath)
    
    # Generate suggestions
    if key_files:
        suggestions.append(f"Update key_files_modified in ACTIVE.md to include: {', '.join('`' + f + '`' for f in key_files[:5])}")
        auto_applicable.append({
            "field": "key_files_modified",
            "action": "append",
            "values": key_files[:15]  # Protocol limit
        })
    
    if test_files:
        suggestions.append(f"Update integration_status in ACTIVE.md to reflect new tests: {len(test_files)} test file(s) modified")
        manual_review.append({
            "field": "integration_status",
            "reason": "Test changes detected",
            "files": test_files
        })
    
    if spec_files:
        suggestions.append(f"Spec files modified: {', '.join('`' + f + '`' for f in spec_files)} — review for critical_decisions updates")
        manual_review.append({
            "field": "critical_decisions",
            "reason": "Specification changes may contain new architectural decisions",
            "files": spec_files
        })
    
    if context_files:
        suggestions.append(f"Context files modified: {', '.join('`' + f + '`' for f in context_files)} — ACTIVE.md may already be updated")
    
    # Workstream-specific suggestions
    related_workstreams = set()
    for change in changes:
        if change.get("relates_to_workstream"):
            related_workstreams.update(change["relates_to_workstream"])
    
    if related_workstreams:
        ws_list = ", ".join(sorted(related_workstreams))
        suggestions.append(f"Changes may relate to workstream(s): {ws_list}")
    
    return {
        "suggestions": suggestions,
        "auto_applicable": auto_applicable,
        "manual_review": manual_review
    }


def check_staleness(active_path: str = ".context/ACTIVE.md") -> Dict[str, Any]:
    """Check if ACTIVE.md is stale (>24h since last update).
    
    Args:
        active_path: Path to ACTIVE.md (relative or absolute)
    
    Returns:
        dict: {
            "success": bool,
            "is_stale": bool,
            "hours_since_architect_update": float,
            "hours_since_worker_update": float,
            "recommendation": str
        }
    """
    # Resolve full path if needed
    if not Path(active_path).is_absolute():
        try:
            root = resolve_project_root()
            active_path = str(root / active_path)
        except FileNotFoundError:
            return format_tool_response(
                False,
                "Could not resolve project root",
                is_stale=False,
                hours_since_architect_update=0.0,
                hours_since_worker_update=0.0,
                recommendation=""
            )
    
    # Parse ACTIVE.md
    parse_result = parse_yaml_frontmatter(active_path)
    if not parse_result["success"]:
        return format_tool_response(
            False,
            f"Failed to parse ACTIVE.md: {', '.join(parse_result['errors'])}",
            is_stale=False,
            hours_since_architect_update=0.0,
            hours_since_worker_update=0.0,
            recommendation="Cannot check staleness - YAML parse error"
        )
    
    frontmatter = parse_result["frontmatter"]
    
    # Extract timestamps
    ts_architect = frontmatter.get("last_architect_update")
    ts_worker = frontmatter.get("last_worker_update")
    
    if not ts_architect and not ts_worker:
        return format_tool_response(
            False,
            "ACTIVE.md missing timestamp fields",
            is_stale=True,
            hours_since_architect_update=0.0,
            hours_since_worker_update=0.0,
            recommendation="Add last_architect_update and last_worker_update timestamps"
        )
    
    now = datetime.now().astimezone()
    
    hours_arch = 0.0
    hours_work = 0.0
    
    try:
        if ts_architect:
            dt_arch = datetime.fromisoformat(ts_architect.replace('Z', '+00:00'))
            if dt_arch.tzinfo is None:
                dt_arch = dt_arch.astimezone()
            diff = now - dt_arch
            hours_arch = diff.total_seconds() / 3600.0
        
        if ts_worker:
            dt_work = datetime.fromisoformat(ts_worker.replace('Z', '+00:00'))
            if dt_work.tzinfo is None:
                dt_work = dt_work.astimezone()
            diff = now - dt_work
            hours_work = diff.total_seconds() / 3600.0
    except ValueError as e:
        return format_tool_response(
            False,
            f"Invalid timestamp format: {e}",
            is_stale=False,
            hours_since_architect_update=0.0,
            hours_since_worker_update=0.0,
            recommendation=""
        )
    
    # Determine staleness (use most recent update)
    hours_since_last =min(hours_arch if hours_arch > 0 else float('inf'), 
                           hours_work if hours_work > 0 else float('inf'))
    
    if hours_since_last == float('inf'):
        hours_since_last = 0.0
    
    is_stale = hours_since_last > 24
    
    # Generate recommendation
    if hours_since_last > 48:
        recommendation = f"ALERT: ACTIVE.md is very stale ({hours_since_last:.1f}h). Architect should review immediately."
    elif hours_since_last > 24:
        recommendation = f"WARNING: ACTIVE.md is stale ({hours_since_last:.1f}h). Consider updating."
    else:
        recommendation = f"ACTIVE.md is fresh ({hours_since_last:.1f}h since last update)."
    
    return format_tool_response(
        True,
        recommendation,
        is_stale=is_stale,
        hours_since_architect_update=round(hours_arch, 2),
        hours_since_worker_update=round(hours_work, 2),
        recommendation=recommendation
    )


def generate_change_report(project_root: Optional[str] = None, since: Optional[str] = None) -> Dict[str, Any]:
    """Generate a comprehensive report of project state for the Architect.
    
    Combines:
    - File change detection  
    - ACTIVE.md staleness
    - Suggested actions
    
    Args:
        project_root: Project root path
        since: ISO 8601 timestamp for change detection (default: 24h ago)
    
    Returns:
        dict: Full status report
    """
    try:
        root = resolve_project_root(project_root)
    except FileNotFoundError:
        return format_tool_response(
            False,
            "Could not resolve project root",
            report={}
        )
    
    # Default: check last 24 hours
    if since is None:
        since_dt = datetime.now().astimezone() - timedelta(hours=24)
        since = since_dt.isoformat()
    
    report = {}
    
    # 1. File changes
    changes_result = detect_changes_since(since, str(root))
    report["file_changes"] = {
        "count": len(changes_result.get("changes", [])),
        "summary": changes_result.get("summary", ""),
        "changes": changes_result.get("changes", [])[:20],  # Top 20
        "suggested_updates": changes_result.get("suggested_updates", [])
    }
    
    # 2. Staleness check
    staleness_result = check_staleness(str(root / ".context" / "ACTIVE.md"))
    report["active_md_staleness"] = {
        "is_stale": staleness_result.get("is_stale", False),
        "hours_since_architect": staleness_result.get("hours_since_architect_update", 0.0),
        "hours_since_worker": staleness_result.get("hours_since_worker_update", 0.0),
        "recommendation": staleness_result.get("recommendation", "")
    }
    
    # 3. Summary
    summary_lines = []
    summary_lines.append(f"Project Status Report (since {since})")
    summary_lines.append(f"- File Changes: {report['file_changes']['count']}")
    summary_lines.append(f"- ACTIVE.md Status: {report['active_md_staleness']['recommendation']}")
    
    if report['file_changes']['suggested_updates']:
        summary_lines.append(f"- Suggested Updates: {len(report['file_changes']['suggested_updates'])}")
    
    report["summary"] = "\n".join(summary_lines)
    
    return format_tool_response(
        True,
        "Change report generated",
        report=report
    )


# ============================================================================
# Optional: Watchdog Mode (Real-time monitoring)
# ============================================================================

if _HAS_WATCHDOG:
    class ProjectFileHandler(FileSystemEventHandler):
        """Handles file system events for watchdog mode."""
        
        def __init__(self, ignore_patterns: List[str]):
            super().__init__()
            self.ignore_patterns = ignore_patterns
            self.change_queue = []
        
        def _should_ignore(self, path: str) -> bool:
            """Check if path matches ignore patterns."""
            path_obj = Path(path)
            return _should_ignore(path_obj)
        
        def on_modified(self, event):
            """Handle file modification events."""
            if event.is_directory or self._should_ignore(event.src_path):
                return
            
            self.change_queue.append({
                "filepath": event.src_path,
                "change_type": "modified",
                "timestamp": datetime.now().astimezone().isoformat()
            })
        
        def on_created(self, event):
            """Handle file creation events."""
            if event.is_directory or self._should_ignore(event.src_path):
                return
            
            self.change_queue.append({
                "filepath": event.src_path,
                "change_type": "created",
                "timestamp": datetime.now().astimezone().isoformat()
            })
        
        def on_deleted(self, event):
            """Handle file deletion events."""
            if event.is_directory or self._should_ignore(event.src_path):
                return
            
            self.change_queue.append({
                "filepath": event.src_path,
                "change_type": "deleted",
                "timestamp": datetime.now().astimezone().isoformat()
            })
    
    def start_monitoring(project_root: Optional[str] = None, duration_seconds: int = 60) -> Dict[str, Any]:
        """Start watchdog monitor (requires watchdog library).
        
        Args:
            project_root: Project root to monitor
            duration_seconds: How long to monitor (default: 60s)
        
        Returns:
            dict: Monitoring results
        """
        try:
            root = resolve_project_root(project_root)
        except FileNotFoundError:
            return format_tool_response(
                False,
                "Could not resolve project root",
                changes=[]
            )
        
        handler = ProjectFileHandler(IGNORE_PATTERNS)
        observer = Observer()
        
        # Watch monitored directories
        for dir_name in MONITORED_DIRS:
            dir_path = root / dir_name
            if dir_path.exists():
                observer.schedule(handler, str(dir_path), recursive=True)
        
        observer.start()
        
        try:
            import time
            time.sleep(duration_seconds)
        finally:
            observer.stop()
            observer.join()
        
        # Process queue
        changes = handler.change_queue
        
        return format_tool_response(
            True,
            f"Monitored for {duration_seconds}s, detected {len(changes)} changes",
            changes=changes
        )

else:
    def start_monitoring(project_root: Optional[str] = None, duration_seconds: int = 60) -> Dict[str, Any]:
        """Watchdog mode not available (library not installed).
        
        Returns:
            dict: Error response
        """
        return format_tool_response(
            False,
            "Watchdog library not installed. Use poll mode with detect_changes_since() instead.",
            changes=[]
        )


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import json
    
    # Simple CLI for testing
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python watchdog_sync.py staleness")
        print("  python watchdog_sync.py changes <since_timestamp>")
        print("  python watchdog_sync.py report")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "staleness":
        result = check_staleness()
        print(json.dumps(result, indent=2))
    
    elif command == "changes":
        if len(sys.argv) < 3:
            print("Error: Missing timestamp argument")
            sys.exit(1)
        since = sys.argv[2]
        result = detect_changes_since(since)
        print(json.dumps(result, indent=2))
    
    elif command == "report":
        result = generate_change_report()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
