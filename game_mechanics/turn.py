from typing import List

from game_mechanics.card_structures.trash import Trash
from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player
from game_mechanics.supply import Supply
from game_mechanics.player.turn_state import TurnState


class Turn:
    def __init__(self, player: Player, other_players: List[Player], supply: Supply, trash: Trash):
        self.player = player
        self.other_players = other_players
        self.supply = supply
        self.trash = trash

        self.turn_state = TurnState()

    def play(self):
        """
        Play one turn of the game (with all its phases).
        """
        self.player.turns_played += 1
        self._action_phase()
        self._buy_phase()
        self._night_phase()
        self._cleanup_phase()

    def _action_phase(self):
        continue_phase = True
        playable_cards = self.player.get_playable_cards(Phase.ActionPhase)
        while continue_phase and self.turn_state.actions > 0 and len(playable_cards) > 0:
            pass

    def _buy_phase(self):
        while self.turn_state.buys > 0:
            self.player.hand.sort(key=lambda x: x.name)

    def _night_phase(self):
        return

    def _cleanup_phase(self):
        self.player.discard_hand()
        self.player.discard_play()
