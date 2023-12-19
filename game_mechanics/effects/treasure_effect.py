from typing import Callable, Any

from game_mechanics.effects.effect import Effect


class TreasureEffect(Effect):
    def __init__(self, value: int | Callable[[Any], int]):
        super().__init__()
        self.value = value

    def activate(self, game, player=None, **kwargs) -> Any:
        if type(self.value) is int:
            coins = self.value
        else:
            coins = self.value(game, player)
        player.turn_state.coins += coins
