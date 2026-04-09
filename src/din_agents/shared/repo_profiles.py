"""Manifest-driven repo profiles for DIN workspace routing and tool constraints."""

from __future__ import annotations

import json
from functools import lru_cache
from os import getenv
from pathlib import Path

from pydantic import BaseModel, Field


_WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
_REPO_ENV_VARS = {
    "din_core": "DIN_CORE_PATH",
    "react_din": "REACT_DIN_PATH",
    "din_studio": "DIN_STUDIO_PATH",
    "din_agents": "DIN_AGENTS_PATH",
}
_FALLBACK_MANIFEST = {
    "version": 1,
    "repos": [
        {
            "id": "react_din",
            "display_name": "react-din",
            "path": "react-din",
            "role": "api",
            "tags": ["react", "public api", "components", "patch schema", "exports"],
            "depends_on": [],
            "used_by": ["din_core", "din_studio", "din_agents"],
            "entry_points": ["src/index.ts", "schemas/patch.schema.json", "project/COVERAGE_MANIFEST.json"],
            "owned_contracts": ["public api", "package exports", "patch schema"],
            "shared_contracts": ["patch schema", "serialization", "persisted node ids", "round-trip"],
            "hard_boundaries": [
                "Do not implement editor workflows here.",
                "Do not implement Rust runtime logic here.",
            ],
            "validation_commands": ["npm run lint", "npm run typecheck", "npm run ci:check"],
            "summary_path": "project/SUMMARY.md",
            "api_summary_path": "../docs/summaries/react-din-api.md",
            "repo_manifest_path": "project/REPO_MANIFEST.json",
            "skills_path": "project/skills",
        },
        {
            "id": "din_core",
            "display_name": "din-core",
            "path": "din-core",
            "role": "runtime",
            "tags": ["rust", "runtime", "compiler", "registry", "validation", "migration", "ffi", "wasm"],
            "depends_on": ["react_din"],
            "used_by": ["din_studio", "din_agents"],
            "entry_points": ["crates/din-patch", "crates/din-core", "schemas/patch.schema.json"],
            "owned_contracts": ["runtime semantics", "registry authority", "patch validation", "ffi", "wasm"],
            "shared_contracts": ["patch schema", "serialization", "persisted node ids", "round-trip", "registry"],
            "hard_boundaries": [
                "Do not fork the public schema away from react-din.",
                "Keep FFI and WASM wrappers thin.",
            ],
            "validation_commands": [
                "cargo fmt --all --check",
                "cargo clippy --workspace --all-targets -- -D warnings",
                "cargo test --workspace",
            ],
            "summary_path": "project/SUMMARY.md",
            "api_summary_path": "../docs/summaries/din-core-api.md",
            "repo_manifest_path": "project/REPO_MANIFEST.json",
            "skills_path": "project/skills",
        },
        {
            "id": "din_studio",
            "display_name": "din-studio",
            "path": "din-studio",
            "role": "ui",
            "tags": ["editor", "ui", "shell", "launcher", "mcp", "codegen", "surface manifest"],
            "depends_on": ["react_din", "din_core"],
            "used_by": ["din_agents"],
            "entry_points": [
                "ui/editor/nodeCatalog.ts",
                "targets/mcp",
                "project/COVERAGE_MANIFEST.json",
                "project/SURFACE_MANIFEST.json",
            ],
            "owned_contracts": ["editor workflows", "mcp target", "surface manifest", "code generation surface"],
            "shared_contracts": ["persisted node ids", "node catalog parity", "public patch surface"],
            "hard_boundaries": [
                "Do not own the public patch schema here.",
                "Do not own Rust runtime semantics here.",
            ],
            "validation_commands": ["npm run lint", "npm run typecheck", "npm run test", "npm run test:e2e"],
            "summary_path": "project/SUMMARY.md",
            "api_summary_path": "../docs/summaries/din-studio-api.md",
            "repo_manifest_path": "project/REPO_MANIFEST.json",
            "skills_path": "project/skills",
        },
        {
            "id": "din_agents",
            "display_name": "din-agents",
            "path": "din-agents",
            "role": "orchestration",
            "tags": ["automation", "routing", "quality gates", "crewai", "repo selection", "control plane"],
            "depends_on": ["din_core", "react_din", "din_studio"],
            "used_by": ["workspace operators"],
            "entry_points": [
                "src/din_agents/flow.py",
                "src/din_agents/shared/repo_profiles.py",
                "src/din_agents/shared/rules.py",
            ],
            "owned_contracts": ["repo routing", "quality gate selection", "control plane prompt inputs"],
            "shared_contracts": ["workspace routing metadata", "repo ownership map"],
            "hard_boundaries": [
                "Do not redefine sibling ownership in code without updating the workspace manifest.",
                "Do not own patch, runtime, or editor semantics.",
            ],
            "validation_commands": ["uv run pytest", "uv run ruff check src"],
            "summary_path": "project/SUMMARY.md",
            "api_summary_path": "../docs/summaries/din-agents-api.md",
            "repo_manifest_path": "project/REPO_MANIFEST.json",
            "skills_path": "project/skills",
        },
    ],
}


class QualityGate(BaseModel):
    """One shell command run as a pre-merge check for a repo."""

    name: str
    command: str
    notes: str = ""


class RepoProfile(BaseModel):
    """Compact manifest-backed profile used by routing, tools, and prompts."""

    repo_id: str
    display_name: str
    path: str
    role: str
    tags: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
    used_by: list[str] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)
    owned_contracts: list[str] = Field(default_factory=list)
    shared_contracts: list[str] = Field(default_factory=list)
    hard_boundaries: list[str] = Field(default_factory=list)
    quality_gates: list[QualityGate] = Field(default_factory=list)
    summary_path: str
    api_summary_path: str
    repo_manifest_path: str
    skills_path: str

    @property
    def context_files(self) -> list[str]:
        return [self.summary_path, self.api_summary_path, self.repo_manifest_path]


def _workspace_root() -> Path:
    env_root = getenv("DIN_WORKSPACE_ROOT")
    return Path(env_root).expanduser().resolve() if env_root else _WORKSPACE_ROOT


def _load_workspace_manifest() -> dict:
    manifest_path = _workspace_root() / "project" / "WORKSPACE_MANIFEST.json"
    if manifest_path.is_file():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return _FALLBACK_MANIFEST


def _resolve_repo_root(repo_id: str, relative_path: str) -> Path:
    env_name = _REPO_ENV_VARS.get(repo_id)
    env_path = getenv(env_name) if env_name else None
    if env_path:
        return Path(env_path).expanduser().resolve()
    return (_workspace_root() / relative_path).resolve()


def _resolve_context_path(repo_root: Path, repo_relative_root: str, relative_path: str) -> str:
    repo_candidate = (repo_root / relative_path).resolve()
    workspace_candidate = (_workspace_root() / repo_relative_root / relative_path).resolve()
    if repo_candidate.exists() or not workspace_candidate.exists():
        return str(repo_candidate)
    return str(workspace_candidate)


def _quality_gate_name(command: str) -> str:
    if "cargo fmt" in command:
        return "fmt"
    if "clippy" in command:
        return "clippy"
    if "cargo test" in command:
        return "test"
    if "pytest" in command:
        return "test"
    if "ruff" in command:
        return "ruff"
    if "lint" in command:
        return "lint"
    if "typecheck" in command:
        return "typecheck"
    if "e2e" in command:
        return "test_e2e"
    if "validate" in command:
        return "validate"
    return command.split()[0].replace(":", "_")


def _build_profile(entry: dict) -> RepoProfile:
    repo_root = _resolve_repo_root(entry["id"], entry["path"])
    return RepoProfile(
        repo_id=entry["id"],
        display_name=entry["display_name"],
        path=str(repo_root),
        role=entry["role"],
        tags=list(entry.get("tags", [])),
        depends_on=list(entry.get("depends_on", [])),
        used_by=list(entry.get("used_by", [])),
        entry_points=list(entry.get("entry_points", [])),
        owned_contracts=list(entry.get("owned_contracts", [])),
        shared_contracts=list(entry.get("shared_contracts", [])),
        hard_boundaries=list(entry.get("hard_boundaries", [])),
        quality_gates=[
            QualityGate(name=_quality_gate_name(command), command=command)
            for command in entry.get("validation_commands", [])
        ],
        summary_path=_resolve_context_path(repo_root, entry["path"], entry["summary_path"]),
        api_summary_path=_resolve_context_path(repo_root, entry["path"], entry["api_summary_path"]),
        repo_manifest_path=_resolve_context_path(repo_root, entry["path"], entry["repo_manifest_path"]),
        skills_path=_resolve_context_path(repo_root, entry["path"], entry["skills_path"]),
    )


@lru_cache(maxsize=1)
def get_repo_profiles() -> dict[str, RepoProfile]:
    """Return manifest-backed profiles used by routing, tools, and prompt generation."""
    manifest = _load_workspace_manifest()
    profiles = {_entry["id"]: _build_profile(_entry) for _entry in manifest.get("repos", [])}
    return profiles


def get_repo_profile(repo_id: str) -> RepoProfile:
    """Lookup a profile by stable repo id."""
    profiles = get_repo_profiles()
    if repo_id not in profiles:
        raise KeyError(f"Unknown repo id: {repo_id}")
    return profiles[repo_id]


def render_repo_profile(repo_id: str) -> str:
    """Return a short route card for prompts and repo contract lookups."""
    profile = get_repo_profile(repo_id)
    tags = "\n".join(f"- {tag}" for tag in profile.tags)
    entry_points = "\n".join(f"- {item}" for item in profile.entry_points)
    context_files = "\n".join(f"- {item}" for item in profile.context_files)
    hard_boundaries = "\n".join(f"- {item}" for item in profile.hard_boundaries)
    quality_gates = "\n".join(f"- `{gate.command}`" for gate in profile.quality_gates)
    return f"""Repo: {profile.display_name}
Role: {profile.role}
Path: {profile.path}

Tags:
{tags}

Entry points:
{entry_points}

Context files:
{context_files}

Hard boundaries:
{hard_boundaries}

Validation:
{quality_gates}
"""


def render_quality_gates(repo_id: str) -> str:
    """Compact list of quality gate commands suitable for prompt or tool context."""
    profile = get_repo_profile(repo_id)
    return "\n".join(f"- `{gate.command}`" for gate in profile.quality_gates)
