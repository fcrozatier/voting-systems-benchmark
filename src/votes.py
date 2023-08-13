from typing import Self

from src.pairings import *
from src.utilities import *


class Vote:
    def __init__(self, comparisons: Pairings, budget: int, rematch=1, p=1) -> None:
        self.comparisons = comparisons
        self.budget = budget
        self.rematch = rematch
        self.p = p
        self.true_ranking = random_cycle(comparisons.N)

        self.start_vote()

    def start_vote(self) -> Self:
        while self.budget > 0:
            (i, j) = self.comparisons.next_comparison()

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

    def single_vote(self, pair: tuple, ranking: list, p: int = 1):
        return vote(pair, ranking, p)

    def rank(self) -> list[int]:
        pass

    def score(self):
        return top_10(self.true_ranking, self.rank())
