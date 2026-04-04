"""Report assembly helpers (no LLM)."""

from crewai.crews.crew_output import CrewOutput
from crewai.tasks.task_output import TaskOutput

from din_agents.flow import _crew_tasks_markdown
from din_agents.main import _dedupe_control_plane_report


def test_crew_tasks_markdown_joins_all_task_outputs() -> None:
    result = CrewOutput(
        raw="final task only",
        tasks_output=[
            TaskOutput(description="a", name="assess_patch_contract", raw="First brief.", agent="ag"),
            TaskOutput(description="b", name="review_registry_and_runtime", raw="Second brief.", agent="ag"),
            TaskOutput(description="c", name="plan_rust_validation", raw="Third brief.", agent="ag"),
        ],
    )
    md = _crew_tasks_markdown(result)
    assert "assess_patch_contract" in md
    assert "First brief." in md
    assert "review_registry_and_runtime" in md
    assert "Second brief." in md
    assert "plan_rust_validation" in md
    assert "Third brief." in md


def test_crew_tasks_markdown_falls_back_to_raw() -> None:
    result = CrewOutput(raw="only raw", tasks_output=[])
    assert _crew_tasks_markdown(result) == "only raw"


def test_dedupe_control_plane_report_trims_repeated_header() -> None:
    block = (
        "# DIN Control Plane Report\n\n## Request\nx\n\n"
        "## Routing\n```\n```\n\n## Repo Briefs\n### din-core\nbody\n\n"
        "## Quality Gates\n### din-core\n- `cargo test`\n"
    )
    doubled = block + "\n" + block
    out = _dedupe_control_plane_report(doubled)
    assert out.count("# DIN Control Plane Report") == 1
    assert out.rstrip() == block.rstrip()
