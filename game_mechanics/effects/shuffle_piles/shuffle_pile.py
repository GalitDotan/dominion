from typing import Any

from game_mechanics.effects.effect import Effect

'''
def shuffle_discard_to_draw_pile(self):
    """
    Shuffle all cards in the DiscardCard pile and put them on the bottom of the Draw pile.
    """
    cards = self.state.discard_pile.draw_all()
    shuffle(cards)
    self.state.discard_pile.put_all(cards)
'''


class ShuffleDiscardToDrawPile(Effect):

    def __init__(self):
        super().__init__()

    def apply(self, game, player=None) -> Any:
        """
        Shuffle the discard pile into the draw pile.
        """
        discard_pile = player.discard_pile
        draw_pile = player.draw_pile
        discard_pile.shuffle()
        cards = discard_pile.draw_all()
        draw_pile.put_all(cards)
