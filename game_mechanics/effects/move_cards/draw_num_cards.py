from game_mechanics.effects.effect import Effect
from game_mechanics.states.game import Game


class DrawNum(Effect):
    def __init__(self, game: Game, num: int):
        super().__init__(game)
        self.num = num

    def on_activation(self, game: None, player):
        self.player.draw(self.num)
