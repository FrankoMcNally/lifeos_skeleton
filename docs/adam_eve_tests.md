"""
Adam & Eve Test Module 🧪
=========================

Purpose
-------
The Adam & Eve simulation creates digital humans with DNA, families, and survival rules.  
The test module ensures everything works correctly **before scaling up to large experiments.**

What It Tests
-------------

1. Founders
   - First **4–12 couples** are created properly (configurable by test).
   - Each individual has DNA, memory, and a loyal partner.

2. Pairing Rules
   - Adults pair up when old enough.
   - No incest (siblings cannot pair).
   - Partners remain loyal once bonded.

3. Reproduction
   - Couples have children within their cap (e.g. 2–3 in tests, 4–8 in baseline).
   - Births cost parents energy.
   - Newborns start as children and can reproduce in later phases.

4. Environment
   - Food and oxygen are replenished each generation.
   - Agents forage for food (random or PSAI-biased).
   - Metabolism reduces energy each tick.
   - Starvation or oxygen shortage leads to death.
   - Elders can donate energy to struggling youth.

5. Roles
   - child → promoted to forager or guardian at adulthood.
   - Agents promoted to elder at threshold generation.
   - Metrics track population role mix.

6. Memory
   - Each agent remembers recent events (`RingMemory`).
   - `SharedLedger` logs global events across all agents.

7. Artifacts
   Every run produces data for inspection:
   - **metrics.csv** — alive, births, deaths, energy, food, oxygen, role mix.
   - **lineage.json** — family tree.
   - **reproduction_events.json** — births, deaths, pairings.
   - **traits_loaded.json** — any trait definitions used.
   - **shared_memory.json** — collective memory of world events.

Test Files
----------

- **tests/test_adam_eve.py**
  - Creates small test runs (2–4 couples, 4–6 generations).
  - Asserts that all outputs exist and contain valid data.
  - Validates:
    * Pair caps
    * Kinship rules
    * PSAI bias logic
    * Shared memory usage

- **tests/test_adam_eve_free.py**
  - Verifies that reproduction can occur freely after adulthood (not locked to phase 1).
  - Confirms children of children (multi-generational lineage) also reproduce.

In Plain English
----------------
Think of this module as a checklist for a spaceship launch 🚀:

- Do we have astronauts? (**founders exist**)
- Are they seated with the right partners? (**pairing rules**)
- Do they have kids at the right time? (**reproduction**)
- Do they have enough supplies? (**environment**)
- Do they survive or die based on oxygen and food? (**death events**)
- Did they log everything? (**artifacts**)

✅ If all tests pass, the simulation is safe to scale up.
"""
