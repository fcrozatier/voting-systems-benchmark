from itertools import combinations, pairwise
from random import random

import networkx as nx
import numpy as np
from scipy.stats import kendalltau


def random_cycle(size):
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


def cycle_edges(cycle: list[int]):
    return [*list(pairwise(cycle)), (cycle[-1], cycle[0])]


def sort_tuple(tuple):
    """Returns the tuple (a,b) if a < b and (b,a) otherwise"""

    return tuple if min(tuple) == tuple[0] else (tuple[1], tuple[0])


def random_expander_edges(k, N):
    """
    k = number of random cycles
    N = size of cycles

    Edges to create a random regular expander graph from k random N-cycles sharing no edge. The resulting graph is 2k-regular of degree N.

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
            cycle = random_cycle(N)

            cycle_edges = cycle_edges(cycle)
            cycle_edges_sorted = list(map(sort_tuple, cycle_edges))
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
    tau = 0
    for i, j in combinations(list_a, 2):
        tau += np.sign(list_a.index(i) - list_a.index(j)) == -np.sign(list_b.index(i) - list_b.index(j))

    n = len(list_a)
    return 2 * tau / (n * (n - 1))


def make_ranking(L: list):
    return [L.index(i) for i in range(len(L))]


def kendall_tau(list_a, list_b):
    """
    Use Scipy implementation to compute kendall tau between two lists.

    Need to transform permutations into rankings first
    """
    return (1 - kendalltau(make_ranking(list_a), make_ranking(list_b)).statistic) / 2


def top_10_closeness(list_a, list_b):
    """
    A pseudo-metric to check whether list_a and list_b have a similar top 10%

    It is symmetric and transitive but not reflexive
    """
    assert len(list_a) == len(list_b), "Lists must have the same size"

    l = len(list_a) // 10

    set_a = set(list_a[:l])
    set_b = set(list_b[:l])

    return 1 - len(set_a.intersection(set_b)) / l


def random_ranking(n: int) -> list[int]:
    """A random ranking is a random permutation of size n"""
    return list(np.random.permutation(n))


def vote(pair: tuple, ranking: list, p=1):
    """Vote on a pair of entries.

    Returns (a,b) with probability p if b is ranked higher than a in the ranking, and (b,a) accordingly
    """
    a, b = pair

    if ranking.index(a) < ranking.index(b):
        if random() < p:
            return (a, b)
        else:
            return (b, a)
    else:
        if random() < p:
            return (b, a)
        else:
            return (a, b)


def page_ranked(G):
    """Returns the ranked list of vertices of G, according to page rank"""

    # Compute PageRank
    pr = nx.pagerank(G)
    # Sort entries with decreasing score
    sorted_entries = sorted(list(pr.items()), key=lambda e: e[1])
    # Return the sorted entries numbers
    return list(map(lambda x: x[0], sorted_entries))
