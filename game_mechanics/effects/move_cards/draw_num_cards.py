from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.shuffle_piles.shuffle_pile import ShuffleDiscardToDrawPile


class DrawNum(Effect):

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        """
        Draw num cards from player's draw pile to his hand.
        If draw pile gets emptied - shuffle it to the draw pile and keep drawing.
        If there are no more cards both in the draw and discard pile - stop.
        """
        cards = []
        draw_pile = player.draw_pile
        for _ in range(self.num):
            if draw_pile.is_empty():
                await game.apply_effect(ShuffleDiscardToDrawPile(), player)
            if draw_pile.is_empty():  # still empty
                break  # no more cards to draw
            cards.append(draw_pile.draw())
        player.hand.extend(cards)


def draw_card(self):
    """
    Get a card from the Draw pile and put it in the Hand.
    """
    if self.state.draw_pile.is_empty():
        self.shuffle_discard_to_draw_pile()
    return self.state.draw_pile.draw()


def draw_cards(self, amount: int):
    """
    Draw a card `amount` times.
    If the Draw and DiscardCard piles got emptied - it could return less than the desired `amount` of cards.
    """
    cards = [self.draw_card() for _ in range(amount)]
    return [card for card in cards if card]  # card could be None


def draw_hand(self, num: int = 5):
    return self.draw_cards(num)
