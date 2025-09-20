# LifeOS Skeleton

A minimal but extensible framework for simulating **evolutionary and cognitive traits** in a digital environment.  
This repo provides the **core building blocks** for experimenting with digital genomes, lineages, traits, and multiverse-style simulations.

---

## 🚀 Features

- **Core Modules**
  - `genome.py`: defines digital genomes and traits
  - `lineage.py`: tracks ancestry and reproduction
  - `multiverse.py`: manages multiple evolving environments
  - `metrics.py`: collects simulation statistics
  - `traits.py`: configurable behavioral traits
  - `policy.py`: strategy and decision-making policies

- **Experiment Configurations**
  - YAML configs under `configs/` (e.g. `sample_small.yaml`) to define population size, mutation rates, policies, and scenarios.

- **Testing & Validation**
  - Full test suite under `tests/`
  - Includes pipeline tests (config + run) to validate reproducibility
  - CI-friendly structure for future automation

- **Reproducibility**
  - Deterministic seeds (`configs/sample_small.yaml`)
  - Results written to structured `runs/` folders (auto-ignored by Git)

---

## 🧬 Vision

This skeleton is the **first step** toward building **DNA-inspired digital beings** that can evolve and interact in a **multiverse sandbox**.  
The long-term goal is to explore:
- How digital organisms adapt across simulated generations  
- Emergent behaviors (cooperation, curiosity, creativity)  
- Sandbox universes where structured language, mathematics, and spirituality can be introduced as catalysts for evolution  

Think of this repo as **LifeOS v0.1** — a foundation on which more advanced simulations will grow.

---

## 📂 Project Structure

```
lifeos_skeleton/
│
├── lifeos/                 # Core simulation modules
│   ├── genome.py
│   ├── lineage.py
│   ├── multiverse.py
│   ├── traits.py
│   ├── policy.py
│   └── ...
│
├── configs/                # Example experiment configs
│   └── sample_small.yaml
│
├── tests/                  # Unit & pipeline tests
├── runs/                   # Experiment outputs (ignored in Git)
│
├── README.md               # Project overview
├── requirements.txt        # Dependencies
├── LICENSE.md              # MIT License
└── CONTRIBUTING.md         # Guidelines for contributors
```

---

## ⚡ Quickstart

1. Clone the repo:
   ```bash
   git clone https://github.com/FrankoMcNally/lifeos_skeleton.git
   cd lifeos_skeleton
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests to verify setup:
   ```bash
   pytest -q
   ```

4. Run a sample experiment:
   ```bash
   python run_experiment.py --config configs/sample_small.yaml
   ```

---

## 📈 Example Output

- Simulation logs and metrics will be saved under `runs/EXP_<timestamp>_multiverse_smoke/`
- Includes:
  - `lineage.json`: ancestry data
  - `metrics.csv`: performance and trait statistics
  - `config.yaml`: snapshot of experiment parameters

---

## 🛠 Roadmap

- [ ] Add richer trait models (language, rhythm, problem-solving)
- [ ] Extend multiverse sandbox with parallel universes
- [ ] Track emergent behaviors across thousands of generations
- [ ] Provide visualization tools for family trees and evolution
- [ ] Connect with DNA-inspired Prime Path & Tri-Linear frameworks

---

## 🤝 Contributing

Contributions, ideas, and extensions are welcome!  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the MIT License.  
See [LICENSE.md](LICENSE.md) for details.

---

> **LifeOS Skeleton** is the seed of a bigger journey — evolving digital beings, one trait at a time.
