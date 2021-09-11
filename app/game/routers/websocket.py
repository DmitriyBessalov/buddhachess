from random import randint
import json
import ast
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis

from app.auth.routers.api import create_anonimous_token

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

    def disconnect(self, group_id: str, ws_session_id: int):
        del self.active_connections[group_id][ws_session_id]
        print('disconnect')

    async def send_personal_message(self, message: str, group_id: str, ws_session_id: int):
        await self.active_connections[group_id][ws_session_id].send_text(message)
        print('send_personal_message: ' + message)

    async def broadcast(self, message: str, group_id: str):
        for _ws_session_id in self.active_connections[group_id]:
            await self.active_connections[group_id][_ws_session_id].send_text(message)
            print('broadcast: ' + message)


manager = ConnectionManager()


async def listgames(remove_ws_session_id: int = 0):
    data = ''

    for key in r.keys('game_*'):
        k = ast.literal_eval(r.get(key).decode("utf-8"))
        k['ttl'] = r.ttl(key)

        if k['ws_session_id'] != remove_ws_session_id:
            del k['ws_session_id']
            data = data + str(k) + ', '
        else:
            r.delete("game_" + str(k["game_id"]))

    if data == '':
        data = '[]'

    return {"cmd": "list_games", "list_games": ast.literal_eval(data)}


@router.websocket("/create/{ws_session_id}/{access_token}")
async def websocket_endpoint(websocket: WebSocket, ws_session_id: int, access_token: str, group_id='start'):
    username = await create_anonimous_token(access_token)
    await manager.connect(websocket, group_id, ws_session_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            ws_json = json.loads(data)
            response_data = {}

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

                response_data = await listgames()
                await manager.broadcast(json.dumps(response_data), group_id)

            if ws_json['cmd'] == 'show_games':
                response_data = await listgames()
                await manager.send_personal_message(json.dumps(response_data), group_id, ws_session_id)

            if ws_json['cmd'] == 'join_game':
                game = r.get('game_' + str(ws_json['game_id']))
                game = ast.literal_eval(game.decode("utf-8"))

                if game['user'] != username['username']:
                    response_data = {"cmd": "join_game",
                                     "game_id": ws_json['game_id'],
                                     "chess_variant": game["chess_variant"],
                                     "position_960": game['position_960'],
                                     # "time_while": 2160,
                                     # "time_black": 2160,
                                     # "time_move_add": 5,
                                     # "time_start": time.time()
                                     }
                    if 'position_960' in game:
                        response_data["rival_white"] = game['position_960']

                    if game['color'] == "true":
                        response_data["rival_white"] = game["user"]
                        response_data["rival_black"] = username['username']
                    else:
                        response_data["rival_black"] = game['user']
                        response_data["rival_white"] = username['username']

    except WebSocketDisconnect:
        manager.disconnect(group_id, ws_session_id)
        response_data = await listgames(ws_session_id)
        await manager.broadcast(json.dumps(response_data), group_id)
