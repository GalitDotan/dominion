from abc import ABC, abstractmethod
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision


class PlayCard(Effect, ABC):
    """
    Put a card from a structure to the play area and apply all card's effects.
    """

    def __init__(self, card, from_struct):
        super().__init__()
        self.card = card
        self.from_struct = from_struct

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        self.from_struct.remove(self.card)
        player.play_area.play(self.card)
        for effect in self.card.effects_to_activate(game):
            await game.apply_effect(effect, player)


class PlayCardDecision(Effect, ABC):
    """
    Decide which card to play and play it.
    """

    async def apply(self, game, player=None, card=None, *args, **kwargs) -> Any:
        """
        Move given card from given card structure to the play area.
        Apply all the effect of the card for the current phase.
        """
        struct = self.get_card_structure(game, player=None, *args, **kwargs)
        if not card:
            playable_cards = struct.get_cards_for_phase(self)
            card = PlayerDecision(playable_cards, allow_none_noice=True)
        if card:
            return game.apply_effect(PlayCard(card=card,
                                              from_struct=self.get_card_structure(game, player, *args, **kwargs)))

    @abstractmethod
    def get_card_structure(self, game, player=None, *args, **kwargs):
        pass


class PlayCardFromHand(PlayCardDecision):

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand
