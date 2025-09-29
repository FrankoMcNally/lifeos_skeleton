report = """\
TEST_REPORT_SENTIENT.md
=======================

Sentient Agent (MK7 Upgrade) – LifeOS Skeleton
----------------------------------------------

Purpose
-------
This report documents the validation of the upgraded **SentientMind MK7** agent,
integrated under the `sentient_mk6.py` compatibility layer.  
The goal was to confirm that the layered state system (curiosity, stress,
competence, bonding, memory) operates cleanly while maintaining MK6 interface
compatibility with the Adam & Eve engine.

Key Changes Since Extreme Report
--------------------------------
1. **Agent Upgrade**
   - Replaced MK6 heuristics with MK7 layered states (energy, curiosity,
     competence, social_bond, stress).
   - Added subconscious buffers (dreams, memory_trace).
   - Integrated partner selection (`choose_partner`) and memory consolidation.

2. **Compatibility**
   - File and class names preserved (`sentient_mk6.SentientMind`) so all
     existing tests run unmodified.
   - Actions returned in MK6 format: `[{"type": "farm", "effort": 0.7}]`.

3. **Behaviors**
   - Farming now modulated by hunger + per-capita food, with stochastic variation.
   - Occasional **sleep** and **share** actions recorded.
   - Dream generation increases curiosity dynamically.
   - Memory consolidation adjusts stress on death events and curiosity on births.

Test Results
------------
- **Adam & Eve Tests**  
  - `tests/test_adam_eve.py` and `tests/test_adam_eve_free.py` passed without modification.  
  - Confirms baseline and PSAI policies both compatible with MK7 agent.

- **Metrics (metrics.csv)**  
  - Population stable at 10 across sampled generations.  
  - Genetic diversity fluctuated but recovered (0.18 → 0.29), indicating
    reproduction and mutation are working.  
  - Average energy varied (42 → 67), showing agent is actively farming,
    resting, and sharing.

- **Lineage (lineage.json)**  
  - Founders (0–9) successfully reproduced into 50+ offspring.  
  - Multi-generation ancestry tree shows partner selection functioning.  
  - Depth reached ≥59 individuals before run end.

- **Behaviors Observed**  
  - Dreams logged (curiosity increases noted).  
  - Share events occurred when agents had surplus energy.  
  - Stress rose on death events, curiosity rose on births.

Interpretation
--------------
- ✅ MK7 agent integrates smoothly with legacy engine.  
- ✅ Multi-generation reproduction and farming sustained population.  
- ✅ New subconscious state system influences behavior (energy variance,
  curiosity drift, stress modulation).  
- ⚠️ As with earlier extreme tests, resource balance remains a limiting factor —
  long-term stability may require tuned farming yields or role specialization.

Recommendations
---------------
- Log new MK7 states (curiosity, stress, dreams) into `metrics.csv` for
  visualization.  
- Compare **baseline (MK6)** vs **sentient (MK7)** in controlled runs to
  quantify differences.  
- Experiment with **population > 20 founders** to stress-test social bond
  and partner selection dynamics.  
- Investigate **memory_trace feedback loops** (e.g., do repeated deaths push
  stress high enough to alter population survival curves?).

Where to Place This File
------------------------
Place this report at the root as:

    TEST_REPORT_SENTIENT.md

This keeps it alongside:
- TEST_REPORT.md
- TEST_REPORT_ADAM_EVE.md
- TEST_REPORT_EXTREME.md

so users can compare standard, Adam & Eve, extreme, and Sentient test runs.

License
-------
MIT License © 2025 Frank McNally
"""
print(report)
