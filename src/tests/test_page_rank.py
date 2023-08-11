import networkx as nx

from src.pagerank.pagerank import *


def test_page_rank():
    G = nx.DiGraph()
    G.add_nodes_from(range(3))
    G.add_edges_from([(2, 1), (2, 1), (1, 0)])

    rank = page_rank(G)
    assert rank == [0, 1, 2]
