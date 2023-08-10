from itertools import zip_longest
from random import sample, shuffle

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


class ConnectedComponentsComparisons(Comparisons):
    def __init__(self, N) -> None:
        super().__init__(N)
        self._components = []
        self._cycle = []
        self._last_node_component_index = 0
        self._nb_components_memo = []

    def next_comparison(self):
        if len(self._cycle) == 0:
            # Strongly connected components, ordered in decreasing sizes, items shuffled
            self._components = [list(c) for c in nx.strongly_connected_components(self.graph)]
            self._components = sorted(self._components, key=lambda comp: len(comp), reverse=True)
            [shuffle(comp) for comp in self._components]
            self._nb_components_memo.append(len(self._components))

            self._cycle.append(self._components[0].pop())
            self._last_node_component_index = 0

        if len(self._cycle) == self.N:
            comparison = (self._cycle[0], self._cycle[-1])
            self._cycle = []
            return comparison

        # If there is only one component
        if len(self._components) == 1:
            self._cycle.append(self._components[0].pop())

            return tuple(self._cycle[-2:])

        # Pick a random node in the biggest non empty component not containing the last node
        for i, comp in enumerate(self._components):
            if i == self._last_node_component_index or len(comp) == 0:
                continue

            self._last_node_component_index = i
            self._cycle.append(comp.pop())
            return tuple(self._cycle[-2:])

        # If we couldn't find any non empty component not containing the last node
        self._cycle.append(self._components[self._last_node_component_index].pop())
        return tuple(self._cycle[-2:])


class CCZip(Comparisons):
    def __init__(self, N) -> None:
        super().__init__(N)
        self._components = []
        self._edges = None
        self._nb_components_memo = []

    def next_comparison(self):
        if not self._edges:
            # Strongly connected components, ordered in decreasing sizes, items shuffled
            self._components = [list(c) for c in nx.strongly_connected_components(self.graph)]
            self._components = sorted(self._components, key=lambda comp: len(comp), reverse=True)
            [shuffle(comp) for comp in self._components]
            self._nb_components_memo.append(len(self._components))

            # Create a cycle by cycling around the components
            padded_rows = list(zip_longest(*self._components))
            cycle = []
            for row in padded_rows:
                for node in row:
                    if node != None:
                        cycle.append(node)

            self._edges = cycle_edges(cycle).__iter__()

        try:
            return self._edges.__next__()
        except StopIteration:
            self._edges = None
            return self.next_comparison()


class CCSlow(Comparisons):
    def __init__(self, N) -> None:
        super().__init__(N)
        self._components = []
        self._cycle = []
        self._last_node_component_index = 0
        self._nb_components_memo = []

    def next_comparison(self):
        # Strongly connected components, ordered in decreasing sizes, items shuffled
        self._components = [list(c) for c in nx.strongly_connected_components(self.graph)]
        self._components = sorted(self._components, key=lambda comp: len(comp), reverse=True)
        [shuffle(comp) for comp in self._components]

        if len(self._cycle) == 0:
            self._nb_components_memo.append(len(self._components))

            self._cycle.append(self._components[0].pop())
            self._last_node_component_index = 0

        if len(self._cycle) == self.N:
            comparison = (self._cycle[0], self._cycle[-1])
            self._cycle = []
            return comparison

        # If there is only one component
        if len(self._components) == 1:
            next_node = list(set(self._components[0]) - set(self._cycle)).pop()
            self._cycle.append(next_node)

            return tuple(self._cycle[-2:])

        # Pick a random node in the biggest component containing new nodes for the current cycle and not the last node
        for i, comp in enumerate(self._components):
            if i == self._last_node_component_index or len(set(comp) - set(self._cycle)) == 0:
                continue

            next_node = list(set(self._components[i]) - set(self._cycle)).pop()
            self._cycle.append(next_node)
            self._last_node_component_index = i
            return tuple(self._cycle[-2:])

        # If we couldn't find a node in a component not containing the last node
        next_node = list(set(self._components[self._last_node_component_index]) - set(self._cycle)).pop()
        self._cycle.append(next_node)
        return tuple(self._cycle[-2:])
