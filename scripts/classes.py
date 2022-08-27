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
        step = 0
        edges = [(i, (i + 1) % self.size) for i in range(self.size)]
        step += 1
        self.graph.add_edges_from(edges)
        yield nx.diameter(self.graph)

        while abs(self.F(self.size, step, 0)) > 1:
            edges = [
                (i, self.F(self.size, step, i) % self.size) for i in range(self.size)
            ]

            step += 1
            self.graph.add_edges_from(edges)
            yield nx.diameter(self.graph)


class Benchmark:
    def __init__(
        self,
        F1: FunctionType = lambda N, k, i: i + ceil(N / 2**k),
        F2: FunctionType = lambda N, k, i: i + ceil(N / 2**k),
        sample=100,
    ):
        self.F1 = F1
        self.F2 = F2
        self.sample = sample

    """
    Test whether F1 is a strongly superior method to F2
    """

    def strong(self, Nmin, Nmax):
        exceptions = set()
        delta = []
        for i in range(self.sample):
            n = randint(Nmin, Nmax)
            g1 = ComparisonGraph(n, self.F1)
            g2 = ComparisonGraph(n, self.F2)

            print("----------------------------------")
            print(f"Iteration {i}/{self.sample}: n={n}")

            for step, (d1, d2) in enumerate(zip(g1.diameters(), g2.diameters())):
                # Prevent too many iterations: the diameter changes the most in the first iterations
                if step >= 10:
                    break

                print(f"\t{d1}, {d2}, {d1 <= d2}")
                if d1 > d2:
                    exceptions.add(n)
                    delta.append(d1 - d2)

        print("\n")
        print("Benchmark results")
        print("-----------------")
        print(f"Sample size: {self.sample}")
        print(
            f"F1 strongly better than F2 at {(1 - len(exceptions)/(Nmax-Nmin+1))*100}%"
        )
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
