import pytest

from src.pairings import *


def test_pairings():
    c = Pairings(N=10)

    assert c.matrix.shape == (10, 10)

    c.record_vote(0, 1)
    c.record_vote(0, 1)

    assert c.matrix[0][1] == 2
    assert c.graph.edges[(0, 1)]["weight"] == 2


def test_random_cycles_pairings():
    comp_data = RandomCycles(10)
    pairings = [comp_data.next_comparison() for _ in range(15)]

    for c in pairings:
        assert isinstance(c, tuple)
        assert len(c) == 2


def test_connected_components_pairings():
    comparison_object = CCBiggest(10)

    # We initially have 10 connected components
    assert len(list(nx.strongly_connected_components(comparison_object.graph))) == 10

    for i in range(10):
        (a, b) = comparison_object.next_comparison()
        comparison_object.record_vote(a, b)

        if i != 9:
            # At each iterations there are more and more distinct elements in the new cycle of pairings
            assert len(set(comparison_object._cycle)) == i + 2

    assert len(comparison_object.graph.edges) == 10


def test_cczip():
    comparison_object = CCZip(10)

    # We initially have 10 connected components
    assert len(list(nx.strongly_connected_components(comparison_object.graph))) == 10

    for i in range(10):
        (a, b) = comparison_object.next_comparison()
        comparison_object.record_vote(a, b)

    assert len(comparison_object.graph.edges) == 10


def test_reachability_pairings():
    comparison_object = Reachability(10)

    nodes_visited = set()
    for i in range(10):
        (a, b) = comparison_object.next_comparison()
        comparison_object.record_vote(a, b)
        nodes_visited.add(a)
        nodes_visited.add(b)

    assert len(nodes_visited) == 10


def test_ccslow():
    comparison_object = CCSlow(10)

    # We initially have 10 connected components
    assert len(list(nx.strongly_connected_components(comparison_object.graph))) == 10

    for i in range(10):
        (a, b) = comparison_object.next_comparison()
        comparison_object.record_vote(a, b)

    assert len(list(nx.strongly_connected_components(comparison_object.graph))) < 10
