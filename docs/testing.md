"""
Testing the Adam & Eve Simulation 🧪
===================================

This project includes both baseline **LifeOS Skeleton tests** and the **Adam & Eve lineage extension tests**.  
Tests are designed to validate that DNA, pairing rules, reproduction, environment, and shared memory all work together.

---

Windows Users ⚠️ (important)
----------------------------

### Running Tests
On Windows, **always use `py` instead of `python`** when invoking test scripts.  
Otherwise you may see errors like:

    'python' is not recognized as an internal or external command

or  

    No module named pytest

### Run all tests
    py -m pytest -v tests

### Run only Adam & Eve tests
    py -m pytest -v tests/test_adam_eve.py
    py -m pytest -v tests/test_adam_eve_free.py

---

Linux / macOS Users
-------------------

### Run all tests
    python3 -m pytest -v tests

### Run only Adam & Eve tests
    python3 -m pytest -v tests/test_adam_eve.py
    python3 -m pytest -v tests/test_adam_eve_free.py

---

Test Artifacts
--------------

Each run saves artifacts under `runs/`:

- `metrics.csv` — population, births, deaths, energy, food, oxygen
- `lineage.json` — family tree
- `reproduction_events.json` — birth/death logs
- `traits_loaded.json` — trait catalog (if used)
- `shared_memory.json` — global memory log

---

Known Hurdles (Documented)
---------------------------

- **`py` vs `python` on Windows**: Always use `py` in commands.
- **Missing pytest**: Install with `py -m pip install pytest`.
- **Import errors (`lifeos.adam_eve_engine` not found)**: Run from the repo root (`lifeos_skeleton/`), not from inside the `tests/` folder.
- **Shared memory attribute mismatch**: Ensure you’ve updated `adam_eve_memory.py` and `adam_eve_engine.py` with `capacity_bytes` and `used_bytes` fixes.

---

✅ If all tests pass, you’ll see output like:

    collected 14 items
    14 passed in 0.55s

At that point, the Adam & Eve module is considered **validated** and safe for larger runs.
"""
