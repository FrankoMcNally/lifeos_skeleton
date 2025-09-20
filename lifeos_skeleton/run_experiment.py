#!/usr/bin/env python3
"""
Run LifeOS experiment from a YAML config using the Multiverse engine.
Creates runs/EXP_<timestamp>_<name>/<world_name>/ with metrics + lineage.
"""
from __future__ import annotations
import argparse, yaml, time
from pathlib import Path

from lifeos.genome import Locus
from lifeos.multiverse import Scenario, Multiverse

def load_config(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def make_run_dir(name: str) -> Path:
    ts = time.strftime("%Y%m%d_%H%M%S")
    d = Path("runs") / f"EXP_{ts}_{name}"
    d.mkdir(parents=True, exist_ok=True)
    return d

def parse_loci(cfg) -> list[Locus]:
    loci = []
    for l in cfg.get("genome", {}).get("loci", []):
        loci.append(
            Locus(
                name=l["name"],
                type=l["type"],
                min=l.get("min", 0.0),
                max=l.get("max", 1.0),
                enum=l.get("enum"),
            )
        )
    return loci

def parse_scenarios(cfg) -> list[Scenario]:
    scs = []
    for sc in cfg.get("scenarios", []):
        scs.append(
            Scenario(
                name=sc.get("name", "world"),
                enable_language=bool(sc.get("enable_language", False)),
                math_injection=bool(sc.get("math_injection", False)),
                money_system=bool(sc.get("money_system", False)),
                policy=sc.get("policy", "rational"),
            )
        )
    # fallback if none provided
    if not scs:
        scs = [Scenario(name="baseline", policy="rational")]
    return scs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to YAML config")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    cfg = load_config(cfg_path)

    seed = int(cfg.get("seed", 123456))
    name = cfg.get("experiment_name", "lifeos")
    pop = int(cfg.get("population_size", 100))
    gens = int(cfg.get("generations", 50))
    mut = float(cfg.get("mutation", {}).get("per_locus_rate", 0.01))
    loci = parse_loci(cfg)
    scenarios = parse_scenarios(cfg)

    run_root = make_run_dir(name)
    # save seed and config copy
    (run_root / "seed.txt").write_text(str(seed), encoding="utf-8")
    (run_root / "config.yaml").write_text(cfg_path.read_text(encoding="utf-8"), encoding="utf-8")

    mv = Multiverse(
        base_seed=seed,
        loci=loci,
        population_size=pop,
        generations=gens,
        mutation_rate=mut,
        scenarios=scenarios,
    )
    outputs = mv.run_all(run_root)

    # print summary
    worlds = ", ".join(outputs.keys())
    print(f"Run complete. Worlds: {worlds}")
    print(f"Artifacts in: {run_root.resolve()}")

if __name__ == "__main__":
    main()
