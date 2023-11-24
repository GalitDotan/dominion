from game_mechanics.choices.action_choices import play_action_by_choice
from game_mechanics.game_stages.phase.phase import Phase
from game_supplies.card_types import Action


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
        self.continue_phase = play_action_by_choice(self.player, self.turn_state)
