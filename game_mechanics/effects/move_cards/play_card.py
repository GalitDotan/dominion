from abc import ABC, abstractmethod
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision


class PlayCard(Effect, ABC):

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
            struct.remove(card)
            player.play_area.play(card)
            for effect in card.effects_to_activate(game):
                await game.apply_effect(effect, player)
        return card

    @abstractmethod
    def get_card_structure(self, game, player=None, *args, **kwargs):
        pass


class PlayCardFromHand(PlayCard):

    def get_card_structure(self, game, player=None, *args, **kwargs):
        return player.hand
