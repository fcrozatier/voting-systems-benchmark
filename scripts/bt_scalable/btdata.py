import networkx as nx
import numpy as np


class BtData:
    def __init__(self, x, return_graph=False):
        if isinstance(x, np.ndarray) or isinstance(x, np.matrix):
            if x.shape[0] != x.shape[1]:
                raise ValueError("If x is a matrix, it must be square.")
            wins = x
            g = self._matrix_to_graph(wins)
        elif isinstance(x, nx.Graph):
            if not nx.is_directed(x):
                raise ValueError("If x is a graph, it must be a directed networkx graph.")
            wins = self._graph_to_matrix(x)
            g = x
        else:
            raise ValueError("x must be a matrix or a directed networkx graph.")

        comp = nx.strongly_connected_components(g)
        components = [list(comp) for comp in comp]
        self.wins = wins
        self.components = components
        self.graph = g if return_graph else None

    def _graph_to_matrix(self, graph):
        items = sorted(graph.nodes())
        n_items = len(items)
        wins = np.zeros((n_items, n_items))
        for winner, loser in graph.edges():
            i = items.index(winner)
            j = items.index(loser)
            wins[i][j] += graph[winner][loser]["weight"]
        return wins

    def _matrix_to_graph(self, wins):
        g = nx.DiGraph()
        n_items = wins.shape[0]
        for i in range(n_items):
            for j in range(n_items):
                weight = wins[i][j]
                if weight > 0:
                    g.add_edge(i, j, weight=weight)
        return g


# Exemple d'utilisation
# Supposons que vous avez déjà chargé vos données dans la variable "data" en Python (un dictionnaire avec les paires de données).

# Création de l'objet BtData à partir des données
# bt_data = BtData(data)

# Affichage des matrices de victoires
# print("Wins Matrix:")
# print(bt_data.wins)

# Affichage des composantes connexes
# print("Connected Components:")
# print(bt_data.components)
