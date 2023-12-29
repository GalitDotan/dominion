from typing import Any

from game_mechanics.effects.game_stages.game_stage import GameStage
from game_mechanics.effects.game_stages.phase.action_phase import ActionPhase
from game_mechanics.effects.game_stages.phase.buy_phase import BuyPhase
from game_mechanics.effects.game_stages.phase.cleanup_phase import CleanUpPhase
from game_mechanics.effects.game_stages.phase.night_phase import NightPhase
from game_mechanics.effects.game_stages.phase.treasure_phase import TreasurePhase
from game_mechanics.player.player_turn_state import PlayerTurnStats

PHASE_ORDER = (ActionPhase, TreasurePhase, BuyPhase, NightPhase, CleanUpPhase)


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

    async def apply(self, game, player=None, **kwargs) -> Any:
        """
        Play this turn (with all its phases).
        """
        curr_player = game.curr_player
        opponents = game.get_opponents_ordered(player.name)

        curr_player.turns_played += 1

        curr_player.init_turn_state(my_turn=True)
        for opponent in opponents:
            opponent.init_turn_state(my_turn=False)

        for CurrPhase in self.phase_order:
            await game.apply_effect(CurrPhase(), curr_player)

    def init_turn_state(self, player, is_curr):
        """
        Initiate the state of current turn.
        By Default:
            * For current player - is initiated with 1 action, 1 buy and 0 coins.
            * For other player - is initiated with 0 action, 0 buy and 0 coins.

        Args:
            my turn: is current turn mine.
        """
        actions = 1 if is_curr else 0
        buys = 1 if is_curr else 0
        player.turn_stats = PlayerTurnStats(actions=actions, buys=buys, coins=0)
