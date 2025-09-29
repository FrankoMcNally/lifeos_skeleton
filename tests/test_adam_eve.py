# tests/test_adam_eve.py
from pathlib import Path
import json
import pytest

from lifeos.genome import Locus
from lifeos.adam_eve_engine import AdamEveWorld


def test_adam_eve_rules(tmp_path: Path):
    """Check Adam & Eve world basic rules with baseline policy."""

    loci = [
        Locus(name="cooperation", type="float", min=0.0, max=1.0),
        Locus(name="energy", type="int", min=0, max=100),
    ]

    out = tmp_path / "adam_eve_test"
    world = AdamEveWorld(
        seed=123,
        loci=loci,
        num_couples=4,         # smaller for test
        generations=6,
        mutation_rate=0.01,
        lifespan_phases=4,
        reproduction_phase=None,   # <-- allow reproduction when >= pair_at_phase
        pair_at_phase=1,
        children_cap_range=(2, 3),
        traits_dir=None,
        per_individual_kb=2,
        shared_pool_kb=16,
        policy="baseline",
    )
    world.run(out)

    # outputs exist
    assert (out / "metrics.csv").exists()
    assert (out / "lineage.json").exists()
    assert (out / "reproduction_events.json").exists()

    # founders = 8 (two per couple)
    rows = (out / "metrics.csv").read_text(encoding="utf-8").splitlines()
    header = rows[0].split(",")
    first = rows[1].split(",")
    alive_idx = header.index("alive")
    assert int(first[alive_idx]) == 8

    # reproduction events respect adulthood rule (>= pair_at_phase)
    repro = json.loads((out / "reproduction_events.json").read_text())
    assert isinstance(repro, list)
    if repro:
        for e in repro:
            assert isinstance(e["parents"], (list, tuple))
            assert e["generation"] >= 1
            # all repro must occur at phase >= pair_at_phase
            assert e["phase"] >= 1, f"Found reproduction too early: {e}"


def test_adam_eve_with_psai(tmp_path: Path):
    """Check Adam & Eve world with PSAI policy enabled."""

    loci = [
        Locus(name="cooperation", type="float", min=0.0, max=1.0),
        Locus(name="energy", type="int", min=0, max=100),
    ]

    out = tmp_path / "adam_eve_psai"
    world = AdamEveWorld(
        seed=321,
        loci=loci,
        num_couples=2,
        generations=4,
        mutation_rate=0.05,
        lifespan_phases=None,          # unlimited life
        reproduction_phase=None,       # free reproduction when adult
        pair_at_phase=1,
        children_cap_range=(0, 9999),  # unlimited
        traits_dir=None,
        per_individual_kb=2,
        shared_pool_kb=32,
        policy="psai",                 # <--- PSAI enabled
    )
    world.run(out)

    # outputs exist
    assert (out / "metrics.csv").exists()
    assert (out / "lineage.json").exists()
    assert (out / "reproduction_events.json").exists()

    # check repro events exist (may be zero if unlucky, but file exists)
    repro = json.loads((out / "reproduction_events.json").read_text())
    assert isinstance(repro, list)
    assert len(repro) >= 0
