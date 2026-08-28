# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: core/chatManager.py — WebSocket Connection Manager (Live Chat)
# ================================================================================
# Why this file is used:
#   - It manages incoming WebSocket client sockets for the live chat service.
#
# What components are inside:
#   - ConnectionManager:
#       - active_connections  -> Map linking active user IDs to WebSocket connections.
#       - connect()           -> Registers new socket parameters.
#       - disconnect()        -> Removes socket parameters.
#       - send_to_user()      -> Pushes JSON payloads directly to target sockets.
#       - is_online()         -> Verifies socket activity status.
#   - manager                 -> Singleton helper instance.
# ================================================================================
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, data: dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(data)

    def is_online(self, user_id: int) -> bool:
        return user_id in self.active_connections

manager = ConnectionManager()