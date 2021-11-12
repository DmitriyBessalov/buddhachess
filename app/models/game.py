import ormar
from app.models.base import BaseModel
import time


class Game(BaseModel):
    start_position: int = ormar.Integer()
    while_user_id: int = ormar.Integer()
    black_user_id: int = ormar.Integer()
    status_id: int = ormar.Integer()
    moves: str = ormar.String(max_length=2047)
    move_time: int = ormar.Integer(default=80)
    move_time_end: int = ormar.Integer(default=round(time.time()+400))
    while_time_end: int = ormar.Integer(default=800)
    black_time_end: int = ormar.Integer(default=800)


class Game_Start_Position(BaseModel):
    chess_variant: str = ormar.String(max_length=15)
    position: int = ormar.Integer(maximum=960)
    position_FEN: str = ormar.String(max_length=127)

    #  = [
    #     (1, 'Инь-Ян'),
    #     (2, 'Фланговая'),
    #     (3, 'Инь-ян / Фланговая'),
    #     (4, 'Инь-ян / Фибоначчи'),
    #     (5, 'Классические'),
    #     (6, 'Фишера'),
    # ]


class Game_Status(BaseModel):
    status: str

    # status = [
    #     (0, 'Ход белых'),
    #     (1, 'Ход черных'),
    #     (2, 'Белые победили'),
    #     (3, 'Чёрные победили'),
    #     (4, 'Белые сдались'),
    #     (5, 'Черные сдались'),
    #     (6, 'Белые дисконнект'),
    #     (7, 'Черные дисконнект'),
    #     (8, 'Пат'),
    #     (9, 'Ничья'),
    # ]
