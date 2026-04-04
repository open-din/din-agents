#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
from pathlib import Path

from din_agents.flow import DinControlPlaneFlow


def _dedupe_control_plane_report(text: str) -> str:
    """Drop a repeated final report when the same document is concatenated twice."""
    marker = "# DIN Control Plane Report"
    first = text.find(marker)
    if first == -1:
        return text
    second = text.find(marker, first + len(marker))
    if second == -1:
        return text
    return text[:second].rstrip() + "\n"



def run_request(
    request: str,
    repo_hint: str | None = None,
    *,
    report_path: str | None = None,
    quiet: bool = False,
    print_report: bool = True,
) -> str:
    prev_quiet = os.environ.get("DIN_AGENTS_QUIET")
    if quiet:
        os.environ["DIN_AGENTS_QUIET"] = "1"
    try:
        flow = DinControlPlaneFlow()
        path = report_path or os.environ.get("DIN_AGENTS_REPORT_PATH", "").strip()
        if path:
            flow.state.report_path = path
        flow.kickoff(inputs={"request": request, "repo_hint": repo_hint or ""})
        out = _dedupe_control_plane_report(flow.state.final_output)
        flow.state.final_output = out
        report_file = Path(flow.state.report_path)
        if report_file.is_file():
            report_file.write_text(out, encoding="utf-8")
        if print_report and os.environ.get("DIN_AGENTS_NO_PRINT", "").lower() not in ("1", "true", "yes"):
            print(out)
        return out
    finally:
        if quiet:
            if prev_quiet is None:
                os.environ.pop("DIN_AGENTS_QUIET", None)
            else:
                os.environ["DIN_AGENTS_QUIET"] = prev_quiet


def kickoff() -> str:
    request = os.environ.get(
        "DIN_AGENTS_REQUEST",
        "Assess a DIN change request across din-core, react-din, and din-studio.",
    )
    repo_hint = os.environ.get("DIN_AGENTS_REPO_HINT", "")
    quiet = os.environ.get("DIN_AGENTS_QUIET", "").lower() in ("1", "true", "yes")
    report_path = os.environ.get("DIN_AGENTS_REPORT_PATH", "").strip() or None
    return run_request(request=request, repo_hint=repo_hint, report_path=report_path, quiet=quiet)


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
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Less terminal noise from CrewAI (boxes, tool chatter). Report is still printed.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="report_path",
        default="",
        help="Write the markdown report to this path (default: output/control-plane-report.md).",
    )
    parser.add_argument(
        "--no-print",
        action="store_true",
        help="Do not print the report to stdout (still writes --output / default report path).",
    )
    args = parser.parse_args()

    request = args.request or os.environ.get(
        "DIN_AGENTS_REQUEST",
        "Assess a DIN change request across din-core, react-din, and din-studio.",
    )
    report_path = args.report_path.strip() or None
    if args.no_print:
        os.environ["DIN_AGENTS_NO_PRINT"] = "1"
    try:
        return run_request(
            request=request,
            repo_hint=args.repo_hint,
            report_path=report_path,
            quiet=args.quiet,
            print_report=not args.no_print,
        )
    finally:
        if args.no_print:
            os.environ.pop("DIN_AGENTS_NO_PRINT", None)


if __name__ == "__main__":
    kickoff()
