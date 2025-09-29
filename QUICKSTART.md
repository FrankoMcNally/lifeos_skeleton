"""
Quickstart Guide – LifeOS Skeleton
==================================

This is the short reference for getting started quickly with LifeOS.
For full details, see the main README.md.


1. Install Dependencies
------------------------
Windows (PowerShell):
    py -m pip install -r requirements.txt

Linux / macOS / Git Bash:
    python3 -m pip install -r requirements.txt


2. Verify Installation
------------------------
Windows (PowerShell):
    py -m pytest -v

Linux / macOS:
    pytest -v

Expected: All tests should pass ✅


3. Run Your First Experiment
------------------------------
Windows:
    py run_experiment.py --config configs/sample_small.yaml

Linux / macOS:
    python3 run_experiment.py --config configs/sample_small.yaml

Output: runs/EXP_<timestamp>_sample_small/ with:
    • metrics.csv → diversity & energy per generation
    • lineage.json → ancestry tree


4. Adam & Eve Module
----------------------
Windows:
    py run_adam_eve.py --config configs/adam_eve_free.yaml

Linux / macOS:
    python3 run_adam_eve.py --config configs/adam_eve_free.yaml

Output: runs/ADAM_EVE_<timestamp>_<name>/ with:
    • metrics.csv
    • lineage.json
    • reproduction_events.json
    • traits_loaded.json
    • shared_memory.json


5. Next Steps
---------------
    • Edit configs in /configs to design new worlds
    • Explore traits, mutation rates, and policies
    • Track population survival and adaptation across generations


Common Issues
---------------
    • "pytest not found" on Windows → use `py -m pytest -v` instead.
    • "Config file not found" → ensure configs/ is in the project root.
    • Empty runs directory → check config validity and rerun experiment.
    • Windows users → always use `py` instead of `python` when running scripts.


🎯 That’s it — you’re up and running!
"""
