from game_mechanics.game_options.game_decisions import NumOptions
from game_mechanics.effects.effect import Effect


class Draw(Effect):
    def on_activation(self, decision: NumOptions):
        self.player.draw(decision.num)
