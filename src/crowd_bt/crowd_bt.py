# https://github.com/anishathalye/gavel/blob/master/gavel/crowd_bt.py

from typing import Self

from numpy import exp, log
from scipy.special import betaln, psi

from src.crowd_bt.judge import *
from src.crowd_bt.models import Annotator, Item
from src.pairings import Pairings
from src.utilities import *
from src.votes import Vote

# See this paper for more information:
# http://people.stern.nyu.edu/xchen3/images/crowd_pairwise.pdf

# parameters chosen according to experiments in paper
GAMMA = float(0.1)  # tradeoff parameter
LAMBDA = float(1)  # regularization parameter
KAPPA = float(0.0001)  # to ensure positivity of variance
MU_PRIOR = float(0)
SIGMA_SQ_PRIOR = float(1)
ALPHA_PRIOR = float(10)
BETA_PRIOR = float(1)
EPSILON = 0.25  # epsilon-greedy


def argmax(f, xs):
    return max(xs, key=f)


# via https://en.wikipedia.org/wiki/Normal_distribution
def divergence_gaussian(mu_1, sigma_sq_1, mu_2, sigma_sq_2):
    ratio = sigma_sq_1 / sigma_sq_2

    return (mu_1 - mu_2) ** 2 / (2 * sigma_sq_2) + (ratio - 1 - log(ratio)) / 2


# via https://en.wikipedia.org/wiki/Beta_distribution
def divergence_beta(alpha_1, beta_1, alpha_2, beta_2):
    return (
        betaln(alpha_2, beta_2)
        - betaln(alpha_1, beta_1)
        + (alpha_1 - alpha_2) * psi(alpha_1)
        + (beta_1 - beta_2) * psi(beta_1)
        + (alpha_2 - alpha_1 + beta_2 - beta_1) * psi(alpha_1 + beta_1)
    )


# returns new (alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser)
def update(alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser):
    (updated_alpha, updated_beta, _) = update_annotator(
        alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser
    )
    (updated_mu_winner, updated_mu_loser) = update_mus(
        alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser
    )
    (updated_sigma_sq_winner, updated_sigma_sq_loser) = update_sigma_sqs(
        alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser
    )
    return (
        updated_alpha,
        updated_beta,
        updated_mu_winner,
        updated_sigma_sq_winner,
        updated_mu_loser,
        updated_sigma_sq_loser,
    )


def expected_information_gain(alpha, beta, mu_a, sigma_sq_a, mu_b, sigma_sq_b):
    (alpha_1, beta_1, c) = update_annotator(alpha, beta, mu_a, sigma_sq_a, mu_b, sigma_sq_b)
    (mu_a_1, mu_b_1) = update_mus(alpha, beta, mu_a, sigma_sq_a, mu_b, sigma_sq_b)
    (sigma_sq_a_1, sigma_sq_b_1) = update_sigma_sqs(alpha, beta, mu_a, sigma_sq_a, mu_b, sigma_sq_b)
    prob_a_ranked_above = c
    (alpha_2, beta_2, _) = update_annotator(alpha, beta, mu_b, sigma_sq_b, mu_a, sigma_sq_a)
    (mu_b_2, mu_a_2) = update_mus(alpha, beta, mu_b, sigma_sq_b, mu_a, sigma_sq_a)
    (sigma_sq_b_2, sigma_sq_a_2) = update_sigma_sqs(alpha, beta, mu_b, sigma_sq_b, mu_a, sigma_sq_a)

    return prob_a_ranked_above * (
        divergence_gaussian(mu_a_1, sigma_sq_a_1, mu_a, sigma_sq_a)
        + divergence_gaussian(mu_b_1, sigma_sq_b_1, mu_b, sigma_sq_b)
        + GAMMA * divergence_beta(alpha_1, beta_1, alpha, beta)
    ) + (1 - prob_a_ranked_above) * (
        divergence_gaussian(mu_a_2, sigma_sq_a_2, mu_a, sigma_sq_a)
        + divergence_gaussian(mu_b_2, sigma_sq_b_2, mu_b, sigma_sq_b)
        + GAMMA * divergence_beta(alpha_2, beta_2, alpha, beta)
    )


# returns (updated mu of winner, updated mu of loser)
def update_mus(alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser):
    mult = (alpha * exp(mu_winner)) / (alpha * exp(mu_winner) + beta * exp(mu_loser)) - (exp(mu_winner)) / (
        exp(mu_winner) + exp(mu_loser)
    )
    updated_mu_winner = mu_winner + sigma_sq_winner * mult
    updated_mu_loser = mu_loser - sigma_sq_loser * mult

    return (updated_mu_winner, updated_mu_loser)


# returns (updated sigma squared of winner, updated sigma squared of loser)
def update_sigma_sqs(alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser):
    mult = (alpha * exp(mu_winner) * beta * exp(mu_loser)) / ((alpha * exp(mu_winner) + beta * exp(mu_loser)) ** 2) - (
        exp(mu_winner) * exp(mu_loser)
    ) / ((exp(mu_winner) + exp(mu_loser)) ** 2)

    updated_sigma_sq_winner = sigma_sq_winner * max(1 + sigma_sq_winner * mult, KAPPA)
    updated_sigma_sq_loser = sigma_sq_loser * max(1 + sigma_sq_loser * mult, KAPPA)

    return (updated_sigma_sq_winner, updated_sigma_sq_loser)


# returns (updated alpha, updated beta, pr i >k j which is c)
def update_annotator(alpha, beta, mu_winner, sigma_sq_winner, mu_loser, sigma_sq_loser):
    c_1 = exp(mu_winner) / (exp(mu_winner) + exp(mu_loser)) + 0.5 * (sigma_sq_winner + sigma_sq_loser) * (
        exp(mu_winner) * exp(mu_loser) * (exp(mu_loser) - exp(mu_winner))
    ) / ((exp(mu_winner) + exp(mu_loser)) ** 3)
    c_2 = 1 - c_1
    c = (c_1 * alpha + c_2 * beta) / (alpha + beta)

    E_heta = (c_1 * (alpha + 1) * alpha + c_2 * alpha * beta) / (c * (alpha + beta + 1) * (alpha + beta))
    E_heta_sq = (c_1 * (alpha + 2) * (alpha + 1) * alpha + c_2 * (alpha + 1) * alpha * beta) / (
        c * (alpha + beta + 2) * (alpha + beta + 1) * (alpha + beta)
    )

    variance = E_heta_sq - E_heta**2
    updated_alpha = ((E_heta - E_heta_sq) * E_heta) / variance
    updated_beta = (E_heta - E_heta_sq) * (1 - E_heta) / variance

    return (updated_alpha, updated_beta, c)


class CrowdBTPairings(Pairings):
    def __init__(self, N) -> None:
        super().__init__(N)

        self.annotators = [Annotator() for _ in range(N)]
        self.items = [Item(i) for i in range(N)]
        self.current_annotator = None

    def next_comparison(self) -> tuple[int, int]:
        annotator: Annotator = np.random.choice(self.annotators)
        maybe_init_annotator(annotator, self.items)

        annotator.update_next(choose_next(annotator, self.items))
        prev = annotator.prev
        next = annotator.next

        self.current_annotator = annotator

        return (prev.id, next.id)


class CrowdBT(Vote):
    def single_vote(self, pair: tuple, ranking: list, p: int = 1):
        comparisons: CrowdBTPairings = self.comparisons
        loser_id, winner_id = vote(pair, ranking, p)
        next_wins = winner_id == pair[1]
        perform_vote(comparisons.current_annotator, next_wins)
        return loser_id, winner_id

    def rank(self):
        comparisons: CrowdBTPairings = self.comparisons
        self.ranking = list(map(lambda i: i.id, sorted(comparisons.items, key=lambda i: i.mu)))
        return self.ranking
