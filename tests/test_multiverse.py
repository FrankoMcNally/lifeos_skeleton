from pathlib import Path
from lifeos.genome import Locus
from lifeos import Scenario, Multiverse  # <-- now imported via __init__.py

def test_multiverse_runs(tmp_path: Path):
    loci = [
        Locus(name="size", type="float", min=0.5, max=3.0),
        Locus(name="energy", type="int", min=0, max=100),
        Locus(name="color", type="enum", enum=["red", "green", "blue"]),
    ]
    scenarios = [
        Scenario(name="baseline", policy="rational"),
        Scenario(name="spiritual_communal", policy="spiritual"),
    ]

    mv = Multiverse(
        base_seed=123456,
        loci=loci,
        population_size=30,
        generations=10,
        mutation_rate=0.05,
        scenarios=scenarios,
    )
    outputs = mv.run_all(tmp_path)

    assert "baseline" in outputs and "spiritual_communal" in outputs

    for wname, wpath in outputs.items():
        mfile = wpath / "metrics.csv"
        assert mfile.exists()
        lines = mfile.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) >= 2  # header + data row
