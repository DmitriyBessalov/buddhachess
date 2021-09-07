from random import random, randint
from typing import List
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import redis

from app.auth import servises

r = redis.Redis(host='127.0.0.1', port=6379, db=1)

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        print('init')

    async def connect(self, websocket: WebSocket, group_id, client_id):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = {}
        self.active_connections[group_id][client_id] = '111'
        self.active_connections['22'] = '222'
        print('connect')


    def disconnect(self, websocket: WebSocket, group_id):
        del self.active_connections[group_id]
        # self.active_connections.remove(websocket)
        print('disconnect')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        print('send_personal_message: ' + message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            print('broadcast: ' + message)


manager = ConnectionManager()


@router.websocket("/create")
async def websocket_endpoint(websocket: WebSocket, group_id='start', username=Depends(servises.get_current_user)):
    await manager.connect(websocket, group_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            ws_json = json.loads(data)
            response_data = {"cmd": "show_games"}
            if ws_json['cmd'] == "create_game":
                # Добавить в редис
                if ws_json['color'] == "random":
                    if randint(0, 1):
                        ws_json['color'] = "white"
                    else:
                        ws_json['color'] = "black"

                if ws_json['chess_variant'] == "960":
                    response_data['position_960'] = randint(0, 959)

                game_id = randint(100000000, 999999999)
                r.set('game_' + str(game_id), json.dumps({
                    "game_id": game_id,
                    "chess_variant": ws_json['chess_variant'],
                    "color": ws_json['color'],
                    "position_960": ws_json['position_960'],
                    "user": username,
                }), ex=600)

            # await manager.send_personal_message(json.dumps(response_data), websocket)
            await manager.broadcast(json.dumps(response_data))
    except WebSocketDisconnect:
        pass
    #     manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")

# @router.websocket("/{group_id}/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, group_id: int, client_id: int):
#     await manager.connect(websocket, group_id, client_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # await manager.send_personal_message(f"You wrote: {data}", websocket)
#             # await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         # await manager.broadcast(f"Client #{client_id} left the chat")
