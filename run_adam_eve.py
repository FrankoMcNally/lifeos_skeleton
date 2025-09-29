# run_adam_eve.py
from pathlib import Path
from lifeos.genome import Locus
from lifeos.adam_eve_engine import AdamEveWorld


def main():
    # Define some loci (basic DNA blueprint for traits)
    loci = [
        Locus(name="cooperation", type="float", min=0.0, max=1.0),
        Locus(name="curiosity", type="float", min=0.0, max=1.0),
        Locus(name="energy", type="int", min=0, max=100),
    ]

    # Configure and build the world
    world = AdamEveWorld(
        seed=42,
        loci=loci,
        num_couples=12,        # start with 12 couples (Adam & Eve style)
        generations=60,        # number of generations to simulate
        mutation_rate=0.02,    # small mutation rate
        lifespan_phases=4,     # capped life cycle
        reproduction_phase=1,  # reproduction starts at phase 1
        pair_at_phase=1,       # pair at phase 1
        children_cap_range=(4, 8),  # each couple has 4–8 children
        traits_dir=None,       # could point to a traits/ dir
        per_individual_kb=2,
        shared_pool_kb=32,     # memory pool shared by all
        policy="baseline",     # can switch to "psai" if desired
    )

    # Output directory for results
    out = Path("runs/adam_eve")
    world.run(out)

    print(f"✅ Simulation complete! Results saved in: {out.resolve()}")
    print("Files generated:")
    print(" - metrics.csv")
    print(" - lineage.json")
    print(" - reproduction_events.json")
    print(" - traits_loaded.json")
    print(" - shared_memory.json")


if __name__ == "__main__":
    main()
