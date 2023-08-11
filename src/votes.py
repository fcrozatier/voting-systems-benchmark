from typing import Self

import networkx as nx
import numpy as np

from src.pairings import *
from src.utilities import *


class Vote:
    def __init__(self, comparisons: Pairings, budget: int, rematch=1, p=1) -> None:
        self.comparisons = comparisons
        self.budget = budget
        self.rematch = rematch
        self.p = p
        self.true_ranking = random_cycle(comparisons.N)

        self.start_vote()

    def start_vote(self) -> Self:
        while self.budget:
            n = self.rematch

            while n > 0:
                (i, j) = self.comparisons.next_comparison()
                (loser, winner) = vote((i, j), self.true_ranking, self.p)
                self.comparisons.record_vote(winner, loser)
                self.budget -= 1
                n -= 1

                if self.budget == 0:
                    break
            else:
                continue
            break
        return self

    def rank(self) -> list[int]:
        pass

    def score(self):
        return top_10(self.true_ranking, self.rank())


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
            cycle = random_cycle(N)
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
