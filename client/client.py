import requests

from consts import Endpoints
from game_mechanics.game_stages.turn import Turn
from game_mechanics.screens.openning_message import OpeningMessage


class DominionClient:
    def __init__(self):
        self.server_url = "127.0.0.1"
        self._url_format = self.server_url + '/{}'

    def get_url(self, endpoint: str):
        return self._url_format.format(endpoint)

    def init_game(self):
        requests.post(url=self.get_url(Endpoints.INIT_GAME))

    def join_game(self):
        pass

    def run(self):
        """
        Run a single-player Dominion game.
        """
        print(OpeningMessage(self._my_player, self._bot_players))
        game_on = True
        while True:
            curr_player = self._play_order[self.player_index]
            other_players = self._play_order.copy()
            other_players.remove(curr_player)

            turn = Turn(curr_player, other_players, self.supply, self.trash)
            turn.play()
            self.to_next_player()

        score_bard = ScoreBoard(self._play_order)
        print(score_bard)
