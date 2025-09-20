import subprocess
import sys
import pathlib

def test_pipeline_runs():
    # Build absolute path to the config file
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    cfg = repo_root / "configs" / "sample_small.yaml"

    # Ensure config file exists
    assert cfg.exists(), f"Config file not found: {cfg}"

    # Run the experiment with that config
    res = subprocess.run(
        [sys.executable, "run_experiment.py", "--config", str(cfg)],
        cwd=repo_root,  # make sure we run from repo root
        capture_output=True,
        text=True
    )

    # Debug info if something goes wrong
    if res.returncode != 0:
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)

    # Assert the script executed successfully
    assert res.returncode == 0, "run_experiment.py failed"

    # Check that the runs/ directory has been created and is not empty
    runs_dir = repo_root / "runs"
    assert runs_dir.exists(), "runs/ directory not created"
    assert any(runs_dir.iterdir()), "runs/ directory is empty — no artifacts created"
