from game_mechanics.decisions.bot.generic_choices import get_bot_player_choice
from game_mechanics.decisions.human.generic_choices import get_human_player_choice
from game_mechanics.decisions.player_decision import CommonChoices
from game_mechanics.game_stages.phase.phase import Phase
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_supplies.card_types import Action
from game_supplies.card_types.card import Card


class ActionPhase(Phase):
    @property
    def playable_types(self):
        return Action,

    def run_phase_iteration(self):
        """
        Play one action card by choice.
        """
        playable_cards = self.get_playable_cards()
        if self.turn_state.actions == 0 or len(playable_cards) == 0:
            return False
        self.continue_phase = self.play_action_by_choice(playable_cards)

    def play_action_by_choice(self, playable_cards: dict[Card, int]) -> bool:
        """
        Choose an action to play
        -
        :param playable_cards: the options to play
        :return: Was a change made?
        """
        playable_cards_keys = list(playable_cards.keys())
        valid_choices = [CommonChoices.NONE_CHOICE.name] + [str(card) for card in playable_cards_keys]
        if isinstance(self.player, BotPlayer):
            chosen_card = get_bot_player_choice(self.player, playable_cards)
        else:
            player: HumanPlayer
            # TODO: display_choices_from_human_hand(player, phase=PhaseName.ActionPhase)
            answer = get_human_player_choice(valid_choices)
            if answer is CommonChoices.NONE_CHOICE:
                return False
            choice = int(answer)
            chosen_card = playable_cards_keys[choice - 1]
        self.player.play_card_from_hand(chosen_card, self.turn_state)
        return True
