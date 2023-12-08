from asyncio import sleep
from typing import Optional

import websockets

from options import ClientOptions, Options
from config import Endpoints, ServerConf
from game_mechanics.game_options.game_decisions import GameOptions
from consts import GameStatus
from utils.name_generator import generate_name


class DominionClient:
    def __init__(self):
        self._server_url = f'{ServerConf.SCHEMA}://{ServerConf.IP}:{ServerConf.PORT}'
        self._url_format = self._server_url + '{}'

        self.player_name: str = generate_name()
        self.game_id: Optional[str] = None

    async def _get_server_response(self, endpoint: str, data: dict) -> str | bytes:
        """
        Get response from the game server.
        """
        url = self._url_format.format(endpoint)
        async with websockets.connect(url) as websocket:
            await websocket.send(data)
            return await websocket.recv()

    def init_game(self) -> str:
        """
        Request a game initiation.
        """
        response = self._get_server_response(Endpoints.INIT_GAME, {})
        self.game_id = response.game_id
        return response.message

    def start_game(self) -> str:
        """
        Start the previously initiated game.
        """
        response = self._get_server_response(Endpoints.INIT_GAME, {'game_id': self.game_id})
        return response.message

    def join_game(self) -> str:
        """
        Join a previously initiated game.
        """
        response = self._get_server_response(Endpoints.JOIN_GAME,
                                             {'game_id': self.game_id, 'player_name': self.player_name})
        self.game_id = response.game_id
        return response.message

    def view_players(self) -> str:
        response = self._get_server_response(Endpoints.VIEW_PLAYERS, {'game_id': self.game_id})
        return response.message

    def view_game_board(self) -> str:
        """
        Request an updated view of the game board.
        """
        response = self._get_server_response(Endpoints.VIEW_GAME_BOARD,
                                             {'game_id': self.game_id, 'player_name': self.player_name})
        return response.message

    def get_game_status(self) -> GameStatus:
        """
        Request an updated game status.
        """
        response = self._get_server_response(Endpoints.GAME_STATUS,
                                             {'game_id': self.game_id, 'player_name': self.player_name})
        return response.game_status

    def get_decision(self) -> Optional[GameOptions]:
        """
        Check if there's a decision to make.
        If there is - get it.
        """
        response = self._get_server_response(Endpoints.GET_DECISION,
                                             data={'game_id': self.game_id, 'player_name': self.player_name})
        return response.game_decision

    def send_decision_response(self, choices: list[int] | int):
        """
        After a choice has been made - send it to the server.
        """
        response = self._get_server_response(Endpoints.DECIDE,
                                             data={'game_id': self.game_id, 'player_name': self.player_name,
                                                   'decision': choices})

    def play_game(self):
        """
        Play a Dominion game.
        """
        game_status: GameStatus = self.get_game_status()
        while game_status == GameStatus.IN_PROGRESS:
            decision = self.get_decision()
            if decision:
                self.make_decision(decision)
                self.send_decision_response(decision.indexes_chosen)

    def make_decision(self, decision: Options):
        """
        Print decision and get client's response.
        If valid - update decision.
        Otherwise - repeat.
        """
        answer = input(decision)
        if ' ' in answer:
            choices = [int(c) for c in answer.split()]
        else:
            choices = [int(answer)]
        if not decision.is_valid_choice(choices):
            print("Invalid choice")
            self.make_decision(decision)
        decision.decide(choices)

    async def hello(self):
        uri = f'{ServerConf.SCHEMA}://{ServerConf.IP}/{Endpoints.WEB_SOCKET}:{ServerConf.PORT}'
        print(uri)
        async with websockets.connect(uri) as websocket:
            name = input("What's your name? ")

            await websocket.send(name)
            print(f">>> {name}")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")

    def run(self):
        print(f'Hello {self.player_name} and welcome to Dominion')
        decision = ClientOptions(options=['Init', 'Join'], min_choices_allowed=1, max_choices_allowed=1)
        self.make_decision(decision)
        if decision.decision == 'Init':
            self.init_game()
            print(f'Current players: {self.view_players()}')
            decision = ClientOptions(options=['Yes', 'No'], min_choices_allowed=1, max_choices_allowed=1,
                                     question="Would you like to start the game?")
            while not decision.decided or decision.decision == 'Yes':
                decision.undo_decision()
                self.make_decision(decision)
        else:
            self.join_game()
            game_status: GameStatus = self.get_game_status()
            while game_status != GameStatus.IN_PROGRESS:
                sleep(1)

        self.play_game()


if __name__ == '__main__':
    client = DominionClient()
    client.hello()
