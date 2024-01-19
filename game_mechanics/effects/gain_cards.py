from abc import abstractmethod, ABC
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerCheckboxChoice


class GainCard(Effect, ABC):
    def __init__(self, pile_name: str):
        super().__init__()
        self.pile_name = pile_name

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        card = game.supply.get_card(self.pile_name)
        if not card:
            return
        player.gain_card(card)
        struct = self.get_card_structure(game, player, *args, **kwargs)
        struct.append(card)
        return card

    @abstractmethod
    def get_card_structure(self, game, player=None, *args, **kwargs):
        pass


class GainCardToHand(GainCard):

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand


class GainCardToDiscard(GainCard):

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.discard_pile


class GainCardsDecision(Effect):

    def __init__(self, gain_type: type[GainCard] = GainCardToDiscard,
                 amount: int | tuple[int, int] = -1,
                 cost: int | tuple[int, int] = -1,
                 allowed_pile_names: list[str] | None = None):
        """
        Asking the player to choose piles to gain from, the applying a gain effect.

        Args:
            gain_type: The type of gain effect.
            amount: Amount of cards to gain. Could be a number, a range, or (-1) for unlimited.
            cost: Cost of the card to gain. Could be a number, a range, or (-1) for unlimited.
            allowed_pile_names: If not None - limit the options only to the allowed piles_sorted.
        """
        super().__init__()
        self.gain_type: type[GainCard] = gain_type
        self.amount = amount
        self.cost = cost
        self.allowed_pile_names = allowed_pile_names

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        chosen_piles = await game.apply_effect(PlayerCheckboxChoice(self.allowed_pile_names), player, *args, **kwargs)
        gained_cards = []
        for pile_name in chosen_piles:
            card = await game.apply_effect(self.gain_type(pile_name), player, *args, **kwargs)
            if card:
                gained_cards.append(card)
        return gained_cards
