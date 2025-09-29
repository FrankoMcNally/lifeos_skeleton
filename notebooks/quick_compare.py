# quick_compare.py
"""
Quick demo runner for compare_metrics.
- Finds the most recent Baseline + PSAI run dirs under ./runs
- Calls compare_metrics.py with those paths
- Drops results into ./comparisons_auto
- Prints the Final Snapshot directly to the terminal
- Full summary (Final + Evolution) saved to comparison_summary.md
- Interactive plots saved as dashboard_comparison.html

Usage:
  py quick_compare.py
  (or: python quick_compare.py)
"""

import subprocess
import sys
from pathlib import Path


def find_latest_run(substring: str) -> Path:
    runs_dir = Path("runs")
    if not runs_dir.exists():
        raise FileNotFoundError("No ./runs directory found. Run Adam & Eve first.")
    candidates = [p for p in runs_dir.iterdir() if substring.lower() in p.name.lower()]
    if not candidates:
        raise FileNotFoundError(f"No run dirs found with '{substring}' in name.")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main():
    try:
        baseline = find_latest_run("free") or find_latest_run("baseline")
        psai = find_latest_run("psai")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    out_dir = Path("comparisons_auto")
    out_dir.mkdir(exist_ok=True)

    print(f"📂 Baseline run: {baseline}")
    print(f"📂 PSAI run: {psai}")
    print(f"📂 Output dir: {out_dir}")

    # Call compare_metrics.py with py (preferred) or python
    cmd = [
        sys.executable, "notebooks/compare_metrics.py",
        "--baseline", str(baseline),
        "--psai", str(psai),
        "--out", str(out_dir),
        "--step", "5",
    ]
    print("▶ Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    # Print only the "Final Snapshot" from Markdown
    md_path = out_dir / "comparison_summary.md"
    if md_path.exists():
        lines = md_path.read_text(encoding="utf-8").splitlines()
        print("\n📑 --- Final Snapshot (Markdown) ---")
        capture = False
        for line in lines:
            if line.strip().startswith("## Final Snapshot"):
                capture = True
            elif line.strip().startswith("## Evolution"):
                capture = False
            if capture:
                print(line)
        print("📑 --- End of Final Snapshot ---\n")
        print(f"🔗 Full summary: {md_path}")
        print(f"🔗 Dashboard:   {out_dir / 'dashboard_comparison.html'}")
    else:
        print("⚠️ No Markdown summary found.")


if __name__ == "__main__":
    main()
