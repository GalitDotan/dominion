from game_mechanics.game_stages.phase.phase import Phase
from game_mechanics.player.player import Player
from game_mechanics.states.game_state import GameState


class CleanUpPhase(Phase):

    def __init__(self, player: Player, opponents: list[Player], game_state: GameState):
        super().__init__(player, opponents, game_state)
        self.verbose: bool = False

    def run_phase_iteration(self):
        # TODO: discard play
        # TODO: discard hand
        pass
