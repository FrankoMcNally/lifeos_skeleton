# LifeOS Skeleton

LifeOS Skeleton is a modular framework for simulating evolving life systems.  
It combines **genome-driven evolution**, **structured lineage rules**, and a newly
integrated **Sentient AI agent (MK7)** into a single testable engine.  

The framework is designed for **research, experimentation, and stress testing**:
from small proof-of-concept runs to extreme multiverse scenarios.

---

## ✨ Features

- **Genome Encoding & Trait Expression**  
  Encode DNA, map to traits, and track their expression over generations.

- **Sentient Agent (MK7)**  
  - Layered states: energy, curiosity, competence, social bond, stress.  
  - Subconscious buffers: dreams and memory trace.  
  - PSAI partner selection (cooperation + energy weighted).  
  - Drop-in compatible with legacy MK6 interface.  

- **Policy-Driven Decisions**  
  Agents farm, rest, share, and forage based on hunger, resources, and
  subconscious state.

- **Lineage & Reproduction Rules**  
  Track ancestry across generations with configurable caps, loyalty enforcement,
  and phase-based reproduction.

- **Testing & Reporting Module**  
  - Standard tests (`docs/TEST_REPORT.md`).  
  - Adam & Eve lineage validation (`docs/TEST_REPORT_ADAM_EVE.md`).  
  - Extreme stress tests (`docs/TEST_REPORT_EXTREME.md`).  
  - Sentient validation (`docs/TEST_REPORT_SENTIENT.md`).  

- **Multiverse Experiments**  
  Run multiple configurations (`baseline`, `psai`, `adaptive`, `competitive`)
  across stress levels.

- **Resource Monitoring**  
  `monitor_resources.py` tracks CPU & memory usage for heavy runs.

- **Time Mapping**  
  Each run now includes a `digital_years` column in `metrics.csv`:  
  ```
  digital_years = generation × 20
  ```
  This maps generations to a human-readable timeline.

---

## ⚡ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/FrankoMcNally/lifeos_skeleton.git
cd lifeos_skeleton
pip install -r requirements.txt
```

---

## 🚀 Quickstart

Run a small pipeline test:

```bash
py run_experiment.py --config configs/sample_small.yaml
```

Artifacts will appear under `runs/`:

- `metrics.csv` – population, energy, diversity, **digital years**  
- `lineage.json` – ancestry tree  
- `reproduction_events.json` – birth/death logs  

---

## 🌱 Adam & Eve Module

Structured lineage simulation with 12 founding couples:

- 4 lifespan phases (elders survive beyond reproduction)  
- Reproduction in phase 2 only  
- Loyalty enforced (no incest, fixed couples)  
- Children capped (4–8 per couple)  
- Lineage traces back to original couples  
- Individual + shared memory pools  
- PSAI hooks for attraction and competence  

Run it with:

```bash
py run_adam_eve.py --config configs/adam_eve.yaml
```

Outputs (in `runs/`):

- `metrics.csv`  
- `lineage.json`  
- `reproduction_events.json`  
- `traits_loaded.json`  

---

## 🔥 Stress Testing

Stress configs:

- `stress_medium.yaml` (500 population, 200 generations)  
- `stress_large.yaml` (1000 population, 500 generations)  
- `stress_extreme.yaml` (2000 population, 1000 generations)  

Run:

```bash
py run_experiment.py --config configs/stress_extreme.yaml
```

Track system usage:

```bash
python monitor_resources.py
```

Outputs:

- `runs/system_monitor.csv`  
- `docs/TEST_REPORT_EXTREME.md`  

---

## 📑 Test Reports

All test reports are now organized under the `docs/` folder:

- [`docs/TEST_REPORT.md`](docs/TEST_REPORT.md) – Standard validation  
- [`docs/TEST_REPORT_ADAM_EVE.md`](docs/TEST_REPORT_ADAM_EVE.md) – Adam & Eve structured lineage  
- [`docs/TEST_REPORT_EXTREME.md`](docs/TEST_REPORT_EXTREME.md) – Extreme stress tests  
- [`docs/TEST_REPORT_SENTIENT.md`](docs/TEST_REPORT_SENTIENT.md) – Sentient MK7 integration results  

Each report includes metrics (with `digital_years`), lineage snapshots, and reproduction logs.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo  
2. Create a feature branch  
3. Submit a pull request with a clear description  

---

## 📜 License

MIT License © 2025 Frank McNally
