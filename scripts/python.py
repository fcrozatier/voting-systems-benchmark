from math import ceil

import networkx as nx

# Todo benchmark functions 1/2**x 1/x 1/log(x)


class ComparisonGraph:
    """
    F is the function of N, k, i used at step k to connect node i and F(N,k,i).

    In this implementation:
    - the distance between F(N,k,i) and i must decrease with k,
    - the distance between F(N,k,i) and i must be the same for all nodes i at a given step k, ie |F(N,k,i) - i| = |F(N,k,0) - 0| for all i

    Examples of such functions F are of the form i + f(N,k) with f based on usual functions like 1 / k, 1/ sqrt(k), 1/2**k, 1/log(k) etc.
    """

    def __init__(self, size, F=lambda N, k, i: i + ceil(N / 2**k)):
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


graph = ComparisonGraph(2**11)
for d in graph.diameters():
    print(d)

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
