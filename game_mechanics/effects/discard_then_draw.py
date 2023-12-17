from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision
from game_mechanics.game_options.range_options import RangeOptions


class DiscardThenDraw(Effect):
    """
    DiscardCard cards by decision, then draw as many.
    """

    def __init__(self):
        super().__init__()

    def activate(self, game, player=None) -> Any:

        player.hand.discard(to_discard)
        return RangeOptions(len(to_discard))
