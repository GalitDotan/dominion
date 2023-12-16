from game_mechanics.effects.effect import Effect


class DrawNum(Effect):

    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def activate(self, game, player=None):
        player.draw(self.num)
