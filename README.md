LifeOS Skeleton
LifeOS Skeleton is a modular framework for simulating evolving life systems.
It provides genome encoding, trait expression, policies, reproduction rules, lineage tracking, and multiverse experimentation.


Features
Genome encoding and decoding
Trait mapping and expression
Policy-driven decision making
Reproduction and lineage tracking
Multiverse experiments with configurable worlds
Stress-test ready (small → extreme)
Adam & Eve module extension for structured lineage testing
Prime Sentient AI (PSAI) hooks for future adaptive behavior


Installation
Clone the repo and install dependencies:

git clone https://github.com/FrankoMcNally/lifeos_skeleton.git

cd lifeos_skeleton

pip install -r requirements.txt


Quickstart
Run a small pipeline test:

py run_experiment.py --config configs/sample_small.yaml

Artifacts will appear under runs/:

metrics.csv
lineage.json


Adam & Eve Module
The Adam & Eve module extends LifeOS with structured reproduction rules:

12 founding couples (24 instances)
4 lifespan phases (elders survive beyond reproduction)
Reproduction in phase 2 only
Loyalty enforced (no incest, fixed couples)
Children capped (4–8 per couple)
Lineage traces back to original 12 couples
Kilobyte-scale memory per instance + shared pool
PSAI hooks for attraction and competence

Run it with:

py run_adam_eve.py --config configs/adam_eve.yaml

Outputs (in runs/):

metrics.csv
lineage.json
reproduction_events.json
traits_loaded.json


Stress Testing
Stress configs:

stress_medium.yaml (500 population, 200 generations)
stress_large.yaml (1000 population, 500 generations)
stress_extreme.yaml (2000 population, 1000 generations)

Run:

py run_experiment.py --config configs/stress_extreme.yaml

Resource usage is tracked via:

python monitor_resources.py

Results are summarized in:

runs/system_monitor.csv
TEST_REPORT.md
TEST_REPORT_ADAM_EVE.md


Test Reports
See the reports for detailed results:

TEST_REPORT.md – Stress tests, pipeline validation, system monitoring
TEST_REPORT_ADAM_EVE.md – Adam & Eve lineage module validation

Each report includes metrics snapshots directly in tables (no external PNGs needed).


Contributing
Contributions are welcome!

Fork the repo
Create a feature branch
Submit a pull request with clear description


License
MIT License © 2025 Frank McNally

