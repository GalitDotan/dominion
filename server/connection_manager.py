from starlette.websockets import WebSocket


class WebSocketsManager:
    """
    Manager of all active websocket connections.
    """

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id)

    async def send_personal_message(self, message: str, client_id: str):
        websocket = self.active_connections[client_id]
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def receive_text(self, client_id: str):
        websocket = self.active_connections[client_id]
        await websocket.receive_text()
