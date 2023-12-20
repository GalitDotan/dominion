from abc import abstractmethod, ABC
from typing import Any

from game_mechanics.effects.game_stages.game_stage import GameStage


class Phase(GameStage, ABC):

    def __init__(self):
        super().__init__()
        self.continue_phase: bool = True

    def apply(self, game, player=None) -> Any:
        """
        Play this phase.
        Each type of phase can implement what happens before, during and after phase iterations.
        before_run_iterations() would happen ones in the beginning.
        Then there's a loop of run_phase_iteration().
        Then after_run_iterations() would run one time.

        Args:
            game: The game.
            player: The player.
        """
        game.send_player_view(f'Starting {self.name}')
        game.curr_phase = self
        playable_cards = game.get_playable_cards()
        if not playable_cards:
            game.send_player_view(f'No playable cards for {self.name}')
            return
        self.before_run_iterations()
        while self.continue_phase:
            self.run_phase_iteration()
        self.after_run_iterations()

    def before_run_iterations(self):
        return

    def after_run_iterations(self):
        return

    @abstractmethod
    def run_phase_iteration(self):
        pass
