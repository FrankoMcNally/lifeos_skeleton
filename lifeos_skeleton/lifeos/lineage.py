from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Individual:
    id: int
    genome: object
    parents: Optional[List[int]] = None

class LineageTracker:
    def __init__(self):
        self.individuals = {}

    def add_individual(self, individual: Individual):
        """Register a new individual in the lineage."""
        self.individuals[individual.id] = individual

    def get_individual(self, id: int) -> Optional[Individual]:
        """Retrieve an individual by ID."""
        return self.individuals.get(id)

    def get_parents(self, id: int) -> List[int]:
        """Get the parents of an individual."""
        ind = self.get_individual(id)
        return ind.parents if ind and ind.parents else []

    def get_children(self, parent_id: int) -> List[int]:
        """Find all children of a given parent."""
        return [ind.id for ind in self.individuals.values()
                if ind.parents and parent_id in ind.parents]
