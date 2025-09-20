import random
from lifeos.genome import Locus, Genome, MutationModel

def test_random_init_and_mutation():
    rng = random.Random(42)

    loci = [
        Locus(name="height", type="float", min=1.5, max=2.0),
        Locus(name="age", type="int", min=0, max=100),
        Locus(name="eye_color", type="enum", enum=["blue", "green", "brown"]),
    ]

    genome = Genome.random_init(loci, rng)
    assert len(genome.values) == 3

    # Values should be within bounds
    assert 1.5 <= genome.values[0] <= 2.0
    assert 0 <= genome.values[1] <= 100
    assert genome.values[2] in ["blue", "green", "brown"]

    # Mutate and check it still respects constraints
    model = MutationModel(per_locus_rate=1.0)  # force mutation on all
    new_genome = model.mutate(genome, rng)
    assert len(new_genome.values) == 3
    assert 1.5 <= new_genome.values[0] <= 2.0
    assert 0 <= new_genome.values[1] <= 100
    assert new_genome.values[2] in ["blue", "green", "brown"]
