from sqlalchemy import Column, String, Integer
from app.db.db import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    # chess_variants = [
    #     (1, 'Инь-Ян'),
    #     (2, 'Фланговая'),
    #     (3, 'Инь-ян / Фланговая'),
    #     (4, 'Инь-ян / Фибоначчи'),
    #     (15, 'Классические'),
    #     (16, 'Фишера'),
    # ]
    #
    # chess_variant = Column
    arrangement = Column(Integer)
    # white = Column(Integer, ForeignKey())
    # black = Column(Integer, ForeignKey())
    moves = Column(String)

    # status = [
    #     (0, 'В игре'),
    #     (1, 'Белые победили'),
    #     (2, 'Чёрные победили'),
    #     (3, 'Белые сдались'),
    #     (4, 'Черные сдались'),
    #     (5, 'Белые дисконнект'),
    #     (6, 'Черные дисконнект'),
    #     (7, 'Пат'),
    #     (9, 'Ничья'),
    # ]
    # result = Column

    # start_game = Column
