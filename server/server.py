import os.path
from threading import Thread

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from game_mechanics.game_config import GameConfiguration, GameStatus
from game_mechanics.game_runner import GameRunner
from game_mechanics.states.game_state import GameState
from server.connection_manager import WebSocketsManager
from server_consts import ServerConf

ROOT = 'static/templates'
CHAT_FILE = 'chat.html'

app = FastAPI()

ws_manager = WebSocketsManager()

not_started_games: dict[str:GameConfiguration] = {}
running_games: set[GameState] = set()
threads: set[Thread] = set()


@app.get("/", response_class=HTMLResponse)
async def get():
    with open(os.path.join(ROOT, CHAT_FILE)) as fh:
        data = fh.read()
    return HTMLResponse(content=data, media_type="text/html")


@app.websocket('/ws/{client_id}')
async def game_initiation_manager(websocket: WebSocket, client_id: str):
    await ws_manager.connect(client_id, websocket)
    try:
        while True:
            await ws_manager.send_personal_message(f"Type 'init' or 'join <id>'", client_id)
            choice = await websocket.receive_text()
            if choice == 'init':
                _init_game(client_id)
            elif choice.startswith('join'):
                game_id = choice.removeprefix('join ')
                _join_game(client_id, game_id)
            else:
                raise HTTPException(status_code=404, detail=f'Unknown request {choice}')
            _play_game(client_id)


    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
        await ws_manager.broadcast(f"Player #{client_id} got disconnected")


async def _init_game(client_id: str):
    game_conf = GameConfiguration()
    await ws_manager.send_personal_message(f"Your new game: {game_conf.game_id}", client_id)
    await ws_manager.broadcast(f"Client #{client_id} initiated game: {game_conf.game_id}")
    started = False
    while not started:
        await ws_manager.send_personal_message(f"Type 'start' whenever you wish to start the game", client_id)
        data = await ws_manager.receive_text(client_id)
        if data == 'start':
            started = True
            _start_game(client_id)
        else:
            await ws_manager.send_personal_message(f"You wrote: {data}", client_id)
            await ws_manager.broadcast(f"Client #{client_id} says: {data}")


async def _join_game(client_id: str, game_id: str):
    games: list[GameConfiguration] = list(not_started_games.values())
    for game in games:
        if game.game_id == game_id:
            game.player_ids.append(client_id)
            await ws_manager.send_personal_message(
                f"You have joined {game.game_id}. Please wait for host to start the game", client_id)
            _wait_root(client_id)
            break


def _start_game(client_id: str):
    game = not_started_games.pop(client_id)
    gm = GameState(game_conf=game)
    ws_manager.broadcast(f'Starting game {game.game_id}')
    th = GameRunner.threaded_run(gm)
    threads.add(th)
    running_games.add(gm)


async def _wait_root(client_id: str, wait_for_status: GameStatus = GameStatus.IN_PROGRESS):
    game = not_started_games[client_id]
    while game.status != wait_for_status:
        await ws_manager.send_personal_message(f"Welcome to the chat room. Here you'll wait for your game to start",
                                               client_id)
        data = await ws_manager.receive_text(client_id)
        await ws_manager.send_personal_message(f"You wrote: {data}", client_id)
        await ws_manager.broadcast(f"Client #{client_id} says: {data}")


def _play_game(client_id: str):
    gm: GameState = [gm for gm in running_games if client_id in running_games.game_conf.player_ids][0]


if __name__ == "__main__":
    uvicorn.run(app, host=ServerConf.HOST, port=ServerConf.PORT)
