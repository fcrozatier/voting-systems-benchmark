import numpy as np

from src.utilities import *
from src.votes import Vote


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


class BradleyTerry(Vote):
    def rank(self):
        self.ranking = ranking_from_scores(bradley_terry_scores(self.comparisons.matrix))
        return self.ranking
