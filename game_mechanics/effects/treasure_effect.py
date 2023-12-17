from typing import Callable, Any

from pydantic import BaseModel

from game_mechanics.effects.effect import Effect


class TreasureEffect(Effect):
    def __init__(self, value: int | Callable[[Any], int]):
        super().__init__()
        self.value = value

    def activate(self, game, player=None) -> Any:
        if type(self.value) is int:
            coins = self.value
        else:
            coins = self.value(game, player)
        player.turn_state.coins += coins


class TreasureEffectKwargs(BaseModel):
    value: int | Callable[[Any], int]
