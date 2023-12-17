from game_mechanics.effects.effect import Effect
from game_mechanics.effects.shuffle_piles.shuffle_pile import ShuffleDiscardToDrawPile


class DrawNum(Effect):

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def activate(self, game, player=None):
        """
        Draw num cards from player's draw pile to his hand.
        If draw pile gets emptied - shuffle it to the draw pile and keep drawing.
        If there are no more cards both in the draw and discard pile - stop.
        """
        cards = []
        draw_pile = player.draw_pile
        for _ in range(self.num):
            if draw_pile.is_empty():
                game.apply_effect(ShuffleDiscardToDrawPile())
            if draw_pile.is_empty():  # still empty
                break  # no more cards to draw
            cards.append(draw_pile.draw())
        player.hand.put_all(cards)
