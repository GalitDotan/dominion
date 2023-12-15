from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.empty_options import EmptyOptions
from options import Options


class Reaction(Effect):
    def on_activation(self, game, decision: Options, player: str):
        pass

    def __init__(self, effect_type: type[Effect]):
        super().__init__()
        self._effect_type = effect_type

    def should_activate(self, game):
        """
        Check if condition is satisfied.
        """
        return self._activation_condition(game)

    def activate_if_satisfied(self, game):
        """
        Activate reaction if condition is satisfied.
        """
        if self.should_activate(game):
            self.activate(game, EmptyOptions())
