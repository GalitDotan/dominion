from game_mechanics.effects.game_stages.phase.phase import Phase


class ActionPhase(Phase):
    def run_phase_iteration(self):
        pass  # TODO: play actions

    def activate(self, game, player=None) -> Any:
        pass
