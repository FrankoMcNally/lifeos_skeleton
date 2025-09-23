# lifeos/policy.py

from typing import Literal
from .traits import Traits

# Define allowed actions
Action = Literal["eat", "rest", "explore"]

class Policy:
    """A simple decision-making policy based on traits."""

    def decide(self, traits: Traits) -> Action:
        # Example rules:
        if traits.energy < 30:
            return "eat"
        elif traits.size > 2.0:
            return "explore"
        else:
            return "rest"
