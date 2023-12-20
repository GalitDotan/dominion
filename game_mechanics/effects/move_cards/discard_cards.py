from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision

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


class DiscardCards(Effect):
    """
    Discard a given number of cards.
    """

    def __init__(self, cards_amount: int | tuple[int, int]):
        super().__init__()
        self.cards_amount: int | tuple[int, int] = cards_amount

    def apply(self, game, player=None, **kwargs) -> Any:
        cards = game.apply_effect(PlayerDecision(), player, **kwargs)

        for card in cards:
            player.hand.remove(card)
            player.discard_pile.put(card)

    def _verify_chosen_amount(self, chosen_amount, remaining_amount):  # TODO: add this to functionality
        if type(self.cards_amount) is int:
            return self.cards_amount == chosen_amount or remaining_amount == 0
        else:
            min_amount, max_amount = self.cards_amount
            return (min_amount <= chosen_amount <= max_amount) or (min_amount > chosen_amount and remaining_amount == 0)


class DiscardHand(Effect):
    """
    Discard all cards in hand.
    """

    def apply(self, game, player=None, **kwargs) -> Any:
        pass
