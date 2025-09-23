# LifeOS Skeleton

LifeOS is a DNA-inspired simulation framework for creating and evolving digital humans inside sandbox worlds.  
It provides a **genome → traits → behavior → reproduction → lineage** pipeline with pluggable policies and multiverse scenarios.

---

## Features

- **Genome / DNA framework** – flexible loci supporting float, int, and enum values  
- **Trait decoder** – maps raw DNA values into human-like traits  
- **Policies** – e.g. Rational or Spiritual, influence decisions ("eat", "rest", "explore")  
- **Reproduction & mutation** – genomes crossover and mutate over generations  
- **Lineage tracking** – all individuals traced to their ancestors  
- **Multiverse engine** – runs multiple worlds with different scenarios  
- **Experiment runner** – configure and run via YAML configs  
- **Metrics & artifacts** – population size, energy levels, diversity, lineage dumps  

---

## Repository Layout

lifeos_skeleton/
├── configs/ # Example YAML experiment configs
│ └── sample_small.yaml
├── lifeos/ # Core simulation engine
│ ├── genome.py
│ ├── traits.py
│ ├── lineage.py
│ ├── reproduction.py
│ ├── policy.py
│ ├── multiverse_engine.py
│ └── ...
├── tests/ # Pytest-based test suite
│ ├── test_multiverse.py
│ ├── test_pipeline_small.py
│ └── ...
├── runs/ # Auto-generated experiment outputs (ignored by Git)
├── run_experiment.py # CLI entrypoint for running experiments
├── analyze_results.py # Utility for visualizing experiment data
├── monitor_resources.py # Resource usage monitor for stress tests
├── requirements.txt
└── README.md

yaml
Copy code

⚠️ **Important:**  
Older versions of this repo had a **nested folder structure** (`lifeos_skeleton/lifeos_skeleton/`).  
This caused confusion and failing tests. The current version uses a **single clean root** layout.  

📌 **Note on `runs/`:**  
All experiment results (`runs/`) are excluded from version control (via `.gitignore`) to keep the repo lightweight.  
Generate your own by running experiments with the provided configs and analysis tools.

---

## Quick Start

### 1. Install dependencies

**Windows PowerShell** (recommended):

```powershell
py -m pip install -r requirements.txt
Linux / macOS / Git Bash:

bash
Copy code
python3 -m pip install -r requirements.txt
2. Run tests to verify install
Windows PowerShell:

powershell
Copy code
py -m pytest -v
Linux / macOS:

bash
Copy code
pytest -v
Expected: All tests should pass ✅

3. Run an experiment
powershell
Copy code
py run_experiment.py --config configs/sample_small.yaml
4. Analyze results
powershell
Copy code
py analyze_results.py --runs runs
This generates summary CSVs and PNG plots for each world.

Example Config (configs/sample_small.yaml)
yaml
Copy code
experiment_name: "multiverse_smoke"
seed: 123456
population_size: 200
generations: 200
mutation:
  per_locus_rate: 0.01
genome:
  loci:
    - name: cooperation
      type: float
      min: 0.0
      max: 1.0
    - name: curiosity
      type: float
      min: 0.0
      max: 1.0
scenarios:
  - name: "baseline"
    policy: "rational"
  - name: "spiritual_communal"
    policy: "spiritual"
What You Can Do
Simulate multiple civilizations in parallel

Explore different survival policies (rational vs spiritual)

Track genetic diversity across generations

Build evolutionary trees of digital humans

Roadmap
Visualization of sandbox worlds

Expanded policies (economic, cooperative, adversarial)

Integration with real-world DNA markers

Long-term multiverse experiments

Common Issues
pytest not found on Windows: Use py -m pytest -v instead.

Config file not found: Ensure the repo is in the updated single-root layout with configs/ directly inside the root.

Empty runs directory: Check that your config file is valid and experiment executed without errors.

Runs not in repo: By design, runs/ outputs are excluded. Generate fresh results locally.

Documentation & Community
Quickstart Guide

Contributing Guidelines

Changelog

Test Report

License
MIT License © 2025