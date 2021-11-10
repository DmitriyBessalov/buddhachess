# from sqlalchemy import Column, Integer
# from app.db import Base

#
# class Game(Base):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     chess_variant_id = Column(Integer)
#     position = int
#     while_user_id = Column(Integer)
#     black_user_id = Column(Integer)
#     status_id = Column(Integer)
#     moves = str
#
#
# class GameChessVariant(Base):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     chess_variant: str

    #  = [
    #     (1, 'Инь-Ян'),
    #     (2, 'Фланговая'),
    #     (3, 'Инь-ян / Фланговая'),
    #     (4, 'Инь-ян / Фибоначчи'),
    #     (15, 'Классические'),
    #     (16, 'Фишера'),
    # ]


# class GameStatus(Base):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     status: str

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
