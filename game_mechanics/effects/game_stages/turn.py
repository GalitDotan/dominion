from typing import Any

from game_mechanics.effects.game_stages.game_stage import GameStage
from game_mechanics.effects.game_stages.phase.action_phase import ActionPhase
from game_mechanics.effects.game_stages.phase.buy_phase import BuyPhaseTreasures
from game_mechanics.effects.game_stages.phase.cleanup_phase import CleanUpPhase
from game_mechanics.effects.game_stages.phase.night_phase import NightPhase

PHASE_ORDER = (ActionPhase, BuyPhaseTreasures, NightPhase, CleanUpPhase)


class Turn(GameStage):
    """
    One turn of a Dominion game.
    Includes 4 stages:
        1. Action
        2. Buy
        3. Night
        4. Clean-up
    
    The play function is responsible for managing all the state changes and the decision.
    """

    def __init__(self):
        super().__init__()
        self.is_finished: bool = False
        self.played = []
        self.added = []
        self.removed = []

        self.phase_order = PHASE_ORDER

    def activate(self, game, player=None) -> Any:
        """
        Play this turn (with all its phases).
        """
        curr_player = game.curr_player
        opponents = game.get_opponents(player.name)

        curr_player.on_turn_start(my_turn=True)
        for opponent in opponents:
            opponent.on_turn_start(my_turn=False)

        for CurrPhase in self.phase_order:
            game.apply_effect(CurrPhase())
