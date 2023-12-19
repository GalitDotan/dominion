from typing import Any

from game_mechanics.effects.effect import Effect

'''
def discard_hand(self):
    """
    Move all cards from hand to DiscardCard pile.
    """
    cards = self.state.hand.remove_all()
    self.state.discard_pile.put_all(cards)


def discard_play(self):
    """
    Move all non-Duration cards from the Play Area to the DiscardCard pile.
    """
    cards = self.state.play_area.do_cleanup()
    self.state.discard_pile.put_all(cards)

'''


class DiscardCard(Effect):

    def activate(self, game, player=None) -> Any:
        pass


class DiscardCards(Effect):

    def activate(self, game, player=None) -> Any:
        pass


class DiscardHand(Effect):
    def activate(self, game, player=None) -> Any:
        pass
