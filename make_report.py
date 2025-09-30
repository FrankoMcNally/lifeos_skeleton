import subprocess
import sys
from pathlib import Path
import argparse
import pandas as pd

def run(cmd):
    print(f"\n>>> Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def summarize_metrics(metrics_path: Path, output_md: Path):
    print(f"\n>>> Summarizing metrics from {metrics_path}")
    df = pd.read_csv(metrics_path)

    if "digital_years" not in df.columns and "generation" in df.columns:
        df["digital_years"] = df["generation"] * 20

    summary = []
    summary.append("# Latest Run Summary\n")
    summary.append(f"Source file: `{metrics_path}`\n")
    summary.append("## Key Stats\n")

    if "alive" in df.columns:
        summary.append(f"- Population (final): {df['alive'].iloc[-1]}")
        summary.append(f"- Population (max): {df['alive'].max()}")
        summary.append(f"- Population (min): {df['alive'].min()}")

    if "avg_energy" in df.columns:
        summary.append(f"- Avg Energy (final): {df['avg_energy'].iloc[-1]:.2f}")
        summary.append(f"- Avg Energy (mean): {df['avg_energy'].mean():.2f}")

    if "genetic_diversity" in df.columns:
        summary.append(f"- Diversity (final): {df['genetic_diversity'].iloc[-1]:.2f}")
        summary.append(f"- Diversity (mean): {df['genetic_diversity'].mean():.2f}")

    summary.append("\n## Timeline\n")
    summary.append(f"- Generations: {df['generation'].max()}")
    summary.append(f"- Digital Years: {df['digital_years'].max()}")

    output_md.write_text("\n".join(summary), encoding="utf-8")
    print(f"✅ Summary written to {output_md}")

def main():
    parser = argparse.ArgumentParser(description="Run LifeOS simulation pipeline with reporting.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to YAML config (e.g., configs/adam_eve.yaml or configs/stress_medium.yaml)"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    config_path = Path(args.config)
    run_name = config_path.stem  # e.g., adam_eve, stress_medium
    runs_dir = repo_root / "runs" / run_name

    # 1. Run tests
    run("pytest -v tests")

    # 2. Run chosen experiment
    run(f"py run_experiment.py --config {config_path}")

    # 3. Generate metrics report plots
    run("py visualize_report.py")

    # 4. Generate lineage tree PDF (only if adam_eve run)
    lineage_json = runs_dir / "lineage.json"
    if lineage_json.exists():
        run("py visualize_lineage_pdf.py")

    # 5. Summarize metrics into Markdown
    metrics_path = runs_dir / "metrics.csv"
    output_md = repo_root / "docs" / f"LATEST_RUN_{run_name.upper()}.md"
    summarize_metrics(metrics_path, output_md)

    print("\n✅ Full pipeline complete!")
    print(f"Artifacts in {runs_dir}:")
    print("- metrics.csv")
    if lineage_json.exists():
        print("- lineage.json")
        print("- lineage_tree.pdf (zoomable tree)")
    print("- metrics_plot.png (population/energy/diversity)")
    print(f"\n📑 Summary available at {output_md}")

if __name__ == "__main__":
    main()
