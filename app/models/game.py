from sqlalchemy import Column, String, Integer, Boolean
from db import Base
import time


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_position = Column(Integer)
    while_user_id = Column(Integer)
    black_user_id = Column(Integer)
    status_id = Column(Integer)
    moves = Column(String)
    move_time = Column(Integer, default=80)
    move_time_end = Column(Integer, default=round(time.time()+400))
    while_time_end = Column(Integer, default=800)
    black_time_end = Column(Integer, default=800)


table_game = Game.__table__


class GameStartPosition(Base):
    __tablename__ = "game_start_position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chess_variant = Column(String)
    position = Column(Integer)
    FEN = Column(String)

    #  = [
    #     (0, 'Классика'),
    #     (1, 'Инь-Ян'),
    #     (2, 'Фланговая'),
    #     (3, 'Инь-ян / Фланговая'),
    #     (4, 'Инь-ян / Фибоначчи'),
    # ]


table_game_start_position = GameStartPosition.__table__


class GameStatus(Base):
    __tablename__ = "game_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)

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


table_game_status = GameStatus.__table__
