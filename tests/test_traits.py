# tests/test_traits.py

from lifeos.genome import Genome
from lifeos.traits import TraitDecoder

def test_trait_decoder():
    genome = Genome(loci=["size", "energy", "color"], values=[1.5, 80, "blue"])
    decoder = TraitDecoder()
    traits = decoder.decode(genome)

    assert traits.size == 1.5
    assert traits.energy == 80
    assert traits.color == "blue"
    assert traits.as_dict() == {"size": 1.5, "energy": 80, "color": "blue"}
