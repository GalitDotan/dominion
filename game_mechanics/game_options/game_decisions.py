from abc import ABC
from typing import Any

from game_mechanics.game_supplies.card_types.card import Card
from options import ServerOptions


class GameOptions(ServerOptions, ABC):
    """
    Represents a decision a curr_player has to make.
    """
    pass


class EmptyOptions(GameOptions):
    """
    An "Empty Options" is a dummy decision (a curr_player does not have a decision to make.
    """

    def __init__(self):
        super().__init__(options=[], min_choices_allowed=0, max_choices_allowed=0)


class NumOptions(GameOptions):
    """
    Deciding on a number from given range.
    """

    def __init__(self, options: list[Any], min_choices_allowed: int = 1, max_choices_allowed: int = 1,
                 default: int = 0):
        super().__init__(options, min_choices_allowed, max_choices_allowed)
        self.num = default


class CardsOptions(GameOptions, ABC):
    """
    Choosing cards from a given list
    """

    def __init__(self, options: list[Any], min_choices_allowed: int, max_choices_allowed: int):
        super().__init__(options, min_choices_allowed, max_choices_allowed)
        self.chosen_cards: list[Card] = []
