import json
import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional


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
    except Exception:
        pass  # Fail silently in tool

    return dirs


def list_local_skills(skills_root: Optional[str] = None) -> Dict[str, List[str]]:
    """
    List local SKILL.md files under the skills directory and registered paths.

    Args:
        skills_root: Optional override for the default skills root.

    Returns:
        Dictionary with discovered skill entries from all sources.
    """
    project_root = Path(__file__).resolve().parents[2]
    default_root = Path(__file__).resolve().parents[1] / "skills"
    
    roots = [Path(skills_root)] if skills_root else [default_root]
    if not skills_root:
        roots.extend(_load_registry_dirs(project_root))

    entries: List[str] = []

    for root in roots:
        if not root.exists():
            continue

        for skill_doc in root.rglob("SKILL.md"):
            if "__pycache__" in skill_doc.parts:
                continue
            try:
                # If inside default root, keep relative path clean
                if default_root in skill_doc.parents:
                    relative = skill_doc.parent.relative_to(default_root)
                    entries.append(str(relative).replace("\\", "/"))
                else:
                    # For external roots, include the root name to avoid collisions
                    # or just use the folder name if it's unique enough?
                    # Let's use the full relative path from the root
                    relative = skill_doc.parent.relative_to(root)
                    # Prefix with root name to distinguish
                    entries.append(f"{root.name}/{str(relative).replace('\\', '/')}")
            except ValueError:
                entries.append(skill_doc.parent.name)

    entries.sort()
    return {"root": "multiple", "skills": entries}


def check_npx_skills_available() -> Dict[str, Optional[str]]:
    """
    Check whether Node.js and npx are available for Skills CLI usage.

    Returns:
        Dictionary describing availability and any missing dependency.
    """
    node_path = shutil.which("node")
    npx_path = shutil.which("npx")

    return {
        "node": node_path,
        "npx": npx_path,
        "available": bool(node_path and npx_path),
        "note": None if node_path and npx_path else "Node.js and npx are required for skills CLI",
    }



def search_awesome_skills(query: str, limit: int = 5) -> List[Dict[str, str]]:
    """
    Search awesome-agent-skills README for skills.
    """
    url = "https://raw.githubusercontent.com/heilcheng/awesome-agent-skills/main/README.md"
    results: List[Dict[str, str]] = []

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read().decode("utf-8")
    except Exception as e:
        # print(f"?? Failed to fetch awesome-agent-skills: {e}")
        return []

    # Regex to find markdown table rows: | [Name](link) | Description |
    # Matches: | [Title](URL) | Description |
    pattern = re.compile(r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\s*\|")
    
    query_lower = query.lower()
    
    for match in pattern.finditer(content):
        name, link, desc = match.groups()
        full_text = f"{name} {desc}".lower()
        
        if query_lower in full_text:
            results.append({
                "skill": name.strip(),
                "repo": "awesome-list",
                "url": link.strip(),
                "description": desc.strip(),
                "install": f"npx skills add {link.strip()}" if "github.com" in link else "Manual install required"
            })
            if len(results) >= limit:
                break
                
    return results


def search_skills_catalog(query: str, limit: int = 5) -> Dict[str, object]:
    """
    Search skills.sh catalog and awesome-agent-skills by keyword.

    Args:
        query: Search terms to look up.
        limit: Maximum number of results to return per source.

    Returns:
        Dictionary with the query, combined results, and any warnings.
    """
    if not query.strip():
        return {"query": query, "results": [], "warning": "Empty query"}

    encoded_query = urllib.parse.quote(query.strip())
    url = f"https://skills.sh/?q={encoded_query}"

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            html = response.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        return {
            "query": query,
            "results": [],
            "warning": f"Failed to fetch skills.sh: {exc}",
        }

    # Extract candidate URLs like https://skills.sh/owner/repo/skill-name
    pattern = re.compile(r"https://skills\.sh/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
    matches = pattern.findall(html)
    results: List[Dict[str, str]] = []
    seen: set[str] = set()

    for match in matches:
        if match in seen:
            continue
        seen.add(match)
        parts = match.split("/")
        if len(parts) >= 3:
            owner_repo = "/".join(parts[:2])
            skill_name = parts[2]
        else:
            owner_repo = match
            skill_name = ""

        results.append(
            {
                "skill": skill_name,
                "repo": owner_repo,
                "url": f"https://skills.sh/{match}",
                "install": f"npx skills add {owner_repo}@{skill_name}" if skill_name else "",
                "description": "From skills.sh catalog"
            }
        )
        if len(results) >= limit:
            break
            
    # Combine with awesome-skills results
    awesome_results = search_awesome_skills(query, limit)
    results.extend(awesome_results)

    return {
        "query": query,
        "results": results,
        "warning": "" if results else "No results parsed. Try another query or use npx skills find.",
    }
