from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerChoiceFromRange
from game_mechanics.effects.reactions.on_effect_reaction import Reaction
from game_mechanics.effects.shuffle_piles.shuffle_pile import ShuffleDiscardToDrawPile


class DrawCards(Effect):
    def __init__(self, amount: int | tuple[int, int]):
        super().__init__()
        self.amount = amount

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        """
        Draw num cards from player_name's draw pile to his hand.
        If draw pile gets emptied - shuffle it to the draw pile and keep drawing.
        If there are no more cards both in the draw and discard pile - stop.
        """
        if type(self.amount) is int:
            draw_amount = self.amount
        elif type(self.amount) is tuple:
            draw_amount = self.amount if type(self.amount) is int else await game.apply_effect(
                PlayerChoiceFromRange(self.amount), player)
        else:
            draw_amount = 0
        cards = []
        draw_pile = player.draw_pile
        for _ in range(draw_amount):
            if draw_pile.is_empty():
                await game.apply_effect(ShuffleDiscardToDrawPile(), player)
            if draw_pile.is_empty():  # still empty
                break  # no more cards to draw
            cards.append(draw_pile.draw())
        player.hand.extend(cards)
        # self._add_awaiting_reactions(game, player.name, cards)
        return cards

    def _add_awaiting_reactions(self, game, player_name, drawn_cards):
        for card in drawn_cards:
            if drawn_cards.REACTION in card.types():  # TODO: update
                game.add_waiting_reaction(Reaction(react_on_effect=DrawCards, apply_condition=None), player_name)


class DrawHand(DrawCards):
    def __init__(self, amount: int = 5):
        super().__init__(amount)
