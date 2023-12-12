from abc import ABC
from typing import Optional

from game_mechanics.effects.effect import Effect


class GameStage(Effect, ABC):
    def __init__(self, player: str, opponents: list[str], game_state, name: Optional[str] = None):
        super().__init__()
        self.name = name if name else self.__class__.__name__
        self.player = player
        self.opponents = opponents
        self.game_state = game_state
        self.verbose: bool = True
