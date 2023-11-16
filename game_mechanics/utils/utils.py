from random import shuffle
from typing import List

from game_supplies.card_types.card import Card


def shuffle_copy(cards: List[Card]):
    """
    Copy the list and return a shuffled version of it.

    :param cards: the cards.
    :return: a shuffled copy of the cards.
    """
    shuffled = cards.copy()
    shuffle(shuffled)
    return shuffled
