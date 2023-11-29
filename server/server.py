from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from consts import Endpoints, GameStatus, ServerConf
from game_mechanics.game import Game
from models.game_initiator import GameInitiator
from response_model.response_model import ResponseModel

app = FastAPI()

games: dict[str, Game] = {}
game_initiators: dict[str, GameInitiator]
game_runners: set[Thread] = set()


def game_runner(game: Game):
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
    game_initiators[initiator.game_id] = initiator
    return ResponseModel(game_id=initiator.id,
                         game_status=GameStatus.INITIATED)


@app.post(Endpoints.START_GAME)
async def start_game(game_id: str) -> ResponseModel:
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
    initiator = _get_game_if_exists(game_id, search_active=False)
    initiator.add_player(player_name)
    return ResponseModel(game_id=game_id,
                         game_status=GameStatus.IN_PROGRESS,
                         message="Player was added to the game")


@app.post(Endpoints.VIEW_GAME_BOARD)
async def view_game_board(game_id: str, player_name: str) -> ResponseModel:
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return ResponseModel(game_id=game_id,
                         game_status=game.status.name,
                         message=game.get_player_view(player_name))


@app.post(Endpoints.GAME_STATUS)
async def get_game_status(game_id: str):
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return ResponseModel(game_id=game_id,
                         game_status=game.status.name)


@app.post(Endpoints.ADD_BOT)
async def add_bot_to_game() -> ResponseModel:
    pass  # TODO: implement bot addition


if __name__ == "__main__":
    uvicorn.run(app, host=ServerConf.HOST, port=ServerConf.PORT)
