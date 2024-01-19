from abc import ABC, abstractmethod
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerCheckboxChoice


class PlayCard(Effect, ABC):
    """
    Put a card from a structure to the play area and apply all card's effects.
    """

    def __init__(self, card):
        super().__init__()
        self.card = card

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        """
        Move the card from the structure to the play area.
        """
        card_struct = self.get_card_structure(game, player, *args, **kwargs)
        card_struct.remove(self.card)
        player.play_area.play(self.card)
        for effect in self.card.effects_to_activate(game):
            await game.apply_effect(effect, player)

    @abstractmethod
    def get_card_structure(self, game, player=None, *args, **kwargs):
        pass


class PlayCardFromHand(PlayCard):

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand


class PlayCardDecision(Effect, ABC):
    """
    Decide which card to play and play it.
    """

    def __init__(self, play_type: type[PlayCard]):
        """
        Asking the player to choose piles to gain from, the applying a gain effect.

        Args:
            play_type
        """
        super().__init__()
        self.play_type: type[PlayCard] = play_type

    async def apply(self, game, player=None, card=None, *args, **kwargs) -> Any:
        """
        Move given card from given card structure to the play area.
        Apply all the effect of the card for the current phase.
        """
        struct = self.get_card_structure(game, player=None, *args, **kwargs)
        if not card:
            playable_cards = struct.get_cards_for_phase(self)
            card = PlayerCheckboxChoice(playable_cards, allow_none_noice=True)
        if card:
            return await game.apply_effect(self.play_type(card), player, *args, **kwargs)

    @abstractmethod
    def get_card_structure(self, game, player=None, *args, **kwargs):
        pass


class PlayCardFromHandDecision(PlayCardDecision):
    def __init__(self):
        super().__init__(play_type=PlayCardFromHand)

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand
