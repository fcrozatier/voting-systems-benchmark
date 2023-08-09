from src.comparisons import *


def test_comparisons():
    c = Comparisons(N=10)

    assert c.matrix.shape == (10, 10)

    c.record_vote(0, 1)
    c.record_vote(0, 1)

    assert c.matrix[0][1] == 2
    assert c.graph.edges[(0, 1)]["weight"] == 2


def test_random_expander_comparisons():
    re = RandomCyclesComparisons(10)
    comparisons = [re.next_comparison() for _ in range(15)]

    for c in comparisons:
        assert isinstance(c, tuple)
        assert len(c) == 2
