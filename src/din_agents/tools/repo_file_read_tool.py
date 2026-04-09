"""Scoped file read: one CrewAI tool instance per repo (din_core, react_din, din_studio)."""

from __future__ import annotations

from pathlib import Path
from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from din_agents.shared.repo_paths import resolved_path_under_repo
from din_agents.shared.repo_profiles import get_repo_profile
from din_agents.shared.runtime_prefs import max_repo_read_tool_chars

_MAX_READ_BYTES = 200_000


class RepoFileReadInput(BaseModel):
    """Arguments for reading from a single DIN checkout."""

    relative_path: str = Field(
        ...,
        description=(
            "File or directory path relative to the repository root "
            "(POSIX slashes, e.g. README.md or crates/foo/src/lib.rs). "
            "No '..'. Pass a directory path to list its contents."
        ),
    )


class RepoFileReadTool(BaseTool):
    """Reads are limited to ``get_repo_profile(allowed_repo_id).path``."""

    name: str = Field(description="Tool id exposed to the LLM (e.g. read_din_core_repo_file).")
    description: str = Field(description="When and how to use this reader.")
    allowed_repo_id: str = Field(
        description="din_core, react_din, or din_studio — set at construction, not by the model.",
    )
    args_schema: Type[BaseModel] = Field(default=RepoFileReadInput)

    def _run(self, relative_path: str) -> str:
        root = Path(get_repo_profile(self.allowed_repo_id).path).expanduser().resolve()
        try:
            target = resolved_path_under_repo(str(root), relative_path)
        except ValueError as exc:
            return f"Invalid path: {exc}"

        if target.is_dir():
            return self._list_directory(target, root)
        if not target.is_file():
            return f"Not found: {relative_path}"

        try:
            raw = target.read_bytes()
        except OSError as exc:
            return f"Read failed: {exc}"

        if len(raw) > _MAX_READ_BYTES:
            return (
                f"File too large ({len(raw)} bytes, limit {_MAX_READ_BYTES}). "
                "Try a more specific path or read a sub-module."
            )

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return f"Binary file ({len(raw)} bytes) — cannot display."

        limit = max_repo_read_tool_chars()
        if len(text) > limit:
            full = len(text)
            text = text[:limit].rstrip()
            text += (
                "\n\n---\n"
                f"[truncated: {full} UTF-8 chars in file; showing first {limit}. "
                "Open a smaller path (module / tests) or raise "
                "`DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS`.]\n"
            )
        return text

    def _list_directory(self, target: Path, root: Path) -> str:
        try:
            entries = sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError as exc:
            return f"List failed: {exc}"

        lines: list[str] = [f"Directory: {target.relative_to(root)}/\n"]
        for entry in entries[:200]:
            prefix = "d " if entry.is_dir() else "  "
            lines.append(f"{prefix}{entry.name}")
        if len(entries) > 200:
            lines.append(f"  ... and {len(entries) - 200} more entries")
        return "\n".join(lines)


def make_repo_file_read_tool(allowed_repo_id: str) -> RepoFileReadTool:
    """Build a reader bound to one DIN sibling repo."""
    profile = get_repo_profile(allowed_repo_id)
    safe_id = allowed_repo_id.strip().replace(" ", "_")
    return RepoFileReadTool(
        name=f"read_{safe_id}_repo_file",
        description=(
            f"Read ONE file or list a directory in the {profile.display_name} repository "
            f"(root: `{profile.path}`). Pass a relative_path from the repo root. "
            "Use to inspect existing code, docs, configs, or directory layout before "
            "making changes. For directories, returns a listing of entries."
        ),
        allowed_repo_id=allowed_repo_id,
    )
