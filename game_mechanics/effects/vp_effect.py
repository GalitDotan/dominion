from typing import Any, Callable

from pydantic import BaseModel

from game_mechanics.effects.effect import Effect


class VPEffect(Effect):
    def __init__(self, value: int | Callable[[Any], int]):
        super().__init__()
        self.value = value

    def activate(self, game, player=None) -> Any:
        value = self.estimate(game, player)
        player.achieved_victory_points += value

    def estimate(self, game, player=None) -> int:
        if type(self.value) is int:
            return self.value
        return self.value(game, player)


class VPEffectKwargs(BaseModel):
    value: int | Callable[[Any], int]
