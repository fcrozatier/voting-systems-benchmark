from random import sample

import networkx as nx
import numpy as np

from src.utilities import *


class Comparisons:
    def __init__(self, N) -> None:
        self.N = N
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(N))
        self.matrix = np.zeros((N, N))

    def next_comparison(self) -> tuple[int, int]:
        pass

    def record_vote(self, winner, loser):
        # coefficient i,j is the number of times i beats j
        self.matrix[winner][loser] += 1

        if (winner, loser) in self.graph.edges:
            self.graph.edges[(winner, loser)]["weight"] += 1
        else:
            self.graph.add_edge(winner, loser, weight=1)


class RandomComparisons(Comparisons):
    def __init__(self, N) -> None:
        super().__init__(N)

    def next_comparison(self):
        return tuple(sample(range(self.N), 2))


class RandomCyclesComparisons(Comparisons):
    def __init__(self, N) -> None:
        super().__init__(N)
        self._edges = None

    def next_comparison(self):
        if not self._edges:
            cycle = random_cycle(self.N)
            edges = cycle_edges(cycle)
            self._edges = edges.__iter__()

        try:
            return self._edges.__next__()
        except StopIteration:
            self._edges = None
            return self.next_comparison()
