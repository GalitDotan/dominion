from typing import Any

from game_mechanics.effects.game_stages.phase.phase import Phase


class ActionPhase(Phase):
    def run_phase_iteration(self):
        pass  # TODO: play actions

    async def apply(self, game, player=None, **kwargs) -> Any:
        pass
