"""
Genome engine: typed loci, bounded values, and mutation model.
"""

from dataclasses import dataclass, field
from typing import List, Any, Optional
import random


@dataclass
class Locus:
    name: str
    type: str  # "int" | "float" | "enum"
    min: float = 0.0
    max: float = 1.0
    enum: Optional[List[str]] = None


@dataclass
class Genome:
    loci: List[Locus]
    values: List[Any] = field(default_factory=list)

    def __init__(self, loci: Optional[List[Locus]] = None, values: Optional[List[Any]] = None, length: Optional[int] = None):
        rng = random.Random()
        if loci is not None and values is not None:
            # Explicit loci + values constructor
            self.loci = loci
            self.values = values
        elif loci is not None:
            # Random initialization from loci
            self.loci = loci
            self.values = []
            for loc in loci:
                if loc.type == "float":
                    self.values.append(rng.uniform(loc.min, loc.max))
                elif loc.type == "int":
                    self.values.append(rng.randint(int(loc.min), int(loc.max)))
                elif loc.type == "enum" and loc.enum:
                    self.values.append(rng.choice(loc.enum))
        elif length is not None:
            # Backwards compatibility: generate float loci
            self.loci = [
                Locus(name=f"gene_{i}", type="float", min=0.0, max=1.0)
                for i in range(length)
            ]
            self.values = [rng.uniform(0.0, 1.0) for _ in range(length)]
        else:
            raise ValueError("Must supply loci+values, loci, or length")

    @classmethod
    def random_init(cls, loci: List[Locus], rng: random.Random) -> "Genome":
        vals = []
        for loc in loci:
            if loc.type == "float":
                vals.append(rng.uniform(loc.min, loc.max))
            elif loc.type == "int":
                vals.append(rng.randint(int(loc.min), int(loc.max)))
            elif loc.type == "enum" and loc.enum:
                vals.append(rng.choice(loc.enum))
            else:
                raise ValueError(f"Unsupported locus type: {loc.type}")
        return cls(loci=loci, values=vals)

    def mutate(self, rate: float = 0.01):
        rng = random.Random()
        for i, loc in enumerate(self.loci):
            if rng.random() < rate:
                if loc.type == "float":
                    self.values[i] = rng.uniform(loc.min, loc.max)
                elif loc.type == "int":
                    self.values[i] = rng.randint(int(loc.min), int(loc.max))
                elif loc.type == "enum" and loc.enum:
                    self.values[i] = rng.choice(loc.enum)

    def __repr__(self):
        return f"Genome(values={self.values})"


class MutationModel:
    """
    Simple per-locus mutation model.
    """

    def __init__(self, per_locus_rate: float = 0.01):
        self.per_locus_rate = per_locus_rate

    def mutate(self, genome: Genome, rng: Optional[random.Random] = None) -> Genome:
        rng = rng or random.Random()
        new_vals = []
        for loc, val in zip(genome.loci, genome.values):
            if rng.random() < self.per_locus_rate:
                if loc.type == "float":
                    new_vals.append(rng.uniform(loc.min, loc.max))
                elif loc.type == "int":
                    new_vals.append(rng.randint(int(loc.min), int(loc.max)))
                elif loc.type == "enum" and loc.enum:
                    new_vals.append(rng.choice(loc.enum))
                else:
                    new_vals.append(val)
            else:
                new_vals.append(val)
        return Genome(loci=genome.loci, values=new_vals)
