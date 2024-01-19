from abc import ABC, abstractmethod
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.gain_cards import GainCardToDiscard, GainCard, GainCardToHand
from game_mechanics.effects.player_decision import PlayerCheckboxChoice


class BuyCard(Effect, ABC):
    def __init__(self, pile_name: str):
        super().__init__()
        self.pile_name = pile_name

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        if not player:
            player = game.curr_player

        # gain card from the pile
        gain_effect_type: type[GainCard] = self.get_gain_effect(game, player, *args, **kwargs)
        gained_card = await game.apply_effect(gain_effect_type(self.pile_name), player, *args, **kwargs)

        # update stats
        player.turn_stats.coins -= gained_card.cost
        player.turn_stats.buys -= 1

    @abstractmethod
    def get_gain_effect(self, game, player=None, *args, **kwargs) -> type[GainCard]:
        pass


class BuyCardToDiscard(BuyCard):

    def get_gain_effect(self, game, player=None, *args, **kwargs):
        return GainCardToDiscard


class BuyCardToHand(BuyCard):

    def get_gain_effect(self, game, player=None, *args, **kwargs):
        return GainCardToHand


class BuyCardsDecision(Effect):

    def __init__(self, buy_type: type[BuyCard] = BuyCardToDiscard,
                 amount: int | tuple[int, int] = -1,
                 cost: int | tuple[int, int] = -1):
        """
        Asking the player to choose piles to gain from, the applying a gain effect.

        Args:
            amount: Amount of cards to gain. Could be a number, a range, or (-1) for unlimited.
            cost: Cost of the card to gain. Could be a number, a range, or (-1) for unlimited.
        """
        super().__init__()
        self.buy_type: type[BuyCard] = buy_type
        self.amount = amount
        self.cost = cost

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        """
        Asking the player to choose piles to gain from, the applying a gain effect.
        """
        allowed_piles = game.supply.get_non_empty_pile_names(card_condition=lambda p: p.cost <= player.turn_stats.coins)
        chosen_piles = await game.apply_effect(PlayerCheckboxChoice(allowed_piles), player, *args, **kwargs)
        bought_cards = []
        for pile_name in chosen_piles:
            card = await game.apply_effect(self.buy_type(pile_name))
            if card:
                bought_cards.append(card)
        return bought_cards
