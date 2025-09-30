import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Path to your metrics file
csv_path = Path("runs/adam_eve/metrics.csv")
print(f"Loading {csv_path}")

# Load data
df = pd.read_csv(csv_path)

# If digital_years not present, create it (assuming 1 gen = 20 years)
if "digital_years" not in df.columns and "generation" in df.columns:
    df["digital_years"] = df["generation"] * 20

sns.set(style="whitegrid")
plt.figure(figsize=(12, 7))

# Plot population (alive)
if "alive" in df.columns:
    sns.lineplot(data=df, x="digital_years", y="alive", label="Alive (Population)")

# Plot average energy
if "avg_energy" in df.columns:
    sns.lineplot(data=df, x="digital_years", y="avg_energy", label="Avg Energy")

# Plot genetic diversity
if "genetic_diversity" in df.columns:
    sns.lineplot(data=df, x="digital_years", y="genetic_diversity", label="Genetic Diversity")

plt.title("LifeOS Adam & Eve – Metrics over Digital Years")
plt.xlabel("Digital Years")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.show()
