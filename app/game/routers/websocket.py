from random import randint
from typing import List
import json
import ast
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis

from app.auth.servises import get_current_user_with_anonimous

r = redis.Redis(host='127.0.0.1', port=6379, db=1)

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        print('init')

    async def connect(self, websocket: WebSocket, group_id: str, ws_session_id: int):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = {}
        self.active_connections[group_id][ws_session_id] = websocket
        print('connect')

    async def disconnect(self, websocket: WebSocket, group_id: str, ws_session_id: int):
        del self.active_connections[group_id]
        self.active_connections[group_id][ws_session_id].remove(websocket)
        print('disconnect')

    async def send_personal_message(self, websocket: WebSocket, message: str, group_id: str, ws_session_id: int):
        await websocket.send_text(message)
        print('send_personal_message: ' + message)

    async def broadcast(self, group_id: str, message: str):
        for connection in self.active_connections[group_id]:
            await self.active_connections[group_id][connection].send_text(message)
            print('broadcast: ' + message)


manager = ConnectionManager()


@router.websocket("/create/{ws_session_id}/{access_token}")
async def websocket_endpoint(websocket: WebSocket, ws_session_id: int, access_token: str, group_id='start'):
    username = await get_current_user_with_anonimous(token=access_token)
    await manager.connect(websocket, group_id, username['username'])
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            ws_json = json.loads(data)
            response_data = {"cmd": "error"}

            if ws_json['cmd'] == "create_game":
                # Добавить в редис
                if ws_json['color'] == "random":
                    ws_json['color'] = str(bool(randint(0, 1))).lower()

                game_id = randint(100000000, 999999999)
                r_dict = {
                    "game_id": game_id,
                    "chess_variant": ws_json['chess_variant'],
                    "color": ws_json['color'],
                    "user": username['username'],
                    "ws_session_id": ws_session_id
                }

                if ws_json['chess_variant'] == "960":
                    r_dict["position_960"] = response_data['position_960'] = randint(0, 959)

                r.set('game_' + str(game_id), json.dumps(r_dict), ex=600)

                # await manager.send_personal_message(websocket, json.dumps(r_dict), group_id,  )

            # if ws_json['cmd'] == 'join_game':
            #     game = r.get('game_' + str(ws_json['game_id']))
            #     game = ast.literal_eval(game.decode("utf-8"))
            #
            #     if game['user'] != username['username']:
            #         response_data = {"cmd": "join_game",
            #                          "game_id": ws_json['game_id'],
            #                          "chess_variant": game["chess_variant"],
            #                          "position_960": game['position_960'],
            #                          "time_while": 2160,
            #                          "time_black": 2160,
            #                          "time_move_add": 5,
            #                          "time_start": time.time()
            #                          }
            #
            #         if game['color'] == "white":
            #             response_data["rival_white"] = game["user"]
            #             response_data["rival_black"] = username['username']
            #         else:
            #             response_data["rival_black"] = game['user']
            #             response_data["rival_white"] = username['username']

            if ws_json['cmd'] == 'show_games' or ws_json['cmd'] == 'join_game' or ws_json['cmd'] == 'disconnect' or \
                    ws_json['cmd'] == 'create_game':
                data = ''

                for key in r.keys('game_*'):
                    k = ast.literal_eval(r.get(key).decode("utf-8"))
                    k['ttl'] = r.ttl(key)
                    data = data + str(k) + ', '

                if data == '':
                    data = '[]'

                # if ws_json['cmd'] == 'show_games':
                response_data["cmd"] = "list_games"
                response_data["list_games"] = ast.literal_eval(data)

            # await manager.send_personal_message(json.dumps(response_data), websocket)
            await manager.broadcast(group_id, json.dumps(response_data))
    except WebSocketDisconnect:
        await manager.disconnect(websocket, group_id, ws_session_id)
