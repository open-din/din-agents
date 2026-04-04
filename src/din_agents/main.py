#!/usr/bin/env python
from __future__ import annotations

import argparse
import os

from din_agents.flow import DinControlPlaneFlow


def run_request(request: str, repo_hint: str | None = None) -> str:
    flow = DinControlPlaneFlow()
    flow.kickoff(inputs={"request": request, "repo_hint": repo_hint or ""})
    return flow.state.final_output


def kickoff() -> str:
    request = os.environ.get(
        "DIN_AGENTS_REQUEST",
        "Assess a DIN change request across din-core, react-din, and din-studio.",
    )
    repo_hint = os.environ.get("DIN_AGENTS_REPO_HINT", "")
    report = run_request(request=request, repo_hint=repo_hint)
    print(report)
    return report


def plot() -> None:
    flow = DinControlPlaneFlow()
    flow.plot("din_control_plane")


def run_request_cli() -> str:
    parser = argparse.ArgumentParser(description="Run the DIN CrewAI control plane.")
    parser.add_argument("request", nargs="?", help="Request to route through the control plane.")
    parser.add_argument(
        "--repo-hint",
        dest="repo_hint",
        choices=["din_core", "react_din", "din_studio"],
        default="",
        help="Optional explicit repo hint.",
    )
    args = parser.parse_args()

    request = args.request or os.environ.get(
        "DIN_AGENTS_REQUEST",
        "Assess a DIN change request across din-core, react-din, and din-studio.",
    )
    report = run_request(request=request, repo_hint=args.repo_hint)
    print(report)
    return report


if __name__ == "__main__":
    kickoff()
