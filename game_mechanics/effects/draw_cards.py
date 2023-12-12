from game_mechanics.game_options.range_options import RangeOptions
from game_mechanics.effects.effect import Effect


class Draw(Effect):
    def on_activation(self, game_state: RangeOptions, player):
        self.player.draw(decision.num)
