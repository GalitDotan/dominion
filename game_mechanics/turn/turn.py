from typing import Any

from game_mechanics.card_structures.trash import Trash
from game_mechanics.choices.action_choices import play_action_by_choice
from game_mechanics.choices.buy_choices import play_treasures_by_choice, buy_card_by_choice, autoplay_treasures
from game_mechanics.consts import HeadlineFormats
from game_mechanics.phases.phases import Phase
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.player.turn_state import TurnState
from game_mechanics.supply import Supply


class Turn:
    def __init__(self, player: Player, other_players: list[Player], supply: Supply, trash: Trash):
        self.name = f"{player.name}'s {player.turns_played + 1} Turn"
        self.player = player
        self.other_players = other_players
        self.supply = supply
        self.trash = trash

        self.turn_state = TurnState()
        self.is_finished: bool = False
        self.played = []
        self.added = []
        self.removed = []

    def play(self):
        """
        Play one turn of the game (with all its phases).
        """
        print(HeadlineFormats.H1.format(f"{self.player.name}'s turn"))
        self.player.turns_played += 1

        phases = [self._action_phase, self._buy_phase, self._night_phase, self._cleanup_phase]

        for phase in phases:
            if isinstance(self.player, HumanPlayer):
                self.print_if_human(self)
            phase()

    def print_if_human(self, message: Any):
        if isinstance(self.player, HumanPlayer):
            print(str(message))

    def __repr__(self):
        opponents = '\r\n'.join([str(player) for player in self.other_players])
        you_h1 = HeadlineFormats.H1.format(f"You [{self.player.name}]")
        opponents_h1 = HeadlineFormats.H1.format("The Other Players")
        if not self.is_finished:
            return f"""
{you_h1}
{self.turn_state}
{self.player}
{opponents_h1}
{opponents}
{self.supply}
        """
        end_turn = HeadlineFormats.H2.format(f"{self.player.name}'s turn has ended")
        played = HeadlineFormats.H3.format(f"Played: {self.played}")
        added = HeadlineFormats.H3.format(f"Added: {self.added}")
        removed = HeadlineFormats.H3.format(f"Removed: {self.removed}")
        return f"""
        {end_turn}
        {played}
        {added}
        {removed}
        """

    def _action_phase(self):
        continue_phase = True
        playable_cards = self.player.get_playable_cards(Phase.ActionPhase)
        if not playable_cards:
            self.print_if_human("You have no action cards in hand... moving to buy phase")
            return
        self.print_if_human(HeadlineFormats.H1.format("Welcome to your Action Phase!"))
        while continue_phase and self.turn_state.actions > 0 and len(playable_cards) > 0:
            play_action_by_choice(self.player, self.turn_state)
            playable_cards = self.player.get_playable_cards(Phase.ActionPhase)

    def _buy_phase(self):
        self.print_if_human(HeadlineFormats.H1.format("Welcome to your Buy Phase!"))

        continue_play_treasures = True
        playable_cards = self.player.get_playable_cards(Phase.BuyPhase)
        if len(playable_cards) > 0:
            self.print_if_human(f'Playable cards: {[str(card) for card in playable_cards]}')
            self.print_if_human("You may choose treasures to play")
            autoplay_treasures(self.player, self.turn_state)
            playable_cards = self.player.get_playable_cards(Phase.BuyPhase)
        while continue_play_treasures and self.turn_state.buys > 0 and len(playable_cards) > 0:
            continue_play_treasures = play_treasures_by_choice(self.player, self.turn_state)
            playable_cards = self.player.get_playable_cards(Phase.BuyPhase)

        self.print_if_human("Now, let's buy some cards")
        self.print_if_human(str(self.supply))
        continue_buys = True
        piles_to_buy_from = self.supply.get_piles_allowed_for_buy(max_cost=self.turn_state.coins)
        while continue_buys and len(piles_to_buy_from) > 0 and self.turn_state.buys > 0:
            buy_card_by_choice(self.player, self.turn_state, self.supply)

    def _night_phase(self, include_night: bool = False):
        if include_night:
            self.print_if_human(HeadlineFormats.H1.format("Welcome to your Night Phase!"))
        return

    def _cleanup_phase(self):
        self.player.discard_hand()
        self.player.discard_play()
