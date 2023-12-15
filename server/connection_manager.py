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
        return await websocket.receive_text()

    def rename_active_client(self, curr_name: str, new_name: str):
        """
        Rename a client's name.

         Params:
            curr_name: The currently saved name.
            new_name: The new name.
        """
        conn = self.active_connections.pop(curr_name)
        self.active_connections[new_name] = conn
