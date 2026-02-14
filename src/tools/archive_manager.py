import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, TypedDict


class ArchiveMeta(TypedDict):
    original_path: str
    archive_date: str
    reason: str
    archived_by: str
    replacement: Optional[str]


class ArchiveStatus(TypedDict):
    status: str
    message: str
    archive_path: Optional[str]
    snapshot_path: Optional[str]
    items: Optional[List[Dict[str, Any]]]


class ArchiveManager:
    """Manages the archival of project artifacts and deprecated items.
    
    This tool follows the 'stdlib only' constraint to ensure it can be run
    without external dependencies, making it suitable for environment maintenance.
    """

    def __init__(self, project_root: Optional[str] = None):
        """Initializes the ArchiveManager with the project root.
        
        Args:
            project_root: The absolute path to the project root. If None, it uses the current working directory.
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.archive_dir = self.project_root / ".archive"
        self.completed_dir = self.archive_dir / "completed"
        self.deprecated_dir = self.archive_dir / "deprecated"
        self.snapshots_dir = self.archive_dir / "snapshots"
        
        # Ensure directories exist
        self.completed_dir.mkdir(parents=True, exist_ok=True)
        self.deprecated_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def _create_meta(self, source_path: Path, archive_path: Path, reason: str, replacement: Optional[str] = None) -> None:
        """Creates a .meta.json sidecar file for an archived item.
        
        Args:
            source_path: The original path of the item.
            archive_path: The path where the item is archived.
            reason: The reason for archival.
            replacement: (Optional) The path to the replacement item if deprecated.
        """
        meta: ArchiveMeta = {
            "original_path": str(source_path.relative_to(self.project_root)),
            "archive_date": datetime.now().isoformat(),
            "reason": reason,
            "archived_by": "ArchiveManager",
            "replacement": replacement
        }

        meta_file = archive_path.with_suffix(archive_path.suffix + ".meta.json")
        if archive_path.is_dir():
            meta_file = archive_path.parent / (archive_path.name + ".meta.json")

        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)

    def archive_completed(self, source_path: str, reason: str) -> Dict[str, Any]:
        """Move a file/directory to .archive/completed/ with metadata.
        
        Args:
            source_path: Path to the item to archive (relative to project root or absolute).
            reason: Reason for archival.
            
        Returns:
            A status dictionary with "status", "message", and "archive_path".
        """
        try:
            src = Path(source_path)
            if not src.is_absolute():
                src = self.project_root / src

            if not src.exists():
                return {"status": "error", "message": f"Source path {source_path} does not exist."}

            target = self.completed_dir / src.name
            if target.exists():
                # Append timestamp if conflict
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                target = self.completed_dir / f"{src.name}_{timestamp}"

            shutil.move(str(src), str(target))
            self._create_meta(src, target, reason)

            return {
                "status": "success",
                "message": f"Archived {source_path} to {target.relative_to(self.project_root)}",
                "archive_path": str(target.relative_to(self.project_root))
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to archive: {str(e)}"}

    def archive_deprecated(self, source_path: str, replacement: str) -> Dict[str, Any]:
        """Move to .archive/deprecated/ noting what replaced it.
        
        Args:
            source_path: Path to the item to archive.
            replacement: Path or description of the replacement.
            
        Returns:
            A status dictionary.
        """
        try:
            src = Path(source_path)
            if not src.is_absolute():
                src = self.project_root / src

            if not src.exists():
                return {"status": "error", "message": f"Source path {source_path} does not exist."}

            target = self.deprecated_dir / src.name
            if target.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                target = self.deprecated_dir / f"{src.name}_{timestamp}"

            shutil.move(str(src), str(target))
            self._create_meta(src, target, "Deprecated", replacement=replacement)

            return {
                "status": "success",
                "message": f"Deprecated {source_path} moved to {target.relative_to(self.project_root)}",
                "archive_path": str(target.relative_to(self.project_root))
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to deprecate: {str(e)}"}

    def create_snapshot(self, label: str) -> Dict[str, Any]:
        """Create a timestamped snapshot of current ACTIVE.md + PLAN.md state.
        
        Args:
            label: A descriptive label for the snapshot.
            
        Returns:
            A status dictionary.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_dir = self.snapshots_dir / f"{label}_{timestamp}"
            snapshot_dir.mkdir(parents=True, exist_ok=True)

            files_to_snapshot = [
                self.project_root / ".context" / "ACTIVE.md",
                self.project_root / "PLAN.md"
            ]

            copied = []
            for f in files_to_snapshot:
                if f.exists():
                    shutil.copy2(str(f), str(snapshot_dir / f.name))
                    copied.append(f.name)

            return {
                "status": "success",
                "message": f"Created snapshot {label} with files: {', '.join(copied)}",
                "snapshot_path": str(snapshot_dir.relative_to(self.project_root))
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to create snapshot: {str(e)}"}

    def list_archive(self, category: str = "all") -> Dict[str, Any]:
        """List archived items with metadata.
        
        Args:
            category: "completed", "deprecated", "snapshots", or "all".
            
        Returns:
            A status dictionary with "items".
        """
        try:
            items = []
            dirs_to_check = []
            if category == "all":
                dirs_to_check = [self.completed_dir, self.deprecated_dir, self.snapshots_dir]
            elif category == "completed":
                dirs_to_check = [self.completed_dir]
            elif category == "deprecated":
                dirs_to_check = [self.deprecated_dir]
            elif category == "snapshots":
                dirs_to_check = [self.snapshots_dir]
            else:
                return {"status": "error", "message": f"Invalid category: {category}"}

            for d in dirs_to_check:
                if not d.exists():
                    continue
                for item in d.iterdir():
                    if item.name == ".keep" or item.name.endswith(".meta.json"):
                        continue
                    
                    meta_file = item.with_suffix(item.suffix + ".meta.json")
                    if item.is_dir():
                        meta_file = d / (item.name + ".meta.json")
                        
                    meta = {}
                    if meta_file.exists():
                        try:
                            with open(meta_file, "r") as f:
                                meta = json.load(f)
                        except Exception:
                            meta = {"error": "Failed to read metadata"}
                    
                    items.append({
                        "name": item.name,
                        "category": d.name,
                        "path": str(item.relative_to(self.project_root)),
                        "meta": meta
                    })

            return {"status": "success", "items": items}
        except Exception as e:
            return {"status": "error", "message": f"Failed to list archive: {str(e)}"}

    def restore_from_archive(self, archive_path: str) -> Dict[str, Any]:
        """Restore an archived item to its original location.
        
        Args:
            archive_path: Path to the item within .archive/ (relative to project root or absolute).
            
        Returns:
            A status dictionary.
        """
        try:
            arch_p = Path(archive_path)
            if not arch_p.is_absolute():
                arch_p = self.project_root / arch_p

            if not arch_p.exists():
                return {"status": "error", "message": f"Archive path {archive_path} does not exist."}

            meta_file = arch_p.with_suffix(arch_p.suffix + ".meta.json")
            if arch_p.is_dir():
                meta_file = arch_p.parent / (arch_p.name + ".meta.json")

            if not meta_file.exists():
                return {"status": "error", "message": f"Metadata not found for {archive_path}. Cannot restore."}

            with open(meta_file, "r") as f:
                meta = json.load(f)

            orig_path = self.project_root / meta["original_path"]
            
            if orig_path.exists():
                return {
                    "status": "error", 
                    "message": f"Conflict: Original path {meta['original_path']} already exists. Restore aborted."
                }

            orig_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(arch_p), str(orig_path))
            if meta_file.exists():
                meta_file.unlink() # Delete metadata upon restoration

            return {
                "status": "success",
                "message": f"Restored {archive_path} to {meta['original_path']}"
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to restore: {str(e)}"}


def archive_completed(source_path: str, reason: str) -> dict:
    """Archival helper for completed items."""
    return ArchiveManager().archive_completed(source_path, reason)


def archive_deprecated(source_path: str, replacement: str) -> dict:
    """Archival helper for deprecated items."""
    return ArchiveManager().archive_deprecated(source_path, replacement)


def create_snapshot(label: str) -> dict:
    """Archival helper for snapshots."""
    return ArchiveManager().create_snapshot(label)


def list_archive(category: str = "all") -> dict:
    """Archival helper to list contents."""
    return ArchiveManager().list_archive(category)


def restore_from_archive(archive_path: str) -> dict:
    """Archival helper to restore items."""
    return ArchiveManager().restore_from_archive(archive_path)
