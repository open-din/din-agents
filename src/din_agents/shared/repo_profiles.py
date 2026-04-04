from __future__ import annotations

from functools import lru_cache
from os import getenv

from pydantic import BaseModel, Field


class QualityGate(BaseModel):
    name: str
    command: str
    notes: str = ""


class RepoProfile(BaseModel):
    repo_id: str
    display_name: str
    path: str
    primary_language: str
    secondary_languages: list[str] = Field(default_factory=list)
    tech_stack: list[str] = Field(default_factory=list)
    owned_surfaces: list[str] = Field(default_factory=list)
    canonical_docs: list[str] = Field(default_factory=list)
    boundaries: list[str] = Field(default_factory=list)
    quality_gates: list[QualityGate] = Field(default_factory=list)
    routing_keywords: list[str] = Field(default_factory=list)
    prompt_notes: list[str] = Field(default_factory=list)


def _repo_path(env_name: str, fallback: str) -> str:
    return getenv(env_name, fallback)


@lru_cache(maxsize=1)
def get_repo_profiles() -> dict[str, RepoProfile]:
    return {
        "din_core": RepoProfile(
            repo_id="din_core",
            display_name="din-core",
            path=_repo_path("DIN_CORE_PATH", "/Users/veacks/Sites/din-core"),
            primary_language="Rust",
            secondary_languages=["JSON Schema", "C ABI", "WASM bindings"],
            tech_stack=["cargo", "serde", "wasm-bindgen", "workspace crates"],
            owned_surfaces=[
                "Patch semantics",
                "Node registry authority",
                "Compiler and runtime behavior",
                "FFI and WASM thin wrappers",
            ],
            canonical_docs=[
                "/Users/veacks/Sites/din-core/AGENTS.md",
                "/Users/veacks/Sites/din-core/project/SUMMARY.md",
                "/Users/veacks/Sites/din-core/project/USERFLOW.md",
                "/Users/veacks/Sites/din-core/project/TEST_MATRIX.md",
                "/Users/veacks/Sites/din-core/schemas/patch.schema.json",
                "/Users/veacks/Sites/din-core/fixtures/canonical_patch.json",
            ],
            boundaries=[
                "Keep react-din patch compatibility as the top external contract.",
                "Prefer changes in din-patch and din-core before widening FFI or WASM.",
                "Keep one authoritative node registry for compiler, docs, and tests.",
            ],
            quality_gates=[
                QualityGate(name="fmt", command="cargo fmt --all --check"),
                QualityGate(
                    name="clippy",
                    command="cargo clippy --workspace --all-targets -- -D warnings",
                ),
                QualityGate(name="test", command="cargo test --workspace"),
            ],
            routing_keywords=[
                "rust",
                "cargo",
                "ffi",
                "wasm",
                "patch migration",
                "patch contract",
                "round-trip",
                "registry",
                "node id",
                "compiler",
                "runtime",
                "din-core",
            ],
            prompt_notes=[
                "Persist exact patch node IDs such as osc, stepSequencer, and midiCC.",
                "Treat round-trip patch preservation and interface naming parity as release gates.",
                "FFI and WASM wrappers should stay thin and reuse Rust-native logic.",
            ],
        ),
        "react_din": RepoProfile(
            repo_id="react_din",
            display_name="react-din",
            path=_repo_path("REACT_DIN_PATH", "/Users/veacks/Sites/react-din"),
            primary_language="TypeScript",
            secondary_languages=["TSX", "JSON Schema", "Markdown"],
            tech_stack=["React", "tsup", "Vitest", "Testing Library", "ESLint"],
            owned_surfaces=[
                "Public @open-din/react API",
                "Patch schema export",
                "Component docs and coverage manifest",
                "Library packaging and subpath exports",
            ],
            canonical_docs=[
                "/Users/veacks/Sites/react-din/AGENTS.md",
                "/Users/veacks/Sites/react-din/project/SUMMARY.md",
                "/Users/veacks/Sites/react-din/project/USERFLOW.md",
                "/Users/veacks/Sites/react-din/project/TEST_MATRIX.md",
                "/Users/veacks/Sites/react-din/project/COVERAGE_MANIFEST.json",
                "/Users/veacks/Sites/react-din/schemas/patch.schema.json",
            ],
            boundaries=[
                "DIN Studio-owned editor workflows and tests live in din-studio.",
                "Patch schema governance lives in this repo for the public PatchDocument shape.",
                "Visible UI copy should live in dedicated copy modules.",
            ],
            quality_gates=[
                QualityGate(name="lint", command="npm run lint"),
                QualityGate(name="typecheck", command="npm run typecheck"),
                QualityGate(name="ci_check", command="npm run ci:check"),
                QualityGate(name="validate_changes", command="npm run validate:changes"),
            ],
            routing_keywords=[
                "react",
                "tsx",
                "component",
                "public api",
                "@open-din/react",
                "coverage manifest",
                "docs/components",
                "patch schema",
                "schema export",
                "tsup",
                "library",
                "react-din",
            ],
            prompt_notes=[
                "Keep documentation in English for docs, project files, and contributor-facing JSDoc.",
                "Mapped source changes must update docs, tests, and coverage manifest together.",
                "Published package must keep exporting @open-din/react/patch/schema.json.",
            ],
        ),
        "din_studio": RepoProfile(
            repo_id="din_studio",
            display_name="din-studio",
            path=_repo_path("DIN_STUDIO_PATH", "/Users/veacks/Sites/din-studio"),
            primary_language="TypeScript",
            secondary_languages=["TSX", "Electron", "Playwright"],
            tech_stack=["React", "Vite", "Electron", "Vitest", "Playwright", "ws"],
            owned_surfaces=[
                "Editor graph workflows",
                "Panels, launcher, and shell surfaces",
                "MCP target bridge and tests",
                "Studio AI catalog and prompts",
            ],
            canonical_docs=[
                "/Users/veacks/Sites/din-studio/AGENTS.md",
                "/Users/veacks/Sites/din-studio/project/SUMMARY.md",
                "/Users/veacks/Sites/din-studio/project/USERFLOW.md",
                "/Users/veacks/Sites/din-studio/project/TEST_MATRIX.md",
                "/Users/veacks/Sites/din-studio/project/COVERAGE_MANIFEST.json",
                "/Users/veacks/Sites/din-studio/project/SURFACE_MANIFEST.json",
            ],
            boundaries=[
                "Public patch schema and @open-din/react API are owned by react-din.",
                "Rust patch semantics and node registry authority live in din-core.",
                "Changes under targets/mcp must keep targets/mcp/tests updated.",
            ],
            quality_gates=[
                QualityGate(name="lint", command="npm run lint"),
                QualityGate(name="typecheck", command="npm run typecheck"),
                QualityGate(name="validate_manifests", command="npm run validate:manifests"),
                QualityGate(name="validate_docs", command="npm run validate:docs"),
                QualityGate(name="test", command="npm run test"),
                QualityGate(name="test_e2e", command="npm run test:e2e"),
            ],
            routing_keywords=[
                "electron",
                "vite",
                "editor",
                "launcher",
                "panel",
                "surface manifest",
                "mcp",
                "targets/mcp",
                "node catalog",
                "codegen",
                "e2e",
                "ui/ai",
                "din-studio",
            ],
            prompt_notes=[
                "Keep contributor-facing docs and UI copy in English.",
                "Editor node changes must align nodeCatalog, codegen tests, feature docs, and TEST_MATRIX scenarios.",
                "Visible workflow changes must update SURFACE_MANIFEST and at least one automated test.",
            ],
        ),
    }


def get_repo_profile(repo_id: str) -> RepoProfile:
    profiles = get_repo_profiles()
    if repo_id not in profiles:
        raise KeyError(f"Unknown repo id: {repo_id}")
    return profiles[repo_id]


def render_repo_profile(repo_id: str) -> str:
    profile = get_repo_profile(repo_id)
    owned_surfaces = "\n".join(f"- {surface}" for surface in profile.owned_surfaces)
    docs = "\n".join(f"- {path}" for path in profile.canonical_docs)
    boundaries = "\n".join(f"- {item}" for item in profile.boundaries)
    quality_gates = "\n".join(
        f"- {gate.name}: `{gate.command}` {gate.notes}".rstrip()
        for gate in profile.quality_gates
    )
    prompt_notes = "\n".join(f"- {note}" for note in profile.prompt_notes)
    secondary_languages = ", ".join(profile.secondary_languages) or "None"
    tech_stack = ", ".join(profile.tech_stack)

    return f"""Repo: {profile.display_name}
Path: {profile.path}
Primary language: {profile.primary_language}
Secondary languages: {secondary_languages}
Tech stack: {tech_stack}

Owned surfaces:
{owned_surfaces}

Canonical docs:
{docs}

Boundaries:
{boundaries}

Quality gates:
{quality_gates}

Prompt notes:
{prompt_notes}
"""


def render_quality_gates(repo_id: str) -> str:
    profile = get_repo_profile(repo_id)
    return "\n".join(
        f"- {gate.name}: `{gate.command}`" for gate in profile.quality_gates
    )
