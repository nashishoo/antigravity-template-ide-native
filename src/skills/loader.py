import importlib.util
import inspect
import json
import re
from pathlib import Path
from typing import Dict, Callable, Any, List, Optional


def _load_registry_dirs(project_root: Path) -> List[Path]:
    """Load additional skill directories from .agent/skills.json."""
    registry_path = project_root / ".agent" / "skills.json"
    dirs: List[Path] = []

    if not registry_path.exists():
        return dirs

    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        for path_str in data.get("skills_dirs", []):
            path = Path(path_str)
            if not path.is_absolute():
                path = (project_root / path).resolve()
            if path.exists() and path.is_dir():
                dirs.append(path)
            else:
                print(f"?? Detailed Warning: Registry skill directory not found: {path}")
    except Exception as e:
        print(f"?? Failed to load skills registry: {e}")

    return dirs


def _iter_skill_dirs(skills_dir: Path) -> List[Path]:
    """Return directories that contain a SKILL.md file.

    Args:
        skills_dir: Root directory for skills.

    Returns:
        Sorted list of skill directories.
    """
    skill_dirs: List[Path] = []
    for skill_doc in skills_dir.rglob("SKILL.md"):
        if "__pycache__" in skill_doc.parts:
            continue
        skill_dirs.append(skill_doc.parent)

    unique_dirs: List[Path] = []
    seen: set[Path] = set()
    for path in skill_dirs:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique_dirs.append(path)

    return sorted(unique_dirs, key=lambda p: str(p))


def _module_name_for_skill(skill_path: Path) -> str:
    """Create a safe module name for dynamic imports.

    Args:
        skill_path: Path to the skill directory.

    Returns:
        Sanitized module name string.
    """
    safe = re.sub(r"[^0-9a-zA-Z_]", "_", "_".join(skill_path.parts))
    return f"src.skills.dynamic_{safe}"


def load_skills(agent_tools: Dict[str, Callable[..., Any]]) -> str:
    """
    Scans src/skills/ and registered local directories for skill packages.

    For each subfolder:
    1. Looks for tools.py: Registers public functions as tools.
    2. Looks for SKILL.md: Reads documentation content.

    Args:
        agent_tools: The dictionary of tools to update with new skill-based tools.

    Returns:
        A combined string of all SKILL.md contents to be injected into context.
    """
    # 1. Identify all root directories to scan
    project_root = Path(__file__).resolve().parents[2]
    default_skills_dir = Path(__file__).parent
    
    skill_roots = [default_skills_dir] + _load_registry_dirs(project_root)
    skill_docs: List[str] = []

    print(f"-> Scanning {len(skill_roots)} skill sources...")

    for root in skill_roots:
        if not root.exists():
            continue

        print(f"  > Scanning root: {root}")
        
        # Iterate over directories containing SKILL.md
        for skill_path in _iter_skill_dirs(root):
            # Calculate a relative name for display/ID purposes
            try:
                skill_name = str(skill_path.relative_to(root)).replace("\\", "/")
            except ValueError:
                skill_name = skill_path.name

            print(f"   - Found skill: {skill_name}")

            # 1. Load Tools (tools.py)
            tools_file = skill_path / "tools.py"
            if tools_file.exists():
                try:
                    module_name = _module_name_for_skill(skill_path)
                    spec = importlib.util.spec_from_file_location(
                        f"{module_name}.tools", tools_file
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        count = 0
                        for name, obj in inspect.getmembers(module, inspect.isfunction):
                            if not name.startswith("_") and obj.__module__ == module.__name__:
                                agent_tools[name] = obj
                                count += 1
                        print(f"     * Loaded {count} tools from tools.py")
                except Exception as e:
                    print(f"     ! Failed to load tools: {e}")

            # 2. Load Documentation (SKILL.md)
            doc_file = skill_path / "SKILL.md"
            if doc_file.exists():
                try:
                    content = doc_file.read_text(encoding="utf-8").strip()
                    if content:
                        skill_docs.append(f"\n--- SKILL: {skill_name} ({root.name}) ---\n{content}")
                        print(f"     * Loaded documentation from SKILL.md")
                except Exception as e:
                    print(f"     ! Failed to load docs: {e}")

    return "\n".join(skill_docs)
