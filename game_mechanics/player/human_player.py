from game_mechanics.player.player import Player


class HumanPlayer(Player):
    def __repr__(self, long: bool = True):
        return super().__repr__(long=long)
