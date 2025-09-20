# tests/test_reproduction.py
import random
from lifeos.genome import Genome, Locus, MutationModel
from lifeos.reproduction import ReproductionModel

def test_mating_and_mutation():
    loci = [Locus("trait1", float), Locus("trait2", int)]
    g1 = Genome(loci, [1.0, 10])
    g2 = Genome(loci, [2.0, 20])

    model = ReproductionModel(MutationModel())
    rng = random.Random(42)

    child = model.mate(g1, g2, rng)

    assert isinstance(child, Genome)
    assert len(child.values) == 2
    assert child.values[0] in [1.0, 2.0]  # inherited
    assert 0 <= child.values[1] <= 100    # mutation possible
