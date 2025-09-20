# LifeOS Skeleton

A minimal framework for simulating evolutionary and cognitive traits in a digital environment.  
This repo is intended as a starting point for experimenting with **digital genomes**, **lineages**, and **emergent behaviors** across multiple simulated worlds.

---

## 📂 Project Structure

```
lifeos_skeleton/
│
├── configs/              # YAML experiment configuration files
├── docs/                 # Documentation and notes
├── lifeos/               # Core framework modules
│   ├── genome.py
│   ├── lineage.py
│   ├── policy.py
│   ├── reproduction.py
│   ├── traits.py
│   ├── vault.py
│   └── ...
├── runs/                 # Saved outputs of experiments
├── tests/                # Pytest unit and integration tests
│   ├── test_genome.py
│   ├── test_lineage.py
│   ├── test_policy.py
│   ├── test_traits.py
│   ├── test_reproduction.py
│   ├── test_multiverse.py
│   ├── test_pipeline_small.py
│   ├── test_prime_map.py
│   └── test_vault.py
├── analyze_results.py    # Summarize run outputs
├── run_experiment.py     # Entry point for running experiments
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🚀 Quick Start

1. **Install dependencies**  
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Run a sample experiment**  
   ```bash
   python run_experiment.py --config configs/sample_small.yaml
   ```

3. **Analyze results**  
   ```bash
   python analyze_results.py
   ```

---

## 🧪 Running Tests

Unit and integration tests are provided with **pytest**.  

```bash
python -m pytest -q
```

---

## 📊 Example Output

After a successful run, results are saved in the `runs/` folder.  
For example:

```
runs/
└── EXP_20250919_092820_multiverse_smoke/
    ├── logs/
    ├── summary.csv
    └── checkpoints/
```

The `summary.csv` file contains diversity and energy metrics per world.

---

## 🛠 Features

- Digital genomes with configurable loci  
- Lineage tracking  
- Multiple scenarios (baseline, language, math, spiritual/communal)  
- Mutation and reproduction models  
- Configurable policies (rational, spiritual, etc.)  
- Test suite for validation and reproducibility  

---

## 📌 Roadmap

- Add richer trait libraries  
- Extend policies and decision models  
- Explore larger-scale multiverse experiments  
- Provide visualization tools for results  

---

## ⚖️ License

MIT License.  
Feel free to fork, extend, and experiment. Please retain attribution to the original project.  
