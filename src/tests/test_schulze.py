import numpy as np

from src.schulze.schulze import *


def test_strongest_path_and_ranking():
    # https://en.wikipedia.org/wiki/Schulze_method#Example

    M = np.zeros((5, 5))
    M[0][1] = 20
    M[0][2] = 26
    M[0][3] = 30
    M[0][4] = 22
    M[1][0] = 25
    M[1][2] = 16
    M[1][3] = 33
    M[1][4] = 18
    M[2][0] = 19
    M[2][1] = 29
    M[2][3] = 17
    M[2][4] = 24
    M[3][0] = 15
    M[3][1] = 12
    M[3][2] = 28
    M[3][4] = 14
    M[4][0] = 23
    M[4][1] = 27
    M[4][2] = 21
    M[4][3] = 31

    P = strongest_paths(M)

    S = np.zeros((5, 5))
    S[0][1] = 28
    S[0][2] = 28
    S[0][3] = 30
    S[0][4] = 24
    S[1][0] = 25
    S[1][2] = 28
    S[1][3] = 33
    S[1][4] = 24
    S[2][0] = 25
    S[2][1] = 29
    S[2][3] = 29
    S[2][4] = 24
    S[3][0] = 25
    S[3][1] = 28
    S[3][2] = 28
    S[3][4] = 24
    S[4][0] = 25
    S[4][1] = 28
    S[4][2] = 28
    S[4][3] = 31

    assert np.shape(P) == (5, 5)
    for i in range(5):
        for j in range(5):
            assert P[i][j] == S[i][j]

    ranking = schulze_ranking(P)

    assert ranking == [3, 1, 2, 0, 4]
