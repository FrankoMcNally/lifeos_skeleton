# lifeos/reproduction.py
from typing import Tuple
import random
from .genome import Genome, MutationModel

class ReproductionModel:
    def __init__(self, mutation_model: MutationModel | None = None):
        self.mutation_model = mutation_model or MutationModel()

    def mate(self, parent1: Genome, parent2: Genome, rng: random.Random | None = None) -> Genome:
        """Create a child genome by combining values from two parents."""
        if rng is None:
            rng = random.Random()

        child_vals = []
        for v1, v2 in zip(parent1.values, parent2.values):
            child_vals.append(rng.choice([v1, v2]))

        child = Genome(loci=parent1.loci, values=child_vals)
        return self.mutation_model.mutate(child, rng)
