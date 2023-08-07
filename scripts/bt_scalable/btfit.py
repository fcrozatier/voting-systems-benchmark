import networkx as nx
import numpy as np

from scripts.bt_scalable.btdata import BtData


class BtFit:
    def __init__(self, btdata, a, map_by_component=False, subset=None, maxit=10000, epsilon=1e-3):
        self.btdata = btdata
        self.a = a
        self.map_by_component = map_by_component
        self.subset = subset
        self.maxit = maxit
        self.epsilon = epsilon
        self.call = None
        self.pi = None
        self.iters = None
        self.converged = None
        self.N = None
        self.diagonal = None
        self.names_dimnames = None

    def name_vector(self, vector, items):
        return {item: value for item, value in zip(items, vector)}

    def name_matrix(self, matrix, items):
        return {items[i]: {items[j]: matrix[i, j] for j in range(len(items))} for i in range(len(items))}

    def name_dimnames(self, data, dimnames):
        data_dict = self.name_matrix(data, dimnames[0])
        for i, item in enumerate(dimnames[0]):
            data_dict[item]["_dimname"] = dimnames[1][i]
        return data_dict

    def fit(self):
        components = self.btdata.components
        wins = self.btdata.wins

        if len(components) == 1 and self.subset is not None:
            print("There is only one component, so subset argument ignored")
            self.subset = None

        if self.subset is not None:
            self.btdata = self.select_components(self.subset)

        orig_components = components
        orig_n = len(orig_components)
        wins = self.btdata.wins
        components = self.btdata.components
        n = len(components)

        if not np.array_equal(wins.index, wins.columns):
            raise ValueError("The wins matrix should have identical row and column names")

        if np.isscalar(wins.iloc[0, 0]) or wins.shape[0] == 1:
            raise ValueError("There is not enough data to fit the model")

        if isinstance(components, list):
            if sum(len(c) > 1 for c in components) == 0:
                raise ValueError("There is not enough data to fit the model")

        if self.a < 1:
            raise ValueError("a must be >= 1")

        saved_diag = wins.diagonal().copy()
        wins = wins.values
        np.fill_diagonal(wins, 0)

        names_dimnames = wins.index.tolist()

        if (
            self.a == 1
            or self.a > 1
            and self.map_by_component
            or self.a > 1
            and not self.map_by_component
            and n == 1
            and orig_n > 1
        ):
            components = [c for c in components if len(c) > 1]

            K = [len(c) for c in components]
            b = self.a * np.array(K) - 1

            wins_by_comp = [wins[np.ix_(c, c)] for c in components]

            pi = []
            iters = []
            converged = []
            N = []
            diagonal = []

            for w, bi in zip(wins_by_comp, b):
                fit = self._bt_em(w, a=self.a, b=bi, maxit=self.maxit, epsilon=self.epsilon)
                pi_comp = self.name_vector(fit["pi"], names_dimnames)
                N_comp = self.name_matrix(fit["N"], names_dimnames)
                pi.append(pi_comp)
                N.append(N_comp)
                iters.append(fit["iters"])
                converged.append(fit["converged"])
                diagonal.append(self.name_vector(saved_diag.loc[pi_comp.keys()], pi_comp.keys()))

            if sum(converged) != len(components):
                print(
                    "The algorithm did not converge in at least one component. See the 'converged' element of the output for which."
                )
        else:
            K = wins.shape[0]
            b = self.a * K - 1
            fit = self._bt_em(wins, a=self.a, b=b, maxit=self.maxit, epsilon=self.epsilon)
            pi_full = self.name_vector(fit["pi"], names_dimnames)
            N_full = self.name_matrix(fit["N"], names_dimnames)
            pi = [pi_full]
            N = [N_full]
            iters = [fit["iters"]]
            converged = [fit["converged"]]
            diagonal = [self.name_vector(saved_diag, names_dimnames)]

            if not converged[0]:
                print("The algorithm did not converge in maxit =", self.maxit, "iterations")

        pi_perm = [sorted(p, key=p.get, reverse=True) for p in pi]
        pi = [self.name_vector(p, items) for p, items in zip(pi, pi_perm)]
        N = [self.name_matrix(n, items) for n, items in zip(N, pi_perm)]
        diagonal = [self.name_vector(d, items) for d, items in zip(diagonal, pi_perm)]

        self.call = "btfit"
        self.pi = pi
        self.iters = iters
        self.converged = converged
        self.N = N
        self.diagonal = diagonal
        self.names_dimnames = [names_dimnames]

    def _bt_em(self, wins, a, b, maxit, epsilon):
        K = wins.shape[0]
        pi = np.ones(K)
        pi_prev = np.zeros(K)
        iters = 0
        converged = False

        while not converged and iters < maxit:
            pi_prev[:] = pi
            S = wins.sum(axis=1)
            for i in range(K):
                pi[i] = (a - 1 + S[i]) / (
                    b * pi[i] + np.sum(wins[i, j] * pi[i] / (pi[i] + pi[j]) for j in range(K) if j != i)
                )

            if np.all(np.abs((pi - pi_prev) / pi) < epsilon):
                converged = True
            iters += 1

        result = {
            "pi": pi,
            "iters": iters,
            "converged": converged,
            "N": wins,
        }

        return result

    def select_components(self, subset, return_graph=False):
        if return_graph and self.btdata.graph is None:
            raise ValueError("There needs to be a graph component in btdata to return a graph here")

        components = self.btdata.components
        wins = self.btdata.wins

        if not callable(subset) and not isinstance(subset, str) and not isinstance(subset, np.ndarray):
            raise ValueError("subset is not of the correct form - see the documentation for more details.")

        if isinstance(subset, np.ndarray):
            if len(subset) != len(components):
                raise ValueError("length(subset) == length(btdata.components) is not TRUE")

        if callable(subset):
            test_of_function = subset(components[0])
            if (
                not isinstance(test_of_function, bool)
                or isinstance(test_of_function, np.ndarray)
                and len(test_of_function) > 1
            ):
                raise ValueError("if subset is a function, it must return either True or False")

        if isinstance(subset, str):
            if not all(item in components for item in subset):
                raise ValueError("not all elements of subset are names of components")

        if isinstance(subset, str):
            sub_comps = [components[item] for item in subset]
        else:
            sub_comps = list(filter(subset, components))

        if len(sub_comps) == 0:
            raise ValueError("The subset condition has removed all components")

        sub_wins = wins.loc[sub_comps, sub_comps]

        if not return_graph:
            return BtData(wins=sub_wins, components=sub_comps)

        if self.btdata.graph is not None and return_graph:
            graph = self.btdata.graph
            g = graph.subgraph(sub_comps)
            return BtData(wins=sub_wins, components=sub_comps, graph=g)


# Exemple d'utilisation
# Supposons que vous avez déjà chargé vos données dans la variable "btdata" en Python (un objet contenant les composants, les victoires, etc.).
# Par exemple : btdata = BtData(data) où "data" est un dictionnaire contenant les paires de données.
# Exemple de création de l'objet BtFit
# fit = BtFit(btdata, a=1)
# fit.fit()
# print(fit.pi)  # Affichage des forces estimées des éléments
