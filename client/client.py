from typing import Optional

import requests

from consts import Endpoints, GameStatus
from game_mechanics.game_stages.turn import Turn
from game_mechanics.screens.openning_message import OpeningMessage
from response_model.response_model import ResponseModel
from utils.name_generator import generate_name


class DominionClient:
    def __init__(self):
        self._server_url = "127.0.0.1"
        self._url_format = self._server_url + '/{}'

        self.player_name: str = generate_name()
        self.game_id: Optional[str] = None

    def _get_response(self, endpoint: str, data: dict) -> ResponseModel:
        url = self._url_format.format(endpoint)
        response = requests.post(url=url, data=data)
        date = ResponseModel(**response.json())
        return date

    def init_game(self) -> str:
        response = self._get_response(Endpoints.INIT_GAME, {})
        self.game_id = response.game_id
        return response.message

    def start_game(self) -> str:
        response = self._get_response(Endpoints.INIT_GAME, {'game_id': self.game_id})
        return response.message

    def join_game(self) -> str:
        response = self._get_response(Endpoints.JOIN_GAME, {'game_id': self.game_id, 'player_name': self.player_name})
        self.game_id = response.game_id
        return response.message

    def view_game_board(self) -> str:
        response = self._get_response(Endpoints.VIEW_GAME_BOARD,
                                      {'game_id': self.game_id, 'player_name': self.player_name})
        return response.message

    def get_game_status(self) -> str:
        response = self._get_response(Endpoints.VIEW_GAME_BOARD,
                                      {'game_id': self.game_id, 'player_name': self.player_name})
        return response.game_status.name

    def play_game(self):
        """
        Play a Dominion game.
        """
        game_Status = self.get_game_status()
        while game_Status == GameStatus.IN_PROGRESS:
            curr_player = self._play_order[self.player_index]  # TODO: fix
            other_players = self._play_order.copy()
            other_players.remove(curr_player)

            turn = Turn(curr_player, other_players, self.supply, self.trash)
            turn.play()
            self.to_next_player()

    def run(self):
        pass  # TODO: run client


if __name__ == '__main__':
    client = DominionClient()
    client.run()
