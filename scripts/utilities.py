from itertools import combinations, pairwise

import numpy as np


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
        return [*list(pairwise(cycle)), (cycle[-1], cycle[0])]

    assert k > 1, "You need at least 2 cycles"
    assert N * (N - 1) > 2 * k, f"There is not enough room for {k} cycles in a graph of size {N}"

    cycles = []
    edges = set()

    for i in range(k):
        while len(edges) != (i + 1) * N:
            cycle = random_cycle(N)

            cycle_edges = [*list(pairwise(cycle)), (cycle[-1], cycle[0])]
            cycle_edges_sorted = list(map(sort_tuple, cycle_edges))
            edges_copy = set([*edges, *cycle_edges_sorted])

            if len(edges_copy) == len(edges) + N:
                cycles.append(cycle)
                edges = set([*edges_copy])

    return list(edges)


def kendall_tau_distance(list_a: list, list_b: list) -> int:
    """Compute the Kendall tau distance between to ordering of the same set"""
    tau = 0
    for i, j in combinations(list_a, 2):
        tau += np.sign(list_a.index(i) - list_a.index(j)) == -np.sign(list_b.index(i) - list_b.index(j))
    return tau
