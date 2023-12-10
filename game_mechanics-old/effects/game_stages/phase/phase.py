from abc import abstractmethod
from typing import Optional

from consts import HeadlineFormats
from game_mechanics.effects.game_stages.game_stage import GameStage
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.player.player import Player
from game_mechanics.states.game_state import GameState


class Phase(GameStage):
    def __init__(self, player: Player, opponents: list[Player], game_state: GameState, name: Optional[str] = None):
        super().__init__(player=player, opponents=opponents, game_state=game_state, name=name)
        self.continue_phase: bool = True

    def __repr__(self):
        return self.name

    @property
    def playable_types(self) -> tuple[Card, ...]:
        return ()

    def play(self):
        """
        Play this phase.
        Each type of phase can implement what happens before, during and after phase iterations.
        before_run_iterations() would happen ones in the beginning.
        Then there's a loop of run_phase_iteration().
        Then after_run_iterations() would run one time.
        """
        playable_cards = self.get_playable_cards()
        if not playable_cards:
            self.print("You have no action playable in hand... finishing phase")
            return
        self.print(HeadlineFormats.H1.format(f"Welcome to your {self.name} Phase!"))
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
   