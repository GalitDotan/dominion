from game_mechanics.effects.effect import Effect


class ShuffleDiscardToDrawPile(Effect):

    def __init__(self):
        super().__init__()

    def activate(self, game, player=None) -> Any:
        """
        Shuffle the discard pile into the draw pile.
        """
        discard_pile = player.discard_pile
        draw_pile = player.draw_pile
        discard_pile.shuffle()
        cards = discard_pile.draw_all()
        draw_pile.put_all(cards)
