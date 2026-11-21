"""Common CLI and strict summary contract checks."""

import json
import subprocess

import pytest

from sims.common import io


def test_summary_exact_keys_and_assumptions(tmp_path, monkeypatch):
    monkeypatch.setattr(io, "git_sha", lambda: "test-sha")
    path = io.write_summary(tmp_path, "test", "1", "quick", {"source": "test"}, {}, {}, 0.1)
    summary = json.loads(path.read_text(encoding="utf-8"))
    assert set(summary) == io.SUMMARY_KEYS
    assert summary["assumptions"] == {"source": "test"}
    assert summary["git_sha"] == "test-sha"


def test_git_sha_fallbacks(monkeypatch):
    def missing_git(*args, **kwargs):
        raise FileNotFoundError("git unavailable")
    monkeypatch.setattr(io.subprocess, "run", missing_git)
    monkeypatch.setenv("WME_GIT_SHA", "server-supplied-sha")
    assert io.git_sha() == "server-supplied-sha"
    monkeypatch.delenv("WME_GIT_SHA")
    assert io.git_sha() == "unknown"


def test_git_head_precedes_environment(monkeypatch):
    monkeypatch.setenv("WME_GIT_SHA", "environment")
    monkeypatch.setattr(io.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, "head-sha\n", ""))
    assert io.git_sha() == "head-sha"


def test_cli_defaults_and_exclusion():
    parser = io.argument_parser("01_energy_audit")
    args = parser.parse_args([])
    assert args.mode == "full"
    assert args.workers == 1
    assert args.out.as_posix() == "results/01_energy_audit"
    with pytest.raises(SystemExit):
        parser.parse_args(["--quick", "--full"])


@pytest.mark.parametrize("workers", ["0", "9", "-1", "1.5"])
def test_cli_enforces_worker_budget(workers):
    with pytest.raises(SystemExit):
        io.argument_parser("01_energy_audit").parse_args(["--workers", workers])
