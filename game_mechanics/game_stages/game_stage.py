from abc import abstractmethod
from typing import Any, Optional

from game_mechanics.card_structures.trash import Trash
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.supply import Supply


class GameStage:
    def __init__(self, player: Player, other_players: list[Player], supply: Supply, trash: Trash,
                 name: Optional[str] = None):
        self.name = name if name else self.__class__.__name__
        self.player = player
        self.other_players = other_players
        self.supply = supply
        self.trash = trash
        self.verbose: bool = True

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def play(self):
        pass

    def print_if_human(self, message: Any):
        """
        Print to screen, only if the player is human.
        """
        if self.verbose and isinstance(self.player, HumanPlayer):
            print(str(message))
