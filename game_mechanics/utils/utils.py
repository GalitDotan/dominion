from random import shuffle

from game_mechanics.game_supplies.card_types.card_type import CardType


def shuffle_copy(cards: list[CardType]):
    """
    Copy the list and return a shuffled version of it.

    :param cards: the cards.
    :return: a shuffled copy of the cards.
    """
    shuffled = cards.copy()
    shuffle(shuffled)
    return shuffled
