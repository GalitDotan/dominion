from game_mechanics.effects.effect import Effect
from game_mechanics.states.game import Game


class IncStateCounter(Effect):
    def __init__(self, game: Game, coins: int = 0, actions: int = 0, buys: int = 0):
        super().__init__(game)
        self.coins = coins
        self.actions = actions
        self.buys = buys

    def on_activation(self, game: None, player):
        turn_state = self.turn_state
        turn_state.coins += self.coins
        turn_state.actions += self.actions
        turn_state.buys += self.buys
