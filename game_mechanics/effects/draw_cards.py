from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerIntDecision
from game_mechanics.effects.reactions.on_effect_reaction import Reaction


class DrawCards(Effect):
    def __init__(self, amount: int | tuple[int, int]):
        super().__init__()
        self.amount = amount

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        if type(self.amount) is int:
            draw_amount = self.amount
        elif type(self.amount) is tuple:
            draw_amount = self.amount if type(self.amount) is int else await game.apply_effect(
                PlayerIntDecision(self.amount), player)
        else:
            draw_amount = 0
        cards = player.draw_pile.draw_cards(draw_amount)
        player.hand.extend(cards)
        self._add_awaiting_reactions(game, player.name, cards)
        return cards

    def _add_awaiting_reactions(self, game, player_name, drawn_cards):
        for card in drawn_cards:
            if drawn_cards.REACTION in card.types():
                game.add_waiting_reaction(Reaction(react_on_effect=DrawCards, apply_condition=None), player_name)
