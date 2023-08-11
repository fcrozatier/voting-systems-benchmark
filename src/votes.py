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
        while self.budget:
            n = self.rematch

            while n > 0:
                (i, j) = self.comparisons.next_comparison()
                (loser, winner) = vote((i, j), self.true_ranking, self.p)
                self.comparisons.record_vote(winner, loser)
                self.budget -= 1
                n -= 1

                if self.budget == 0:
                    break
            else:
                continue
            break
        return self

    def rank(self) -> list[int]:
        pass

    def score(self):
        return top_10(self.true_ranking, self.rank())
