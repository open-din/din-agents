"""Scoped file write: one CrewAI tool instance per repo (din_core, react_din, din_studio)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from din_agents.shared.repo_paths import resolved_path_under_repo
from din_agents.shared.repo_profiles import get_repo_profile

_MAX_BYTES = 750_000


class RepoFileWriteInput(BaseModel):
    """Arguments for writing into a single DIN checkout."""

    relative_path: str = Field(
        ...,
        description=(
            "File path relative to that repository's root "
            "(POSIX slashes, e.g. README.md or crates/foo/src/lib.rs). No '..'."
        ),
    )
    content: str = Field(..., description="Full UTF-8 text to write; replaces an existing file.")


class RepoFileWriteTool(BaseTool):
    """Writes are limited to ``get_repo_profile(allowed_repo_id).path``."""

    name: str = Field(description="Tool id exposed to the LLM (e.g. write_din_core_repo_file).")
    description: str = Field(description="When and how to use this writer.")
    allowed_repo_id: str = Field(
        description="din_core, react_din, or din_studio — set at construction, not by the model.",
    )
    args_schema: Type[BaseModel] = Field(default=RepoFileWriteInput)

    def _run(self, relative_path: str, content: str) -> str:
        flag = os.environ.get("DIN_AGENTS_REPO_WRITE", "1").lower()
        if flag in ("0", "false", "no"):
            return (
                "Repo writes are disabled (set DIN_AGENTS_REPO_WRITE=1 or unset) — "
                "no file was written."
            )
        raw = content.encode("utf-8")
        if len(raw) > _MAX_BYTES:
            return f"Refused: content larger than {_MAX_BYTES} bytes."

        root = Path(get_repo_profile(self.allowed_repo_id).path).expanduser().resolve()
        try:
            target = resolved_path_under_repo(str(root), relative_path)
        except ValueError as exc:
            return f"Invalid path: {exc}"

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        except OSError as exc:
            return f"Write failed: {exc}"

        return f"Wrote {len(raw)} bytes to {target}"


def make_repo_file_write_tool(allowed_repo_id: str) -> RepoFileWriteTool:
    """Build a writer bound to one DIN sibling repo."""
    profile = get_repo_profile(allowed_repo_id)
    safe_id = allowed_repo_id.strip().replace(" ", "_")
    return RepoFileWriteTool(
        name=f"write_{safe_id}_repo_file",
        description=(
            f"Write or overwrite ONE file in the {profile.display_name} repository "
            f"(root: `{profile.path}`). Use relative_path from that root; parent dirs are created. "
            "Do not pass absolute paths. Use when the user asked for concrete edits in this repo."
        ),
        allowed_repo_id=allowed_repo_id,
    )
