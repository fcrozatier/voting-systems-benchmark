from itertools import chain, combinations, pairwise
from random import random, sample

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
    """
    Returns the list of edges making a cycle, with each tuple sorted
    """
    return sort_tuples([*list(pairwise(cycle)), (cycle[-1], cycle[0])])


def sort_tuples(tuples: list[tuple]):
    """Returns the tuple (a,b) if a < b and (b,a) otherwise"""

    return list(map(lambda x: tuple(sorted(x)), tuples))


def independent_cycle(edges, edge_list):
    """
    Returns a new cycle that is independent from edge_list
    """
    sorted_edges = set(sort_tuples(edges))
    sorted_edge_list = set(sort_tuples(edge_list))

    redundant_edges = list(sorted_edges.intersection(sorted_edge_list))
    redundant_nodes = list(chain.from_iterable(redundant_edges))

    def permute(nodes_list, times=100, force=False):
        for _ in range(times):
            permuted_edges = sort_tuples(pairwise(np.random.permutation(nodes_list)))

            intersection_size = len(set(permuted_edges).intersection(redundant_edges))
            if intersection_size == 0 or force:
                return permuted_edges

        return None

    # try to permute all the redundant nodes a few times
    permuted_edges = permute(redundant_nodes)
    if permuted_edges:
        return list((sorted_edges.difference(redundant_edges)).union(permuted_edges))

    # try to find new independent pairs from redundant ones
    new_edges = []
    for i in range(len(redundant_edges)):
        edge = tuple(sorted(sample(redundant_nodes, 2)))

        if len(set(edges)) == 2 and edge not in redundant_edges:
            a, b = edge
            new_edges.append(tuple(sorted(edge)))
            redundant_nodes.remove(a)
            redundant_nodes.remove(b)

    # try again to permute the remaining edges
    permuted_edges = permute(redundant_nodes)
    if permuted_edges:
        return list((sorted_edges.difference(redundant_edges)).union(permuted_edges, new_edges))

    # otherwise no luck
    permuted_edges = permute(redundant_nodes, times=1, force=True)
    return list((sorted_edges.difference(redundant_edges)).union(permuted_edges, new_edges))


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
    tau = 0
    for i, j in combinations(list_a, 2):
        tau += np.sign(list_a.index(i) - list_a.index(j)) == -np.sign(list_b.index(i) - list_b.index(j))

    n = len(list_a)
    return 2 * tau / (n * (n - 1))


def make_ranking(L: list):
    return [L.index(i) for i in range(len(L))]


def kendall_tau(list_a, list_b):
    """
    Uses Scipy implementation to compute kendall tau between two lists.

    Needs to transform permutations into rankings first
    """
    return (1 - kendalltau(make_ranking(list_a), make_ranking(list_b)).statistic) / 2


def top_10(ranking_a, ranking_b):
    """
    A pseudo-metric to check whether two rankings (increasing order) have a similar top 10%

    It is symmetric and transitive but not reflexive
    """
    assert set(ranking_a) == set(ranking_b), "Lists must have the same elements"

    l = len(ranking_a) // 10

    set_a = set(ranking_a[-l:])
    set_b = set(ranking_b[-l:])

    return 1 - len(set_a.intersection(set_b)) / l


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


def page_rank(G: nx.DiGraph):
    """
    Returns the ranked list of vertices of G in increasing order, according to page rank
    """

    # Compute PageRank
    pr = nx.pagerank(G)
    # Sort entries with decreasing score
    sorted_entries = sorted(list(pr.items()), key=lambda e: e[1])
    # Return the sorted entries numbers
    return list(map(lambda x: x[0], sorted_entries))


def ranking_from_scores(array):
    """
    Returns a ranking in increasing order (best entries at the end) from a list of scores
    """
    sorted_array = sorted(list(enumerate(array)), key=lambda e: e[1])

    return [i for (i, _) in sorted_array]
