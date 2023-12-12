from typing import Any

from game_mechanics.game_options.game_options import GameOptions


class RangeOptions(GameOptions):
    """
    Deciding on a number from given range.
    """

    def __init__(self, options: list[Any], min_choices_allowed: int = 1, max_choices_allowed: int = 1,
                 default: int = 0):
        super().__init__(options, min_choices_allowed, max_choices_allowed)
        self.num = default
