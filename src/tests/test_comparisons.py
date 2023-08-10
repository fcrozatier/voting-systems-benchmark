import pytest

from src.comparisons import *


def test_comparisons():
    c = Comparisons(N=10)

    assert c.matrix.shape == (10, 10)

    c.record_vote(0, 1)
    c.record_vote(0, 1)

    assert c.matrix[0][1] == 2
    assert c.graph.edges[(0, 1)]["weight"] == 2


def test_random_expander_comparisons():
    comp_data = RandomCyclesComparisons(10)
    comparisons = [comp_data.next_comparison() for _ in range(15)]

    for c in comparisons:
        assert isinstance(c, tuple)
        assert len(c) == 2


def test_connected_components_comparisons():
    comparison_object = ConnectedComponentsComparisons(10)

    # We initially have 10 connected components
    assert len(list(nx.strongly_connected_components(comparison_object.graph))) == 10

    for i in range(10):
        (a, b) = comparison_object.next_comparison()
        comparison_object.record_vote(a, b)

        if i != 9:
            # At each iterations there are more and more distinct elements in the new cycle of comparisons
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


# def test_cczip2():
#     comparison_object = CCZip(8)

#     for w, l in [
#         (0, 1),
#         (1, 2),
#         (2, 3),
#         (3, 2),
#         (3, 4),
#         (4, 3),
#         (4, 5),
#         (2, 5),
#         (5, 6),
#         (6, 5),
#         (1, 6),
#         (1, 7),
#         (7, 6),
#         (7, 0),
#     ]:
#         comparison_object.record_vote(w, l)

#     assert len(list(nx.strongly_connected_components(comparison_object.graph))) == 3

#     breakpoint()
#     comparison_object.next_comparison()


def test_ccslow():
    comparison_object = CCSlow(10)

    # We initially have 10 connected components
    assert len(list(nx.strongly_connected_components(comparison_object.graph))) == 10

    for i in range(10):
        (a, b) = comparison_object.next_comparison()
        comparison_object.record_vote(a, b)

        if i != 9:
            # At each iterations there are more and more distinct elements in the new cycle of comparisons
            assert len(set(comparison_object._cycle)) == i + 2

    assert len(comparison_object.graph.edges) == 10
