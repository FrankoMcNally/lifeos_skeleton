# lifeos/traits.py

from dataclasses import dataclass
from typing import Dict, Any
from .genome import Genome

@dataclass
class Traits:
    """Phenotypic expression of a genome (what the being looks like)."""
    size: float
    energy: int
    color: str

    def as_dict(self) -> Dict[str, Any]:
        """Return traits as a dictionary (for logging, debugging, etc.)."""
        return {
            "size": self.size,
            "energy": self.energy,
            "color": self.color,
        }

class TraitDecoder:
    """Converts raw genome values into high-level traits."""

    def decode(self, genome: Genome) -> Traits:
        # We assume genome.values = [float, int, str] from earlier steps
        size = genome.values[0]      # e.g., 1.0 → size
        energy = genome.values[1]    # e.g., 50 → energy
        color = genome.values[2]     # e.g., "green" → color

        return Traits(size=size, energy=energy, color=color)
