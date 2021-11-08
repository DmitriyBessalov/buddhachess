from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        print('ws_init')

    async def connect(self, websocket: WebSocket, group_id: int, ws_session_id: int):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = {}
        self.active_connections[group_id][ws_session_id] = websocket
        print('ws_connect')

    def disconnect(self, group_id: int, ws_session_id: int):
        del self.active_connections[group_id][ws_session_id]
        print('ws_disconnect')

    async def send_personal_message(self, message: str, group_id: int, ws_session_id: int):
        await self.active_connections[group_id][ws_session_id].send_text(message)
        print('ws_send_personal_message: ' + message)

    async def broadcast(self, message: str, group_id: int):
        for _ws_session_id in self.active_connections[group_id]:
            await self.active_connections[group_id][_ws_session_id].send_text(message)
            print('broadcast: ' + message)
