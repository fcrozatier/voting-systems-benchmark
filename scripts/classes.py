from functools import reduce
from itertools import pairwise
from math import ceil
from random import randint
from statistics import mean
from types import FunctionType

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
        size: int,
        F: FunctionType = lambda N, k, i: i + ceil(N / 2**k),
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
            self.graph.add_edges_from(
                (i, self.F(self.size, step, i) % self.size) for i in range(self.size)
            )
            yield nx.diameter(self.graph)


class Benchmark:
    """
    stategies: the different strategies F1, F2, F3 etc to compare
    """

    def __init__(
        self,
        *strategies,
        sample=100,
    ):
        self.strategies = strategies
        self.sample = sample

    def strong(self, Nmin, Nmax):
        """
        Test whether F1 is strongly superior to F2 and F2 strongly superior to F3 etc.
        """
        exceptions = set()
        delta = []
        for i in range(self.sample):
            n = randint(Nmin, Nmax)
            graphs = (ComparisonGraph(n, F) for F in self.strategies)

            print("----------------------------------")
            print(f"Iteration {i+1}/{self.sample}: n={n}")

            for step, diameters in enumerate(zip(*(g.diameters() for g in graphs))):
                # Prevent too many iterations: the diameter changes the most in the first iterations
                if step >= 10:
                    break

                better = reduce(
                    lambda a, b: a and b, (a <= b for a, b in pairwise(diameters))
                )

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
        print(f"Strongly better: {round(1 - len(exceptions)/(self.sample), 4)*100}%")
        if len(delta) > 0:
            print(f"Average diameter difference when not better: {mean(delta)}")


# Data with n = 13
# step 1, diameter 4096 4096.0
# step 2, diameter 2048 2048.0
# step 3, diameter 1025 1025.0
# step 4, diameter 513 514.0
# step 5, diameter 258 259.0
# step 6, diameter 130 132.0
# step 7, diameter 67 69.0
# step 8, diameter 35 38.0
# step 9, diameter 20 23.0
# step 10, diameter 12 16.0
# step 11, diameter 9 13.0
# step 12, diameter 7 12.0
# step 13, diameter 7 12.0
