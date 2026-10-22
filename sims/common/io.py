"""CLI, deterministic multiprocessing and SPEC §3 output conventions."""

import argparse
import csv
import json
import math
import multiprocessing
import os
from pathlib import Path
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[2]
SUMMARY_KEYS = frozenset({"module", "version", "git_sha", "mode", "assumptions",
                          "key_results", "validation", "runtime_s"})
FIGURE_DPI = 150  # SPEC §3 output convention.
MAX_WORKERS = 8  # SPEC §3 server core budget.


def git_sha() -> str:
    """Return repository HEAD, then WME_GIT_SHA, otherwise 'unknown'."""
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                                check=True, capture_output=True, text=True,
                                timeout=5)
        sha = result.stdout.strip()
        if sha:
            return sha
    except (OSError, subprocess.SubprocessError):
        pass
    return os.environ.get("WME_GIT_SHA", "").strip() or "unknown"


def write_summary(out_dir, module, version, mode, assumptions, key_results,
                  validation, runtime_s) -> Path:
    """Write exactly the eight SPEC §3 keys; runtime is elapsed seconds."""
    if mode not in {"quick", "full"}:
        raise ValueError("mode must be quick or full")
    if not isinstance(assumptions, dict):
        raise TypeError("assumptions must be a dict")
    if not math.isfinite(runtime_s) or runtime_s < 0:
        raise ValueError("runtime_s must be finite and nonnegative")
    payload = dict(module=module, version=version, git_sha=git_sha(), mode=mode,
                   assumptions=assumptions, key_results=key_results,
                   validation=validation, runtime_s=runtime_s)
    path = Path(out_dir) / "summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")
    return path


def write_csv(path, rows) -> Path:
    """Write tidy records with explicit unit-bearing column names."""
    rows = iter(rows)
    first = next(rows, None)
    if first is None:
        raise ValueError("CSV requires at least one row to define columns")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(first))
        writer.writeheader()
        writer.writerow(first)
        writer.writerows(rows)
    return path


def save_fig(fig, path) -> Path:
    """Save PNG at 150 dpi; require axis labels with bracketed units."""
    for ax in fig.axes:
        for label in (ax.get_xlabel(), ax.get_ylabel()):
            if "[" not in label or "]" not in label:
                raise ValueError("Every plot axis must be labelled with [units]")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    return path


def worker_count(value: str) -> int:
    """Parse the supported 1..8 process budget."""
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("workers must be an integer") from exc
    if not 1 <= count <= MAX_WORKERS:
        raise argparse.ArgumentTypeError("workers must be between 1 and 8")
    return count


def argument_parser(module: str) -> argparse.ArgumentParser:
    """Build shared CLI; default mode is full and worker count is one."""
    parser = argparse.ArgumentParser(description=f"WME-1 {module}")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", dest="mode", action="store_const", const="quick")
    mode.add_argument("--full", dest="mode", action="store_const", const="full")
    parser.set_defaults(mode="full")
    parser.add_argument("--workers", type=worker_count, default=1)
    parser.add_argument("--out", type=Path, default=Path("results") / module)
    return parser


def ordered_map(function, items, workers=1):
    """Map independent tasks in input order; spawn at most eight processes."""
    worker_count(str(workers))
    items = list(items)
    if workers == 1 or len(items) < 2:
        return [function(item) for item in items]
    with multiprocessing.get_context("spawn").Pool(min(workers, len(items))) as pool:
        return pool.map(function, items)
