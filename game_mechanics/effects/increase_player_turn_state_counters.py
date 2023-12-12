from game_mechanics.effects.effect import Effect
from game_mechanics.states.game_state import GameState


class IncStateCounter(Effect):
    def __init__(self, game_state: GameState, coins: int = 0, actions: int = 0, buys: int = 0):
        super().__init__(game_state)
        self.coins = coins
        self.actions = actions
        self.buys = buys

    def on_activation(self, game_state: None, player):
        turn_state = self.turn_state
        turn_state.coins += self.coins
        turn_state.actions += self.actions
        turn_state.buys += self.buys
