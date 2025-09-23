# lifeos_skeleton/tests/test_pipeline_small.py
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

def test_pipeline_runs():
    # paths relative to *this file*
    tests_dir = Path(__file__).resolve().parent        # .../lifeos_skeleton/tests
    repo_root = tests_dir.parent                       # .../lifeos_skeleton

    cfg = repo_root / "configs" / "sample_small.yaml"
    assert cfg.exists(), f"Config file not found: {cfg}"

    # Run the experiment from the repo root (where run_experiment.py now lives)
    cmd = [sys.executable, "run_experiment.py", "--config", str(cfg)]
    res = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)

    # Helpful debug if anything goes wrong
    if res.returncode != 0:
        print("STDOUT:\n", res.stdout)
        print("STDERR:\n", res.stderr)

    assert res.returncode == 0, "run_experiment.py failed"

    # Artifacts should appear under runs/
    runs_dir = repo_root / "runs"
    assert runs_dir.exists(), f"runs/ directory not created at {runs_dir}"
    assert any(runs_dir.iterdir()), "runs/ directory is empty — no artifacts created"
