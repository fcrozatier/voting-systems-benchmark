import numpy as np


def strongest_paths(M):
    """
    Input: M a comparison matrix with (i,j) the number of times i is preferred to j

    Output: P a matrix with (i,j) the strength of the strongest path i->j

    Reference: https://en.wikipedia.org/wiki/Schulze_method#Implementation
    """

    N = np.shape(M)[0]
    P = np.copy(M)

    for i in range(N):
        for j in range(i + 1, N):
            if P[i][j] < P[j][i]:
                P[i][j] = 0
            else:
                P[j][i] = 0

    for i in range(N):
        for j in range(N):
            if i != j:
                for k in range(N):
                    if i != k and j != k:
                        P[j][k] = max(P[j][k], min(P[j, i], P[i][k]))

    return P


def schulze_ranking(S):
    """
    input: strongest path matrix
    output: schulze ranking in increasing order
    """
    N = np.shape(S)[0]
    ranking = [0]

    i = 1
    while i < N:
        for index, j in enumerate(ranking):
            if S[i][j] < S[j][i]:
                ranking.insert(index, i)
                break
        else:
            ranking.insert(len(ranking), i)

        i += 1

    return ranking
