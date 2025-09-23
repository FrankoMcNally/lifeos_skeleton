"""
Reproduction engine: crossover model for digital beings.
"""

import random
from typing import Optional
from .genome import Genome


class ReproductionModel:
    """Handles reproduction between two genomes."""

    def __init__(self, crossover_rate: float = 0.5):
        self.crossover_rate = crossover_rate

    def mate(self, parent1: Genome, parent2: Genome, rng: Optional[random.Random] = None) -> Genome:
        """
        Simple crossover reproduction:
        - Each gene is inherited from one parent at random.
        """
        if rng is None:
            rng = random.Random()

        if len(parent1.loci) != len(parent2.loci):
            raise ValueError("Parents must have the same loci structure for reproduction")

        child_values = []
        for v1, v2 in zip(parent1.values, parent2.values):
            # Choose gene from parent1 or parent2
            child_values.append(v1 if rng.random() < self.crossover_rate else v2)

        return Genome(loci=parent1.loci, values=child_values)


# Functional API (legacy support for tests)
def reproduce(parent1: Genome, parent2: Genome, rng: Optional[random.Random] = None) -> Genome:
    model = ReproductionModel()
    return model.mate(parent1, parent2, rng)
