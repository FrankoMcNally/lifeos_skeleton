import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# === Paths ===
run_dir = Path("runs/adam_eve")
lineage_path = run_dir / "lineage.json"
png_path = run_dir / "lineage_tree.png"
pdf_path = run_dir / "lineage_tree.pdf"

print(f"Loading lineage from {lineage_path}")

with open(lineage_path, "r") as f:
    lineage = json.load(f)

# Build directed graph
G = nx.DiGraph()
for child, parents in lineage.items():
    child_str = str(child)
    G.add_node(child_str)
    if parents:
        for parent in parents:
            if parent is not None:
                G.add_edge(str(parent), child_str)

# Layout
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
plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"✅ PNG saved to {png_path}")

# Save PNG into PDF
c = canvas.Canvas(str(pdf_path), pagesize=A4)
width, height = A4
c.drawImage(str(png_path), 30, 150, width-60, height-200)  # fit nicely on A4
c.showPage()
c.save()
print(f"✅ PDF saved to {pdf_path}")
