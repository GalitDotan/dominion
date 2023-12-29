from random import shuffle

from game_mechanics.game_supplies.base_card import CardObject


def shuffle_copy(cards: list[CardObject]):
    """
    Copy the list and return a shuffled version of it.

    :param cards: the cards.
    :return: a shuffled copy of the cards.
    """
    shuffled = cards.copy()
    shuffle(shuffled)
    return shuffled
