import numpy as np

from src.bradley_terry.bradley_terry import bradley_terry_scores


def test_bradley_terry_scores():
    # Worked example
    # https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model#Estimating_the_parameters
    M = np.zeros((4, 4))
    M[0][1] = 2
    M[0][2] = 0
    M[0][3] = 1

    M[1][0] = 3
    M[1][2] = 5
    M[1][3] = 0

    M[2][0] = 0
    M[2][1] = 3
    M[2][3] = 1

    M[3][0] = 4
    M[3][1] = 0
    M[3][2] = 3

    values = [0.148, 0.304, 0.164, 0.384]
    estimates = bradley_terry_scores(M, 1)

    for i, p in enumerate(estimates):
        assert round(p, 3) == values[i]

    values = [0.139, 0.226, 0.143, 0.492]
    estimates = bradley_terry_scores(M, 19)

    for i, p in enumerate(estimates):
        assert round(p, 3) == values[i]
