from typing import Any

from game_mechanics.consts import HeadlineFormats
from game_mechanics.game_stages.game_stage import GameStage
from game_mechanics.game_stages.phase.action_phase import ActionPhase
from game_mechanics.game_stages.phase.buy_phase import BuyPhase
from game_mechanics.game_stages.phase.cleanup_phase import CleanUpPhase
from game_mechanics.game_stages.phase.night_phase import NightPhase
from game_mechanics.game_stages.phase.phase import Phase
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.states.player_turn_state import PlayerTurnState
from game_mechanics.states.game_state import GameState


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

    def __init__(self, player: Player, opponents: list[Player], game_state: GameState):
        super().__init__(player, opponents, game_state, name=f"{player.name}'s {player.turns_played + 1} Turn")

        self.turn_state = PlayerTurnState()
        self.opponents_turn_stage = {opponent: PlayerTurnState(actions=0, buys=1, coins=0) for opponent in
                                     self.opponents}
        self.is_finished: bool = False
        self.played = []
        self.added = []
        self.removed = []

    def play(self):
        """
        Play one game_stages of the game (with all its phases).
        """
        print(HeadlineFormats.H1.format(f"{self.player.name}'s game_stages"))
        self.player.turns_played += 1

        for CurrPhase in [ActionPhase, BuyPhase, NightPhase, CleanUpPhase]:
            CurrPhase: type
            if isinstance(self.player, HumanPlayer):
                self.print_if_human(self)
            phase: Phase = CurrPhase(player=self.player, opponents=self.opponents, turn_state=self.turn_state,
                                     game_state=self.game_state)
            phase.play()

    def print_if_human(self, message: Any):
        if isinstance(self.player, HumanPlayer):
            print(str(message))

    def __repr__(self):
        opponents = '\r\n'.join([str(player) for player in self.opponents])
        you_h1 = HeadlineFormats.H1.format(f"You [{self.player.name}]")
        opponents_h1 = HeadlineFormats.H1.format("The Other Players")
        if not self.is_finished:
            return f"""
{you_h1}
{self.turn_state}
{self.player}
{opponents_h1}
{opponents}
{self.game_state.supply}
        """
        end_turn = HeadlineFormats.H2.format(f"{self.player.name}'s game_stages has ended")
        played = HeadlineFormats.H3.format(f"Played: {self.played}")
        added = HeadlineFormats.H3.format(f"Added: {self.added}")
        removed = HeadlineFormats.H3.format(f"Removed: {self.removed}")
        return f"""
        {end_turn}
        {played}
        {added}
        {removed}
        """

    def _night_phase(self, include_night: bool = False):
        if include_night:
            self.print_if_human(HeadlineFormats.H1.format("Welcome to your Night Phase!"))
        return

    def _cleanup_phase(self):
        self.player.discard_hand()
        self.player.discard_play()
