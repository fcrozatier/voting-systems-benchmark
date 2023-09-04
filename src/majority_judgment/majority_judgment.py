from random import sample
from typing import Dict, Self

import numpy as np

from src.utilities import clip, random_list_from_gaussian_scores, top_10


class MajorityJudgement:
    def __init__(self, N, budget) -> None:
        self.N = N
        self.budget = budget
        self.ranked_entries = random_list_from_gaussian_scores(N)

        self.start_vote()

    def start_vote(self) -> Self:
        while self.budget > 0:
            item = sample(self.ranked_entries, 1)[0]

            self.single_vote(item)
            self.budget -= 1

            if self.budget == 0:
                break

        return self

    def single_vote(self, item: dict):
        note = clip(np.random.normal(item["score"], 2), minimum=0, maximum=10)

        if "votes" not in item:
            item["votes"] = []

        item["votes"].append(note)

    def rank(self) -> list[int]:
        for item in self.ranked_entries:
            item["final"] = np.median(item["votes"])

        self.ranked = sorted(self.ranked_entries, key=lambda x: x["final"], reverse=True)
        return self.ranked

    def score(self):
        true_ranking = list(map(lambda x: x["index"], self.ranked_entries))
        final_ranking = list(map(lambda x: x["index"], self.rank()))
        return top_10(true_ranking, final_ranking)
