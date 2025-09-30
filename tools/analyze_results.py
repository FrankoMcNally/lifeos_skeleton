import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

run_dir = Path("runs/adam_eve")
metrics_path = run_dir / "metrics.csv"
lineage_path = run_dir / "lineage.json"

print(f"Loading {metrics_path}")
df = pd.read_csv(metrics_path)

# Add digital_years if missing
if "digital_years" not in df.columns and "generation" in df.columns:
    df["digital_years"] = df["generation"] * 20

print("\n=== Metrics Summary ===")
print(df.describe())

# Quick population plot
if "alive" in df.columns:
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="digital_years", y="alive", label="Alive")
    plt.title("Population Trend")
    plt.savefig(run_dir / "quick_population.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ Saved quick_population.png")

# Load lineage (if available)
if lineage_path.exists():
    with open(lineage_path, "r") as f:
        lineage = json.load(f)
    print("\n=== Lineage Stats ===")
    print(f"Total individuals: {len(lineage)}")
    founders = [k for k, v in lineage.items() if not v]
    print(f"Founders: {len(founders)}")
