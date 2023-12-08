from game_mechanics.effects.effect import Effect
from game_mechanics.states.game_state import GameState


class DrawNum(Effect):
    def __init__(self, game_state: GameState, num: int):
        super().__init__(game_state)
        self.num = num

    def on_activation(self, game_state: None, player):
        self.player.draw(self.num)
