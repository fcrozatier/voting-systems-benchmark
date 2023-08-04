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
    edges = cycle_edges(cycle)

    assert len(edges) == N

    for a, b in edges:
        assert a < b


def test_sort_tuples():
    tuples = [(1, 0), (0, 2), (5, 4)]
    sorted_tuples = sort_tuples(tuples)

    assert sorted_tuples == [(0, 1), (0, 2), (4, 5)]


@pytest.mark.skip
def test_independent_cycle():
    # In the case of a 5 cycle, the function manages to find the star
    edges = [(1, 3), (3, 4), (4, 2), (2, 5), (5, 1)]
    edge_list = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]

    new_cycle = independent_cycle(edges, edge_list)

    assert len(new_cycle) == 5
    assert set(sort_tuples(new_cycle)) == set(sort_tuples([(1, 3), (3, 5), (5, 2), (2, 4), (4, 1)]))


def test_page_ranked():
    G = nx.DiGraph()
    G.add_nodes_from(range(3))
    G.add_edges_from([(2, 1), (2, 1), (1, 0)])

    rank = page_rank(G)
    assert rank == [0, 1, 2]


def test_ranking_from_scores():
    values = [0.139, 0.226, 0.143, 0.492]
    assert ranking_from_scores(values) == [3, 1, 2, 0]
