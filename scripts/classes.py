import operator
from functools import reduce
from itertools import pairwise
from math import ceil
from random import randint
from statistics import mean

import networkx as nx


class ComparisonGraph:
    """
    F is the function of N, k, i used at step k to connect node i and F(N,k,i).

    In this implementation:
    - the distance between F(N,k,i) and i must decrease with k,
    - the distance between F(N,k,i) and i must be the same for all nodes i at a given step k, ie |F(N,k,i) - i| = |F(N,k,0) - 0| for all i

    Examples of such functions F are of the form i + f(N,k) with f based on usual functions like 1 / k, 1/ sqrt(k), 1/2**k, 1/log(k) etc.
    """

    def __init__(
        self,
        size,
        F=lambda N, k, i: i + ceil(N / 2**k),
    ):
        self.size = size
        self.F = F
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(size))

    def diameters(self):
        step = 1
        self.graph.add_edges_from((i, (i + 1) % self.size) for i in range(self.size))
        yield nx.diameter(self.graph)

        while abs(self.F(self.size, step, 0)) > 1:
            step += 1
            self.graph.add_edges_from((i, self.F(self.size, step, i) % self.size) for i in range(self.size))
            yield nx.diameter(self.graph)


class Benchmark:
    """
    strategies: the different strategies F1, F2, F3 etc to compare
    """

    def __init__(
        self,
        strategy1,
        strategy2,
        sample,
    ):
        self.strategies = [strategy1, strategy2]
        self.sample = sample

    def strong(self, Nmin, Nmax):
        """
        Test whether F1 is strongly superior to F2 and F2 strongly superior to F3 etc.
        """
        exceptions = set()
        delta = []
        weak = [0] * len(self.strategies)
        for i in range(self.sample):
            n = randint(Nmin, Nmax)
            graphs = (ComparisonGraph(n, F) for F in self.strategies)

            print("----------------------------------")
            print(f"Iteration {i+1}/{self.sample}: n={n}")

            for step, diameters in enumerate(zip(*(g.diameters() for g in graphs))):
                # Prevent too many iterations: the diameter changes the most in the first iterations
                if step >= 10:
                    break

                # is strategy1 better than strategy2 at this step?
                better = reduce(lambda a, b: a and b, (a <= b for a, b in pairwise(diameters)))

                # strategy that weakly wins
                if len(list(filter(lambda x: x == min(diameters), diameters))) == 1:
                    weak[diameters.index(min(diameters))] += 1

                print(f"\t{diameters}, {better}")
                if not better:
                    exceptions.add(n)
                    for (a, b) in pairwise(diameters):
                        if a > b:
                            delta.append(a - b)

        print("\n")
        print("Benchmark results")
        print("-----------------")
        print(f"Sample size: {self.sample}")
        print(f"F1 strongly better: {round(1 - len(exceptions)/(self.sample), 4)*100}%")
        if len(delta) > 0:
            print(f"Average diameter difference when not better: {mean(delta)}")

        print("\n")
        for i, p in enumerate(weak):
            print(f"- Strategy F{i+1} is weakly better {round(p/reduce(operator.add, weak) * 100, 2)}% of the time")
