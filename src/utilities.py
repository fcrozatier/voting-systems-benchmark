from itertools import combinations, pairwise
from random import random, sample

import networkx as nx
import numpy as np
from scipy.stats import kendalltau


def random_list(size):
    """
    Returns a random cycle of given size using Durstenfeld algorithm
    https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm

    Note: this is faster than np.random.permutation since there are only (n-1)! cycles against n! permutations of size n
    """

    if size == 0 or size == 1:
        return []

    items = list(range(size))

    i = len(items) - 1
    while i > 1:
        k = np.random.randint(1, i + 1)
        items[k], items[i] = items[i], items[k]
        i -= 1

    return items


def clip(x, minimum, maximum):
    return max(min(x, maximum), minimum)


def random_list_from_gaussian_scores(size, m=5, s=2):
    L = list(range(size))
    L = list(map(lambda x: {"index": x, "score": clip(np.random.normal(m, s), minimum=0, maximum=10)}, L))
    return sorted(L, key=lambda x: x["score"], reverse=True)


def cycle_edges(cycle: list[int]):
    """
    Returns the list of edges making a cycle, with each tuple sorted
    """
    return sort_tuples([*list(pairwise(cycle)), (cycle[-1], cycle[0])])


def sort_tuples(tuples: list[tuple]):
    """Returns the tuple (a,b) if a < b and (b,a) otherwise"""

    return list(map(lambda x: tuple(sorted(x)), tuples))


def random_expander_edges(k, N):
    """
    k = number of random cycles
    N = size of cycles

    Edges to create a random regular expander graph from k random N-cycles sharing no edges. The resulting graph is 2k-regular of degree N.

    Returns the list of edges
    """
    if N < 2:
        return []
    elif N < 5:
        cycle = range(N)
        return cycle_edges(cycle)

    assert k > 1, "You need at least 2 cycles"
    assert N * (N - 1) > 2 * k, f"There is not enough room for {k} cycles in a graph of size {N}"

    cycles = []
    edges = set()

    for i in range(k):
        while len(edges) != (i + 1) * N:
            cycle = random_list(N)

            cycle_edges = cycle_edges(cycle)
            cycle_edges_sorted = list(map(sort_tuples, cycle_edges))
            edges_copy = set([*edges, *cycle_edges_sorted])

            if len(edges_copy) == len(edges) + N:
                cycles.append(cycle)
                edges = set([*edges_copy])

    return list(edges)


def kendall_tau_naive(list_a: list, list_b: list) -> int:
    """
    Compute the normalized Kendall tau distance between to ordering of the same set

    Naive O(n^2) implementation
    """
    inversions = 0
    for i, j in combinations(list_a, 2):
        inversions += np.sign(list_a.index(i) - list_a.index(j)) == -np.sign(list_b.index(i) - list_b.index(j))

    n = len(list_a)
    return inversions / ((n * (n - 1)) / 2)


def make_ranking(L: list):
    return [L.index(i) for i in range(len(L))]


def kendall_tau(list_a, list_b):
    """
    Uses Scipy implementation to compute kendall tau between two lists.

    Needs to transform permutations into rankings first
    """
    kt, _ = kendalltau(make_ranking(list_a), make_ranking(list_b))
    return (1 - kt) / 2


def top_10(ranking_a, ranking_b):
    """
    A pseudo-metric to check whether two rankings (increasing order) have a similar top 10%

    It is symmetric and transitive but not separate
    """
    assert set(ranking_a) == set(ranking_b), "Lists must have the same elements"

    l = len(ranking_a) // 10

    set_a = set(ranking_a[-l:])
    set_b = set(ranking_b[-l:])

    return 1 - len(set_a.intersection(set_b)) / l


def weighted_distance(original, permutation):
    """
    Measures how far appart a list an a permutation are. The distance is weighted with weights increasing with index
    """
    from math import e, exp, sqrt

    N = len(original)
    ranking_original = make_ranking(original)
    ranking_other = make_ranking(permutation)

    # Normalize the sum of weights to N
    normalize = N / ((1 - e ** (-N)) / (1 - e**-1))
    weights = [normalize * exp(-(N - 1 - i)) for i in range(N)]
    sq_distance = 0

    data = zip(ranking_original, ranking_other, weights)
    for rank_original, rank_other, weight in data:
        sq_distance += ((rank_original - rank_other) ** 2) * weight

    return sqrt(sq_distance)


def random_ranking(n: int) -> list[int]:
    """A random ranking is a random permutation of size n"""
    return list(np.random.permutation(n))


def vote(pair: tuple, ranking: list, p=1):
    """Vote on a pair of entries.

    Returns (a,b) with probability p if b is ranked higher than a in the ranking, and (b,a) otherwise
    """
    a, b = pair
    r = random()

    if ranking.index(a) < ranking.index(b):
        if r < p:
            return (a, b)
        else:
            return (b, a)
    else:
        if r < p:
            return (b, a)
        else:
            return (a, b)


def ranking_from_scores(array):
    """
    Returns a ranking in increasing order (best entries at the end) from a list of scores
    """
    sorted_array = sorted(list(enumerate(array)), key=lambda e: e[1])

    return [i for (i, _) in sorted_array]
