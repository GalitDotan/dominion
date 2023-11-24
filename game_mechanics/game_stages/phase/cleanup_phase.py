from typing import Optional

from game_mechanics.player.player import Player
from game_mechanics.player.turn_state import TurnState
from game_mechanics.game_stages.phase.phase import Phase


class CleanUpPhase(Phase):
    def run_phase_iteration(self):
        pass

    def __init__(self, name: Optional[str], player: Player, turn_state: TurnState):
        super().__init__(name, player, turn_state)
        self.verbose: bool = False
