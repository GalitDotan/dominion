from random import shuffle

from game_mechanics.game_supplies.card_types.card import Card


def shuffle_copy(cards: list[Card]):
    """
    Copy the list and return a shuffled version of it.

    :param cards: the cards_packs.
    :return: a shuffled copy of the cards_packs.
    """
    shuffled = cards.copy()
    shuffle(shuffled)
    return shuffled
