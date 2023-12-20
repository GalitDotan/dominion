from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.gain_cards import GainCardsToDiscard


class BuyCardsToDiscard(Effect):
    def __init__(self, amount: int | tuple[int, int] = -1, cost: int | tuple[int, int] = -1):
        """
        Default is (-1) meaning there is no limitation on the amount.
        """
        super().__init__()
        self.amount = amount
        self.cost = cost

    def apply(self, game, player=None, *args, **kwargs) -> Any:
        gained_cards = game.apply_effect(GainCardsToDiscard(self.amount, self.cost), player, *args, **kwargs)
        player.turn_stats.coins -= sum([card.cost for card in gained_cards])
        player.turn_stats.buys -= len(gained_cards)
