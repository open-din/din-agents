"""Tests for din-core audio backlog helpers."""

from unittest.mock import patch

import pytest

from din_agents.din_core_audio_tasks import (
    AUDIO_TASKS,
    build_request,
    get_task,
    list_tasks,
    run_all_sequential,
    task_at_step,
)


def test_audio_tasks_count_and_unique_ids():
    assert len(AUDIO_TASKS) == 25
    ids = [t.id for t in AUDIO_TASKS]
    assert len(ids) == len(set(ids))


def test_list_tasks_matches_tuple():
    assert list_tasks() == AUDIO_TASKS


def test_get_task_known():
    spec = get_task("gain")
    assert spec.surface == "Gain"
    assert spec.category == "nodes"


def test_get_task_unknown():
    with pytest.raises(KeyError, match="Unknown audio task"):
        get_task("not_a_task")


def test_task_at_step():
    assert task_at_step(1).id == "gain"
    assert task_at_step(len(AUDIO_TASKS)).id == "analyzer"


def test_task_at_step_bounds():
    with pytest.raises(IndexError, match="step must be between"):
        task_at_step(0)
    with pytest.raises(IndexError, match="step must be between"):
        task_at_step(len(AUDIO_TASKS) + 1)


def test_build_request_includes_surface_and_objective():
    body = build_request(get_task("analyzer"))
    assert "Analyzer" in body
    assert "din-core audio" in body
    assert "Acceptance criteria" in body
    assert "AnalyserNode" in body


def test_build_request_without_web_audio_hint():
    body = build_request(get_task("patch"))
    assert "Patch" in body
    assert "no single Web Audio leaf node" in body


@patch("din_agents.din_core_audio_tasks.run_request")
def test_run_all_sequential_invokes_control_plane_per_task(mock_run, tmp_path):
    run_all_sequential(
        output_dir=tmp_path,
        report_path_single=None,
        quiet=True,
        print_report=False,
    )
    assert mock_run.call_count == len(AUDIO_TASKS)
    paths_written = {c.kwargs["report_path"] for c in mock_run.call_args_list}
    assert paths_written == {str(tmp_path / f"{t.id}.md") for t in AUDIO_TASKS}


@patch("builtins.input", side_effect=EOFError())
@patch("din_agents.din_core_audio_tasks.run_request")
def test_run_all_sequential_prompt_stops_on_eof(mock_run, _mock_input, tmp_path):
    """EOF on input() ends the backlog after the first task."""
    run_all_sequential(
        output_dir=tmp_path,
        report_path_single=None,
        quiet=True,
        print_report=False,
        pause_between_s=0.0,
        prompt_between=True,
    )
    assert mock_run.call_count == 1


@patch("din_agents.din_core_audio_tasks.time.sleep", autospec=True)
@patch("din_agents.din_core_audio_tasks.run_request")
def test_run_all_sequential_pause_between_tasks(mock_run, mock_sleep, tmp_path):
    run_all_sequential(
        output_dir=tmp_path,
        report_path_single=None,
        quiet=True,
        print_report=False,
        pause_between_s=1.5,
    )
    assert mock_run.call_count == len(AUDIO_TASKS)
    assert mock_sleep.call_count == len(AUDIO_TASKS) - 1
    mock_sleep.assert_called_with(1.5)


@patch("din_agents.din_core_audio_tasks.run_request")
def test_run_all_sequential_stem_siblings_when_report_path(mock_run, tmp_path):
    report = tmp_path / "brief.md"
    run_all_sequential(
        output_dir=None,
        report_path_single=str(report),
        quiet=True,
        print_report=False,
    )
    assert mock_run.call_count == len(AUDIO_TASKS)
    assert {c.kwargs["report_path"] for c in mock_run.call_args_list} == {
        str(tmp_path / f"brief-{t.id}.md") for t in AUDIO_TASKS
    }
