import networkx as nx

from src.utilities import *
from src.votes import *


def page_rank(G: nx.DiGraph):
    """
    Returns the ranked list of vertices of G in increasing order, according to page rank
    """

    # Compute PageRank
    pr = nx.pagerank(G)
    # Sort entries with increasing scores
    sorted_entries = sorted(list(pr.items()), key=lambda e: e[1], reverse=True)
    # Return the sorted entries numbers
    return list(map(lambda x: x[0], sorted_entries))


def initialize_graph(N: int):
    G = nx.DiGraph()
    G.add_nodes_from(list(range(N)))
    return G


def iteratedPageRank(ranking: list[int], vote_budget: int, reassess=1, p=0.9):
    """
    ranking: the 'true' ranking
    vote_budget: how many votes to make
    reassess: how many times to compare a specific pair
    p: probability to vote according to the true ranking
    """
    N = len(ranking)
    G = initialize_graph(N)

    remaining_votes = vote_budget
    while remaining_votes > 0:
        if remaining_votes == vote_budget:
            # initial loop: vote on the edges of a random cycle
            cycle = random_list(N)
        else:
            # iteration: make a new independent cycle from the page rank on G
            cycle = page_rank(G)

        edges = cycle_edges(cycle)

        for pair in edges:
            i = reassess
            while i > 0:
                i -= 1
                arrow = vote(pair, ranking, p)
                remaining_votes -= 1
                G.add_edges_from([arrow])

                if remaining_votes == 0:
                    break
        else:
            continue
        break

    return page_rank(G)


class PageRank(Vote):
    def rank(self):
        return page_rank(self.comparisons.graph)


class IteratedPageRank(PageRank):
    def next_comparison(self):
        if not hasattr(self, "_edges"):
            new_cycle = random_list(self.N)
        elif self._edges == None:
            new_cycle = page_rank(self.comparisons.graph)

        if "new_cycle" in locals():
            edges = cycle_edges(new_cycle)
            self._edges = edges.__iter__()

        try:
            return self._edges.__next__()
        except StopIteration:
            self._edges = None
            return self.next_comparison()
