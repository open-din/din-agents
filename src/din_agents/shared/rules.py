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
    "din-agents": "din_agents",
    "din_agents": "din_agents",
}

PRODUCT_REPO_IDS: tuple[str, ...] = ("din_core", "react_din", "din_studio")

_MULTI_REPO_SCOPE_PHRASES = (
    "each project",
    "each repo",
    "all projects",
    "all repos",
    "every project",
    "every repo",
    "across all",
)
_REPO_WIDE_TOOLING_HINTS = ("husky", "pre-commit", "precommit", "git hook", "git hooks")


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


def _mentions_multi_repo_scope(lowered: str) -> bool:
    return any(phrase in lowered for phrase in _MULTI_REPO_SCOPE_PHRASES)


def _mentions_repo_tooling(lowered: str) -> bool:
    return any(hint in lowered for hint in _REPO_WIDE_TOOLING_HINTS)


def _search_terms(values: list[str]) -> set[str]:
    terms: set[str] = set()
    for value in values:
        lowered = value.lower()
        if lowered:
            terms.add(lowered)
        if "/" in lowered:
            terms.add(lowered.rsplit("/", 1)[-1])
    return terms


def _score_request(lowered: str) -> dict[str, int]:
    profiles = get_repo_profiles()
    scores: dict[str, int] = defaultdict(int)
    for repo_id, profile in profiles.items():
        tag_terms = _search_terms(profile.tags)
        entry_terms = _search_terms(profile.entry_points)
        owned_terms = _search_terms(profile.owned_contracts)
        if profile.role in lowered:
            scores[repo_id] += 1
        for term in tag_terms:
            if term in lowered:
                scores[repo_id] += 2
        for term in entry_terms:
            if term in lowered:
                scores[repo_id] += 2
        for term in owned_terms:
            if term in lowered:
                scores[repo_id] += 1
    return scores


def _match_contract_repos(lowered: str) -> list[str]:
    matches: list[str] = []
    for repo_id, profile in get_repo_profiles().items():
        contract_terms = _search_terms(profile.owned_contracts + profile.shared_contracts)
        if any(term in lowered for term in contract_terms):
            matches.append(repo_id)
    return matches


def route_request(request: str, repo_hint: str | None = None) -> RoutingDecision:
    """Route to one repo by default and escalate only for shared contracts or explicit workspace scope."""
    lowered = request.lower()
    scores = _score_request(lowered)
    reasons: list[str] = []
    mentions = _extract_repo_mentions(request)
    normalized_hint = _normalize_repo_hint(repo_hint)

    if normalized_hint in get_repo_profiles():
        scores[normalized_hint] += 5
        reasons.append(f"Explicit repo hint selected `{normalized_hint}`.")

    if mentions:
        for repo_id in mentions:
            scores[repo_id] += 4
        reasons.append(
            "Request explicitly mentions: "
            + ", ".join(get_repo_profile(repo_id).display_name for repo_id in mentions)
        )

    primary_repo = max(scores, key=scores.get) if scores else "din_studio"
    affected_repos = [primary_repo]
    reasons.append(f"Primary repo resolved to `{primary_repo}`.")

    explicit_cross_repo_scope = (
        _mentions_multi_repo_scope(lowered)
        or "cross-repo" in lowered
        or "cross repo" in lowered
        or "across " in lowered
    )

    if _mentions_multi_repo_scope(lowered) and _mentions_repo_tooling(lowered):
        affected_repos = list(PRODUCT_REPO_IDS)
        reasons.append("Explicit workspace-wide tooling request detected.")
    elif normalized_hint == primary_repo and not explicit_cross_repo_scope:
        reasons.append(
            f"Kept to explicit repo hint `{primary_repo}`; treat other repo mentions as coordination context."
        )
    else:
        contract_repos = [repo_id for repo_id in _match_contract_repos(lowered) if repo_id != primary_repo]
        for repo_id in contract_repos:
            if repo_id not in affected_repos:
                affected_repos.append(repo_id)
        if contract_repos:
            reasons.append(
                "Shared or owned contract language detected for: "
                + ", ".join(get_repo_profile(repo_id).display_name for repo_id in contract_repos)
            )

    cross_repo = len(affected_repos) > 1
    if cross_repo:
        reasons.append(
            "Escalated to cross-repo handling for: "
            + ", ".join(get_repo_profile(repo_id).display_name for repo_id in affected_repos)
        )
        route = "cross_repo"
    else:
        route = primary_repo
        reasons.append("Kept to one repo by default.")

    return RoutingDecision(
        route=route,
        affected_repos=affected_repos,
        cross_repo=cross_repo,
        reasons=reasons,
    )


def select_quality_gates(affected_repos: list[str]) -> dict[str, list[str]]:
    """Map repo ids to ordered shell commands from each repo profile."""
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
