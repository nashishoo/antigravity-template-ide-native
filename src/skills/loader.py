import importlib.util
import inspect
import re
from pathlib import Path
from typing import Dict, Callable, Any, List


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
    Scans src/skills/ directory for skill packages.

    For each subfolder in src/skills/:
    1. Looks for tools.py: Registers public functions as tools.
    2. Looks for SKILL.md: Reads documentation content.

    Args:
        agent_tools: The dictionary of tools to update with new skill-based tools.

    Returns:
        A combined string of all SKILL.md contents to be injected into context.
    """
    skills_dir = Path(__file__).parent
    skill_docs: List[str] = []

    if not skills_dir.exists():
        print(f"s? Skills directory not found: {skills_dir}")
        return ""

    print(f"Scanning for skills in {skills_dir}...")

    # Iterate over directories containing SKILL.md (including nested locations)
    for skill_path in _iter_skill_dirs(skills_dir):
        skill_name = str(skill_path.relative_to(skills_dir)).replace("\\", "/")
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
                    print(f"     o Loaded {count} tools from tools.py")
            except Exception as e:
                print(f"     ? Failed to load tools: {e}")

        # 2. Load Documentation (SKILL.md)
        doc_file = skill_path / "SKILL.md"
        if doc_file.exists():
            try:
                content = doc_file.read_text(encoding="utf-8").strip()
                if content:
                    skill_docs.append(f"\n--- SKILL: {skill_name} ---\n{content}")
                    print(f"     o Loaded documentation from SKILL.md")
            except Exception as e:
                print(f"     ? Failed to load docs: {e}")

    return "\n".join(skill_docs)
