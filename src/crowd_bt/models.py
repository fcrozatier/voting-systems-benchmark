from src.crowd_bt import bt


class Annotator:
    def __init__(self) -> None:
        self.alpha = bt.ALPHA_PRIOR
        self.beta = bt.BETA_PRIOR
        self.prev: Item = None
        self.next: Item = None

    def update_next(self, new_next):
        self.prev = self.next
        self.next = new_next


class Item:
    def __init__(self, id) -> None:
        self.id = id
        self.mu = bt.MU_PRIOR
        self.sigma_sq = bt.SIGMA_SQ_PRIOR
