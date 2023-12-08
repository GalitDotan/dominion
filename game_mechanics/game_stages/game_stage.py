from abc import abstractmethod
from typing import Any, Optional

from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.states.game_state import GameState


class GameStage:
    def __init__(self, player: Player, opponents: list[Player], game_state: GameState, name: Optional[str] = None):
        self.name = name if name else self.__class__.__name__
        self.player = player
        self.opponents = opponents
        self.game_state = game_state
        self.verbose: bool = True

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def play(self):
        pass

    def print(self, message: Any):
        """
        Print to screen, only if the curr_player is human.
        """
        if self.verbose and isinstance(self.player, HumanPlayer):
            print(str(message))
