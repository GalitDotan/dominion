from abc import ABC

from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.game_options import EmptyOptions
from game_mechanics.player.player import Player
from game_mechanics.states.game_state import GameState
from options import Options


class Reaction(Effect):
    def on_activation(self, game_state: GameState, decision: Options, player: Player):
        pass

    def __init__(self, effect_type: type[Effect]):
        super().__init__()
        self._effect_type = effect_type

    def should_activate(self, game_state: GameState):
        """
        Check if condition is satisfied.
        """
        return self._activation_condition(game_state)

    def activate_if_satisfied(self, game_state: GameState):
        """
        Activate reaction if condition is satisfied.
        """
        if self.should_activate(game_state):
            self.activate(game_state, EmptyOptions())
