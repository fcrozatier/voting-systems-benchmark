from math import sqrt

import pytest

from .utilities import *


def test_random_ranking():
    ranking = random_ranking(10)

    assert len(ranking) == 10
    assert sorted(ranking) == list(range(10))


@pytest.mark.parametrize("pair", [(0, 1), (1, 0), (0, 3), (2, 1)])
def test_vote(pair):
    ranking = [0, 1, 2, 3]

    assert vote(pair, ranking) == tuple(sorted(pair))


@pytest.mark.parametrize("N", [2, 3, 4])
def test_random_cycle(N):
    iterations = 1000
    count = 0
    cycles = {}

    def factorial(n):
        if n == 1:
            return 1
        return n * factorial(n - 1)

    while count < iterations:
        cycle = tuple(random_cycle(N))

        if cycle in cycles:
            cycles[cycle] += 1
        else:
            cycles[cycle] = 1

        count += 1

    # Generates all cycles
    assert len(cycles) == factorial(N - 1), "There are (N-1)! distinct cycles up to permutation"
    assert all(map(lambda x: x[0] == 0, list(cycles.keys()))), "All cycles start at 0"

    # Cycles have uniform probability
    frequencies = list(map(lambda x: x / iterations, cycles.values()))

    assert max(frequencies) <= 1 / len(cycles) + 1 / sqrt(
        N
    ), "All the frequencies should be in the confidence interval"
    assert min(frequencies) >= 1 / len(cycles) - 1 / sqrt(
        N
    ), "All the frequencies should be in the confidence interval"


@pytest.mark.parametrize("N", [2, 3, 4])
def test_cycle_edges(N):
    cycle = random_cycle(N)

    assert len(cycle_edges(cycle)) == N


def test_page_ranked():
    G = nx.DiGraph()
    G.add_nodes_from(range(3))
    G.add_edges_from([(2, 1), (2, 1), (1, 0)])

    rank = page_ranked(G)
    assert rank == [2, 1, 0]
