from game_mechanics.decisions.game_decisions import NumDecision
from game_mechanics.effects.effect import Effect


class Draw(Effect):
    def on_activation(self, decision: NumDecision):
        self.player.draw(decision.num)
