# Running Simulations & Reports – Quick Reference

This guide shows how to run simulations, generate metrics, and analyze results
in the **LifeOS Skeleton** framework.

---

## 1. Verify Codebase (Pytest)

Run **all unit/integration tests** to confirm the framework is healthy:

```powershell
py -m pytest -v
```

- Runs every `test_*.py` in the repo (`tests/` + root).  
- No simulation data generated — just pass/fail checks.  
- ✅ Run this before any major experiment.

---

## 2. Run Simulations

### Adam & Eve World
Couple-based reproduction with lineage rules:

```powershell
py run_adam_eve.py --config configs/adam_eve.yaml
```

Outputs in `runs/adam_eve/`:
- `metrics.csv`
- `lineage.json`
- `reproduction_events.json`
- `traits_loaded.json`
- `shared_memory.json`

---

### General Experiments
Baseline or multiverse simulations:

```powershell
py run_experiment.py --config configs/sample_small.yaml
py run_experiment.py --config configs/sample_large.yaml
```

Outputs in `runs/<name>/`.

---

### Stress Tests
Scale to large populations and generations:

```powershell
py run_experiment.py --config configs/stress_medium.yaml
py run_experiment.py --config configs/stress_large.yaml
py run_experiment.py --config configs/stress_extreme.yaml
```

Outputs in `runs/<stress-level>/`.

---

## 3. Analyze & Report

### Automated Analysis
Read metrics, produce plots, generate summaries:

```powershell
py analyze_and_report.py
py analyze_results.py
```

Requires: `pandas`, `matplotlib`, `seaborn`.

---

### Visualization Scripts

#### Population, Energy, Diversity
```powershell
py visualize_report.py
```
- Reads `runs/adam_eve/metrics.csv`.  
- Plots alive (population), avg energy, diversity vs. digital years.

#### Lineage Tree
```powershell
py visualize_lineage.py
```
- Reads `runs/adam_eve/lineage.json`.  
- Produces `runs/adam_eve/lineage_tree.png`.  
- Uses **networkx** (no pygraphviz required).

---

## 4. Jupyter Interactive Analysis (Optional)

```powershell
py -m jupyter notebook
```

Inside VS Code or browser:
- Open `analyze_run.ipynb` (or create one).  
- Load `metrics.csv`:
  ```python
  import pandas as pd
  df = pd.read_csv("runs/adam_eve/metrics.csv")
  df.head()
  ```
- Plot with `matplotlib` or `seaborn`.  

---

## ✅ Workflow Summary

1. Run pytest → make sure everything passes.  
2. Run simulations → generate metrics & lineage in `runs/`.  
3. Run analysis/report scripts → visualize results.  
4. (Optional) Explore interactively in Jupyter.  

---
