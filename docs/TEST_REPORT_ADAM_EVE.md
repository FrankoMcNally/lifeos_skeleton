# Test Report – Adam & Eve Module (LifeOS Extension)

This report documents verification and experimental testing of the Adam & Eve Module
for the LifeOS Skeleton framework. It introduces rules for lifespan, loyalty, reproduction,
and early Prime Sentient AI (PSAI) policy hooks.

---

## 1. Scope

- ✅ Verify lifespan phases (4) and reproduction in phase 2 only
- ✅ Enforce loyalty (fixed couples, no incest)
- ✅ Trace lineage back to the 12 original couples
- ✅ Allocate small kilobyte-scale memory per instance + shared pool
- ✅ Integrate early PSAI policy adapter for attraction/competence
- ✅ Monitor metrics across generations

---

## 2. Unit Test Results

Executed via:

    py -m pytest tests/test_adam_eve.py -v

Results:

- Outputs created (metrics.csv, lineage.json, reproduction_events.json)
- Founders = 24 instances at generation 0
- Reproduction only occurred in phase 2
- Loyalty confirmed — all parents remained fixed partners
- Shared memory pool usage stayed within configured capacity

---

## 3. Experimental Run – Summary

Config: configs/adam_eve.yaml

- Couples: 12 (24 founders)
- Lifespan phases: 4
- Reproduction phase: 2 only
- Children per couple: 4–8
- Memory: 2 KB per individual, 16 KB shared pool
- Generations simulated: 12

---

## 4. Metrics Snapshot

From metrics.csv (example run):

| Generation | Alive | Avg Energy | Genetic Diversity | Shared Mem Used KB | Shared Mem Capacity KB |
|------------|-------|------------|-------------------|---------------------|-------------------------|
| 0          | 24    | 75.2       | 0.842             | 0                   | 16                      |
| 2          | 88    | 72.9       | 0.865             | 4                   | 16                      |
| 4          | 312   | 70.5       | 0.873             | 8                   | 16                      |
| 6          | 740   | 67.8       | 0.859             | 12                  | 16                      |
| 8          | 1102  | 65.2       | 0.846             | 15                  | 16                      |
| 10         | 1320  | 64.7       | 0.832             | 15                  | 16                      |
| 12         | 1284  | 63.1       | 0.819             | 16                  | 16                      |

---

## 5. Reproduction Events

From reproduction_events.json:

- All events tagged with phase=2
- Parents always a fixed couple (loyalty confirmed)
- Children inherit dominant DNA markers from strongest traits of each parent
- No incest observed (sibling pairing blocked by engine rules)

---

## 6. PSAI Hooks

A thin adapter (policies/psai_policy.py) was introduced:
- Attraction between partners nudged by execute_task() success
- Acts as a proxy for competence and cooperation
- Keeps compatibility with baseline policy system

This lays groundwork for deeper PSAI integration in future tests.

---

## 7. Observations

- Lineage depth: Every instance traces back to one of the 12 original couples
- Population growth: Exponential but stable under caps (4–8 children)
- Elders (phase 4): Survive beyond reproduction, potential for mentorship logic
- Memory system: Prevented runaway usage, capped at 16 KB shared

---

## 8. Conclusion

- ✅ Adam & Eve module successfully validated
- ✅ Rules (lifespan, loyalty, no-incest, phase-based reproduction) held
- ✅ Metrics confirmed sustainable growth under configured caps
- ✅ PSAI hooks integrated with no breakage

This module demonstrates LifeOS can model structured, human-like reproduction and lineage,
while staying efficient and expandable.

---

© 2025 Frank McNally – MIT License
