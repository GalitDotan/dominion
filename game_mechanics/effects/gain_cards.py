from typing import Any, Optional

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision


class GainCards(Effect):
    def __init__(self, amount: int | tuple[int, int] = -1, cost: int | tuple[int, int] = -1,
                 allowed_pile_names: Optional[list[str]] = None):
        """
        Default is (-1) meaning there is no limitation on the amount.
        """
        super().__init__()
        self.amount = amount
        self.cost = cost
        self.allowed_pile_names = allowed_pile_names

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        chosen_piles = await game.apply_effect(PlayerDecision(self.allowed_pile_names), player, *args, **kwargs)
        cards = []
        for pile_name in chosen_piles:
            cards.append(game.supply.get_card(pile_name))
        player.gain_cards(cards)


class GainCardsToHand(Effect):
    def __init__(self, amount: int | tuple[int, int] = -1, cost: int | tuple[int, int] = -1,
                 allowed_pile_names: Optional[list[str]] = None):
        super().__init__()
        self.amount = amount
        self.cost = cost
        self.allowed_pile_names = allowed_pile_names

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        cards = await game.apply_effect(GainCards(self.amount, self.cost, self.allowed_pile_names), player, *args, **kwargs)
        player.hand.extend(cards)
        return cards


class GainCardsToDiscard(Effect):
    def __init__(self, amount: int | tuple[int, int] = -1, cost: int | tuple[int, int] = -1,
                 allowed_pile_names: Optional[list[str]] = None):
        super().__init__()
        self.amount = amount
        self.cost = cost
        self.allowed_pile_names = allowed_pile_names

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        cards = await game.apply_effect(GainCards(self.amount, self.cost, self.allowed_pile_names), player, *args, **kwargs)
        player.discard_pile.put_all(cards)
        return cards
