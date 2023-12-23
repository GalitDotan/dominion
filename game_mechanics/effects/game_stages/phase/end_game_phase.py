from typing import Any

from game_mechanics.effects.game_stages.phase.phase import Phase
from game_mechanics.game_status import GameStatus


class EndGamePhase(Phase):

    async def apply(self, game, player=None, **kwargs) -> Any:
        game.game_conf.status = GameStatus.FINISHED
        # TODO: play all players victory cards

    def run_phase_iteration(self):
        pass
