"""Executable din-core audio backlog: compose control-plane requests per-task."""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from din_agents.main import run_request


@dataclass(frozen=True)
class AudioTaskSpec:
    """One implementable audio surface for din-core."""

    id: str
    category: str
    surface: str
    web_audio_hint: str | None


# Ordered backlog: nodes, effects, sources, patch, analysis (25 tasks).
AUDIO_TASKS: tuple[AudioTaskSpec, ...] = (
    # Nodes
    AudioTaskSpec("gain", "nodes", "Gain", "GainNode"),
    AudioTaskSpec("filter", "nodes", "Filter", "BiquadFilterNode / AudioFilter semantics"),
    AudioTaskSpec("osc", "nodes", "Osc", "OscillatorNode"),
    AudioTaskSpec("delay", "nodes", "Delay", "DelayNode"),
    AudioTaskSpec("compressor", "nodes", "Compressor", "DynamicsCompressorNode"),
    AudioTaskSpec("convolver", "nodes", "Convolver", "ConvolverNode"),
    AudioTaskSpec("panner", "nodes", "Panner", "PannerNode"),
    AudioTaskSpec("stereo_panner", "nodes", "StereoPanner", "StereoPannerNode"),
    AudioTaskSpec("wave_shaper", "nodes", "WaveShaper", "WaveShaperNode"),
    AudioTaskSpec("preset_wave_shaper", "nodes", "PresetWaveShaper", "WaveShaperNode with preset curves"),
    AudioTaskSpec("adsr", "nodes", "ADSR", None),
    # Effects
    AudioTaskSpec("reverb", "effects", "Reverb", "Typically convolver / impulse stack"),
    AudioTaskSpec("chorus", "effects", "Chorus", "Delay + modulation stack"),
    AudioTaskSpec("distortion", "effects", "Distortion", "WaveShaper / custom waveshaping"),
    # Sources
    AudioTaskSpec("sampler", "sources", "Sampler", "AudioBufferSourceNode pattern"),
    AudioTaskSpec("triggered_sampler", "sources", "TriggeredSampler", "One-shot buffer source"),
    AudioTaskSpec("noise", "sources", "Noise", None),
    AudioTaskSpec("noise_burst", "sources", "NoiseBurst", None),
    AudioTaskSpec("media_stream", "sources", "MediaStream", "MediaStreamAudioSourceNode"),
    AudioTaskSpec("constant_source", "sources", "ConstantSource", "ConstantSourceNode"),
    AudioTaskSpec("lfo", "sources", "LFO", "Low-frequency OscillatorNode as modulator"),
    # Patch
    AudioTaskSpec("patch", "patch", "Patch", None),
    AudioTaskSpec("patch_output", "patch", "PatchOutput", None),
    AudioTaskSpec("patch_renderer", "patch", "PatchRenderer", None),
    # Analysis
    AudioTaskSpec("analyzer", "analysis", "Analyzer", "AnalyserNode"),
)

_ID_INDEX: dict[str, AudioTaskSpec] = {t.id: t for t in AUDIO_TASKS}


def task_at_step(step: int) -> AudioTaskSpec:
    """Return the 1-based backlog item (step ``1`` is the first task)."""
    if step < 1 or step > len(AUDIO_TASKS):
        raise IndexError(
            f"step must be between 1 and {len(AUDIO_TASKS)} inclusive, got {step}",
        )
    return AUDIO_TASKS[step - 1]


def list_tasks() -> tuple[AudioTaskSpec, ...]:
    """Return the ordered backlog."""
    return AUDIO_TASKS


def get_task(task_id: str) -> AudioTaskSpec:
    """Resolve a task by id (case-sensitive snake_case)."""
    key = task_id.strip()
    if key not in _ID_INDEX:
        known = ", ".join(sorted(_ID_INDEX))
        raise KeyError(f"Unknown audio task id {task_id!r}. Known ids: {known}")
    return _ID_INDEX[key]


def build_request(spec: AudioTaskSpec) -> str:
    """Build the English control-plane request for this backlog item."""
    wa = spec.web_audio_hint
    wa_line = (
        f"Align runtime semantics with the Web Audio API where `{wa}` applies."
        if wa
        else "Define semantics explicitly in din-core (no single Web Audio leaf node maps 1:1)."
    )
    return f"""din-core audio — implement and land `{spec.surface}` ({spec.category}).

**Objective**: Define the runtime contract, registry entry, patch serialization, and validation for this audio surface in din-core. {wa_line}

**Investigation**: Inspect din-core for existing audio/graph patterns, node IDs, registry tables, patch migrations, FFI/WASM surfaces, fixtures, and tests that must stay in parity.

**Coordination**: If the persisted patch contract or public serialization changes, coordinate react-din schema/types. Touch din-studio only when editor surfaces, MCP tools, or catalogs must reflect this node.

**Acceptance criteria**: Rust tests and fixtures updated; run din-core quality gates from the repo profile; if public `pub` Rustdoc or exported surfaces move, run `./scripts/generate-docs.sh`.

Produce a concrete implementation plan (and execute repo edits in-repo when appropriate) scoped to this surface: `{spec.surface}`.
"""


def _run_one(
    spec: AudioTaskSpec,
    *,
    report_path: str | None,
    quiet: bool,
    print_report: bool,
) -> None:
    request = build_request(spec)
    if os.environ.get("DIN_AGENTS_NO_PRINT", "").lower() not in ("1", "true", "yes"):
        print(f"\n{'=' * 60}\nTask {spec.id} ({spec.surface}) — din-core audio\n{'=' * 60}\n", file=sys.stderr)
    run_request(
        request=request,
        repo_hint="din_core",
        report_path=report_path,
        quiet=quiet,
        print_report=print_report,
    )


def run_all_sequential(
    *,
    output_dir: Path | None,
    report_path_single: str | None,
    quiet: bool,
    print_report: bool,
    pause_between_s: float = 0.0,
    prompt_between: bool = False,
) -> None:
    """Run every backlog task in order (each full control-plane kickoff).

    ``pause_between_s`` spaces out runs to reduce bursts against provider TPM limits
    (e.g. Anthropic input tokens per minute).

    ``prompt_between`` waits for Enter on stdin after each task (except the last)
    so only one crew run is started when you are ready (best for strict TPM limits).
    """
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
    total = len(AUDIO_TASKS)
    for i, spec in enumerate(AUDIO_TASKS, start=1):
        if output_dir is not None:
            per_path = str(output_dir / f"{spec.id}.md")
        elif report_path_single:
            stem = Path(report_path_single).stem
            suffix = Path(report_path_single).suffix or ".md"
            parent = Path(report_path_single).parent
            per_path = str(parent / f"{stem}-{spec.id}{suffix}")
        else:
            per_path = None
        print(f"[{i}/{total}] Running audio task: {spec.id}", file=sys.stderr)
        _run_one(spec, report_path=per_path, quiet=quiet, print_report=print_report)
        if i >= total:
            break
        if prompt_between:
            try:
                input("Press Enter to send the next task (Ctrl+C to stop)… ")
            except EOFError:
                print("EOF: stopping backlog here.", file=sys.stderr)
                return
        if pause_between_s > 0:
            print(f"Pausing {pause_between_s:g}s before next task (TPM / rate limits)…", file=sys.stderr)
            time.sleep(pause_between_s)


def main() -> None:
    """CLI: list backlog ids or run one task through the control plane."""
    parser = argparse.ArgumentParser(
        description="Run a single din-core audio backlog task through the DIN control plane (routes to din-core).",
    )
    parser.add_argument(
        "task_id",
        nargs="?",
        help="Task id (e.g. gain, reverb, patch). Run without this and without --list to print ids.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print all task ids, categories, and surfaces, then exit.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="run_all",
        help="Run every audio task in backlog order (one control-plane run per task).",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help=(
            "With --all: after each task, wait for Enter before starting the next "
            "(task-by-task; disables the default 90s pause unless you also pass --pause-between)."
        ),
    )
    parser.add_argument(
        "--step",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Run only the Nth backlog task (1-based). Next: --step N+1. "
            "Does not chain runs; use this for strict one-send-at-a-time workflows."
        ),
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="",
        help="With --all: write each report to <dir>/<task_id>.md (recommended).",
    )
    parser.add_argument(
        "--pause-between",
        dest="pause_between",
        type=float,
        default=None,
        metavar="SECONDS",
        help=(
            "With --all: wait this many seconds before the next task after any prompt "
            "(default: 90 without --interactive; with --interactive, default 0). Use 0 for no pause."
        ),
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Less terminal noise from CrewAI.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="report_path",
        default="",
        help="Write the markdown report to this path (single task). With --all, writes <stem>-<task_id><suffix> files next to the path.",
    )
    parser.add_argument(
        "--no-print",
        action="store_true",
        help="Do not print the report to stdout.",
    )
    args = parser.parse_args()

    if args.list:
        for t in AUDIO_TASKS:
            print(f"{t.id}\t{t.category}\t{t.surface}")
        return

    if args.step is not None:
        if args.task_id or args.run_all:
            parser.error("--step cannot be used with task_id or --all.")
        if args.step < 1 or args.step > len(AUDIO_TASKS):
            parser.error(f"--step must be between 1 and {len(AUDIO_TASKS)}.")
        spec = task_at_step(args.step)
        report_path = args.report_path.strip() or None
        print(
            f"[step {args.step}/{len(AUDIO_TASKS)}] {spec.id} ({spec.surface})",
            file=sys.stderr,
        )
        if args.no_print:
            os.environ["DIN_AGENTS_NO_PRINT"] = "1"
        try:
            _run_one(
                spec,
                report_path=report_path,
                quiet=args.quiet,
                print_report=not args.no_print,
            )
        finally:
            if args.no_print:
                os.environ.pop("DIN_AGENTS_NO_PRINT", None)
        nxt = args.step + 1
        next_hint = (
            f"Next: uv run run_din_core_audio_task --step {nxt}"
            if nxt <= len(AUDIO_TASKS)
            else "Backlog complete (no further --step)."
        )
        print(next_hint, file=sys.stderr)
        return

    if args.run_all:
        if args.task_id:
            parser.error("Do not pass task_id when using --all.")
        out_dir = Path(args.output_dir).expanduser() if args.output_dir.strip() else None
        report_single = args.report_path.strip() or None
        if out_dir is None and report_single is None:
            out_dir = Path("output") / "din-core-audio-runs"
        if args.pause_between is None:
            pause = 0.0 if args.interactive else 90.0
        else:
            pause = max(0.0, args.pause_between)
        if args.interactive:
            print(
                "Interactive mode: one crew run per Enter (no automatic batching).",
                file=sys.stderr,
            )
        elif pause > 0:
            print(
                f"Using --pause-between={pause:g}s between tasks (input TPM). "
                "For manual pacing use: --all --interactive",
                file=sys.stderr,
            )
        if args.no_print:
            os.environ["DIN_AGENTS_NO_PRINT"] = "1"
        try:
            run_all_sequential(
                output_dir=out_dir,
                report_path_single=report_single if args.output_dir.strip() == "" else None,
                quiet=args.quiet,
                print_report=not args.no_print,
                pause_between_s=pause,
                prompt_between=args.interactive,
            )
        finally:
            if args.no_print:
                os.environ.pop("DIN_AGENTS_NO_PRINT", None)
        return

    if not args.task_id:
        for t in AUDIO_TASKS:
            print(t.id)
        return

    spec = get_task(args.task_id)
    report_path = args.report_path.strip() or None
    if args.no_print:
        os.environ["DIN_AGENTS_NO_PRINT"] = "1"
    try:
        _run_one(
            spec,
            report_path=report_path,
            quiet=args.quiet,
            print_report=not args.no_print,
        )
    finally:
        if args.no_print:
            os.environ.pop("DIN_AGENTS_NO_PRINT", None)


if __name__ == "__main__":
    main()
