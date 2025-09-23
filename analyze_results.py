#!/usr/bin/env python3
"""
Aggregate metrics from runs/*/*/metrics.csv
- Per world: save a line plot of avg_energy and genetic_diversity vs generation
- Global summary: write runs/summary.csv with last-gen metrics per world per EXP
If matplotlib isn't installed, it will still write the CSV summary.

Usage:
  py analyze_results.py --runs runs
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple

def read_metrics_csv(path: Path) -> Tuple[List[int], List[float], List[float]]:
    gens, energy, diversity = [], [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                gens.append(int(row["generation"]))
                energy.append(float(row["avg_energy"]))
                diversity.append(float(row["genetic_diversity"]))
            except (KeyError, ValueError):
                # skip malformed rows
                continue
    return gens, energy, diversity

def plot_world(out_png: Path, gens: List[int], energy: List[float], diversity: List[float]) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return  # plotting optional: silently skip if matplotlib missing

    plt.figure(figsize=(7,4.5))
    if gens:
        plt.plot(gens, energy, label="avg_energy")
        plt.plot(gens, diversity, label="genetic_diversity")
    plt.xlabel("generation")
    plt.ylabel("value")
    plt.title(out_png.parent.name)  # world name
    plt.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs", help="Path to runs/ directory")
    args = ap.parse_args()

    runs_dir = Path(args.runs)
    assert runs_dir.exists(), f"Runs dir not found: {runs_dir}"

    # Summary rows: exp_name, world, last_generation, last_avg_energy, last_diversity
    summary_rows: List[Dict[str, str]] = []

    # Scan EXP_* folders
    for exp in sorted(runs_dir.glob("EXP_*")):
        if not exp.is_dir():
            continue
        # Each subfolder is a world, with metrics.csv
        for world_dir in sorted(exp.iterdir()):
            if not world_dir.is_dir():
                continue
            metrics_csv = world_dir / "metrics.csv"
            if not metrics_csv.exists():
                continue

            gens, energy, diversity = read_metrics_csv(metrics_csv)

            # Save a PNG chart per world (optional; skips if matplotlib not present)
            out_png = world_dir / "metrics.png"
            plot_world(out_png, gens, energy, diversity)

            # Add last generation snapshot to summary
            if gens:
                summary_rows.append({
                    "experiment": exp.name,
                    "world": world_dir.name,
                    "last_generation": str(gens[-1]),
                    "last_avg_energy": f"{energy[-1]:.3f}",
                    "last_genetic_diversity": f"{diversity[-1]:.6f}",
                    "metrics_png": str(out_png.relative_to(runs_dir)) if out_png.exists() else "",
                })

    # Write summary CSV
    if summary_rows:
        out_csv = runs_dir / "summary.csv"
        fieldnames = list(summary_rows[0].keys())
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in summary_rows:
                w.writerow(row)
        print(f"Wrote summary: {out_csv}")
    else:
        print("No metrics found in runs/*/*/metrics.csv")

if __name__ == "__main__":
    main()
