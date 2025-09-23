# tests/test_policy.py

from lifeos.traits import Traits
from lifeos.policy import Policy

def test_policy_decision():
    policy = Policy()

    # Low energy → should decide to eat
    traits = Traits(size=1.0, energy=10, color="green")
    assert policy.decide(traits) == "eat"

    # Large size → should decide to explore
    traits = Traits(size=3.0, energy=80, color="blue")
    assert policy.decide(traits) == "explore"

    # Default case → rest
    traits = Traits(size=1.5, energy=60, color="red")
    assert policy.decide(traits) == "rest"
