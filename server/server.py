import asyncio
from threading import Thread

import websockets
from fastapi import FastAPI, WebSocket
from fastapi.exceptions import HTTPException

from config import Endpoints, ServerConf
from game_mechanics.game import Game
from game_status import GameStatus
from models.game_initiator import GameInitiator
from response_model.response_model import ResponseModel

app = FastAPI()

games: dict[str, Game] = {}
game_initiators: dict[str, GameInitiator]
game_runners: set[Thread] = set()


def game_runner(game: Game):
    """
    This function runs the given game from beginning to end.
    """
    game.run()


def _get_game_if_exists(game_id: str, search_active: bool = True) -> Game or GameInitiator:
    """
    Returns the game matching the id, if exists and is active.

    Params:
        game_id: the id of the game.
        search_active: if true - searches an active game. Otherwise, searches the matching GameInitiator.

    Returns:
        the matching game.

    Raises:
        HTTPException: 404, if given id is not an active game.
    """
    game_dict = games if search_active else game_initiators
    if game_id not in game_dict:
        raise HTTPException(404, detail=f"The ID {game_id} does not exist")
    return game_dict[game_id]


@app.post(Endpoints.INIT_GAME)
async def init_game(initiator: GameInitiator) -> ResponseModel:
    """
    Receives a game initiator and initiates a game.
    """
    game_initiators[initiator.game_id] = initiator
    return ResponseModel(game_id=initiator.id,
                         game_status=GameStatus.INITIATED)


@app.post(Endpoints.START_GAME)
async def start_game(game_id: str) -> ResponseModel:
    """
     Starts a given game.
    """
    initiator: GameInitiator = _get_game_if_exists(game_id, search_active=False)
    game = initiator.init_game()
    games[game.id] = game
    game_initiators.pop(initiator.game_id)
    runner = Thread(target=game_runner, args=(game,))
    game_runners.add(runner)
    runner.run()
    return ResponseModel(game_id=game_id,
                         game_status=GameStatus.IN_PROGRESS,
                         message="Game started")


@app.post(Endpoints.JOIN_GAME)
async def join_game(game_id: str, player_name: str) -> ResponseModel:
    """
    Join an initiated game.
    This would create a player with a given name and add it to a game.
    Note: this would only work if the game hasn't been started yet.

    Params:
        game_id: The game to join.
        player_name: The name of the player to add.
    """
    initiator = _get_game_if_exists(game_id, search_active=False)
    initiator.add_player(player_name)
    return ResponseModel(game_id=game_id,
                         game_status=GameStatus.IN_PROGRESS,
                         message="Player was added to the game")


@app.post(Endpoints.VIEW_GAME_BOARD)
async def view_game_board(game_id: str, player_name: str) -> ResponseModel:
    """
    View the board of a running game from the viewpoint of the given player name.

    Params:
        game_id: The ID of the game.
        player_name: The name of the player.
    """
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return ResponseModel(game_id=game_id,
                         game_status=game.status.name,
                         message=game.get_player_view(player_name))


@app.post(Endpoints.GET_DECISION)
async def get_decision(game_id: str, player_name: str) -> ResponseModel:
    """
    View the board of a running game from the viewpoint of the given player name.

    Params:
        game_id: The ID of the game.
        player_name: The name of the player.
    """
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return ResponseModel(game_id=game_id,
                         game_status=game.status.name,
                         game_decision=game.get_decision(player_name))


@app.post(Endpoints.DECIDE)
async def decide(game_id: str, player_name: str, choices: list[int] | int) -> ResponseModel:
    """
    Apply player's decision.

    Params:
        game_id: The ID of the game.
        player_name: The name of the player.
    """
    game: Game = _get_game_if_exists(game_id, search_active=True)
    game.apply_decision(player_name, choices)
    return ResponseModel(game_id=game_id,
                         game_status=game.status.name,
                         message=game.get_decision(player_name))


@app.post(Endpoints.GAME_STATUS)
async def get_game_status(game_id: str):
    """
    Get the status of an existing game.

    Params:
        game_id: The ID of the game.
    """
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return ResponseModel(game_id=game_id,
                         game_status=game.status.name)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@app.post(Endpoints.ADD_BOT)
async def add_bot_to_game() -> ResponseModel:
    pass  # TODO: implement bot addition


async def init_connection():
    pass


async def main():
    async with websockets.serve(init_connection, ServerConf.IP, ServerConf.PORT):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    # uvicorn.run(app, host=ServerConf.HOST, port=ServerConf.PORT)
    asyncio.run(main())
