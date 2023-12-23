from game_mechanics.effects.game_stages.phase.phase import Phase


class ActionPhase(Phase):

    def should_continue(self, player) -> bool:
        return self.has_playable_cards(player) and player.turn_stats.actions > 0
