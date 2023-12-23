from abc import ABC
from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.game_stages.game_stage import GameStage
from game_mechanics.effects.move_cards.play_card import PlayCard


class Phase(GameStage, ABC):
    def __init__(self, phase_effect: type[Effect] = PlayCard):
        super().__init__()
        self.phase_effect: type[Effect] = phase_effect

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        await self.autoplay_cards(game, player, *args, **kwargs)
        await self.play_phase(game, player, *args, **kwargs)

    async def play_phase(self, game, player=None, *args, **kwargs) -> Any:
        while self.should_continue(player):
            card = self.apply_phase_effect(game, player)
            if not card:
                break

    def apply_phase_effect(self, game, player):
        return game.apply_effect(self.phase_effect(), player)

    def should_continue(self, player) -> bool:
        return self.has_playable_cards(player)

    def has_playable_cards(self, player) -> bool:
        return player.hand.get_cards_for_phase(self)

    async def autoplay_cards(self, game, player=None, *args, **kwargs) -> Any:
        """
        For phases with autoplay features - override this.
        """
        return
