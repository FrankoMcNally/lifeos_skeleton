# tests/test_adam_eve.py
from pathlib import Path
import json
import pytest

from lifeos.genome import Locus
from lifeos.adam_eve_engine import AdamEveWorld
from tools.add_digital_years import add_digital_years


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
        num_couples=20,          # larger population
        generations=50,          # more generations
        mutation_rate=0.01,
        lifespan_phases=4,
        reproduction_phase=None,
        pair_at_phase=1,
        children_cap_range=(2, 3),
        traits_dir=None,
        per_individual_kb=2,
        shared_pool_kb=16,
        policy="baseline",
    )
    world.run(out)

    # Add digital_years column
    add_digital_years(out / "metrics.csv", gen_years=20)

    # outputs exist
    assert (out / "metrics.csv").exists()
    assert (out / "lineage.json").exists()
    assert (out / "reproduction_events.json").exists()

    # founders = 40 (two per couple)
    rows = (out / "metrics.csv").read_text(encoding="utf-8").splitlines()
    header = rows[0].split(",")
    first = rows[1].split(",")
    alive_idx = header.index("alive")
    assert int(first[alive_idx]) == 40

    # reproduction events sanity check
    repro = json.loads((out / "reproduction_events.json").read_text())
    assert isinstance(repro, list)

    if repro:
        for e in repro:
            assert isinstance(e, dict)
            # Defensive checks (keys may not always exist)
            if "parents" in e:
                assert isinstance(e["parents"], (list, tuple))
            if "generation" in e:
                assert isinstance(e["generation"], int)
                assert e["generation"] >= 0
            if "phase" in e:
                assert isinstance(e["phase"], int)
                assert e["phase"] >= 0


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
        num_couples=10,
        generations=30,
        mutation_rate=0.05,
        lifespan_phases=None,          # unlimited life
        reproduction_phase=None,
        pair_at_phase=1,
        children_cap_range=(0, 9999),
        traits_dir=None,
        per_individual_kb=2,
        shared_pool_kb=32,
        policy="psai",
    )
    world.run(out)

    # Add digital_years column
    add_digital_years(out / "metrics.csv", gen_years=20)

    # outputs exist
    assert (out / "metrics.csv").exists()
    assert (out / "lineage.json").exists()
    assert (out / "reproduction_events.json").exists()

    repro = json.loads((out / "reproduction_events.json").read_text())
    assert isinstance(repro, list)
