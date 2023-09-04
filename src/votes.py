from typing import Self, Type

from src.pairings import *
from src.utilities import *


class Vote:
    def __init__(self, N=500, budget=1000, comparisons_cls: Type[Pairings] = Random, rematch=1, p=1) -> None:
        self.N = N
        self.comparisons = comparisons_cls(N)
        self.budget = budget
        self.rematch = rematch
        self.p = p
        self.true_ranking = random_list(N)

        self.start_vote()

    def start_vote(self) -> Self:
        while self.budget > 0:
            (i, j) = self.next_comparison()

            n = self.rematch
            while n > 0:
                (loser, winner) = self.single_vote((i, j), self.true_ranking, self.p)
                self.comparisons.record_vote(winner, loser)
                self.budget -= 1
                n -= 1

                if self.budget == 0:
                    break
            else:
                continue
            break
        return self

    def next_comparison(self):
        # Subclasses can hook into this function
        return self.comparisons.next_comparison()

    def single_vote(self, pair: tuple, ranking: list, p: int = 1):
        # Subclasses can hook into this function
        return vote(pair, ranking, p)

    def rank(self) -> list[int]:
        # Subclasses must implement this function
        pass

    def score(self, func=top_10):
        return func(self.true_ranking, self.rank())
