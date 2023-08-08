from src.comparisons import *


def test_comparison():
    c = Comparisons(N=10)

    assert c.matrix.shape == (10, 10)

    c.record_vote(0, 1)
    c.record_vote(0, 1)

    assert c.matrix[0][1] == 2
    assert c.graph.edges[(0, 1)]["weight"] == 2
