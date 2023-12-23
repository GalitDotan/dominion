from typing import Any

from game_mechanics.effects.draw_cards import DrawCards
from game_mechanics.effects.game_stages.phase.phase import Phase
from game_mechanics.effects.move_cards.discard_cards import DiscardHand, DiscardPlayArea


class CleanUpPhase(Phase):
    async def apply(self, game, player=None, draw_amount=5, *args, **kwargs) -> Any:
        if player:
            game.apply_effect(DiscardHand(), player)
            game.apply_effect(DiscardPlayArea(), player)
            game.apply_effect(DrawCards(amount=draw_amount), player)
