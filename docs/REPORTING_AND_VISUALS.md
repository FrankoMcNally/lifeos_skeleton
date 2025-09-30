# Reporting & Visuals Guide

This document describes how to set up dependencies, run tests, generate reports, and visualize metrics produced by the **LifeOS Skeleton** framework.

---

## 1. Requirements

All dependencies are listed in `requirements.txt`.  
Install them with:

```powershell
py -m pip install -r requirements.txt
```

Additional visualization dependencies:

```powershell
py -m pip install seaborn networkx
```

> ✅ Note: We rely only on `networkx` for lineage visualization.  
> `pygraphviz` is **not required** — it can cause Windows build errors.  
> The built-in layouts in `networkx` (e.g., spring layout, shell layout) are sufficient.

---

## 2. Running Tests

Run the full suite:

```powershell
py -m pytest -v tests
```

Run specific Adam & Eve tests:

```powershell
py -m pytest -v tests/test_adam_eve.py
py -m pytest -v tests/test_adam_eve_free.py
```

Check that all tests pass ✅ before running large experiments.

---

## 3. Generating Reports

### Standard Runs
```powershell
py run_experiment.py --config configs/sample_small.yaml
```

### Adam & Eve Lineage
```powershell
py run_adam_eve.py --config configs/adam_eve.yaml
```

Each run saves artifacts in a `runs/<name>/` folder:
- `metrics.csv` — population, energy, diversity over generations
- `lineage.json` — ancestry tree
- `reproduction_events.json` — birth/death log
- `traits_loaded.json` — traits catalog
- `shared_memory.json` — collective event log

---

## 4. Metrics File (`metrics.csv`)

**Columns typically include:**
- `generation` → simulation generation
- `digital_years` → mapped years (`generation × 20`)
- `alive` → current population
- `avg_energy` → average energy per individual
- `genetic_diversity` → diversity score across genome

**Tip:** Always prefer `digital_years` for human-readable timelines.

---

## 5. Visualization Scripts

### A) Population, Energy, Diversity
Script: `visualize_report.py`

```powershell
py visualize_report.py
```

This plots:
- Alive (population)
- Avg Energy
- Genetic Diversity  
vs. Digital Years.

---

### B) Lineage Tree
Script: `visualize_lineage.py`

```powershell
py visualize_lineage.py
```

This builds a parent → child graph from `lineage.json` and saves:

```
runs/adam_eve/lineage_tree.png
```

⚠️ **Dependency Note:**  
We now use only `networkx`.  
If you previously tried `pygraphviz` and hit build errors, you can uninstall it:

```powershell
py -m pip uninstall pygraphviz -y
```

---

## 6. Jupyter Notebook (Optional)

For interactive exploration:

```powershell
py -m jupyter notebook
```

Open `analyze_run.ipynb` (or create one) and load CSVs:

```python
import pandas as pd
df = pd.read_csv("runs/adam_eve/metrics.csv")
df.head()
```

Add plots with `matplotlib` or `seaborn` inline.

---

## 7. Reports

Validated test reports are stored in `docs/`:
- `TEST_REPORT.md` — baseline validation
- `TEST_REPORT_ADAM_EVE.md` — lineage rules
- `TEST_REPORT_EXTREME.md` — stress tests
- `TEST_REPORT_SENTIENT.md` — Sentient MK7 integration

Each report corresponds to reproducible runs.

---

## 8. Reading the Metrics

- **Population stability** → check `alive` vs `digital_years`
- **Energy balance** → check if `avg_energy` trends upward or downward
- **Diversity** → stable diversity means healthy reproduction; collapse = bottleneck
- **Lineage** → expand `lineage.json` or view `lineage_tree.png` for ancestry depth

---

## ✅ Summary

- Install requirements (`pip install -r requirements.txt` + extras)  
- Run tests with pytest  
- Run experiments (`run_adam_eve.py`)  
- Visualize results with `visualize_report.py` and `visualize_lineage.py` (networkx only)  
- Explore interactively in Jupyter  
- Use `.md` test reports in `docs/` as validation records

This guide ensures any developer or researcher can reproduce your runs, read metrics, and visualize digital life in action.
