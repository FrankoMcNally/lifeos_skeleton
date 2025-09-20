import pytest
from lifeos.lineage import Individual, LineageTracker

def test_add_and_retrieve_individual():
    tracker = LineageTracker()
    ind = Individual(id=1, genome="G1")
    tracker.add_individual(ind)

    assert tracker.get_individual(1) == ind
    assert tracker.get_parents(1) == []

def test_parents_and_children():
    tracker = LineageTracker()
    parent = Individual(id=1, genome="P1")
    child = Individual(id=2, genome="C1", parents=[1])

    tracker.add_individual(parent)
    tracker.add_individual(child)

    assert tracker.get_parents(2) == [1]
    assert tracker.get_children(1) == [2]
