from abc import abstractmethod
from enum import Enum
from typing import Any

from game_mechanics.player.player import Player


class CommonChoices(Enum):
    NONE_CHOICE = 'x'
    UNDO = 'undo'
    HELP_CHOICE = 'help'


class PlayerDecision:
    """
    A representation of a decision that needs to be made in the game.
    """

    def __init__(self, options: list[Any], player: Player, allow_none: bool = True, multi_choice: bool = False):
        if allow_none and CommonChoices.NONE_CHOICE not in options:
            options.append(CommonChoices.NONE_CHOICE)

        self.options = options
        self.allow_none = allow_none
        self.multi_choice = multi_choice
        self.player = player

    @abstractmethod
    def __repr__(self):
        pass
