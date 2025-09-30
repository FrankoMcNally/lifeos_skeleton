import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# Path to lineage file
lineage_path = Path("runs/adam_eve/lineage.json")
print(f"Loading lineage from {lineage_path}")

with open(lineage_path, "r") as f:
    lineage = json.load(f)

# Build graph
G = nx.DiGraph()

for child, parents in lineage.items():
    # Ensure child is a string (networkx prefers string nodes)
    child_str = str(child)
    G.add_node(child_str)

    if parents:  # skip NoneType
        for parent in parents:
            if parent is not None:
                G.add_edge(str(parent), child_str)

# Layout and plot
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

nx.draw(
    G, pos,
    with_labels=True,
    node_size=500,
    node_color="lightblue",
    arrowsize=10,
    font_size=8
)

plt.title("Lineage Tree (Parents → Children)", fontsize=14)
out_path = "runs/adam_eve/lineage_tree.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ Saved lineage tree to {out_path}")
