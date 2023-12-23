from typing import Any

from game_mechanics.effects.game_stages.phase.phase import Phase


class SetupPhase(Phase):  # TODO: move setup functionality here
    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        pass
