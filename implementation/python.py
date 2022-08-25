from math import ceil

import networkx as nx

n = 10
N = 1024

G = nx.Graph()
G.add_nodes_from(range(N))


def step(k):
    if k == 0:
        for i in range(N):
            G.add_edge(i, (i + 1) % N)

    elif k == 1 and n % 2 == 0:
        for i in range(int(N / 2)):
            G.add_edge(i, (i + N / 2) % N)

    elif k == 1 and n % 2 == 1:
        for i in range(ceil(N / 2)):
            G.add_edge(i, (i + ceil(N / 2)) % N)

    else:
        for i in range(N):
            G.add_edge(i, (i + ceil(N / 2 ** (k - 1))) % N)

    print(
        f"step {k}, diameter",
        nx.diameter(G),
        k - 2 + ceil(N / 2**k),
        ceil(k * 0.5 + N / 2**k),
    )


i = 0
while 2**i < N:
    step(i)
    i += 1

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
