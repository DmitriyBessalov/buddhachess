from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from routers.api.v1.auth import create_or_get_anonimous_token
from services.websocket import ConnectionManager, r1, r2
from random import randint
from db import database
import json
import ast

from models.game import table_game_start_position

router = APIRouter()

manager = ConnectionManager()


async def listgames(remove_ws_session_id: int = 0):
    data = ''

    for key in r1.keys('game_*'):
        k = ast.literal_eval(r1.get(key).decode("utf-8"))
        k['ttl'] = r1.ttl(key)

        if k['ws_session_id'] != remove_ws_session_id:
            del k['ws_session_id']
            data = data + str(k) + ', '
        else:
            r1.delete("game_" + str(k["game_id"]))

    if data == '':
        data = '[]'

    return {"cmd": "list_games", "list_games": ast.literal_eval(data)}


@router.websocket("/create/{ws_session_id}/{access_token}")
async def websocket_endpoint(websocket: WebSocket, ws_session_id: int, access_token: str, group_id: int = 0):
    user = await create_or_get_anonimous_token(access_token)
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
                if ws_json['chess_variant'] == "iy":
                    response_data['position'] = randint(0, 45)
                else:
                    response_data['position'] = 0

                r_dict = {
                    "game_id": game_id,
                    "chess_variant": ws_json['chess_variant'],
                    "color": ws_json['color'],
                    "user": user['username'],
                    "ws_session_id": ws_session_id,
                    "position": response_data['position']
                }

                r1.set('game_' + str(game_id), json.dumps(r_dict), ex=600)

                response_data = await listgames()
                await manager.broadcast(json.dumps(response_data), group_id)

            if ws_json['cmd'] == 'show_games':
                response_data = await listgames()
                await manager.send_personal_message(json.dumps(response_data), group_id, ws_session_id)

            if ws_json['cmd'] == 'join_game':
                game = r1.get('game_' + str(ws_json['game_id']))
                game = ast.literal_eval(game.decode("utf-8"))

                if game['user'] != user['username']:
                    r1.delete('game_' + str(ws_json['game_id']))

                    response_data = {"cmd": "join_game", "game_id": ws_json['game_id']}
                    await manager.send_personal_message(json.dumps(response_data), group_id, game["ws_session_id"])

                    if game['color'] == "true":
                        game["user_white"] = game["user"]
                        game["user_black"] = user['username']
                    else:
                        game["user_black"] = game['user']
                        game["user_white"] = user['username']

                    del game["ws_session_id"]
                    del game["user"]
                    del game["color"]

                    r2.set(ws_json['game_id'], json.dumps(game), ex=86000)

    except WebSocketDisconnect:
        manager.disconnect(group_id, ws_session_id)
        response_data = await listgames(ws_session_id)
        await manager.broadcast(json.dumps(response_data), group_id)


@router.websocket("/{game_id}/{access_token}")
async def websocket_endpoint(websocket: WebSocket, game_id: int, access_token: str):
    user = await create_or_get_anonimous_token(access_token)
    ws_session_id = randint(10 ** 10, 10 ** 11)
    await manager.connect(websocket, game_id, ws_session_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            ws_json = json.loads(data)

            if ws_json['cmd'] == 'join_game':
                game = r2.get(game_id)
                response_data = ast.literal_eval(game.decode("utf-8"))
                response_data['cmd'] = 'join_game'

                position = await database.fetch_one(
                    query=table_game_start_position.select() \
                        .where(table_game_start_position.c.chess_variant == response_data['chess_variant']) \
                        .where(table_game_start_position.c.position == response_data['position'])
                )
                position = dict(position.items())
                response_data["FEN"] = position["FEN"]

                await manager.send_personal_message(json.dumps(response_data), game_id, ws_session_id)

            if ws_json['cmd'] == "move":
                await manager.broadcast(json.dumps(ws_json), game_id)

    except WebSocketDisconnect:

        response_data = await listgames(ws_session_id)
        manager.disconnect(game_id, ws_session_id)

        await manager.broadcast(json.dumps(response_data), game_id)
