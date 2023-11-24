from game_mechanics.player.player import Player
from game_mechanics.screens.screen import Screen


class OpeningMessage(Screen):
    def __init__(self, my_player: Player, other_players: list[Player]):
        self.my_player = my_player
        self.other_names = ', '.join([player.name for player in other_players])

    def __repr__(self):
        return f"""
        ##############################################
          Welcome to Dominion, {self.my_player.name}!
          Meet your opponents: {self.other_names}
          Good Luck!
        ##############################################
        """
