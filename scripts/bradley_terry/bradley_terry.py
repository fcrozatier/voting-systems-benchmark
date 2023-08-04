import numpy as np

from scripts.utilities import *


def bradley_terry_scores(M: np.ndarray[int], iterations=20, scores=[]):
    """
    Returns the individual scores of a matrix of win/loss comparisons, as computed by the Bradley-Terry algorithm
    """
    N = M.shape[0]

    if scores == []:
        # Initial scores
        scores = [1 / N for _ in range(N)]

    # https://en.wikipedia.org/wiki/Bradley-Terry_model#Estimating_the_parameters
    def compute_score(i):
        W_i = sum(M[i])
        D = 0
        for j in range(N):
            if j != i and (scores[i] + scores[j]) != 0:
                D += (M[i][j] + M[j][i]) / (scores[i] + scores[j])

        return W_i / D

    new_scores = [compute_score(i) for i in range(N)]
    normalized_new_scores = [v / sum(new_scores) for v in new_scores]

    if iterations == 1:
        return normalized_new_scores
    else:
        iterations -= 1
        return bradley_terry_scores(M, iterations, normalized_new_scores)


def bt(ranking: list[int], vote_budget: int, reassess=1, p=0.9):
    """
    ranking: the 'true' ranking
    vote_budget: how many votes to make
    reassess: how many times to compare a specific pair
    p: probability to vote according to the true ranking
    """
    N = len(ranking)
    M = np.zeros((N, N))

    remaining_votes = vote_budget
    while remaining_votes > 0:
        cycle = random_cycle(N)

        edges = cycle_edges(cycle)

        for i, j in edges:
            n = reassess
            while n > 0:
                n -= 1
                (l, w) = vote((i, j), ranking, p)
                remaining_votes -= 1
                M[w][l] += 1

                if remaining_votes == 0:
                    break
        else:
            continue
        break

    return ranking_from_scores(bradley_terry_scores(M))
