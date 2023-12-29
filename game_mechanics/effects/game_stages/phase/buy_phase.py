from game_mechanics.effects.buy_cards import BuyCardsDecision
from game_mechanics.effects.game_stages.phase.phase import Phase


class BuyPhase(Phase):
    def __init__(self):
        super().__init__(phase_effect=BuyCardsDecision)

    def should_continue(self, player) -> bool:
        return player.turn_stats.buys > 0
