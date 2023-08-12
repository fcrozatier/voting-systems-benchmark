from src.crowd_bt import crowd_bt


class Annotator:
    def __init__(self) -> None:
        self.alpha = crowd_bt.ALPHA_PRIOR
        self.beta = crowd_bt.BETA_PRIOR
        self.prev: Item = None
        self.next: Item = None

    def update_next(self, new_next):
        self.prev = self.next
        self.next = new_next


class Item:
    def __init__(self, id) -> None:
        self.id = id
        self.mu = crowd_bt.MU_PRIOR
        self.sigma_sq = crowd_bt.SIGMA_SQ_PRIOR
