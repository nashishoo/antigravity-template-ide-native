"""Plan Synchronization Tool

This module provides functions to parse, validate, and sync PLAN.md with ACTIVE.md.
It enables workers to extract their workstream context and the Architect to maintain
consistency between strategic planning (PLAN.md) and tactical state (ACTIVE.md).

Author: Worker (Claude Sonnet 4.5 Thinking — Workstream 1.2)
Version: 1.0
"""

import re
from pathlib import Path
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field


# ============================================================================
# Pydantic Models
# ============================================================================

class WorkstreamMetadata(BaseModel):
    """Metadata for a single workstream.
    
    Attributes:
        workstream_id: Unique ID (e.g., "1.2")
        title: Human-readable title
        worker_role: Role description (e.g., "Workflow Engineer")
        model: AI model name (e.g., "Claude Sonnet 4.5 (Thinking)")
        deliverables: List of files/artifacts to create
        dependencies: List of workstream IDs this depends on
        blocks: List of workstream IDs this blocks
        status: Current status (PLANNED, IN_PROGRESS, etc.)
    """
    workstream_id: str
    title: str
    worker_role: Optional[str] = None
    model: Optional[str] = None
    deliverables: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    blocks: List[str] = Field(default_factory=list)
    status: Literal["PLANNED", "IN_PROGRESS", "BLOCKED", "COMPLETED", "CANCELLED"] = "PLANNED"


class PhaseMetadata(BaseModel):
    """Metadata for a single phase.
    
    Attributes:
        phase_id: Phase number (1, 2, 3, ...)
        title: Human-readable title
        duration: Estimated duration (e.g., "~5 hours")
        goal: Phase objective
        workstreams: List of workstreams in this phase
    """
    phase_id: int
    title: str
    duration: Optional[str] = None
    goal: Optional[str] = None
    workstreams: List[WorkstreamMetadata] = Field(default_factory=list)


class PlanMetadata(BaseModel):
    """Parsed PLAN.md metadata.
    
    Attributes:
        architect: Name/model of Architect
        start_date: Project start date
        target_completion: Target completion date
        status: Current project status
        phases: List of all phases
    """
    architect: Optional[str] = None
    start_date: Optional[str] = None
    target_completion: Optional[str] = None
    status: Optional[str] = None
    phases: List[PhaseMetadata] = Field(default_factory=list)
    
    def get_workstream(self, workstream_id: str) -> Optional[WorkstreamMetadata]:
        """Find workstream by ID across all phases.
        
        Args:
            workstream_id: Workstream ID to find
            
        Returns:
            WorkstreamMetadata if found, None otherwise
        """
        for phase in self.phases:
            for ws in phase.workstreams:
                if ws.workstream_id == workstream_id:
                    return ws
        return None
    
    def get_phase(self, phase_id: int) -> Optional[PhaseMetadata]:
        """Find phase by ID.
        
        Args:
            phase_id: Phase ID to find
            
        Returns:
            PhaseMetadata if found, None otherwise
        """
        for phase in self.phases:
            if phase.phase_id == phase_id:
                return phase
        return None


# ============================================================================
# Regex Patterns
# ============================================================================

PHASE_PATTERN = re.compile(r"^## Phase (\d+): (.+)$", re.MULTILINE)
WORKSTREAM_PATTERN = re.compile(r"^### Workstream ([\d\.]+): (.+)$", re.MULTILINE)
METADATA_PATTERN = re.compile(r"^\s*-\s+\*\*([^:]+):\*\*\s*(.*)$", re.MULTILINE)
LIST_ITEM_PATTERN = re.compile(r"^\s+-\s+(.+)$")
HEADER_METADATA_PATTERN = re.compile(r"^\*\*([^:]+):\*\*\s+(.+)$", re.MULTILINE)


# ============================================================================
# Core Functions
# ============================================================================

def parse_plan(plan_path: str = "PLAN.md") -> dict:
    """Parse PLAN.md into structured data.
    
    Args:
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "success": bool,
            "metadata": PlanMetadata | None,
            "errors": List[str],
            "raw_content": str
        }
    """
    path = Path(plan_path)
    
    # Handle missing file
    if not path.exists():
        return {
            "success": False,
            "metadata": None,
            "errors": [f"File not found: {plan_path}"],
            "raw_content": ""
        }
    
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "success": False,
            "metadata": None,
            "errors": [f"Error reading file: {str(e)}"],
            "raw_content": ""
        }
    
    errors = []
    
    # Parse header metadata
    header_metadata = {}
    for match in HEADER_METADATA_PATTERN.finditer(content):
        field_name = match.group(1).strip()
        value = match.group(2).strip()
        header_metadata[field_name.lower().replace(' ', '_')] = value
    
    # Parse phases
    phases = []
    phase_matches = list(PHASE_PATTERN.finditer(content))
    
    for i, phase_match in enumerate(phase_matches):
        phase_id = int(phase_match.group(1))
        phase_title = phase_match.group(2).strip()
        
        # Determine phase section boundaries
        phase_start = phase_match.end()
        phase_end = phase_matches[i + 1].start() if i + 1 < len(phase_matches) else len(content)
        phase_content = content[phase_start:phase_end]
        
        # Extract phase metadata
        phase_meta = {"phase_id": phase_id, "title": phase_title}
        
        # Look for Duration and Goal
        duration_match = re.search(r"^\*\*Duration:\*\*\s+(.+)$", phase_content, re.MULTILINE)
        if duration_match:
            phase_meta["duration"] = duration_match.group(1).strip()
        
        goal_match = re.search(r"^\*\*Goal:\*\*\s+(.+)$", phase_content, re.MULTILINE)
        if goal_match:
            phase_meta["goal"] = goal_match.group(1).strip()
        
        # Parse workstreams in this phase
        workstreams = []
        workstream_matches = list(WORKSTREAM_PATTERN.finditer(phase_content))
        
        for j, ws_match in enumerate(workstream_matches):
            ws_id = ws_match.group(1).strip()
            ws_title = ws_match.group(2).strip()
            
            # Determine workstream section boundaries
            ws_start = ws_match.end()
            ws_end = workstream_matches[j + 1].start() if j + 1 < len(workstream_matches) else len(phase_content)
            ws_content = phase_content[ws_start:ws_end]
            
            # Parse workstream metadata
            ws_metadata = {
                "workstream_id": ws_id,
                "title": ws_title,
                "deliverables": [],
                "dependencies": [],
                "blocks": []
            }
            
            # Extract fields
            lines = ws_content.split('\n')
            current_field = None
            
            for line in lines:
                # Check for metadata fields
                metadata_match = METADATA_PATTERN.match(line)
                if metadata_match:
                    field_name = metadata_match.group(1).strip()
                    value = metadata_match.group(2).strip()
                    
                    if field_name == "Worker Role":
                        ws_metadata["worker_role"] = value
                        current_field = None
                    elif field_name == "Model":
                        ws_metadata["model"] = value
                        current_field = None
                    elif field_name == "Deliverables":
                        current_field = "deliverables"
                        # Check if value is on same line (not common, but possible)
                        if value and value != "":
                            ws_metadata["deliverables"].append(value)
                    elif field_name == "Dependencies":
                        current_field = "dependencies"
                        # Parse dependencies
                        if value.lower() != "none":
                            # Extract workstream IDs
                            dep_ids = re.findall(r"Workstream\s+([\d\.]+)", value)
                            ws_metadata["dependencies"].extend(dep_ids)
                    elif field_name == "Blocks":
                        current_field = "blocks"
                        # Parse blocks
                        if value.lower() != "none":
                            # Extract workstream IDs
                            block_ids = re.findall(r"Workstream\s+([\d\.]+)", value)
                            ws_metadata["blocks"].extend(block_ids)
                    else:
                        current_field = None
                # Check for list items (deliverables under Deliverables field)
                elif current_field == "deliverables":
                    list_match = LIST_ITEM_PATTERN.match(line)
                    if list_match:
                        item_text = list_match.group(1).strip()
                        ws_metadata["deliverables"].append(item_text)
                    elif line.strip() == "":
                        # Empty line might end the deliverables section
                        continue
                    elif not line.startswith(' ') and line.strip():
                        # Non-indented non-empty line ends deliverables section
                        current_field = None
            
            # Determine status from context (simple heuristic)
            ws_metadata["status"] = "PLANNED"  # Default
            
            try:
                workstream = WorkstreamMetadata(**ws_metadata)
                workstreams.append(workstream)
            except Exception as e:
                errors.append(f"Error parsing workstream {ws_id}: {str(e)}")
        
        phase_meta["workstreams"] = workstreams
        
        try:
            phase = PhaseMetadata(**phase_meta)
            phases.append(phase)
        except Exception as e:
            errors.append(f"Error parsing phase {phase_id}: {str(e)}")
    
    # Build PlanMetadata
    plan_data = {
        "architect": header_metadata.get("architect"),
        "start_date": header_metadata.get("start_date"),
        "target_completion": header_metadata.get("target_completion"),
        "status": header_metadata.get("status"),
        "phases": phases
    }
    
    try:
        metadata = PlanMetadata(**plan_data)
        return {
            "success": True,
            "metadata": metadata,
            "errors": errors,
            "raw_content": content
        }
    except Exception as e:
        return {
            "success": False,
            "metadata": None,
            "errors": [f"Error creating PlanMetadata: {str(e)}"] + errors,
            "raw_content": content
        }


def validate_plan(plan_path: str = "PLAN.md") -> dict:
    """Check PLAN.md for consistency.
    
    Args:
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str]
        }
    """
    result = parse_plan(plan_path)
    
    if not result["success"]:
        return {
            "valid": False,
            "errors": result["errors"],
            "warnings": []
        }
    
    metadata = result["metadata"]
    errors = []
    warnings = []
    
    # Collect all workstream IDs
    all_workstream_ids = set()
    for phase in metadata.phases:
        for ws in phase.workstreams:
            all_workstream_ids.add(ws.workstream_id)
    
    # Check for orphan dependencies
    for phase in metadata.phases:
        for ws in phase.workstreams:
            for dep_id in ws.dependencies:
                if dep_id not in all_workstream_ids:
                    errors.append(
                        f"Workstream {ws.workstream_id} depends on non-existent Workstream {dep_id}"
                    )
            
            for block_id in ws.blocks:
                if block_id not in all_workstream_ids:
                    warnings.append(
                        f"Workstream {ws.workstream_id} claims to block non-existent Workstream {block_id}"
                    )
    
    # Check for circular dependencies (simple check)
    def has_circular_dependency(ws_id: str, visited: set, path: List[str]) -> Optional[List[str]]:
        if ws_id in path:
            return path + [ws_id]
        
        ws = metadata.get_workstream(ws_id)
        if not ws:
            return None
        
        for dep_id in ws.dependencies:
            result = has_circular_dependency(dep_id, visited, path + [ws_id])
            if result:
                return result
        
        return None
    
    for phase in metadata.phases:
        for ws in phase.workstreams:
            circular = has_circular_dependency(ws.workstream_id, set(), [])
            if circular:
                errors.append(
                    f"Circular dependency detected: {' → '.join(circular)}"
                )
    
    # Check for missing deliverables
    for phase in metadata.phases:
        for ws in phase.workstreams:
            if not ws.deliverables:
                warnings.append(f"Workstream {ws.workstream_id} has no deliverables")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def generate_worker_context(workstream_id: str, plan_path: str = "PLAN.md") -> dict:
    """Extract context for a specific workstream.
    
    Args:
        workstream_id: Workstream ID (e.g., "1.2")
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "success": bool,
            "workstream": WorkstreamMetadata | None,
            "phase_context": PhaseMetadata | None,
            "dependency_details": List[WorkstreamMetadata],
            "blocks_details": List[WorkstreamMetadata],
            "errors": List[str]
        }
    """
    result = parse_plan(plan_path)
    
    if not result["success"]:
        return {
            "success": False,
            "workstream": None,
            "phase_context": None,
            "dependency_details": [],
            "blocks_details": [],
            "errors": result["errors"]
        }
    
    metadata = result["metadata"]
    workstream = metadata.get_workstream(workstream_id)
    
    if not workstream:
        return {
            "success": False,
            "workstream": None,
            "phase_context": None,
            "dependency_details": [],
            "blocks_details": [],
            "errors": [f"Workstream {workstream_id} not found in PLAN.md"]
        }
    
    # Find parent phase
    phase_context = None
    for phase in metadata.phases:
        if workstream in phase.workstreams:
            phase_context = phase
            break
    
    # Get dependency details
    dependency_details = []
    for dep_id in workstream.dependencies:
        dep_ws = metadata.get_workstream(dep_id)
        if dep_ws:
            dependency_details.append(dep_ws)
    
    # Get blocks details
    blocks_details = []
    for block_id in workstream.blocks:
        block_ws = metadata.get_workstream(block_id)
        if block_ws:
            blocks_details.append(block_ws)
    
    return {
        "success": True,
        "workstream": workstream,
        "phase_context": phase_context,
        "dependency_details": dependency_details,
        "blocks_details": blocks_details,
        "errors": []
    }


def update_workstream_status(
    workstream_id: str, 
    new_status: Literal["PLANNED", "IN_PROGRESS", "BLOCKED", "COMPLETED", "CANCELLED"],
    plan_path: str = "PLAN.md"
) -> dict:
    """Update workstream status in PLAN.md.
    
    Args:
        workstream_id: Workstream ID (e.g., "1.2")
        new_status: New status value
        plan_path: Path to PLAN.md file
        
    Returns:
        dict: {
            "success": bool,
            "old_status": str,
            "new_status": str,
            "updated_lines": int,
            "errors": List[str]
        }
    """
    # Parse to verify workstream exists
    result = parse_plan(plan_path)
    
    if not result["success"]:
        return {
            "success": False,
            "old_status": None,
            "new_status": new_status,
            "updated_lines": 0,
            "errors": result["errors"]
        }
    
    metadata = result["metadata"]
    workstream = metadata.get_workstream(workstream_id)
    
    if not workstream:
        return {
            "success": False,
            "old_status": None,
            "new_status": new_status,
            "updated_lines": 0,
            "errors": [f"Workstream {workstream_id} not found in PLAN.md"]
        }
    
    old_status = workstream.status
    
    # Read file content
    path = Path(plan_path)
    try:
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
    except Exception as e:
        return {
            "success": False,
            "old_status": old_status,
            "new_status": new_status,
            "updated_lines": 0,
            "errors": [f"Error reading file: {str(e)}"]
        }
    
    # Find workstream header and update checklist markers if present
    updated_lines = 0
    status_marker_map = {
        "PLANNED": "[ ]",
        "IN_PROGRESS": "[/]",
        "BLOCKED": "[/]",  # Same as IN_PROGRESS, but add note
        "COMPLETED": "[x]",
        "CANCELLED": "[~]"  # Struck through marker
    }
    
    new_marker = status_marker_map.get(new_status, "[ ]")
    
    # Update lines with checklist markers for this workstream
    for i, line in enumerate(lines):
        # Look for lines with workstream ID and checklist markers
        if f"Workstream {workstream_id}" in line and re.search(r'\[.\]', line):
            # Replace checklist marker
            lines[i] = re.sub(r'\[.\]', new_marker, line)
            updated_lines += 1
    
    # Write back
    try:
        path.write_text('\n'.join(lines), encoding='utf-8')
        return {
            "success": True,
            "old_status": old_status,
            "new_status": new_status,
            "updated_lines": updated_lines,
            "errors": []
        }
    except Exception as e:
        return {
            "success": False,
            "old_status": old_status,
            "new_status": new_status,
            "updated_lines": 0,
            "errors": [f"Error writing file: {str(e)}"]
        }


def sync_check(plan_path: str = "PLAN.md", active_path: str = ".context/ACTIVE.md") -> dict:
    """Check consistency between PLAN.md and ACTIVE.md.
    
    Args:
        plan_path: Path to PLAN.md
        active_path: Path to ACTIVE.md
        
    Returns:
        dict: {
            "in_sync": bool,
            "discrepancies": List[dict],
            "warnings": List[str]
        }
    """
    # Parse PLAN.md
    plan_result = parse_plan(plan_path)
    if not plan_result["success"]:
        return {
            "in_sync": False,
            "discrepancies": [],
            "warnings": [f"Could not parse PLAN.md: {', '.join(plan_result['errors'])}"]
        }
    
    plan_metadata = plan_result["metadata"]
    
    # Parse ACTIVE.md (simple YAML frontmatter parsing)
    active_path_obj = Path(active_path)
    if not active_path_obj.exists():
        return {
            "in_sync": False,
            "discrepancies": [],
            "warnings": ["ACTIVE.md not found, cannot verify sync"]
        }
    
    try:
        active_content = active_path_obj.read_text(encoding='utf-8')
        # Extract YAML frontmatter
        yaml_match = re.search(r'^---\n(.*?)\n---', active_content, re.DOTALL)
        if not yaml_match:
            return {
                "in_sync": False,
                "discrepancies": [],
                "warnings": ["Could not parse ACTIVE.md YAML frontmatter"]
            }
        
        yaml_content = yaml_match.group(1)
        
        # Simple parsing of arrays (not full YAML parser)
        active_workstreams = []
        blocked_workstreams = []
        completed_workstreams = []
        
        # Extract arrays
        active_match = re.search(r'active_workstreams:\s*\n((?:  - .+\n)*)', yaml_content)
        if active_match:
            active_workstreams = re.findall(r'  - "?(.+?)"?\s*$', active_match.group(1), re.MULTILINE)
        
        blocked_match = re.search(r'blocked_workstreams:\s*\n((?:  - .+\n)*)', yaml_content)
        if blocked_match:
            blocked_workstreams = re.findall(r'  - "?(.+?)"?\s*$', blocked_match.group(1), re.MULTILINE)
        
        completed_match = re.search(r'completed_workstreams:\s*\n((?:  - .+\n)*)', yaml_content)
        if completed_match:
            completed_workstreams = re.findall(r'  - "?(.+?)"?\s*$', completed_match.group(1), re.MULTILINE)
        
    except Exception as e:
        return {
            "in_sync": False,
            "discrepancies": [],
            "warnings": [f"Error reading ACTIVE.md: {str(e)}"]
        }
    
    # Check consistency
    discrepancies = []
    
    for phase in plan_metadata.phases:
        for ws in phase.workstreams:
            ws_name = f"Workstream {ws.workstream_id}: {ws.title}"
            
            # Check if status matches ACTIVE.md placement
            if ws.status == "COMPLETED":
                # Should be in completed_workstreams
                found = any(ws.workstream_id in item or ws.title in item for item in completed_workstreams)
                if not found:
                    discrepancies.append({
                        "type": "workstream_mismatch",
                        "workstream_id": ws.workstream_id,
                        "plan_status": "COMPLETED",
                        "active_status": "not in completed_workstreams",
                        "recommendation": f"Add '{ws_name}' to completed_workstreams in ACTIVE.md"
                    })
            
            elif ws.status == "IN_PROGRESS":
                # Should be in active_workstreams
                found = any(ws.workstream_id in item or ws.title in item for item in active_workstreams)
                if not found:
                    discrepancies.append({
                        "type": "workstream_mismatch",
                        "workstream_id": ws.workstream_id,
                        "plan_status": "IN_PROGRESS",
                        "active_status": "not in active_workstreams",
                        "recommendation": f"Add '{ws_name}' to active_workstreams in ACTIVE.md"
                    })
            
            elif ws.status == "BLOCKED":
                # Should be in blocked_workstreams
                found = any(ws.workstream_id in item or ws.title in item for item in blocked_workstreams)
                if not found:
                    discrepancies.append({
                        "type": "workstream_mismatch",
                        "workstream_id": ws.workstream_id,
                        "plan_status": "BLOCKED",
                        "active_status": "not in blocked_workstreams",
                        "recommendation": f"Add '{ws_name}' to blocked_workstreams in ACTIVE.md"
                    })
    
    return {
        "in_sync": len(discrepancies) == 0,
        "discrepancies": discrepancies,
        "warnings": []
    }
