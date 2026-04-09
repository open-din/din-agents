"""Heuristic router and quality command selector for multi-repo DIN requests."""

from __future__ import annotations

from collections import defaultdict

from pydantic import BaseModel, Field

from din_agents.shared.repo_profiles import get_repo_profile, get_repo_profiles


REPO_ALIASES = {
    "din-core": "din_core",
    "din_core": "din_core",
    "react-din": "react_din",
    "react_din": "react_din",
    "din-studio": "din_studio",
    "din_studio": "din_studio",
}

ALL_REPO_IDS: tuple[str, ...] = ("din_core", "react_din", "din_studio")

_MULTI_REPO_SCOPE_PHRASES = (
    "each project",
    "each projects",
    "each repo",
    "all projects",
    "all repos",
    "every project",
    "every repo",
    "for all three",
    "all three repos",
    "across all",
)

_REPO_WIDE_TOOLING_HINTS = (
    "husky",
    "pre-commit",
    "precommit",
    "git hook",
    "git hooks",
)


def _mentions_multi_repo_scope(lowered: str) -> bool:
    if any(p in lowered for p in _MULTI_REPO_SCOPE_PHRASES):
        return True
    if "each" in lowered and ("project" in lowered or "repo" in lowered):
        return True
    if "all" in lowered and ("project" in lowered or "repo" in lowered):
        return True
    return False


def _mentions_repo_tooling(lowered: str) -> bool:
    return any(h in lowered for h in _REPO_WIDE_TOOLING_HINTS)


CROSS_REPO_KEYWORDS = (
    "cross-repo",
    "cross repo",
    "boundary",
    "ownership",
    "compatibility",
    "shared contract",
    "patch schema",
    "patch contract",
    "public contract",
    "public api",
    "node catalog parity",
)


class RoutingDecision(BaseModel):
    """Structured routing outcome listing target repos and rationale."""
    route: str
    affected_repos: list[str] = Field(default_factory=list)
    cross_repo: bool = False
    reasons: list[str] = Field(default_factory=list)


def _normalize_repo_hint(repo_hint: str | None) -> str | None:
    if not repo_hint:
        return None
    return REPO_ALIASES.get(repo_hint.strip().lower(), repo_hint.strip().lower())


def _extract_repo_mentions(text: str) -> list[str]:
    mentions: list[str] = []
    lowered = text.lower()
    for alias, repo_id in REPO_ALIASES.items():
        if alias in lowered and repo_id not in mentions:
            mentions.append(repo_id)
    return mentions


def route_request(request: str, repo_hint: str | None = None) -> RoutingDecision:
    """Score repo keywords, hints, and cross-repo phrases to choose affected repos."""
    lowered = request.lower()
    scores: dict[str, int] = defaultdict(int)
    reasons: list[str] = []
    mentioned = _extract_repo_mentions(request)
    normalized_hint = _normalize_repo_hint(repo_hint)

    profiles = get_repo_profiles()
    for repo_id, profile in profiles.items():
        for keyword in profile.routing_keywords:
            if keyword in lowered:
                scores[repo_id] += 1

    if normalized_hint in profiles:
        scores[normalized_hint] += 3
        reasons.append(f"Explicit repo hint selected `{normalized_hint}`.")

    if mentioned:
        for repo_id in mentioned:
            scores[repo_id] += 4
        reasons.append(
            "Request explicitly mentions: " + ", ".join(get_repo_profile(r).display_name for r in mentioned)
        )

    primary_repo = max(scores, key=scores.get) if scores else "din_studio"
    affected_repos = list(dict.fromkeys(mentioned or [primary_repo]))

    if _mentions_multi_repo_scope(lowered) and _mentions_repo_tooling(lowered):
        affected_repos = list(ALL_REPO_IDS)
        reasons.append(
            "Request applies tooling across DIN repos; routing all siblings (din-core, react-din, din-studio)."
        )

    if any(keyword in lowered for keyword in CROSS_REPO_KEYWORDS):
        if primary_repo in {"din_core", "react_din"}:
            for repo_id in ("din_core", "react_din"):
                if repo_id not in affected_repos:
                    affected_repos.append(repo_id)
        if "studio" in lowered or "editor" in lowered or "node catalog" in lowered:
            if "din_studio" not in affected_repos:
                affected_repos.append("din_studio")
        reasons.append("Request contains cross-repo contract or ownership language.")

    if primary_repo == "din_studio" and ("patch schema" in lowered or "public api" in lowered):
        if "react_din" not in affected_repos:
            affected_repos.append("react_din")
        reasons.append("Studio request touches a surface owned by react-din.")

    if primary_repo == "din_studio" and ("rust" in lowered or "registry" in lowered or "ffi" in lowered):
        if "din_core" not in affected_repos:
            affected_repos.append("din_core")
        reasons.append("Studio request references runtime or registry authority owned by din-core.")

    cross_repo = len(affected_repos) > 1
    if cross_repo:
        reasons.append(
            "Escalated to cross-repo handling for: "
            + ", ".join(get_repo_profile(repo_id).display_name for repo_id in affected_repos)
        )

    return RoutingDecision(
        route="cross_repo" if cross_repo else primary_repo,
        affected_repos=affected_repos,
        cross_repo=cross_repo,
        reasons=reasons or [f"Primary repo resolved to `{primary_repo}` from repo keywords."],
    )


def select_quality_gates(affected_repos: list[str]) -> dict[str, list[str]]:
    """Map repo ids to ordered shell commands from each :class:`RepoProfile`."""
    selection: dict[str, list[str]] = {}
    for repo_id in affected_repos:
        profile = get_repo_profile(repo_id)
        selection[repo_id] = [gate.command for gate in profile.quality_gates]
    return selection


def render_routing_decision(decision: RoutingDecision) -> str:
    """Short markdown block summarizing a routing decision for prompts."""
    affected = ", ".join(get_repo_profile(repo_id).display_name for repo_id in decision.affected_repos)
    reasons = "\n".join(f"- {reason}" for reason in decision.reasons)
    return f"""Route: {decision.route}
Affected repos: {affected}
Cross-repo: {decision.cross_repo}
Reasons:
{reasons}
"""
