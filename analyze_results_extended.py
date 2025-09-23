#!/usr/bin/env python3
"""
Extended analysis of LifeOS runs.
Generates:
- Per-world plots of all metrics over generations
- Global comparison plots per experiment
- Stress comparison plots across experiments
- Summary CSV with last/avg/min/max values
- test_report.md with human-readable summary and links to plots
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Dict, List
import statistics

def read_metrics_csv(path: Path) -> Dict[str, List[float]]:
    """
    Read metrics.csv into {column: list of values}
    Assumes 'generation' column exists.
    """
    data: Dict[str, List[float]] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, val in row.items():
                if key not in data:
                    data[key] = []
                try:
                    data[key].append(float(val))
                except ValueError:
                    data[key].append(float("nan"))
    return data

def safe_plot(x, ys: Dict[str, List[float]], labels: List[str], title: str, out_png: Path):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    plt.figure(figsize=(7, 4.5))
    for key in labels:
        if key in ys and x:
            plt.plot(x, ys[key], label=key)
    plt.xlabel("generation")
    plt.ylabel("value")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png)
    plt.close()

def summarize_metrics(data: Dict[str, List[float]]) -> Dict[str, str]:
    summary = {}
    for key, values in data.items():
        if not values:
            continue
        try:
            clean_vals = [v for v in values if v == v]  # drop NaNs
            if not clean_vals:
                continue
            summary[f"{key}_last"] = f"{clean_vals[-1]:.3f}"
            summary[f"{key}_mean"] = f"{statistics.mean(clean_vals):.3f}"
            summary[f"{key}_min"] = f"{min(clean_vals):.3f}"
            summary[f"{key}_max"] = f"{max(clean_vals):.3f}"
        except Exception:
            continue
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs", help="Path to runs/ directory")
    args = ap.parse_args()

    runs_dir = Path(args.runs)
    assert runs_dir.exists(), f"Runs dir not found: {runs_dir}"

    summary_rows: List[Dict[str, str]] = []
    report_lines: List[str] = ["# LifeOS Stress Test Report\n"]

    # Loop through experiments
    for exp in sorted(runs_dir.glob("EXP_*")):
        if not exp.is_dir():
            continue
        exp_name = exp.name
        report_lines.append(f"\n## Experiment {exp_name}\n")

        # Per-world
        for world_dir in sorted(exp.iterdir()):
            if not world_dir.is_dir():
                continue
            metrics_csv = world_dir / "metrics.csv"
            if not metrics_csv.exists():
                continue

            data = read_metrics_csv(metrics_csv)
            if "generation" not in data:
                continue

            generations = [int(g) for g in data["generation"]]

            # Plot per world
            out_png = world_dir / "metrics.png"
            safe_plot(generations, data, [k for k in data if k != "generation"], world_dir.name, out_png)

            # Summarize
            summary = {"experiment": exp_name, "world": world_dir.name}
            summary.update(summarize_metrics(data))
            summary_rows.append(summary)

            report_lines.append(f"- **{world_dir.name}**: last gen = {generations[-1]}, metrics saved → `{out_png.name}`")

        # Global overlay for experiment
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8, 5))
            for world_dir in sorted(exp.iterdir()):
                metrics_csv = world_dir / "metrics.csv"
                if not metrics_csv.exists():
                    continue
                data = read_metrics_csv(metrics_csv)
                if "generation" in data and "avg_energy" in data:
                    plt.plot(data["generation"], data["avg_energy"], label=world_dir.name)
            plt.xlabel("generation")
            plt.ylabel("avg_energy")
            plt.title(f"Energy Comparison – {exp_name}")
            plt.legend()
            plt.tight_layout()
            out_png = exp / "comparison_energy.png"
            plt.savefig(out_png)
            plt.close()
            report_lines.append(f"Global energy comparison saved → `{out_png}`")
        except Exception:
            pass

    # Write summary.csv
    if summary_rows:
        out_csv = runs_dir / "summary_extended.csv"
        fieldnames = sorted({k for row in summary_rows for k in row.keys()})
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in summary_rows:
                w.writerow(row)
        report_lines.append(f"\nSummary CSV saved → `{out_csv}`")

    # Write markdown report
    out_md = runs_dir / "test_report.md"
    with out_md.open("w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"Wrote extended report: {out_md}")

if __name__ == "__main__":
    main()
