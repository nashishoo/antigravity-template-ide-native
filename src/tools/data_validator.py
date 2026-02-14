"""Data Validation Pipeline.

Validates project data files against expected schemas using Pydantic models.
Supports ACTIVE.md frontmatter, PLAN.md structure, and custom schema definitions.

Author: Worker (Gemini 3 Flash — Workstream 2.2)
Version: 1.0
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

# Add src/tools to path for relative imports if run as script
sys.path.append(str(Path(__file__).parent))

from _common import parse_yaml_frontmatter, format_tool_response, resolve_project_root
import plan_sync

class ActiveMdSchema(BaseModel):
    """Pydantic model matching the ACTIVE.md frontmatter specification."""
    project_name: str = Field(..., max_length=100)
    mission_summary: str = Field(..., max_length=200)
    current_phase: str
    active_workstreams: List[str] = Field(default_factory=list)
    blocked_workstreams: List[str] = Field(default_factory=list)
    completed_workstreams: List[str] = Field(default_factory=list)
    last_architect_update: str
    last_worker_update: str
    critical_decisions: List[str] = Field(default_factory=list)
    key_files_modified: List[str] = Field(default_factory=list)
    integration_status: str
    next_milestone: str
    risk_alerts: List[str] = Field(default_factory=list)

    @field_validator('last_architect_update', 'last_worker_update')
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        """Validate ISO 8601 timestamp format."""
        try:
            # We use a broad check for ISO 8601
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 timestamp: {v}")

def validate_active_md(active_path: Optional[str] = None) -> Dict[str, Any]:
    """Validate ACTIVE.md against the protocol schema.
    
    Args:
        active_path: Path to ACTIVE.md. Defaults to .context/ACTIVE.md.

    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],       # Schema violations
            "warnings": List[str],     # Non-fatal issues
            "field_count": int,
            "staleness_hours": float   # Hours since last update
        }
    """
    if active_path is None:
        try:
            root = resolve_project_root()
            active_path = str(root / ".context" / "ACTIVE.md")
        except FileNotFoundError:
            return format_tool_response(False, "Could not find project root", valid=False, errors=["ACTIVE.md not found"], warnings=[], field_count=0, staleness_hours=0.0)

    res = parse_yaml_frontmatter(active_path)
    if not res["success"]:
        return format_tool_response(False, f"Failed to parse ACTIVE.md: {', '.join(res['errors'])}", valid=False, errors=res["errors"], warnings=[], field_count=0, staleness_hours=0.0)

    frontmatter = res["frontmatter"]
    errors = []
    warnings = []
    field_count = len(frontmatter)

    # Field count enforcement (Protocol spec: Max 15)
    if field_count > 15:
        errors.append(f"Field count exceeds protocol limit (15): {field_count}")
    elif field_count > 13:
        warnings.append(f"Field count approaching protocol limit (15): {field_count}")

    # Schema validation
    try:
        ActiveMdSchema(**frontmatter)
    except Exception as e:
        errors.append(f"Schema validation error: {str(e)}")

    # Staleness detection
    staleness_hours = 0.0
    try:
        # Check both architect and worker updates
        ts_arch = frontmatter.get("last_architect_update")
        ts_work = frontmatter.get("last_worker_update")
        
        now = datetime.now().astimezone()
        
        updates = []
        for ts in [ts_arch, ts_work]:
            if ts:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    # Fallback for naive timestamps in tests/manual edits
                    dt = dt.astimezone()
                updates.append(dt)
        
        if updates:
            latest_update = max(updates)
            diff = now - latest_update
            staleness_hours = diff.total_seconds() / 3600.0
            
            if staleness_hours > 24:
                warnings.append(f"ACTIVE.md is stale ({staleness_hours:.1f} hours since last update)")
    except Exception as e:
        warnings.append(f"Could not calculate staleness: {str(e)}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "field_count": field_count,
        "staleness_hours": round(staleness_hours, 2)
    }

def validate_plan_structure(plan_path: Optional[str] = None) -> Dict[str, Any]:
    """Validate PLAN.md has required sections and consistent structure.
    
    Args:
        plan_path: Path to PLAN.md. Defaults to project root PLAN.md.

    Returns:
        dict: Tool response with validation details.
    """
    if plan_path is None:
        try:
            root = resolve_project_root()
            plan_path = str(root / "PLAN.md")
        except FileNotFoundError:
            return format_tool_response(False, "Could not find project root", valid=False, errors=["PLAN.md not found"])

    # First, use plan_sync's validation logic
    res = plan_sync.validate_plan(plan_path)
    
    errors = res.get("errors", [])
    warnings = res.get("warnings", [])
    
    # Supplemental checks
    path = Path(plan_path)
    if not path.exists():
        return format_tool_response(False, "PLAN.md missing", valid=False, errors=["PLAN.md not found"])

    content = path.read_text(encoding='utf-8')
    
    # Check for Phase headers (at least one)
    if not re.search(r"^## Phase \d+:", content, re.MULTILINE):
        errors.append("Missing Phase headers (e.g., ## Phase 1: ...)")

    # Check for workstream format consistency
    if re.search(r"^### Workstream", content, re.MULTILINE) and not re.search(r"^### Workstream \d+\.\d+:", content, re.MULTILINE):
        warnings.append("Workstream headers may not follow standard N.N format")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def validate_spec(spec_path: str) -> Dict[str, Any]:
    """Validate a spec file has required structure.
    
    Args:
        spec_path: Path to the spec file.

    Returns:
        dict: Tool response with validation details.
    """
    path = Path(spec_path)
    if not path.exists():
        return format_tool_response(False, f"Spec file not found: {spec_path}", valid=False, errors=["File missing"])

    content = path.read_text(encoding='utf-8')
    errors = []
    warnings = []

    # Check for Title (# heading)
    if not re.search(r"^# .+$", content, re.MULTILINE):
        errors.append("Spec missing primary title (# Title)")

    # Check for version info
    if "Version:" not in content:
        warnings.append("Spec missing 'Version:' metadata")

    # Check for non-empty body
    if len(content.strip()) < 50:
        errors.append("Spec content suspiciously short (low detail)")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def validate_project(project_root: Optional[str] = None) -> Dict[str, Any]:
    """Run all validations across the project.
    
    Args:
        project_root: Root directory. Defaults to detected root.

    Returns:
        dict: Aggregated results.
    """
    try:
        root = resolve_project_root(project_root)
    except FileNotFoundError:
        return format_tool_response(False, "Could not resolve project root", overall_valid=False)

    results = {}
    
    # 1. ACTIVE.md
    active_path = root / ".context" / "ACTIVE.md"
    results["active_md"] = validate_active_md(str(active_path))

    # 2. PLAN.md
    plan_path = root / "PLAN.md"
    results["plan_md"] = validate_plan_structure(str(plan_path))

    # 3. Specs
    specs_dir = root / "specs"
    spec_results = []
    if specs_dir.exists():
        for spec_file in specs_dir.glob("*.md"):
            spec_results.append({
                "file": spec_file.name,
                "result": validate_spec(str(spec_file))
            })
    results["specs"] = spec_results

    # 4. Sync Check (cross-validation)
    sync_res = plan_sync.sync_check(str(plan_path), str(active_path))
    results["sync_check"] = sync_res

    overall_valid = results["active_md"]["valid"] and results["plan_md"]["valid"]
    if all(s["result"]["valid"] for s in spec_results) is False:
        overall_valid = False
    if not sync_res["in_sync"]:
        overall_valid = False

    summary = f"Project Validation: {'PASSED' if overall_valid else 'FAILED'}\n"
    summary += f"- ACTIVE.md: {'Valid' if results['active_md']['valid'] else 'Invalid'}\n"
    summary += f"- PLAN.md: {'Valid' if results['plan_md']['valid'] else 'Invalid'}\n"
    summary += f"- Specs: {len([s for s in spec_results if s['result']['valid']])}/{len(spec_results)} Valid\n"
    summary += f"- Sync: {'In Sync' if sync_res['in_sync'] else 'OUT OF SYNC'}"

    return {
        "overall_valid": overall_valid,
        "results": results,
        "summary": summary
    }

if __name__ == "__main__":
    # If run as script, validate everything
    final_res = validate_project()
    print(final_res["summary"])
    if not final_res["overall_valid"]:
        # Print detailed errors
        for key, res in final_res["results"].items():
            if isinstance(res, dict) and not res.get("valid", res.get("in_sync", True)):
                print(f"\n[{key}] Errors: {res.get('errors', res.get('discrepancies', []))}")
        sys.exit(1)
    sys.exit(0)
