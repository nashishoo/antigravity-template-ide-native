import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional


def list_local_skills(skills_root: Optional[str] = None) -> Dict[str, List[str]]:
    """
    List local SKILL.md files under the skills directory.

    Args:
        skills_root: Optional path to the skills root directory. Defaults to
            the project's src/skills directory.

    Returns:
        Dictionary with the skill root path and discovered skill entries.
    """
    root = Path(skills_root) if skills_root else Path(__file__).resolve().parents[1] / "skills"
    entries: List[str] = []

    if not root.exists():
        return {"root": str(root), "skills": entries}

    for skill_doc in root.rglob("SKILL.md"):
        if "__pycache__" in skill_doc.parts:
            continue
        relative_path = skill_doc.parent.relative_to(root)
        entries.append(str(relative_path).replace("\\", "/"))

    entries.sort()
    return {"root": str(root), "skills": entries}


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


def search_skills_catalog(query: str, limit: int = 5) -> Dict[str, object]:
    """
    Search skills.sh catalog by keyword (best-effort HTML parsing).

    Args:
        query: Search terms to look up.
        limit: Maximum number of results to return.

    Returns:
        Dictionary with the query, results, and any warnings.
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
            }
        )
        if len(results) >= limit:
            break

    return {
        "query": query,
        "results": results,
        "warning": "" if results else "No results parsed. Try another query or use npx skills find.",
    }
