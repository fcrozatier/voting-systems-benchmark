from src.pairings import Random, RandomCycles
from src.votes import Vote


def test_vote_cls():
    budget = 1000
    for r in range(1, 6):
        v = Vote(50, budget, Random, rematch=r, p=0.9)

        assert sum(sum(v.comparisons.matrix)) == budget

    # Case where the resulting graph is a tournament graph
    budget = 50**2 * 2
    v = Vote(50, budget, RandomCycles, rematch=r, p=0.9)

    assert sum(sum(v.comparisons.matrix)) == budget
