from typing import Optional

from game_mechanics.effects.game_stages.game_stage import GameStage
from options import Options


class Phase(GameStage):
    def on_activation(self, game_state, decision: Options, player: str):
        pass

    def __init__(self, player: str, opponents: list[str], game_state, name: Optional[str] = None):
        super().__init__(player=player, opponents=opponents, game_state=game_state, name=name)
        self.continue_phase: bool = True

    def __repr__(self):
        return self.name
