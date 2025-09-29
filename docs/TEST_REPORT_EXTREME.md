"""
TEST_REPORT_EXTREME.md
======================

Extreme Stress Test – LifeOS Skeleton
-------------------------------------

Purpose
-------
This report summarizes results from the extreme lineage stress test.
The run was designed to push LifeOS to its maximum, testing multi-generation
survival, farming behavior, and lineage growth.

Key Observations
----------------
1. **Founders**
   - 12 founder pairs created (24 individuals).
   - All paired correctly with loyalty intact.

2. **Reproduction**
   - Continuous reproduction across >3 generations confirmed.
   - Children successfully matured, paired, and reproduced.
   - Example: gen2 children (24–35) paired and produced grandchildren (48–53).

3. **Farming & Resources**
   - Farming events logged from gen1 onward.
   - Initial yields: ~1–2 food units per effort.
   - By gen2–3, efficiency increased (yields up to 4 units).
   - Farming sustained the population until food/oxygen dynamics tightened.

4. **Shared Memory**
   - Ledger contains farming, pairing, and birth events.
   - Confirms collective event history (like a digital chronicle).

5. **Population Dynamics**
   - Population grew quickly in early gens (36 → 42 → 45).
   - Environmental limits (food scarcity) triggered collapse after peak.
   - Oxygen stable, food bottlenecked survival.

6. **Artifacts**
   - `metrics.pdf` → clear population collapse curve after peak.
   - `lineage.json` → ancestry tree expands across 3+ generations.
   - `reproduction_events.json` → confirms multi-gen reproduction loop works.
   - `shared_memory.json` → verifies farming integration and food yields.

Interpretation
--------------
- ✅ Multi-generation reproduction is functioning.
- ✅ Farming logic integrated and producing usable yields.
- ⚠️ Food replenishment is still too low for long-term survival.
- ⚠️ Population overshoots resources, leading to eventual collapse.

Recommendations
---------------
- Tune **base_food_per_gen** and **farming yield scaling**.
- Consider **role specialization** (farmers vs guardians).
- Experiment with **oxygen decay > 0** to simulate harsher survival.
- Use farming efficiency to allow populations to stabilize instead of crash.

Where to Place This File
------------------------
Place this report at the root as:

    TEST_REPORT_EXTREME.md

This keeps it alongside:
- TEST_REPORT.md
- TEST_REPORT_ADAM_EVE.md

so users can compare standard, Adam & Eve, and extreme runs.

License
-------
MIT License © 2025 Frank McNally
"""
