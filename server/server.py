import os.path
from threading import Thread

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from game_mechanics.game_master import GameMaster, GameConfiguration
from game_mechanics.game_runner import GameRunner
from server_consts import ServerConf

# init app
app = FastAPI()
app.mount("/server/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
root = 'static/templates'

# init game configuration
games: dict[str, GameMaster] = {}
game_initiators: dict[str, GameConfiguration]
game_threads: set[Thread] = set()

game_runner = GameRunner()


def _get_game_if_exists(game_id: str, search_active: bool = True) -> GameMaster | GameConfiguration:
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
