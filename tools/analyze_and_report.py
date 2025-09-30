import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Paths
run_dir = Path("runs/adam_eve")
metrics_path = run_dir / "metrics.csv"
report_path = run_dir / "REPORT.md"

print(f"Loading metrics from {metrics_path}")
df = pd.read_csv(metrics_path)

# Add digital_years if missing
if "digital_years" not in df.columns and "generation" in df.columns:
    df["digital_years"] = df["generation"] * 20

sns.set(style="whitegrid")

images = {}

# Population
if "alive" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="digital_years", y="alive", label="Alive")
    plt.title("Population over Digital Years")
    plt.xlabel("Digital Years")
    plt.ylabel("Alive (Population)")
    out = run_dir / "population_vs_years.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    images["population"] = out.name

# Energy
if "avg_energy" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="digital_years", y="avg_energy", label="Avg Energy", color="orange")
    plt.title("Average Energy over Digital Years")
    plt.xlabel("Digital Years")
    plt.ylabel("Average Energy")
    out = run_dir / "avg_energy_vs_years.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    images["energy"] = out.name

# Diversity
if "genetic_diversity" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="digital_years", y="genetic_diversity", label="Genetic Diversity", color="green")
    plt.title("Genetic Diversity over Digital Years")
    plt.xlabel("Digital Years")
    plt.ylabel("Genetic Diversity")
    out = run_dir / "diversity_vs_years.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    images["diversity"] = out.name

# Markdown summary
with open(report_path, "w") as f:
    f.write("# Simulation Report – Adam & Eve\n\n")
    f.write("## Key Metrics\n")
    f.write(f"- Generations: {df['generation'].max()}\n")
    f.write(f"- Final Population: {df['alive'].iloc[-1] if 'alive' in df.columns else 'n/a'}\n")
    f.write(f"- Final Avg Energy: {df['avg_energy'].iloc[-1] if 'avg_energy' in df.columns else 'n/a'}\n")
    f.write(f"- Final Diversity: {df['genetic_diversity'].iloc[-1] if 'genetic_diversity' in df.columns else 'n/a'}\n\n")
    f.write("## Plots\n")
    for label, img in images.items():
        f.write(f"### {label.capitalize()}\n")
        f.write(f"![{label}]({img})\n\n")

print(f"✅ Report saved to {report_path}")
