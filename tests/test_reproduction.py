import random
import lifeos


def test_reproduce_creates_child():
    # Create two parents with the same loci
    loci = [
        lifeos.genome.Locus(name="gene1", type="float", min=0.0, max=1.0),
        lifeos.genome.Locus(name="gene2", type="int", min=0, max=10),
    ]

    rng = random.Random(42)
    parent1 = lifeos.genome.Genome(loci=loci)
    parent2 = lifeos.genome.Genome(loci=loci)

    # Reproduce
    child = lifeos.reproduction.reproduce(parent1, parent2, rng)

    # Assertions
    assert isinstance(child, lifeos.genome.Genome)
    assert len(child.values) == len(parent1.values)
    assert all(
        c in (p1, p2)
        for c, p1, p2 in zip(child.values, parent1.values, parent2.values)
    )
