changelog = """\
# Changelog

All notable changes to this project will be documented in this file.

---

## [2025-09-30] – Requirements Update

### Added
- **pandas>=2.0** added to `requirements.txt` to support CSV handling and
  timeline mapping in `analyze_and_report.py`.
- Ensures all analysis/report scripts run without missing dependency errors.

### Notes
- Developers should reinstall dependencies with:
  `py -m pip install -r requirements.txt`

---

## [2025-09-29] – SentientMind MK7 Integration

### Added
- Upgraded **sentient_mk6.py** to embed **MK7 architecture** while preserving
  MK6 compatibility:
  - Layered states: energy, curiosity, competence, social_bond, stress.
  - Subconscious buffers: dreams and memory_trace.
  - Partner selection (`choose_partner`) based on cooperation + energy.
  - Memory consolidation adjusting stress (death events) and curiosity (birth events).
- Verified that all **Adam & Eve tests** (`test_adam_eve.py`, `test_adam_eve_free.py`)
  pass unmodified with MK7 agent in place.
- Produced new test report: `TEST_REPORT_SENTIENT.md`.

### Changed
- **decide_actions** reworked to return MK6-compatible `[{"type": ..., ...}]`
  while leveraging MK7 behaviors internally.
- Farming, sleep, and share actions now probabilistic and influenced by
  agent state rather than fixed heuristics.
- Dreams increase curiosity dynamically; stress adjusted by lineage events.

### Notes
- First stable baseline with **Sentient AI integration** into LifeOS Skeleton.
- Population and diversity metrics confirm functional multi-generation runs.
- Provides foundation for side-by-side MK6 vs MK7 comparative studies.

---

## [2025-09-22] – Stress Tests & Monitoring Validation

### Added
- Conducted **stress test experiments** with configurations:
  - `stress_medium.yaml`
  - `stress_large.yaml`
  - `stress_extreme.yaml`  
- Verified outputs for multiple worlds (`baseline`, `spiritual_communal`, `adaptive`, `competitive`).  
- Integrated **resource monitoring (`monitor_resources.py`)** to track CPU and memory usage during extreme runs.  
- Added `analyze_results_extended.py` for deeper aggregate analysis across experiments.

### Fixed
- Addressed issues with missing `psutil` dependency.  
- Confirmed compatibility with `matplotlib` for metrics visualization.

### Notes
- Stress test proof-of-concept confirms the framework scales to high population and generation counts.  
- Monitoring and extended analysis scripts are now part of the repo for reproducible validation.
"""
print(changelog)
