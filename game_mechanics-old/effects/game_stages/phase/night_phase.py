from game_mechanics.effects.game_stages.phase.phase import Phase
from game_mechanics.game_supplies.card_types.night_card import Night


class NightPhase(Phase):
    @property
    def playable_types(self):
        return Night,

    def run_phase_iteration(self):
        pass
