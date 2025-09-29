# tests/test_adam_eve_free.py
from pathlib import Path
import json
import pytest

from lifeos.genome import Locus
from lifeos.adam_eve_engine import AdamEveWorld

def test_adam_eve_rules(tmp_path: Path):
    """Check Adam & Eve free reproduction rules."""

    loci = [
        Locus(name="cooperation", type="float", min=0.0, max=1.0),
        Locus(name="energy", type="int", min=0, max=100),
    ]

    world = AdamEveWorld(
        seed=456,
        loci=loci,
        num_couples=12,
        generations=12,
        mutation_rate=0.01,
        lifespan_phases=4,
        reproduction_phase=None,     # <--- free reproduction
        pair_at_phase=1,
        children_cap_range=(2, 3),
        traits_dir=None,
        per_individual_kb=2,
        shared_pool_kb=16,
        policy="baseline",
    )

    out = tmp_path / "adam_eve_free"
    world.run(out)

    # outputs exist
    assert (out / "metrics.csv").exists()
    assert (out / "lineage.json").exists()
    assert (out / "reproduction_events.json").exists()

    # founders = 24 (two per couple)
    rows = (out / "metrics.csv").read_text(encoding="utf-8").splitlines()
    header = rows[0].split(",")
    first = rows[1].split(",")
    alive_idx = header.index("alive")
    assert int(first[alive_idx]) == 24

    # reproduction events: allow phase >= 1 (free reproduction mode)
    repro = json.loads((out / "reproduction_events.json").read_text())
    for e in repro:
        assert e["phase"] >= 1, f"Found reproduction too early: phase={e['phase']}"
