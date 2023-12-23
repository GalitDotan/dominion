from typing import Any

from game_mechanics.effects.autoplay_treasures import AutoplayTreasures
from game_mechanics.effects.game_stages.phase.phase import Phase


class TreasurePhase(Phase):

    async def autoplay_cards(self, game, player=None, *args, **kwargs) -> Any:
        """
        For phases with autoplay features - override this.
        """
        await game.apply_effect(AutoplayTreasures(), player)
