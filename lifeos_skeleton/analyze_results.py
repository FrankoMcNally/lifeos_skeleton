# analyze_results.py
from __future__ import annotations
from pathlib import Path
import csv, sys, time

def find_latest_run(runs_dir: Path) -> Path:
    candidates = [p for p in runs_dir.iterdir() if p.is_dir() and p.name.startswith("EXP_")]
    if not candidates:
        raise SystemExit("No runs found. Run the experiment first.")
    # pick by most recent mtime
    return max(candidates, key=lambda p: p.stat().st_mtime)

def read_metrics(csv_path: Path):
    rows = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            # convert numbers if present
            for k in ["generation", "population", "genetic_diversity", "avg_energy"]:
                if k in row and row[k] != "":
                    try:
                        row[k] = float(row[k])
                    except ValueError:
                        pass
            rows.append(row)
    # sort by generation just in case
    rows.sort(key=lambda x: x.get("generation", 0))
    return rows

def summarize_world(world_dir: Path):
    mfile = world_dir / "metrics.csv"
    if not mfile.exists():
        return None
    rows = read_metrics(mfile)
    if not rows:
        return None
    first = rows[0]
    last = rows[-1]
    gens = int(last.get("generation", 0) - first.get("generation", 0))
    div_first = float(first.get("genetic_diversity", 0.0))
    div_last  = float(last.get("genetic_diversity", 0.0))
    div_trend = div_last - div_first
    eng_first = float(first.get("avg_energy", 0.0))
    eng_last  = float(last.get("avg_energy", 0.0))
    eng_trend = eng_last - eng_first
    return {
        "world": world_dir.name,
        "generations": gens,
        "diversity_first": round(div_first, 6),
        "diversity_last":  round(div_last, 6),
        "diversity_change": round(div_trend, 6),
        "energy_first": round(eng_first, 3),
        "energy_last":  round(eng_last, 3),
        "energy_change": round(eng_trend, 3),
    }

def main():
    root = Path(".")
    runs_dir = root / "runs"
    run_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else find_latest_run(runs_dir)

    print(f"\nAnalyzing run: {run_dir.resolve()}\n")
    summaries = []
    for world_dir in sorted([p for p in run_dir.iterdir() if p.is_dir()]):
        s = summarize_world(world_dir)
        if s:
            summaries.append(s)

    if not summaries:
        raise SystemExit("No world summaries found.")

    # print pretty table
    print(f"{'World':22} {'Gens':>4}   {'Div (first → last | Δ)':30}   {'Energy (first → last | Δ)'}")
    print("-"*90)
    for s in summaries:
        div_str = f"{s['diversity_first']:.4f} → {s['diversity_last']:.4f} | {s['diversity_change']:+.4f}"
        eng_str = f"{s['energy_first']:.1f} → {s['energy_last']:.1f} | {s['energy_change']:+.1f}"
        print(f"{s['world']:22} {s['generations']:>4}   {div_str:30}   {eng_str}")

    # write summary.csv
    out_csv = run_dir / "summary.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        fieldnames = list(summaries[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for s in summaries:
            w.writerow(s)
    print(f"\nSaved: {out_csv.resolve()}\n")

if __name__ == "__main__":
    main()
