from abc import ABC, abstractmethod
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision


class DiscardCards(Effect, ABC):
    """
    Discard a given number of cards.
    """

    def __init__(self, cards_amount: int | tuple[int, int] | None = None):
        """
        Args:
            cards_amount: the amount of cards to discard.
                * If type is int - require an exact number.
                * if type is tuple[int, int] - require a number from this range.
                * If type is None - don't limit the amount.
        """
        super().__init__()
        self.cards_amount: int | tuple[int, int] = cards_amount

    async def apply(self, game, player=None, cards=None, *args, **kwargs) -> Any:
        struct = self.get_card_structure(game, player, *args, **kwargs)
        if not cards:
            cards = self.get_cards_to_discard(game, struct, player, *args, **kwargs)

        for card in cards:
            struct.remove(card)
            player.discard_pile.put(card)

    async def get_cards_to_discard(self, game, struct, player=None, *args, **kwargs):
        return await game.apply_effect(PlayerDecision(struct.cards), player, **kwargs)

    @abstractmethod
    def get_card_structure(self, game, player=None, *args, **kwargs):
        pass

    def _verify_chosen_amount(self, chosen_amount, remaining_amount) -> bool:  # TODO: add this to functionality
        if self.cards_amount is None:
            return True
        if type(self.cards_amount) is int:
            return self.cards_amount == chosen_amount or remaining_amount == 0
        else:
            min_amount, max_amount = self.cards_amount
            return (min_amount <= chosen_amount <= max_amount) or (min_amount > chosen_amount and remaining_amount == 0)


class DiscardFromHand(DiscardCards):
    """
    Discard cards from hand.
    """

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand


class DiscardAllCardsInStruct(DiscardCards, ABC):
    """
    Move all cards from a structure to the discard pile.
    """

    async def get_cards_to_discard(self, game, struct, player=None, *args, **kwargs):
        return struct.cards


class DiscardHand(DiscardAllCardsInStruct):
    """
    Discard all cards from hand.
    """

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand


class DiscardPlayArea(DiscardAllCardsInStruct):
    """
    Discard all cards from player's play area.
    """

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.play_area
