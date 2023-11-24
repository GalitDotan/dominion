from game_mechanics.player.player import Player
from game_mechanics.screens.screen import Screen


class ScoreBoard(Screen):
    def __init__(self, players: list[Player]):
        self.players_sorted_by_score = sorted(players, reverse=True)
        self.winner = self.players_sorted_by_score[0]

    def __repr__(self):
        title = f"*** The winner is {self.winner} ***"
        scores = "\r\n".join([f"{player.name}: {player.victory_points} VP [{player.turns_played} turns]" for player in
                              self.players_sorted_by_score])
        return f"{title}\r\n{scores}"
