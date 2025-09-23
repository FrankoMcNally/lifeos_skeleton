# LifeOS Skeleton

LifeOS Skeleton is a modular simulation framework designed to explore evolutionary dynamics, digital traits, and multiverse experiments.  
This repo provides a clean starting point for experimentation, with utilities for stress testing, metrics analysis, and proof-of-concept demonstrations.

---

## 📂 Repository Layout

```
lifeos_skeleton/
├── configs/              # Example YAML experiment configs
│   ├── sample_small.yaml
│   ├── sample_medium.yaml
│   ├── sample_large.yaml
│   ├── stress_medium.yaml
│   ├── stress_large.yaml
│   └── stress_extreme.yaml
│
├── lifeos/               # Core simulation engine
│   ├── genome.py
│   ├── lineage.py
│   ├── traits.py
│   ├── reproduction.py
│   ├── policy.py
│   ├── artifacts.py
│   ├── metrics.py
│   ├── multiverse_engine.py
│   ├── prime_map.py
│   ├── vault.py
│   └── test_*.py
│
├── tests/                # Pytest-based test suite
│   ├── test_multiverse.py
│   ├── test_pipeline_small.py
│   ├── test_traits.py
│   └── ...
│
├── runs/                 # Auto-generated experiment outputs (ignored by Git)
│
├── analyze_results.py            # Basic metrics aggregation
├── analyze_results_extended.py   # Extended analysis + plots
├── monitor_resources.py          # Resource usage monitor
├── run_experiment.py             # CLI entrypoint for running experiments
├── QUICKSTART.md                 # Simple startup guide
├── TEST_REPORT.md                # Full test results and documentation
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## ⚠️ Important

Older versions of this repo had a **nested folder structure** (`lifeos_skeleton/lifeos_skeleton/`) which caused confusion.  
The current version uses a **single clean root layout** for simplicity.

---

## 🧪 Testing

Run the full test suite with:

```powershell
py -m pytest tests -v
```

All tests must pass before experiments can be launched.

---

## 🚀 Running Experiments

Example (small-scale test):

```powershell
py run_experiment.py --config configs/sample_small.yaml
```

Stress test (extreme):

```powershell
py run_experiment.py --config configs/stress_extreme.yaml
```

Outputs are written to `runs/EXP_*/` including:

- `metrics.csv`  
- `lineage.json`  
- `metrics.png` (if matplotlib installed)  

---

## 📊 Analysis

After running experiments, generate summary reports:

```powershell
py analyze_results.py --runs runs
py analyze_results_extended.py --runs runs
```

This produces:

- `summary.csv` – last generation metrics per run  
- `metrics.png` – plots of energy/diversity over time  
- Extended statistical breakdowns and visualizations

---

## 🖥️ Resource Monitoring

Track CPU, memory, and disk usage during stress tests:

```powershell
py monitor_resources.py
```

Outputs system logs to `runs/system_monitor.csv`.

---

## 📌 Proof of Concept

The repo demonstrates:

- Genome encoding/decoding  
- Trait mapping and diversity tracking  
- Policy-driven reproduction and lineage evolution  
- Stress test validation and monitoring  
- Automated analysis and reporting  

For details, see: **[TEST_REPORT.md](TEST_REPORT.md)**

---

## 📥 Installation

Dependencies:

```powershell
pip install -r requirements.txt
```

Recommended environment: **Python 3.10+** with **VS Code or PyCharm**.

---

## 📜 License

This project is released under the MIT License.
