from typing import Any

from game_mechanics.effects.discard import Discard
from game_mechanics.effects.draw_cards import DrawCards
from game_mechanics.effects.effect import Effect


class DiscardThenDraw(Effect):
    """
    DiscardCard cards by decision, then draw as many.
    """

    def __init__(self):
        super().__init__()

    async def apply(self, game, player=None, **kwargs) -> Any:
        discarded = await game.apply_effect(Discard(), player)
        return await game.apply_effect(DrawCards(amount=len(discarded)), player)
