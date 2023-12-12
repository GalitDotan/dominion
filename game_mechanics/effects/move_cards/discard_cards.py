from game_mechanics.effects.effect import Effect
from game_mechanics.states.game_state import GameState
from options import Options


class DiscardCard(Effect):
    def on_activation(self, game_state: GameState, options: Options, player: Player):
        pass


class DiscardCards(Effect):
    def on_activation(self, game_state: GameState, options: Options, player: Player):
        pass


class DiscardHand(Effect):
    def on_activation(self, game_state: GameState, options: Options, player: Player):
        pass
