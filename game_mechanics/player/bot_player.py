from game_mechanics.player.player import Player


class BotPlayer(Player):
    def __repr__(self, long: bool = False):
        return super().__repr__(long=long)
