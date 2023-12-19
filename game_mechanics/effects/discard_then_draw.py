from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.range_options import RangeOptions


class DiscardThenDraw(Effect):
    """
    DiscardCard cards by decision, then draw as many.
    """

    def __init__(self):
        super().__init__()

    def activate(self, game, player=None) -> Any:
        to_discard = []  # TODO: choice effect
        player.hand.discard(to_discard)
        return RangeOptions(to_discard)  # TODO: is this what I want?
