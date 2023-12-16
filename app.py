import os.path
from asyncio import sleep
from threading import Thread
from typing import Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from game_mechanics.game import Game
from game_mechanics.game_config.game_config import GameConfiguration
from game_mechanics.game_status import GameStatus
from server.connection_manager import WebSocketsManager
from server.server_consts import ServerConf

ROOT = 'server/static/templates'
CHAT_FILE = 'chat.html'

app = FastAPI()

ws_manager = WebSocketsManager()

awaiting_game_confs: dict[str:GameConfiguration] = {}
games: set[Game] = set()
threads: set[Thread] = set()


@app.get("/", response_class=HTMLResponse)
async def get():
    with open(os.path.join(ROOT, CHAT_FILE)) as fh:
        data = fh.read()
    return HTMLResponse(content=data, media_type="text/html")


@app.websocket('/ws/{name}')
async def game_initiation_manager(websocket: WebSocket, name: str):
    await ws_manager.connect(name, websocket)
    try:
        await ws_manager.send_personal_message(f"Enter your name", name)
        new_name = await websocket.receive_text()
        ws_manager.rename_active_client(name, new_name)
        name = new_name
        await ws_manager.send_personal_message(f"Welcome, {name}", name)
        printable_games = [str(gc) for gc in awaiting_game_confs.values()]
        if printable_games:
            await ws_manager.send_personal_message(f"Open games are {printable_games}", name)
            await ws_manager.send_personal_message(
                f"Type 'init' to open a new game or 'join <id>' to join one of the open ones", name)
        else:
            await ws_manager.send_personal_message(f"There are no open games to join", name)
            await ws_manager.send_personal_message(
                f"Type 'init' to open a new game or wait for a game to be opened and then type 'join <id>' to join it",
                name)

        choice = await websocket.receive_text()
        if choice == 'init':
            await _init_game(name)
            return
        elif choice.startswith('join'):
            game_id = choice.removeprefix('join ')
            await _join_game(name, game_id)
            return
        else:
            raise HTTPException(status_code=404, detail=f'Unknown request {choice}')
    except WebSocketDisconnect:
        ws_manager.disconnect(name)
        await ws_manager.broadcast(f"Player #{name} got disconnected")


async def _init_game(name: str):
    """
    Waiting for the current client to type start.
    """
    game_conf = GameConfiguration(player_names=[name], ws_manager=ws_manager)
    awaiting_game_confs[name] = game_conf
    await ws_manager.send_personal_message(f"Your new game: {game_conf.game_id}", name)
    await ws_manager.broadcast(f"{name} initiated game. To join type 'join {game_conf.game_id}'")
    await ws_manager.send_personal_message(f"Type 'start' whenever you wish to start the game", name)
    while True:
        data = await ws_manager.receive_text(name)
        await ws_manager.send_personal_message(f"You wrote: {data}", name)
        await ws_manager.broadcast(f"{name} says: {data}")
        if data == 'start':
            await _start_game(name)
            return


async def _join_game(name: str, game_id: str):
    """
    Join an already initiated game.
    This is allowed only for games that hadn't been started yet.

    :param name: Client's name.
    :param game_id: The game ID.
    """
    game_conf = _find_not_started_game(game_id)
    game_conf.player_names.append(name)
    await ws_manager.send_personal_message(f"You have joined {game_conf.game_id}. "
                                           f"Please wait for host to start the game", name)
    await ws_manager.broadcast(
        f'{name} has joined the game {game_id}, '
        f'which now has {game_conf.num_players} players: {game_conf.player_names}')
    await _wait_root(name, game_id)
    game = _find_in_progres_game(game_id)
    await _play_game(game, name)


async def _start_game(game_host_name: str):
    """
    Start a game by the host name.
    """
    game_conf = awaiting_game_confs.pop(game_host_name)
    game = Game(game_conf=game_conf)
    await ws_manager.broadcast(f'Starting game {game_conf.game_id}')
    await game.run()


async def _wait_root(name: str, game_id: str):
    """
    Waiting for given game to become 'IN_PROGRESS'.
    Meanwhile - send and receive messages.
    """
    await ws_manager.send_personal_message(f"Welcome to the chat room. Here you'll wait for your game to start", name)
    game = _find_not_started_game(game_id)
    while game.status != GameStatus.IN_PROGRESS:
        data = await ws_manager.receive_text(name)
        await ws_manager.send_personal_message(f"You wrote: {data}", name)
        await ws_manager.broadcast(f"{name} says: {data}")


async def _play_game(game: Game, player_name: str):
    while game.game_conf.status == GameStatus.IN_PROGRESS:
        await game.send_player_view(player_name)
        await sleep(1000)


def _find_not_started_game(game_id: str) -> Optional[GameConfiguration]:
    """
    Find a GameConfiguration by game_id.
    """
    game_confs: list[GameConfiguration] = list(awaiting_game_confs.values())
    for game in game_confs:
        if game.game_id == game_id:
            return game


def _find_in_progres_game(game_id: str) -> Optional[Game]:
    """
    Find a GameConfiguration by game_id.
    """
    for game in games:
        if game.game_conf.game_id == game_id:
            return game


if __name__ == "__main__":
    uvicorn.run(app, host=ServerConf.HOST, port=ServerConf.PORT)
