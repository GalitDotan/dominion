import logging
import os
import sys
from asyncio import sleep
from threading import Thread
from typing import Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer

from app_utils.app_config import GameConfigurations
from app_utils.connection_manager import WebSocketsManager
from app_utils.server_consts import ServerConf
from game_mechanics.game import Game
from game_mechanics.game_config.game_config import GameConfiguration
from game_mechanics.game_status import GameStatus
from utils.name_generator import generate_player_name

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Output logs to stdout
    ]
)

logger = logging.getLogger(__name__)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ROOT = 'app_utils/static/templates'
CHAT_FILE = 'chat.html'

RANDOM_CHOICE = 'r'

app = FastAPI()

ws_manager = WebSocketsManager()

awaiting_game_confs: GameConfigurations = GameConfigurations()
games: set[Game] = set()
threads: set[Thread] = set()


@app.get('/', response_class=HTMLResponse)
async def get():
    try:
        with open(os.path.join(ROOT, CHAT_FILE)) as fh:
            data = fh.read()
        return HTMLResponse(content=data, media_type='text/html')
    except Exception as e:
        logger.exception("Error loading the main page")
        raise HTTPException(status_code=500, detail="Failed to load the page")


@app.websocket('/ws/{name}')
async def game_initiation_manager(websocket: WebSocket, name: str):
    await ws_manager.connect(name, websocket)
    try:
        logger.info(f"Getting player {name}'s new name")
        name = await _get_player_name(name)
        await _offer_game_options(name)

        choice = await ws_manager.receive_text(name)
        logger.info(f"Player {name} chose {choice}")
        if choice == 'init':
            await _init_game(name)
        elif choice.startswith('join'):
            game_name = choice.removeprefix('join ')
            await _join_game(name, game_name)
        else:
            await ws_manager.send_personal_message(f'Unknown request: {choice}', name)
            raise HTTPException(status_code=404, detail=f'Unknown request {choice}')
    except WebSocketDisconnect:
        logger.info(f"Player {name} disconnected")
        ws_manager.disconnect(name)
        await ws_manager.broadcast(f'Player {name} has disconnected')


@app.get('/game_state/{game_name}/supply')
async def get_game_state(game_name: str):
    """
    Retrieve the current state of the game by game name.
    """
    game = _find_in_progress_game(game_name)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_name} not found")
    return str(game.supply)


async def _get_player_name(player_id: str) -> str:
    """
    Ask the player for a name, allowing them to choose a random one if desired.
    """
    await ws_manager.send_personal_message(f'Enter your name, or type "{RANDOM_CHOICE}" for random', player_id)
    name = await ws_manager.receive_text(player_id)
    if name == RANDOM_CHOICE:
        name = generate_player_name()
        logger.info(f'The random name {name} was chosen for player {player_id}')
    ws_manager.rename_active_client(player_id, name)
    await ws_manager.send_personal_message(f'Welcome, {name}', name)
    return name


async def _offer_game_options(name: str):
    """
    Show available game options to the player: create or join a game.
    """
    logger.info(f'Showing options for player {name}')
    if awaiting_game_confs.empty():
        await ws_manager.send_personal_message('No open games available.', name)
        await ws_manager.send_personal_message('Type "init" to start a new game or wait for a game to open.', name)
        return
    await ws_manager.send_personal_message(f'Available games: {awaiting_game_confs}', name)
    await ws_manager.send_personal_message(
        'Type "init" to start a new game or "join <GAME-NAME>" to join an available one.', name)


async def _init_game(host_name: str):
    """
    Handle the game initialization process, waiting for the player to type 'start' to begin.
    """
    logger.info(f'Initializing {host_name}\'s game')
    game_conf = GameConfiguration(player_names=[host_name], ws_manager=ws_manager)
    awaiting_game_confs[host_name] = game_conf
    await ws_manager.send_personal_message(f'Your new game: {game_conf.game_name}', host_name)
    await ws_manager.broadcast(f'{host_name}\'s game was initiated. To join, type "join {game_conf.game_name}"')

    await ws_manager.send_personal_message('Type "start" whenever you wish to start the game.', host_name)
    logger.info(f'Waiting to start {host_name}\'s game')

    while True:
        data = await ws_manager.receive_text(host_name)
        logger.info(f'Got new request from {host_name}: {data}')
        if data == 'start':
            logger.info(f'Starting {host_name}\'s game')
            await _start_game(host_name)
            return
        else:
            logger.info(f'Broadcasting {host_name} said: {data}')
            # TODO: only broadcast when specifically asked
            await ws_manager.broadcast(f'{host_name} said: {data}')


async def _join_game(name: str, game_name: str):
    """
    Join an already initiated game.
    """
    logger.info(f"Player {name} wants to join {game_name}")
    game_conf = _find_not_started_game(game_name)
    if not game_conf:
        await ws_manager.send_personal_message(f'The game {game_name} does not exist or has already started', name)
        return

    if name in game_conf.player_names:
        await ws_manager.send_personal_message(f'You are already part of the game {game_name}', name)
        return

    game_conf.player_names.append(name)
    await ws_manager.send_personal_message(f'You have joined {game_conf.game_name}. '
                                           f'Waiting for the host to start.', name)
    await ws_manager.broadcast(f'{name} joined game {game_name}. Players: {game_conf.player_names}')

    game = _wait_for_game_start(game_name)
    await _play_game(game, name)


async def _start_game(host_name: str, game_name: str):
    """
    Start the game initiated by the host.
    """
    game_conf = awaiting_game_confs.remove_conf(host_name, game_name)
    if not game_conf:
        logging.warning(f'No suitable game config for {host_name} with the name {game_name}')
        await ws_manager.send_personal_message(f"Game not found or already started for {host_name}.",
                                               host_name)
        return

    game = Game(game_conf=game_conf)
    games.add(game)

    logger.info(f"Game {game_conf.game_name} is starting with players {game_conf.player_names}")
    await ws_manager.broadcast(f'Starting game {game_conf.game_name}')
    logger.info(f'Running game {game_name}')
    # await game.run()


def _wait_for_game_start(game_name: str) -> Optional[Game]:
    """
    Wait for the game to reach 'IN_PROGRESS' status.
    """
    game_conf = _find_not_started_game(game_name)
    while game_conf and game_conf.status != GameStatus.IN_PROGRESS:
        continue
    return _find_in_progress_game(game_name)


async def _play_game(game: Game, player_name: str):
    """
    Main game loop for a player.
    """
    while game.game_conf.status == GameStatus.IN_PROGRESS:
        await sleep(1)  # Simulate game delay or waiting for player input.


def _find_not_started_game(game_name: str) -> Optional[GameConfiguration]:
    """
    Find a game configuration that hasn't started yet.
    """
    game_confs: list[GameConfiguration] = list(awaiting_game_confs.values())
    for game in game_confs:
        if game.game_name == game_name:
            return game


def _find_in_progress_game(game_name: str) -> Optional[Game]:
    """
    Find a game by its name that is already in progress.
    """
    for game in games:
        if game.game_conf.game_name == game_name:
            return game
    return None


if __name__ == "__main__":
    uvicorn.run(app, host=ServerConf.HOST, port=ServerConf.PORT, log_level="info")
