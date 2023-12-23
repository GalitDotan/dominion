from abc import ABC, abstractmethod
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.gain_cards import GainCardsToDiscard, GainCards


class BuyCards(Effect, ABC):
    def __init__(self, amount: int | tuple[int, int] = -1, cost: int | tuple[int, int] = -1):
        """
        Default is (-1) meaning there is no limitation on the amount.
        """
        super().__init__()
        self.amount = amount
        self.cost = cost

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        gain_effect_type: type[GainCards] = self.get_gain_effect(game, player, *args, **kwargs)
        gained_cards = await game.apply_effect(gain_effect_type(self.amount, self.cost), player, *args, **kwargs)
        player.turn_stats.coins -= sum([card.cost for card in gained_cards])
        player.turn_stats.buys -= len(gained_cards)

    @abstractmethod
    def get_gain_effect(self, game, player=None, *args, **kwargs) -> type[GainCards]:
        pass


class BuyCardsToDiscard(BuyCards):

    def get_gain_effect(self, game, player=None, *args, **kwargs):
        return GainCardsToDiscard
