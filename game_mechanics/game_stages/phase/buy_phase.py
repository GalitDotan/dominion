from game_mechanics.decisions.old.human.generic_choices import get_human_player_multy_choice
from game_mechanics.decisions.old.player_decision import CommonChoices
from game_mechanics.game_stages.phase.buying_stage import BuyingStage
from game_mechanics.game_stages.phase.phase import Phase
from game_mechanics.game_supplies.card_types.treasure_card import Treasure
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer


class BuyPhase(Phase):
    @property
    def playable_types(self):
        return Treasure,

    def before_run_iterations(self):
        """
        Autoplay treasures, if any exists in hand.
        """
        playable_cards = self.get_playable_cards()
        if len(playable_cards) > 0:
            self.print_if_human(f'Playable cards: {[str(card) for card in playable_cards]}')
            self.print_if_human("You may choose treasures to play")
            self.autoplay_treasures()

    def after_run_iterations(self):
        buying_stage = BuyingStage(player=self.player, turn_state=self.turn_state, supply=self.supply,
                                   opponents=self.opponents, trash=self.trash)
        buying_stage.play()

    def run_phase_iteration(self):
        """
        Play one action card by choice.
        """
        playable_cards = self.get_playable_cards()
        if self.turn_state.buys == 0 or len(playable_cards) == 0:
            return False
        self.continue_phase = self.play_treasures_by_choice()

    def autoplay_treasures(self):
        """
        Play all treasures that are defined for automatic play
        """
        if isinstance(self.player, BotPlayer):
            answer = "Y"
        else:
            answer = input("Autoplay treasures? y/n: ").upper()
        if not answer or answer == "Y":
            playable_cards = self.get_playable_cards()
            for card, cnt in playable_cards.items():
                card: Treasure
                if card.automatic_play:
                    for _ in range(cnt):
                        self.player.play_card_from_hand(card, self.turn_state)

    def play_treasures_by_choice(self) -> bool:
        """
        Allow curr_player to choose treasure cards from his hand.
        """
        playable_cards = self.get_playable_cards()
        playable_cards_keys = list(playable_cards.keys())
        valid_choices = [CommonChoices.NONE_CHOICE.name]
        valid_choices.extend([card.name for card in playable_cards_keys])
        if isinstance(self.player, BotPlayer):
            choices = list(range(1, len(valid_choices)))
        else:
            player: HumanPlayer
            choices = get_human_player_multy_choice(valid_choices, "Choose treasures to play")

        if choices[0] is CommonChoices.NONE_CHOICE:
            return False
        chosen_cards = [playable_cards_keys[int(i) - 1] for i in choices]
        for card in chosen_cards:
            for _ in range(playable_cards[card]):
                self.player.play_card_from_hand(card, self.turn_state)
        return True
