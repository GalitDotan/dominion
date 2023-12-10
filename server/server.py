import os.path
from threading import Thread

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from config import Endpoints
from config import ServerConf
from consts import GameStatus
from game_mechanics.game import Game
from game_mechanics.game_runner import GameRunner
from models.game_initiator import GameInitiator
from response_model.response_model import ResponseModel

# init app
app = FastAPI()
app.mount("/server/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
root = 'static/templates'

# init game configuration
games: dict[str, Game] = {}
game_initiators: dict[str, GameInitiator]
game_threads: set[Thread] = set()

game_runner = GameRunner()


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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []  # TODO: each client should have a game id

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


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
    game_threads.add(game_runner.threaded_run(game))
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


@app.post(Endpoints.ADD_BOT)
async def add_bot_to_game() -> ResponseModel:
    pass  # TODO: implement bot addition


@app.get("/", response_class=HTMLResponse)
async def get():
    with open(os.path.join(root, 'chat.html')) as fh:
        data = fh.read()
    return HTMLResponse(content=data, media_type="text/html")


@app.websocket('/ws/{client_name}')
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_name} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_name} left the chat")


if __name__ == "__main__":
    uvicorn.run(app, host=ServerConf.HOST, port=ServerConf.PORT)
