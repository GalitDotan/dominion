from typing import Any

from pydantic import BaseModel

from game_mechanics.effects.effect import Effect


class IncStats(Effect):

    def __init__(self, game, coins: int = 0, actions: int = 0, buys: int = 0):
        super().__init__(game)
        self.coins = coins
        self.actions = actions
        self.buys = buys

    def activate(self, game, player=None) -> Any:
        player.turn_state.coins += self.coins
        player.turn_state.actions += self.actions
        player.turn_state.buys += self.buys


class IncStatsKwargs(BaseModel):
    coins: int
    actions: int
    buys: int
