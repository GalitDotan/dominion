from game_mechanics.game_config import GameConfiguration


class GameMaster:
    """
    The manager of the game.
    It runs the game, asks the players for decisions and applies them.
    """

    def __init__(self, game_conf: GameConfiguration):
        self.game_conf = game_conf

    def __hash__(self):
        return hash(self.game_conf)

    def run_game(self):
        pass
