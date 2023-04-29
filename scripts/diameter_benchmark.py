from itertools import pairwise
from math import ceil, log, sqrt
from random import randint

import networkx as nx
import numpy as np

from scripts.classes import Benchmark


# The inverse strategy
def inverse(N, k, i):
    if k <= 2:
        return i + ceil(N / 2**k)
    return i + ceil(N / (k + 2))


# The log strategy
def inverseLog(N, k, i):
    if k <= 2:
        return i + ceil(N / (1 + sqrt(k)))
    return i + ceil(N / (2 + log(k)))


memo = {}

# The random strategy
def rand(N, k, i):
    global memo

    # Reinitialize on a new benchmark
    if k == 2 and i == 0:
        memo = {}

    if not k in memo:
        # Generate a different value than previously
        newValue = randint(2, N // 2)
        while newValue in list(memo.values()):
            newValue = randint(2, N // 2)
        memo[k] = newValue

    return i + memo[k]


memo2 = {"permutation": [], "edges": []}


def rand2(N, k, i):
    global memo2

    if k == 2 and i == 0:
        memo2 = {"permutation": [], "edges": []}

    # Reinitialize on every step
    if i == 0:
        G = nx.Graph()
        G.add_nodes_from(range(N))
        G.add_edges_from(memo2["edges"])
        # Get a random n-cycle
        permutation = np.random.permutation(N)
        edges = list(pairwise(permutation)) + [(permutation[0], permutation[-1])]
        count = 0
        # Make sure cycle has no edge in the graph to ensure graph regularity
        while any(e in G.edges for e in edges):
            permutation = np.random.permutation(N)
            edges = list(pairwise(permutation)) + [(permutation[0], permutation[-1])]
            count += 1
        print(f"found n-cycle after {count} tries")
        memo2["permutation"] = permutation
        memo2["edges"] += edges

    ([index],) = np.where(memo2["permutation"] == i)

    if k % 2 == 0:
        return memo2["permutation"][(index - 1) % N]

    return memo2["permutation"][(index + 1) % N]


if __name__ == "__main__":

    Benchmark(
        lambda N, k, i: rand2(N, k, i),
        lambda N, k, i: rand(N, k, i),
        sample=10,
    ).strong(1000, 1000)


# I. Inverse VS inverse powers of two
# Benchmark(
#     lambda N, k, i: inverse(N,k,i),
#     lambda N, k, i: i + ceil(N / 2**k),
#     sample=10,
# ).strong(500, 1500)

# Benchmark results
# -----------------
# Sample size: 20
# Strongly better: 100.0%


# - Strategy F1 is weakly better 100.0% of the time
# - Strategy F2 is weakly better 0.0% of the time

# II. Inverse square root VS Inverse function
# Benchmark(
#     lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
#     lambda N, k, i: inverse(N,k,i),
#     sample=20,
# ).strong(500, 1500)

# Benchmark results
# -----------------
# Sample size: 20
# Strongly better: 50.0%
# Average diameter difference when not better: 1


# - Strategy F1 is weakly better 82.42% of the time
# - Strategy F2 is weakly better 17.58% of the time

# III. Inverse log VS Inverse square root
# Benchmark(
#     lambda N, k, i: inverseLog(N,k,i),
#     lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
#     sample=100,
# ).strong(500, 1500)

# Benchmark results
# -----------------
# Sample size: 100
# Strongly better: 47.0%
# Average diameter difference when not better: 1.0138888888888888

# - Strategy F1 is weakly better 76.32% of the time
# - Strategy F2 is weakly better 23.68% of the time


# Benchmark(
#     lambda N, k, i: inverseLog(N, k, i),
#     lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
#     lambda N, k, i: inverse(N, k, i),
#     lambda N, k, i: i + ceil(N / 2**k),
#     sample=1,
# ).strong(1000, 5000)
