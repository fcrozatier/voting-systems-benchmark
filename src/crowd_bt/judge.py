from crowd_bt import bt
from numpy.random import choice, random, shuffle


def maybe_init_annotator(annotator, items):
    if annotator.next is None and annotator.prev is None:
        prev, next = choice(items, 2)
        annotator.prev = prev
        annotator.next = next


def choose_next(annotator, items):
    shuffle(items)  # useful for argmax case as well in the case of ties

    if random() < bt.EPSILON:
        return items[0]
    else:
        return bt.argmax(
            lambda i: bt.expected_information_gain(
                annotator.alpha, annotator.beta, annotator.prev.mu, annotator.prev.sigma_sq, i.mu, i.sigma_sq
            ),
            items,
        )


def perform_vote(annotator, next_won):
    if next_won:
        winner = annotator.next
        loser = annotator.prev
    else:
        winner = annotator.prev
        loser = annotator.next
    u_alpha, u_beta, u_winner_mu, u_winner_sigma_sq, u_loser_mu, u_loser_sigma_sq = bt.update(
        annotator.alpha, annotator.beta, winner.mu, winner.sigma_sq, loser.mu, loser.sigma_sq
    )
    annotator.alpha = u_alpha
    annotator.beta = u_beta
    winner.mu = u_winner_mu
    winner.sigma_sq = u_winner_sigma_sq
    loser.mu = u_loser_mu
    loser.sigma_sq = u_loser_sigma_sq
