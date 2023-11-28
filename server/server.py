from threading import Thread

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from consts import Endpoints
from game_mechanics.game import Game
from game_mechanics.player.player import Player
from models.game_initiator import GameInitiator

app = FastAPI()

active_games: dict[str, Game] = {}
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
    game_dict = active_games if search_active else game_initiators
    if game_id not in game_dict:
        raise HTTPException(404, detail=f"The ID {game_id} does not exist")
    return game_dict[game_id]


@app.post(Endpoints.INIT_GAME)
async def init_game(initiator: GameInitiator):
    game_initiators[initiator.game_id] = initiator
    return initiator.id


@app.post(Endpoints.START_GAME)
async def start_game(game_id: str):
    initiator: GameInitiator = _get_game_if_exists(game_id, search_active=False)
    game = initiator.init_game()
    active_games[game.id] = game
    game_initiators.pop(initiator.game_id)
    runner = Thread(target=game_runner, args=(game,))
    game_runners.add(runner)
    runner.run()
    return "Game started"


@app.post(Endpoints.JOIN_GAME)
async def join_game(game_id: str, player_name: str):
    initiator = _get_game_if_exists(game_id, search_active=False)
    initiator.add_player(player_name)
    return "Player was added to the game"


@app.post(Endpoints.VIEW_GAME_BOARD)
async def view_game_board(game_id: str, player_name: str):
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return game.get_player_view(player_name)


@app.post(Endpoints.GAME_STATUS)
async def get_game_status(game_id: str):
    game: Game = _get_game_if_exists(game_id, search_active=True)
    return game.status.name


@app.post(Endpoints.ADD_BOT)
async def add_bot_to_game():
    pass
