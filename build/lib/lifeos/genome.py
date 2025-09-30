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

class MutationModel:
    def __init__(self, per_locus_rate: float = 0.01):
        self.per_locus_rate = per_locus_rate

    def mutate(self, genome: Genome, rng: random.Random) -> Genome:
        new_vals = []
        for loc, val in zip(genome.loci, genome.values):
            if rng.random() < self.per_locus_rate:
                if loc.type == "float":
                    delta = rng.uniform(-0.05, 0.05)
                    new_vals.append(min(loc.max, max(loc.min, float(val) + delta)))
                elif loc.type == "int":
                    step = rng.choice([-1, 1])
                    new_vals.append(min(int(loc.max), max(int(loc.min), int(val) + step)))
                elif loc.type == "enum" and loc.enum:
                    choices = [x for x in loc.enum if x != val]
                    new_vals.append(rng.choice(choices) if choices else val)
                else:
                    new_vals.append(val)
            else:
                new_vals.append(val)
        return Genome(loci=genome.loci, values=new_vals)
