"""CrewAI sequential context limits — avoid multi-task input TPM spikes.

CrewAI's default sequential behavior injects **all** prior task outputs into each
later task prompt. One long first task (e.g. after tool-heavy reads) can push the
second task over provider input TPM limits. Truncation keeps later steps usable;
set ``DIN_AGENTS_MAX_TASK_CONTEXT_CHARS=0`` to disable (full context).
"""

from __future__ import annotations

from typing import Any

from crewai import Crew
from crewai.tasks.task_output import TaskOutput

from din_agents.shared.runtime_prefs import max_sequential_task_context_chars

_TRUNC_TAIL = (
    "\n\n---\n\n"
    "**Note:** Prior-task context was truncated to respect `DIN_AGENTS_MAX_TASK_CONTEXT_CHARS`. "
    "Use `repo_contract_lookup`, `change_brief_builder`, and the repo file reader for full detail; "
    "the crew inputs still include `{request}` and repo paths."
)


def truncate_sequential_context(prior_output: str) -> str:
    """Cap length of aggregated prior-task text injected into the next task."""
    limit = max_sequential_task_context_chars()
    if limit <= 0 or len(prior_output) <= limit:
        return prior_output
    return prior_output[:limit].rstrip() + _TRUNC_TAIL


class TruncatingCrew(Crew):
    """Same as ``Crew``, but caps default sequential context size."""

    @staticmethod
    def _get_context(task: Any, task_outputs: list[TaskOutput]) -> str:
        full = Crew._get_context(task, task_outputs)
        if not isinstance(full, str):
            return full  # pragma: no cover — defensive
        return truncate_sequential_context(full)
