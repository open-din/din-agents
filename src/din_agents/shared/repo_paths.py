"""Safe path resolution for sibling-repo file tools."""

from __future__ import annotations

from pathlib import Path


def resolved_path_under_repo(repo_root: str, relative_path: str) -> Path:
    """Return an absolute path inside ``repo_root``, or raise ValueError."""
    root = Path(repo_root).expanduser().resolve()
    rel = (relative_path or "").strip().replace("\\", "/").lstrip("/")
    if not rel:
        raise ValueError("relative_path must be non-empty")
    if ".." in Path(rel).parts:
        raise ValueError("relative_path must not contain '..'")
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("path escapes repository root") from exc
    return target
