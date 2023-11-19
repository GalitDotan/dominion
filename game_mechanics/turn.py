from typing import List

from game_mechanics.card_structures.trash import Trash
from game_mechanics.interactions.action_choices import do_action_choice
from game_mechanics.interactions.buy_choices import play_treasures_by_choice
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
        if playable_cards:
            print("Welcome to your Action Phase!")
        else:
            print("You have no action cards in hand... moving to buy phase")
        while continue_phase and self.turn_state.actions > 0 and len(playable_cards) > 0:
            do_action_choice(self.player)
            playable_cards = self.player.get_playable_cards(Phase.ActionPhase)

    def _buy_phase(self):
        print("Welcome to your Buy Phase!")

        continue_play_treasures = True
        playable_cards = self.player.get_playable_cards(Phase.BuyPhase)
        if len(playable_cards) > 0:
            print("Play your treasures")
        while continue_play_treasures and self.turn_state.buys > 0 and len(playable_cards) > 0:
            continue_play_treasures = play_treasures_by_choice(self.player)
            playable_cards = self.player.get_playable_cards(Phase.BuyPhase)

        print("Now, let's buy some cards")
        print(str(self.supply))

    def _night_phase(self, include_night: bool = False):
        if include_night:
            print("Welcome to your Night Phase!")
        return

    def _cleanup_phase(self):
        self.player.discard_hand()
        self.player.discard_play()
